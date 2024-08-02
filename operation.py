from typing import List, Type


def areInstances(data: List, object: Type) -> bool:
    if isinstance(data, list):
        return all(isinstance(o, object) for o in data)
    return False
