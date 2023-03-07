# -*- coding: utf-8 -*-

"""
Organizational Structure

Ref:

- Core concepts: https://docs.aws.amazon.com/whitepapers/latest/organizing-your-aws-environment/core-concepts.html
"""

import typing as T

from anytree import NodeMixin, RenderTree

# from rich import print as rprint

from .better_boto import (
    ParentTypeEnum,
    Parent,
    ChildTypeEnum,
    Child,
    AccountStatusEnum,
    AccountJoinedMethodEnum,
    Account,
    OrganizationUnit,
    Organization,

    AccountIterproxy,
    OrganizationUnitIterproxy,

    list_parents,
    list_children,
    get_root_id,
    list_organizational_units_for_parent,
    list_accounts_for_parent,
    describe_organization,
)

if T.TYPE_CHECKING:
    from boto_session_manager import BotoSesManager


class Node(NodeMixin):
    """
    A node on the organization structure Tree.

    :param id: the id of the object on the node
    :param name: human friendly name, the name of the object on the node
    :param obj: the object on the node could be one of
        Organization, OrganizationUnit, and Account
    """
    def __init__(
        self,
        id: str,
        name: str,
        type: str,
        obj: T.Union[Organization, OrganizationUnit, Account],
        parent=None,
        children=None,
    ):
        self.id = id
        self.name = name
        self.type = type
        self.obj = obj
        self.parent = parent
        if children:
            self.children = children

    def __repr__(self) -> str:
        return f"{self.name} ({self.type})"

    def _iter_accounts(self) -> T.Iterable[Account]:
        node: Node
        for _, _, node in RenderTree(self):
            if node.obj.is_account():
                yield node.obj

    def iter_accounts(self) -> AccountIterproxy:
        return AccountIterproxy(self._iter_accounts())

    def _iter_org_units(self) -> T.Iterable[Account]:
        node: Node
        for _, _, node in RenderTree(self):
            if node.obj.is_ou():
                yield node.obj

    def iter_org_units(self) -> OrganizationUnitIterproxy:
        return OrganizationUnitIterproxy(self._iter_org_units())

def get_org_structure(bsm: "BotoSesManager") -> Node:
    """
    Get the root node of the organization structure tree.
    """
    org = describe_organization(bsm=bsm)
    root_id = get_root_id(bsm=bsm, aws_account_id=bsm.aws_account_id)

    ROOT = Node(id=root_id, name="Root", type="ROOT", obj=org)

    def walk_root(root: Node):
        for ou in list_organizational_units_for_parent(bsm=bsm, parent_id=root.id):
            ou.parent_obj = root.obj
            root.obj.org_units.append(ou)
            leaf = Node(
                id=ou.id,
                name=ou.name,
                type="Org Unit",
                obj=ou,
                parent=root,
            )
            walk_root(leaf)

        for account in list_accounts_for_parent(bsm=bsm, parent_id=root.id):
            account.parent_obj = root.obj
            root.obj.accounts.append(account)
            leaf = Node(
                id=account.id,
                name=account.name,
                type="Account",
                obj=account,
                parent=root,
            )

    walk_root(ROOT)

    # print(RenderTree(ROOT))

    # rprint(ROOT.obj.parent_obj)
    # rprint(ROOT.obj.org_units_names)
    # rprint(ROOT.obj.accounts_names)

    # rprint(ROOT.obj.org_units[0].name)
    # rprint(ROOT.obj.org_units[0].org_units_names)
    # rprint(ROOT.obj.org_units[0].accounts_names)

    # rprint(ROOT.obj.org_units[0].parent_obj.arn)

    return ROOT
