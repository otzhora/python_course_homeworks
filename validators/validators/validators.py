from inspect import signature


TYPES = {
    'int': int,
    'float': float,
    'complex': complex,
    'string': str,
    'dict': dict,
    'list': list,
    'tuple': tuple,
    'range': range,
    'set': set,
    'bool': bool,
}

COMPLEX_TYPES = {
    'number': (int, float, complex),
    'iterable': (str, dict, list, tuple, range, set)
}


def check_value_type(value, req_type):
    if req_type in TYPES:
        return isinstance(value, TYPES[req_type])

    if req_type in COMPLEX_TYPES:
        return isinstance(value, COMPLEX_TYPES[req_type])

    raise ValueError(f'unsopported required type: {req_type}')


def validate_input(*input_types):

    def validate_input_impl(fn):
        assert len(signature(fn).parameters) == len(input_types), "Number of types does not match number of arguments"

        def inner(*args, **kwargs):
            for arg, req_type in zip(args, input_types):
                if not check_value_type(arg, req_type):
                    raise TypeError(f'Expected argument type {req_type} but got {type(arg)}')

            return fn(*args, **kwargs)
        return inner
    return validate_input_impl

def validate_output(req_type):
    def validate_output_impl(fn):
        def inner(*args, **kwargs):
            res = fn(*args, **kwargs)

            if not check_value_type(res, req_type):
                raise TypeError(f'Expected output type {req_type} but got {type(res)}')

            return res
        return inner
    return validate_output_impl

def validate_output_dict(**output_types):
    def validate_output_dict_impl(fn):
        def inner(*args, **kwargs):
            res = fn(*args, **kwargs)

            assert isinstance(res, dict), f"Output of function is expected to be dict, but was {type(res)}"

            for k, v in res.items():
                if k not in output_types:
                    raise KeyError(f'Unexpected key {k}')

                if not check_value_type(v, output_types[k]):
                    raise TypeError(f'Expected type of {k} to be {output_types[k]} but got {type(v)}')

            return res
        return inner
    return validate_output_dict_impl

