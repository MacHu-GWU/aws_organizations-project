# -*- coding: utf-8 -*-

import json
from pathlib import Path

from tabulate import tabulate
import aws_organizations.api as aws_orgs

root_id = "r-123"
org = aws_orgs.Organization(
    id="o-789",
    root_id=root_id,
)
root_node = aws_orgs.Node(
    id=org.id,
    name=aws_orgs.ROOT_NODE_NAME,
    type=aws_orgs.NodeTypeEnum.ROOT.value,
    obj=org,
)

acc = aws_orgs.Account(
    id="111111111111",
    name="admin",
    root_id=org.root_id,
)
acc_node = aws_orgs.Node(
    id=acc.id,
    name=acc.name,
    type=aws_orgs.NodeTypeEnum.ACCOUNT.value,
    obj=acc,
    parent=root_node,
)

sec_ou = aws_orgs.OrganizationalUnit(
    id="ou-111",
    name="Security",
    root_id=org.root_id,
)
sec_ou_node = aws_orgs.Node(
    id=sec_ou.id,
    name=sec_ou.name,
    type=aws_orgs.NodeTypeEnum.ORG_UNIT.value,
    obj=sec_ou,
    parent=root_node,
)

acc_sec_login = aws_orgs.Account(
    id="222222222222",
    name="sec_login",
    root_id=org.root_id,
)
acc_sec_login_node = aws_orgs.Node(
    id=acc_sec_login.id,
    name=acc_sec_login.name,
    type=aws_orgs.NodeTypeEnum.ACCOUNT.value,
    obj=acc_sec_login,
    parent=sec_ou_node,
)

acc_sec_audit = aws_orgs.Account(
    id="333333333333",
    name="sec_audit",
    root_id=org.root_id,
)
acc_sec_audit_node = aws_orgs.Node(
    id=acc_sec_audit.id,
    name=acc_sec_audit.name,
    type=aws_orgs.NodeTypeEnum.ACCOUNT.value,
    obj=acc_sec_audit,
    parent=sec_ou_node,
)

app_ou = aws_orgs.OrganizationalUnit(
    id="ou-222",
    name="Application",
    root_id=org.root_id,
)
app_ou_node = aws_orgs.Node(
    id=app_ou.id,
    name=app_ou.name,
    type=aws_orgs.NodeTypeEnum.ORG_UNIT.value,
    obj=app_ou,
    parent=root_node,
)

acc_devops = aws_orgs.Account(
    id="444444444444",
    name="devops",
    root_id=org.root_id,
)
acc_devops_node = aws_orgs.Node(
    id=acc_devops.id,
    name=acc_devops.name,
    type=aws_orgs.NodeTypeEnum.ACCOUNT.value,
    obj=acc_devops,
    parent=app_ou_node,
)

acc_dev = aws_orgs.Account(
    id="555555555555",
    name="app-dev",
    root_id=org.root_id,
)
acc_dev_node = aws_orgs.Node(
    id=acc_dev.id,
    name=acc_dev.name,
    type=aws_orgs.NodeTypeEnum.ACCOUNT.value,
    obj=acc_dev,
    parent=app_ou_node,
)

app_test = aws_orgs.Account(
    id="666666666666",
    name="app-test",
    root_id=org.root_id,
)
app_test_node = aws_orgs.Node(
    id=app_test.id,
    name=app_test.name,
    type=aws_orgs.NodeTypeEnum.ACCOUNT.value,
    obj=app_test,
    parent=app_ou_node,
)

app_prod = aws_orgs.Account(
    id="777777777777",
    name="app-prod",
    root_id=org.root_id,
)
app_prod_node = aws_orgs.Node(
    id=app_prod.id,
    name=app_prod.name,
    type=aws_orgs.NodeTypeEnum.ACCOUNT.value,
    obj=app_prod,
    parent=app_ou_node,
)

org_struct = aws_orgs.OrgStructure(
    root=root_node,
)

dir_here = Path(__file__).absolute().parent
path_json = dir_here / "org_struct.json"
path_mermaid = dir_here / "org_struct.md"

path_json.write_text(json.dumps(org_struct.serialize(), indent=4))
path_mermaid.write_text(org_struct.to_mermaid())
