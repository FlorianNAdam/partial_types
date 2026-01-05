from typing import Any, Generic, Optional, Type, TypeVar

from pydantic import BaseModel, create_model
from pydantic.fields import Field, FieldInfo

T = TypeVar("T", bound=BaseModel)


class Partial(Generic[T]):
    def __class_getitem__(cls, model: Type[T]) -> Type[BaseModel]:
        fields: dict[str, Any] = {}
        for name, field in model.model_fields.items():
            if field.is_required() or (
                field.json_schema_extra is not None
                and isinstance(field.json_schema_extra, dict)
                and field.json_schema_extra.get("required", False)
            ):
                fields[name] = (
                    Optional[field.annotation],
                    copy_field(
                        field,
                        default=None,
                        default_factory=None,
                    ),
                )

        print("hallo welt")

        return create_model(
            f"Partial{model.__name__}",
            __base__=model,
            **fields,
        )


def copy_field(field_info: FieldInfo, **overrides: Any) -> FieldInfo:
    base_kwargs: dict[str, Any] = {
        k: v
        for k, v in field_info.__repr_args__()
        if k and k not in ("extra", "annotation", "required")
    }

    return Field(**{**base_kwargs, **overrides})
