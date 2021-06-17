from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, Tuple, Set, List


LIST_SEPARATOR = ","


class FieldType(Enum):
    StringField = 0, # Normal field which data is a string
    ListField = 1, # Field which data is a list where items are separated by LIST_SEPARATOR
    NucleotidesField = 2 # Fild which data is a nucleotide sequence


class LineType(Enum):
    Default = 0, # Contains both new field declaration and some data
    Data = 1, # Contains only data
    NewField = 2, # Contains new field declaration
    End = 3 # Item end


@dataclass
class Field:
    name: str
    field_type: FieldType = FieldType.StringField

    def __eq__(self, other):
        if isinstance(other, str):
            return self.name.lower() == other.lower()


FIELDS_AVAILABLE_FOR_PARSING = {
    "DEFINITION": Field("definition"),
    "KEYWORDS": Field("keywords"),
    "AUTHORS": Field("authors", FieldType.ListField),
    "ORIGIN": Field("origin", FieldType.NucleotidesField)
}


@dataclass
class LineProcessingResult:
    field: str
    data: list = field(default_factory=list)
    line_type: LineType = LineType.Default


def process_field_data(data: List[str], field_type: FieldType) -> str:
    if field_type == FieldType.StringField:
        return " ".join(data)
    elif field_type == FieldType.ListField:
        return (" ".join(data)).split(LIST_SEPARATOR)
    elif field_type == FieldType.NucleotidesField:
        return "".join((part for part in data if not part.isnumeric()))
    return ""


def process_line(line: str) -> LineProcessingResult:
    line = line.strip()
    start, *rest  = [word for word in line.split(" ") if word != ""]
    if start.isupper() and len(rest) > 0:
        return LineProcessingResult(start, rest, line_type=LineType.Default)
    elif start.isupper() and len(rest) == 0:
        return LineProcessingResult(start, line_type=LineType.NewField)
    elif start == "//":
        return LineProcessingResult(start, line_type=LineType.End)
    else:
        return LineProcessingResult("", [start] + rest, line_type=LineType.Data)


def add_field(dest: Dict[str, str], field_name: str, field_data: List[str], req_fields: Tuple[Field]) -> None:
    if len(field_name) == 0 or field_name not in req_fields or field_name in dest:
        return
    field_index = req_fields.index(field_name)
    field_type = req_fields[field_index].field_type

    dest[field_name] = process_field_data(field_data, field_type)


def read_gb_file(file_path: str, req_fields: Tuple[str] = ("DEFINITION", "KEYWORDS", "AUTHORS", "ORIGIN")) -> Dict[str, str]:
    req_fields = tuple(FIELDS_AVAILABLE_FOR_PARSING[req_field] for req_field in req_fields)
    result = {}
    current_field = ""
    current_field_data = []

    with open(file_path, "r") as f:
        for line in f:
            line_result = process_line(line)

            if line_result.line_type == LineType.Data:
                current_field_data.extend(line_result.data)
            elif line_result.line_type == LineType.NewField or line_result.line_type == LineType.Default:
                add_field(result, current_field, current_field_data, req_fields)
                current_field = line_result.field
                current_field_data = line_result.data
            elif line_result.line_type == LineType.End:
                add_field(result, current_field, current_field_data, req_fields)

    return result


if __name__ == "__main__":
    print(read_gb_file("BlueScribe.gb"))
