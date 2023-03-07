# -*- coding: utf-8 -*-

import typing as T
import enum
import dataclasses
from datetime import datetime

from iterproxy import IterProxy


class BaseModel:
    pass


class ParentTypeEnum(str, enum.Enum):
    ROOT = "ROOT"
    ORGANIZATIONAL_UNIT = "ORGANIZATIONAL_UNIT"


@dataclasses.dataclass
class Parent(BaseModel):
    id: str = dataclasses.field()
    type: str = dataclasses.field()

    def is_root(self) -> bool:
        return self.type == ParentTypeEnum.ROOT.value

    def is_ou(self) -> bool:
        return self.type == ParentTypeEnum.ORGANIZATIONAL_UNIT.value


class ChildTypeEnum(str, enum.Enum):
    ACCOUNT = "ACCOUNT"
    ORGANIZATIONAL_UNIT = "ORGANIZATIONAL_UNIT"


@dataclasses.dataclass
class Child(BaseModel):
    id: str = dataclasses.field()
    type: str = dataclasses.field()

    def is_account(self) -> bool:
        return self.type == ChildTypeEnum.ACCOUNT.value

    def is_ou(self) -> bool:
        return self.type == ChildTypeEnum.ORGANIZATIONAL_UNIT.value


class AccountStatusEnum(str, enum.Enum):
    ACTIVE = "ACTIVE"
    SUSPENDED = "SUSPENDED"
    PENDING_CLOSURE = "PENDING_CLOSURE"


class AccountJoinedMethodEnum(str, enum.Enum):
    INVITED = "INVITED"
    CREATED = "CREATED"


@dataclasses.dataclass
class Account(BaseModel):
    id: T.Optional[str] = dataclasses.field(default=None)
    arn: T.Optional[str] = dataclasses.field(default=None)
    name: T.Optional[str] = dataclasses.field(default=None)
    email: T.Optional[str] = dataclasses.field(default=None)
    status: T.Optional[str] = dataclasses.field(default=None)
    joined_method: T.Optional[str] = dataclasses.field(default=None)
    joined_timestamp: T.Optional[datetime] = dataclasses.field(default=None)
    # relationship
    parent: "OrganizationUnit" = dataclasses.field(default=None)


@dataclasses.dataclass
class OrganizationUnit(BaseModel):
    id: T.Optional[str] = dataclasses.field(default=None)
    arn: T.Optional[str] = dataclasses.field(default=None)
    name: T.Optional[str] = dataclasses.field(default=None)
    # relationship
    parent: "OrganizationUnit" = dataclasses.field(default=None)
    accounts: T.List[Account] = dataclasses.field(default_factory=list)
    children: T.List["OrganizationUnit"] = dataclasses.field(default_factory=list)


# ------------------------------------------------------------------------------
# Iterproxy
# ------------------------------------------------------------------------------
class ParentIterproxy(IterProxy[Parent]):
    pass


class ChildIterproxy(IterProxy[Child]):
    pass


class AccountIterproxy(IterProxy[Account]):
    pass


class OrganizationUnitIterproxy(IterProxy[OrganizationUnit]):
    pass
