from typing import get_origin, get_args
from collections import deque
from main.state.player_state import PlayerState

def convert_value(value, target_type, key = None):
    # print(f"convert value: {value} to {target_type}")
    origin = get_origin(target_type) # typ tego co chcemy dostać

    if hasattr(target_type, "from_dict") and isinstance(value, dict):
        if target_type is PlayerState and key is not None:
            return PlayerState.from_dict(key, value)
        return target_type.from_dict(value)

    if hasattr(target_type, "from_list") and isinstance(value, list):
        return target_type.from_list(value)

    if origin is dict and isinstance(value, dict):
        key_type, value_type = get_args(target_type)
        return {
            k : convert_value(v, value_type, key=k)
            for k, v in value.items()
        }

    if origin is tuple:
        return tuple(value)

    return value

def auto_to_dict(obj):
    if(hasattr(obj, "to_dict")):
        return obj.to_dict()
    if(hasattr(obj, "to_list")):
        return obj.to_list()
    if(isinstance(obj, dict)):
        return{
            k : auto_to_dict(v)
            for k, v in obj.items()
        }
    if(isinstance(obj, (list, deque))):
        return [auto_to_dict(v) for v in obj]
    
    return obj