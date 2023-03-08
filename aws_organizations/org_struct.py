# -*- coding: utf-8 -*-

"""
Organizational Structure objective oriented interface.

Ref:

- Core concepts: https://docs.aws.amazon.com/whitepapers/latest/organizing-your-aws-environment/core-concepts.html
"""

import dataclasses
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
    OrganizationalUnit,
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
        obj: T.Union[Organization, OrganizationalUnit, Account],
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
        return f"{self.name} ({self.type} {self.id!r})"

    @property
    def path_key(self) -> str:
        return " | ".join([
            node.name
            for node in self.path
        ])

    def _iter_accounts(self, recursive: bool = True) -> T.Iterable[Account]:
        node: Node
        if recursive:
            for _, _, node in RenderTree(self):
                if node.obj.is_account():
                    yield node.obj
        else:
            for node in self.root.children:
                if node.obj.is_account():
                    yield node.obj

    def iter_accounts(self, recursive: bool = True) -> AccountIterproxy:
        return AccountIterproxy(self._iter_accounts(recursive=recursive))

    def _iter_org_units(self, recursive: bool = True) -> T.Iterable[Account]:
        node: Node
        if recursive:
            for _, _, node in RenderTree(self):
                if node.obj.is_ou():
                    yield node.obj
        else:
            for node in self.root.children:
                if node.obj.is_ou():
                    yield node.obj

    def iter_org_units(self, recursive: bool = True) -> OrganizationUnitIterproxy:
        return OrganizationUnitIterproxy(self._iter_org_units(recursive=recursive))


@dataclasses.dataclass
class OrgStructure:
    """
    Abstraction of the AWS Organization structure.

    It is a tree structure of Organization, OrganizationalUnit, and Account.

    API:

    - ``self.root`` is the root node of the tree.
    - ``self.visualize()`` can visualize the tree.
    - ``for ou in self.root.iter_org_units(recursive=True):`` can iterate all OU.
    - ``for acc in self.root.iter_org_accounts(recursive=True):`` can iterate all Accounts.
    - ``self.is_x_in_y()`` can test if an account / ou is in an ou or org.
    """
    root: Node = dataclasses.field()

    _mapper: T.Dict[str, Node] = dataclasses.field(init=False, default_factory=dict)

    def __post_init__(self):
        self._mapper[self.root.id] = self.root
        self._mapper[self.root.obj.id] = self.root
        node: Node
        for _, _, node in RenderTree(self.root):
            self._mapper[node.id] = node

    def visualize(self):
        """
        Visualize (print) the organization structure tree.
        """
        print(RenderTree(self.root))

    def to_csv(self, sep="\t") -> str:
        rows = [
            ("Type", "Path", "Id")
        ]
        node: Node
        for pre, fill, node in RenderTree(self.root):
            rows.append(
                (
                    node.type,
                    node.path_key,
                    node.id,
                )
            )
        return "\n".join([
            sep.join(row)
            for row in rows
        ])

    def get_node(self, id: str) -> Node:
        """
        Get a node by id.
        """
        return self._mapper[id]

    def _resolve_node(
        self,
        node_or_object_or_id: T.Union[
            Node, Organization, OrganizationalUnit, Account, str
        ],
    ) -> Node:
        if isinstance(node_or_object_or_id, str):
            return self._mapper[node_or_object_or_id]
        elif isinstance(node_or_object_or_id, Node):
            return node_or_object_or_id
        else:
            return self._mapper[node_or_object_or_id.id]

    def _is_x_in_y(
        self,
        node_or_object_or_id_x: T.Union[
            Node, Organization, OrganizationalUnit, Account, str
        ],
        node_or_object_or_id_y: T.Union[Node, Organization, OrganizationalUnit, str],
    ) -> bool:
        node_x = self._resolve_node(node_or_object_or_id_x)
        node_y = self._resolve_node(node_or_object_or_id_y)
        return node_y.id in {ou.id for ou in node_x.ancestors}

    def is_x_in_y(
        self,
        x: T.Union[Node, Organization, OrganizationalUnit, Account, str],
        y: T.Union[Node, Organization, OrganizationalUnit, Account, str],
    ) -> bool:
        """
        Test if an account / ou is in an ou or org.
        """
        return self._is_x_in_y(x, y)

    @classmethod
    def get_org_structure(cls, bsm: "BotoSesManager") -> "OrgStructure":
        """
        Get the root node of the organization structure tree.

        :param bsm: the boto session manager of the management AWS Account (Root)
            of this organization.
        """
        org = describe_organization(bsm=bsm)

        root_id = get_root_id(bsm=bsm, aws_account_id=bsm.aws_account_id)

        ROOT = Node(id=root_id, name="Root", type="ROOT", obj=org)

        def walk_through(root: Node):
            """
            depth first search to walk through the organization structure tree or
            organization unit.
            """
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
                walk_through(leaf)

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

        walk_through(ROOT)

        # print(RenderTree(ROOT))

        # rprint(ROOT.obj.parent_obj)
        # rprint(ROOT.obj.org_units_names)
        # rprint(ROOT.obj.accounts_names)

        # rprint(ROOT.obj.org_units[0].name)
        # rprint(ROOT.obj.org_units[0].org_units_names)
        # rprint(ROOT.obj.org_units[0].accounts_names)

        # rprint(ROOT.obj.org_units[0].parent_obj.arn)

        return OrgStructure(root=ROOT)
