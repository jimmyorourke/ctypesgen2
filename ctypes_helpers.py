import ctypes
from typing import Any, Dict


def to_dict(struct: ctypes.Structure) -> Dict[str, Any]:
    """Convert a ctypes.Structure object to a Python dict."""
    result = {}
    def get_value(field_value):
         if hasattr(field_value, "_length_"):
             # Probably an array
             field_value = get_array(field_value)
         elif hasattr(field_value, "_fields_"):
             # Probably another struct
             field_value = to_dict(field_value)
         return field_value
    def get_array(array):
        # Array might be nested or contain structs
        return [get_value(value) for value in array]
    # Danger! struct._fields_ may have either 2 or 3 elements!
    for field in struct._fields_:
        field_name = field[0]
        field_value = getattr(struct, field_name)
        # field_value will either be the value of a primitive, or the type name of nested type
        result[field_name] = get_value(field_value)
    return result

# Monkey patch the __str__ member for ctypes.Structure objects to use the stringified dict representation.
# The __dict__ of built-in types is a dictproxy object that is read only, however we are able to get mutable access
# through the garbage collector. This is a higher level and safer method than applying a curse with the forbiddenfruit
# package. It might not be safe to modify the __repr__ of a built-in, so only __str__ is adjusted.
import gc
underlying_dict = gc.get_referents(ctypes.Structure.__dict__)[0]
underlying_dict["__str__"] = lambda self: str(to_dict(self))
