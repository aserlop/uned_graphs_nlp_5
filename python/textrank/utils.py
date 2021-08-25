from typing import List, Any


def flatten_LL(list_of_list: List[List[Any]]) -> List[Any]:
    """
    Takes a list of list and flatten it into a list ([[], ..., []] -> [])
    :param list_of_list:
    :return: Flattened list
    """
    return [item for sublist in list_of_list for item in sublist]


def str2bool(v: str) -> bool:
    """
    Casts string to boolean
    :param v: string value
    :return: boolean
    """
    v = str(v)
    if isinstance(v, bool):
        return v

    if v.lower() in ('yes', 'true', 't', 'y', '1'):
        return True

    elif v.lower() in ('no', 'false', 'f', 'n', '0'):
        return False
