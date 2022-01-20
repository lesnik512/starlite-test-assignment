from typing import Any, Dict, List, Optional, TypeVar

import sqlalchemy as sa
from sqlalchemy.sql import operators

from app.db.base import Base


TBase = TypeVar("TBase", bound="BaseModel")

# https://github.com/absent1706/sqlalchemy-mixins/blob/master/sqlalchemy_mixins/smartquery.py
operators_map = {
    "isnull": lambda c, v: (c == None) if v else (c != None),
    "exact": operators.eq,
    "ne": operators.ne,  # not equal or is not (for None)
    "gt": operators.gt,  # greater than , >
    "ge": operators.ge,  # greater than or equal, >=
    "lt": operators.lt,  # lower than, <
    "le": operators.le,  # lower than or equal, <=
    "in": operators.in_op,
    "notin": operators.notin_op,
    "between": lambda c, v: c.between(v[0], v[1]),
    "like": operators.like_op,
    "ilike": operators.ilike_op,
    "startswith": operators.startswith_op,
    "istartswith": lambda c, v: c.ilike(v + "%"),
    "endswith": operators.endswith_op,
    "iendswith": lambda c, v: c.ilike("%" + v),
    "overlaps": lambda c, v: getattr(c, "overlaps")(v),
}


class BaseModel(Base):
    __abstract__ = True

    id = sa.Column(sa.Integer, primary_key=True)

    def __str__(self):
        return f"<{type(self).__name__}({self.id=})>"

    @classmethod
    def _build_sorting(cls, sorting: Dict[str, str]) -> List[Any]:
        """Build list of ORDER_BY clauses"""
        result = []
        for field_name, direction in sorting.items():
            field = getattr(cls, field_name)
            result.append(getattr(field, direction)())
        return result

    @classmethod
    def _build_filters(cls, filters: Dict[str, Any]) -> List[Any]:
        """Build list of WHERE conditions"""
        result = []
        for expression, value in filters.items():
            parts = expression.split("__")
            op_name = parts[1] if len(parts) > 1 else "exact"
            if op_name not in operators_map:
                raise KeyError(f"Expression {expression} has incorrect operator {op_name}")
            operator = operators_map[op_name]
            column = getattr(cls, parts[0])
            result.append(operator(column, value))
        return result

    @classmethod
    def _build_grouping(cls, grouping: List[str]) -> List[Any]:
        """Build list of GROUP_BY clauses"""
        result = []
        for field_name in grouping:
            result.append(getattr(cls, field_name))
        return result
