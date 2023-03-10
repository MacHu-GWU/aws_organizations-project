# -*- coding: utf-8 -*-

"""
AWS Organizations related data model.
"""

import typing as T
import enum
import dataclasses
from datetime import datetime

from iterproxy import IterProxy


@dataclasses.dataclass
class BaseModel:
    def to_dict(self) -> dict:
        return dataclasses.asdict(self)

    @classmethod
    def from_dict(cls, data: dict):
        return cls(**data)


class ParentTypeEnum(str, enum.Enum):
    ROOT = "ROOT"
    ORGANIZATIONAL_UNIT = "ORGANIZATIONAL_UNIT"


@dataclasses.dataclass
class Parent(BaseModel):
    id: str = dataclasses.field()
    type: str = dataclasses.field()

    def is_root(self) -> bool:  # pragma: no cover
        return self.type == ParentTypeEnum.ROOT.value

    def is_ou(self) -> bool:  # pragma: no cover
        return self.type == ParentTypeEnum.ORGANIZATIONAL_UNIT.value


class ChildTypeEnum(str, enum.Enum):
    ACCOUNT = "ACCOUNT"
    ORGANIZATIONAL_UNIT = "ORGANIZATIONAL_UNIT"


@dataclasses.dataclass
class Child(BaseModel):
    id: str = dataclasses.field()
    type: str = dataclasses.field()

    def is_account(self) -> bool:  # pragma: no cover
        return self.type == ChildTypeEnum.ACCOUNT.value

    def is_ou(self) -> bool:  # pragma: no cover
        return self.type == ChildTypeEnum.ORGANIZATIONAL_UNIT.value


class AccountOrOrgUnitOrOrg:
    """
    Mixin class for Account, OrganizationUnit and Organization.

    They all have three common testing methods
    ``is_account()``, ``is_ou()``, and ``is_org()``.
    """

    def is_account(self) -> bool:  # pragma: no cover
        return False

    def is_ou(self) -> bool:  # pragma: no cover
        return False

    def is_org(self) -> bool:  # pragma: no cover
        return False


class AccountStatusEnum(str, enum.Enum):
    ACTIVE = "ACTIVE"
    SUSPENDED = "SUSPENDED"
    PENDING_CLOSURE = "PENDING_CLOSURE"


class AccountJoinedMethodEnum(str, enum.Enum):
    INVITED = "INVITED"
    CREATED = "CREATED"


@dataclasses.dataclass
class Account(
    BaseModel,
    AccountOrOrgUnitOrOrg,
):
    """
    Represents an AWS Account.
    """

    id: T.Optional[str] = dataclasses.field(default=None)
    arn: T.Optional[str] = dataclasses.field(default=None)
    name: T.Optional[str] = dataclasses.field(default=None)
    email: T.Optional[str] = dataclasses.field(default=None)
    status: T.Optional[str] = dataclasses.field(default=None)
    joined_method: T.Optional[str] = dataclasses.field(default=None)
    joined_timestamp: T.Optional[datetime] = dataclasses.field(default=None)

    root_id: T.Optional[str] = dataclasses.field(default=None)

    def is_account(self) -> bool:  # pragma: no cover
        return True


@dataclasses.dataclass
class OrganizationalUnit(
    BaseModel,
    AccountOrOrgUnitOrOrg,
):
    """
    Represents an AWS Organization Unit.
    """

    id: T.Optional[str] = dataclasses.field(default=None)
    arn: T.Optional[str] = dataclasses.field(default=None)
    name: T.Optional[str] = dataclasses.field(default=None)

    root_id: T.Optional[str] = dataclasses.field(default=None)

    def is_ou(self) -> bool:  # pragma: no cover
        return True


@dataclasses.dataclass
class Organization(
    BaseModel,
    AccountOrOrgUnitOrOrg,
):
    """
    Represents an AWS Organization.
    """

    id: T.Optional[str] = dataclasses.field(default=None)
    arn: T.Optional[str] = dataclasses.field(default=None)
    feature_set: T.Optional[str] = dataclasses.field(default=None)
    master_account_arn: T.Optional[str] = dataclasses.field(default=None)
    master_account_id: T.Optional[str] = dataclasses.field(default=None)
    master_account_email: T.Optional[str] = dataclasses.field(default=None)
    available_policy_types: T.List[dict] = dataclasses.field(default_factory=list)

    root_id: T.Optional[str] = dataclasses.field(default=None)

    def is_org(self) -> bool:  # pragma: no cover
        return True


# ------------------------------------------------------------------------------
# Iterproxy
# ------------------------------------------------------------------------------
class ParentIterproxy(IterProxy[Parent]):
    pass


class ChildIterproxy(IterProxy[Child]):
    pass


class AccountIterproxy(IterProxy[Account]):
    pass


class OrganizationUnitIterproxy(IterProxy[OrganizationalUnit]):
    pass
