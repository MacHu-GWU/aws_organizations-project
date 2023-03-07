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


class AccountOrOrgUnitOrOrg:
    def is_account(self) -> bool:
        return False

    def is_ou(self) -> bool:
        return False

    def is_org(self) -> bool:
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
    id: T.Optional[str] = dataclasses.field(default=None)
    arn: T.Optional[str] = dataclasses.field(default=None)
    name: T.Optional[str] = dataclasses.field(default=None)
    email: T.Optional[str] = dataclasses.field(default=None)
    status: T.Optional[str] = dataclasses.field(default=None)
    joined_method: T.Optional[str] = dataclasses.field(default=None)
    joined_timestamp: T.Optional[datetime] = dataclasses.field(default=None)

    # relationship
    parent_obj: T.Union["Organization", "OrganizationUnit"] = dataclasses.field(
        default=None
    )

    def is_account(self) -> bool:
        return True


@dataclasses.dataclass
class OrganizationUnit(
    BaseModel,
    AccountOrOrgUnitOrOrg,
):
    id: T.Optional[str] = dataclasses.field(default=None)
    arn: T.Optional[str] = dataclasses.field(default=None)
    name: T.Optional[str] = dataclasses.field(default=None)

    # relationship
    parent_obj: T.Union["Organization", "OrganizationUnit"] = dataclasses.field(
        default=None
    )
    org_units: T.List["OrganizationUnit"] = dataclasses.field(default_factory=list)
    accounts: T.List[Account] = dataclasses.field(default_factory=list)

    def is_ou(self) -> bool:
        return True

    @property
    def org_units_names(self) -> T.List[str]:
        return [ou.name for ou in self.org_units]

    @property
    def accounts_names(self) -> T.List[str]:
        return [account.name for account in self.accounts]


@dataclasses.dataclass
class Organization(
    BaseModel,
    AccountOrOrgUnitOrOrg,
):
    id: T.Optional[str] = dataclasses.field(default=None)
    arn: T.Optional[str] = dataclasses.field(default=None)
    feature_set: T.Optional[str] = dataclasses.field(default=None)
    master_account_arn: T.Optional[str] = dataclasses.field(default=None)
    master_account_id: T.Optional[str] = dataclasses.field(default=None)
    master_account_email: T.Optional[str] = dataclasses.field(default=None)
    available_policy_types: T.List[dict] = dataclasses.field(default_factory=list)

    # relationship
    parent_obj: None = dataclasses.field(default=None)
    org_units: T.List["OrganizationUnit"] = dataclasses.field(default_factory=list)
    accounts: T.List[Account] = dataclasses.field(default_factory=list)

    @property
    def name(self) -> str:
        return f"Organization({self.id})"

    def is_org(self) -> bool:
        return True

    @property
    def org_units_names(self) -> T.List[str]:
        return [ou.name for ou in self.org_units]

    @property
    def accounts_names(self) -> T.List[str]:
        return [account.name for account in self.accounts]


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
