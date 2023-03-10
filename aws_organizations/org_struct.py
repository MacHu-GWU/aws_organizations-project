# -*- coding: utf-8 -*-

"""
Organizational Structure objective oriented interface.

Ref:

- Core concepts: https://docs.aws.amazon.com/whitepapers/latest/organizing-your-aws-environment/core-concepts.html
"""

import typing as T
import enum
import dataclasses

from anytree import NodeMixin, RenderTree

from .better_boto import (
    Account,
    OrganizationalUnit,
    Organization,
    AccountIterproxy,
    OrganizationUnitIterproxy,
    get_root_id,
    list_organizational_units_for_parent,
    list_accounts_for_parent,
    describe_organization,
)

if T.TYPE_CHECKING:  # pragma: no cover
    from boto_session_manager import BotoSesManager

ROOT_NODE_NAME = "root"


class NodeTypeEnum(str, enum.Enum):
    ROOT = "Root"
    ORG_UNIT = "OrgUnit"
    ACCOUNT = "Account"


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
        if children:  # pragma: no cover
            self.children = children

    @property
    def organization_or_account_or_organizational_unit(
        self,
    ) -> T.Union[Organization, OrganizationalUnit, Account]:  # pragma: no cover
        return self.obj

    @property
    def parent_id(self) -> T.Optional[str]:
        if self.parent is None:
            return None
        else:
            return self.parent.id

    def __repr__(self) -> str:
        return f"{self.name} ({self.type} {self.id!r})"

    @property
    def path_key(self) -> str:
        return " | ".join([node.name for node in self.path])

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

    @property
    def accounts(self) -> T.List[Account]:
        return self.iter_accounts(recursive=False).all()

    @property
    def org_units(self) -> T.List[OrganizationalUnit]:
        return self.iter_org_units(recursive=False).all()

    @property
    def all_accounts(self) -> T.List[Account]:
        return self.iter_accounts(recursive=True).all()

    @property
    def all_org_units(self) -> T.List[OrganizationalUnit]:
        return self.iter_org_units(recursive=True).all()

    @property
    def accounts_names(self) -> T.List[str]:
        return [account.name for account in self.accounts]

    @property
    def org_units_names(self) -> T.List[str]:
        return [ou.name for ou in self.org_units]

    @property
    def all_accounts_names(self) -> T.List[str]:
        return [account.name for account in self.all_accounts]

    @property
    def all_org_units_names(self) -> T.List[str]:
        return [ou.name for ou in self.all_org_units]


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

    Example:

        >>> from boto_session_manager import BotoSesManager
        >>> bsm = BotoSesManager() # or BotoSesManager(profile_name="my-profile")
        >>> org_struct = OrgStructure.get_org_structure(bsm)
        >>> org_struct.visualize()
        Root (ROOT 'r-hnp9')
        ├── app (Org Unit 'ou-hnp9-vq6m3h5y')
        │   └── myorg-app-dev (Account '222222222222')
        ├── infra (Org Unit 'ou-hnp9-cxgi4leg')
        │   └── myorg-infra (Account '333333333333')
        ├── sandbox (Org Unit 'ou-hnp9-r7cuoq1v')
        ├── ml (Org Unit 'ou-hnp9-s4uirmja')
        │   ├── myorg-ml-dev (Account '444444444444')
        │   ├── myorg-ml-staging (Account '555555555555')
        │   └── myorg-ml-prod (Account '666666666666')
        └── awshsh-root (Account '111111111111')

        >>> org_struct.root.organization_or_account_or_organizational_unit
        Organization(id='o-a1b2c3d4', arn='arn:aws:organizations::111122223333:organization/o-a1b2c3d4')
        >>> org_struct.root.accounts
        ...
        >>> org_struct.root.org_units
        ...
        >>> org_struct.root.all_accounts
        ...
        >>> org_struct.root.all_org_units
        ...
    """

    root: Node = dataclasses.field()

    _id_to_node: T.Dict[str, Node] = dataclasses.field(init=False, default_factory=dict)
    _name_to_node: T.Dict[str, Node] = dataclasses.field(
        init=False, default_factory=dict
    )

    def __post_init__(self):
        self._id_to_node[self.root_id] = self.root
        self._id_to_node[self.root.obj.id] = self.root

        node: Node
        for _, _, node in RenderTree(self.root):
            self._id_to_node[node.id] = node
            self._name_to_node[node.name] = node

    @property
    def root_id(self) -> str:
        return self.root.obj.root_id

    def visualize(self) -> str:
        """
        Visualize the organization structure tree. It returns a string that
        can be printed.
        """
        return str(RenderTree(self.root))

    def to_csv(self, sep="\t") -> str:
        """ """
        rows = [("Type", "Path", "Id", "ParentId", "RootId")]
        node: Node
        for pre, fill, node in RenderTree(self.root):
            rows.append(
                (
                    node.type,
                    node.path_key,
                    node.id,
                    str(node.parent_id),
                    node.obj.root_id,
                )
            )
        return "\n".join([sep.join(row) for row in rows])

    def get_node_by_id(self, id: str) -> Node:
        """
        Get a node by id.
        """
        return self._id_to_node[id]

    def get_node_by_name(self, name: str) -> Node:
        """
        Get a node by name.
        """
        return self._name_to_node[name]

    def _resolve_node(
        self,
        node_or_object_or_id: T.Union[
            Node, Organization, OrganizationalUnit, Account, str
        ],
    ) -> Node:
        if isinstance(node_or_object_or_id, str):
            return self._id_to_node[node_or_object_or_id]
        elif isinstance(node_or_object_or_id, Node):
            return node_or_object_or_id
        else:
            return self._id_to_node[node_or_object_or_id.id]

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

        :param bsm: the boto session manager of any AWS Account that is in
            the desired organization, doesn't have to be the management
            AWS Account (Root).
        """
        org = describe_organization(bsm=bsm)

        root_id = get_root_id(bsm=bsm, aws_account_id=org.master_account_id)
        org.root_id = root_id

        root_node = Node(
            id=org.id,
            name=ROOT_NODE_NAME,
            type=NodeTypeEnum.ROOT.value,
            obj=org,
        )

        def walk_through(node: Node):
            """
            depth first search to walk through the organization structure tree or
            organization unit.
            """
            if node.obj.is_org():
                parent_id = node.obj.root_id
            elif node.obj.is_ou():
                parent_id = node.obj.id
            else:  # pragma: no cover
                raise NotImplementedError

            for ou in list_organizational_units_for_parent(
                bsm=bsm, parent_id=parent_id
            ):
                ou.root_id = root_id
                leaf = Node(
                    id=ou.id,
                    name=ou.name,
                    type=NodeTypeEnum.ORG_UNIT.value,
                    obj=ou,
                    parent=node,
                )
                walk_through(leaf)

            for account in list_accounts_for_parent(bsm=bsm, parent_id=parent_id):
                account.root_id = root_id
                leaf = Node(
                    id=account.id,
                    name=account.name,
                    type=NodeTypeEnum.ACCOUNT.value,
                    obj=account,
                    parent=node,
                )

        walk_through(root_node)

        return OrgStructure(root=root_node)

    def serialize(self) -> dict:
        entities: T.List[dict] = list()
        node: Node
        for pre, fill, node in RenderTree(self.root):
            # print(node.id, node.name, node.organization_or_account_or_organizational_unit, node.parent)
            entity = dict(
                id=node.id,
                name=node.name,
                type=node.type,
                obj=node.obj.to_dict(),
                parent_id=node.parent.id if node.parent else None,
            )
            entities.append(entity)
        return dict(entities=entities)

    @classmethod
    def deserialize(cls, data: dict) -> "OrgStructure":
        node_mapper = {}
        type_to_object = {
            NodeTypeEnum.ACCOUNT.value: Account,
            NodeTypeEnum.ORG_UNIT.value: OrganizationalUnit,
            NodeTypeEnum.ROOT.value: Organization,
        }
        root: T.Optional[Node] = None
        for entity in data["entities"]:
            entity_object = type_to_object[entity["type"]].from_dict(entity["obj"])
            node = Node(
                id=entity["id"],
                name=entity["name"],
                type=entity["type"],
                obj=entity_object,
            )
            node_mapper[entity["id"]] = node
            if entity["type"] == NodeTypeEnum.ROOT.value:
                root = node
        if root is None:  # pragma: no cover
            raise ValueError("No root node found in the data.")

        for entity in data["entities"]:
            node = node_mapper[entity["id"]]
            parent_id = entity["parent_id"]
            if parent_id is not None:
                parent_node = node_mapper[parent_id]
                node.parent = parent_node

        return OrgStructure(root=root)
