import inspect
from typing import (
    Any,
    Generic,
    Optional,
    Type,
    TypeVar,
    Union,
    get_args,
    get_origin,
    get_type_hints,
)

from pydantic import BaseModel, create_model
from pydantic.fields import Field, FieldInfo

T = TypeVar("T")


class Partial(Generic[T]):
    def __class_getitem__(cls, model: Type[T]) -> Type[BaseModel]:
        if inspect.isclass(model) and issubclass(model, BaseModel):
            return create_partial_pydantic(model)
        elif hasattr(model, "__annotations__"):
            return create_partial_typed_dict(model)
        else:
            raise TypeError(f"Partial does not support {model}")


def create_partial_pydantic(model: Type[T]):
    if not (inspect.isclass(model) and issubclass(model, BaseModel)):
        raise TypeError()

    fields: dict[str, Any] = {}
    for name, field in model.model_fields.items():
        if field.is_required() or (
            field.json_schema_extra is not None
            and isinstance(field.json_schema_extra, dict)
            and field.json_schema_extra.get("required", False)
        ):
            fields[name] = (
                Optional[field.annotation],
                copy_pydantic_field(
                    field,
                    default=None,
                    default_factory=None,
                ),
            )

    return create_model(
        f"Partial{model.__name__}",
        __base__=model,
        **fields,
    )


def copy_pydantic_field(field_info: FieldInfo, **overrides: Any) -> FieldInfo:
    base_kwargs: dict[str, Any] = {
        k: v
        for k, v in field_info.__repr_args__()
        if k and k not in ("extra", "annotation", "required")
    }

    return Field(**{**base_kwargs, **overrides})


def create_partial_typed_dict(model: Type[T]) -> Type[BaseModel]:
    annotations = get_type_hints(model)
    fields: dict[str, Any] = {
        name: (make_optional(typ), None) for name, typ in annotations.items()
    }

    return create_model(f"Partial{model.__name__}", **fields)


def make_optional(typ):
    origin = get_origin(typ)
    args = get_args(typ)

    if origin is Union and type(None) in args:
        return typ
    return Optional[typ]
