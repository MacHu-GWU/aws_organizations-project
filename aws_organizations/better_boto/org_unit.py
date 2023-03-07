# -*- coding: utf-8 -*-

import typing as T

from .model import (
    Parent,
    Child,
    OrganizationUnit,
    Account,
    ParentIterproxy,
    ChildIterproxy,
    OrganizationUnitIterproxy,
    AccountIterproxy,
)

if T.TYPE_CHECKING:
    from boto_session_manager import BotoSesManager


def _list_parents(
    bsm: "BotoSesManager",
    child_id: str,
    page_size: int = 20,
    max_results: int = 1000,
) -> T.Iterator[Parent]:
    paginator = bsm.organizations_client.get_paginator("list_parents")
    for response in paginator.paginate(
        ChildId=child_id,
        PaginationConfig=dict(
            PageSize=page_size,
            MaxResults=max_results,
        ),
    ):
        for dct in response.get("Parents", []):
            yield Parent(
                id=dct["Id"],
                type=dct["Type"],
            )


def list_parents(
    bsm: "BotoSesManager",
    child_id: str,
    page_size: int = 20,
    max_results: int = 1000,
) -> ParentIterproxy:
    return ParentIterproxy(
        _list_parents(
            bsm=bsm,
            child_id=child_id,
            page_size=page_size,
            max_results=max_results,
        )
    )


def _list_children(
    bsm: "BotoSesManager",
    parent_id: str,
    child_type: str,
    page_size: int = 20,
    max_results: int = 1000,
) -> T.Iterator[Child]:
    paginator = bsm.organizations_client.get_paginator("list_children")
    for response in paginator.paginate(
        ParentId=parent_id,
        ChildType=child_type,
        PaginationConfig=dict(
            PageSize=page_size,
            MaxResults=max_results,
        ),
    ):
        for dct in response.get("Children", []):
            yield Child(
                id=dct["Id"],
                type=dct["Type"],
            )


def list_children(
    bsm: "BotoSesManager",
    parent_id: str,
    child_type: str,
    page_size: int = 20,
    max_results: int = 1000,
) -> ChildIterproxy:
    return ChildIterproxy(
        _list_children(
            bsm=bsm,
            parent_id=parent_id,
            child_type=child_type,
            page_size=page_size,
            max_results=max_results,
        )
    )


def get_root_id(
    bsm: "BotoSesManager",
    aws_account_id: str,
) -> str:
    for parent in list_parents(bsm=bsm, child_id=aws_account_id):
        if parent.is_root():
            return parent.id
    raise ValueError("Could not find root id")


def _list_organizational_units_for_parent(
    bsm: "BotoSesManager",
    parent_id: str,
    page_size: int = 20,
    max_results: int = 1000,
) -> T.Iterator[OrganizationUnit]:
    paginator = bsm.organizations_client.get_paginator(
        "list_organizational_units_for_parent"
    )
    for response in paginator.paginate(
        ParentId=parent_id,
        PaginationConfig=dict(
            PageSize=page_size,
            MaxResults=max_results,
        ),
    ):
        for dct in response.get("OrganizationalUnits", []):
            yield OrganizationUnit(
                id=dct["Id"],
                arn=dct["Arn"],
                name=dct["Name"],
            )


def list_organizational_units_for_parent(
    bsm: "BotoSesManager",
    parent_id: str,
    page_size: int = 20,
    max_results: int = 1000,
) -> OrganizationUnitIterproxy:
    return OrganizationUnitIterproxy(
        _list_organizational_units_for_parent(
            bsm=bsm,
            parent_id=parent_id,
            page_size=page_size,
            max_results=max_results,
        )
    )


def _list_accounts_for_parent(
    bsm: "BotoSesManager",
    parent_id: str,
    page_size: int = 20,
    max_results: int = 1000,
) -> T.Iterator[Account]:
    paginator = bsm.organizations_client.get_paginator(
        "list_accounts_for_parent"
    )
    for response in paginator.paginate(
        ParentId=parent_id,
        PaginationConfig=dict(
            PageSize=page_size,
            MaxResults=max_results,
        ),
    ):
        for dct in response.get("Accounts", []):
            yield Account(
                id=dct["Id"],
                arn=dct["Arn"],
                name=dct["Name"],
                email=dct["Email"],
                status=dct["Status"],
                joined_method=dct["JoinedMethod"],
                joined_timestamp=dct["JoinedTimestamp"],
            )


def list_accounts_for_parent(
    bsm: "BotoSesManager",
    parent_id: str,
    page_size: int = 20,
    max_results: int = 1000,
) -> AccountIterproxy:
    return AccountIterproxy(
        _list_accounts_for_parent(
            bsm=bsm,
            parent_id=parent_id,
            page_size=page_size,
            max_results=max_results,
        )
    )
