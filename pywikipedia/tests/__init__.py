import __builtin__

def raw_input(*args, **kwargs):
    raise Exception("No raw_input allowed in tests")

__builtin__.raw_input = raw_input
