# To use this code, make sure you
#
#     import json
#
# and then, to convert JSON from a string, do
#
#     result = i_dpull_type_from_dict(json.loads(json_string))

from dataclasses import dataclass
from typing import Any, Optional, List, TypeVar, Type, cast, Callable


T = TypeVar("T")


def from_str(x: Any) -> str:
    assert isinstance(x, str)
    return x


def from_int(x: Any) -> int:
    assert isinstance(x, int) and not isinstance(x, bool)
    return x


def from_none(x: Any) -> Any:
    assert x is None
    return x


def from_union(fs, x):
    for f in fs:
        try:
            return f(x)
        except:
            pass
    assert False


def to_class(c: Type[T], x: Any) -> dict:
    assert isinstance(x, c)
    return cast(Any, x).to_dict()


def from_list(f: Callable[[Any], T], x: Any) -> List[T]:
    assert isinstance(x, list)
    return [f(y) for y in x]


@dataclass
class X:
    value: str
    timeout: int
    combo: str

    @staticmethod
    def from_dict(obj: Any) -> 'X':
        assert isinstance(obj, dict)
        value = from_str(obj.get("value"))
        timeout = from_int(obj.get("timeout"))
        combo = from_str(obj.get("combo"))
        return X(value, timeout, combo)

    def to_dict(self) -> dict:
        result: dict = {}
        result["value"] = from_str(self.value)
        result["timeout"] = from_int(self.timeout)
        result["combo"] = from_str(self.combo)
        return result


@dataclass
class IDpullTypeElement:
    type: str
    mode: str
    x: Optional[X] = None
    y: Optional[X] = None

    @staticmethod
    def from_dict(obj: Any) -> 'IDpullTypeElement':
        assert isinstance(obj, dict)
        type = from_str(obj.get("type"))
        mode = from_str(obj.get("mode"))
        x = from_union([X.from_dict, from_none], obj.get("x"))
        y = from_union([X.from_dict, from_none], obj.get("y"))
        return IDpullTypeElement(type, mode, x, y)

    def to_dict(self) -> dict:
        result: dict = {}
        result["type"] = from_str(self.type)
        result["mode"] = from_str(self.mode)
        result["x"] = from_union([lambda x: to_class(X, x), from_none], self.x)
        result["y"] = from_union([lambda x: to_class(X, x), from_none], self.y)
        return result


def i_dpull_type_from_dict(s: Any) -> List[IDpullTypeElement]:
    return from_list(IDpullTypeElement.from_dict, s)


def i_dpull_type_to_dict(x: List[IDpullTypeElement]) -> Any:
    return from_list(lambda x: to_class(IDpullTypeElement, x), x)
