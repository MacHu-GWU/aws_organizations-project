# -*- coding: utf-8 -*-

from boto_session_manager import BotoSesManager
from rich import print as rprint

import aws_organizations
from aws_organizations.org_struct import get_org_structure
from aws_organizations.better_boto.org_unit import list_parents, list_children

bsm = BotoSesManager(profile_name="awshsh_root_us_east_1")
# bsm = BotoSesManager(profile_name="awshsh_app_dev_us_east_1")

# root_id = aws_organizations.better_boto.get_root_id(bsm=bsm, aws_account_id=bsm.aws_account_id)
# print(f"root_id = {root_id!r}")

# ------------------------------------------------------------------------------
# list_children
# ------------------------------------------------------------------------------
# res = aws_organizations.better_boto.list_children(
#     bsm=bsm,
#     parent_id=root_id,
#     child_type=aws_organizations.better_boto.ChildTypeEnum.ORGANIZATIONAL_UNIT.value,
# ).all()
# rprint(res)
#
# for child in res:
#     res_ = aws_organizations.better_boto.list_children(
#         bsm=bsm,
#         parent_id=child.id,
#         child_type=aws_organizations.better_boto.ChildTypeEnum.ACCOUNT.value,
#     ).all()
#     rprint(f"children of {child}:")
#     rprint(res_)


# ------------------------------------------------------------------------------
# list_organizational_units_for_parent
# ------------------------------------------------------------------------------
# res = aws_organizations.better_boto.list_organizational_units_for_parent(
#     bsm=bsm,
#     parent_id=root_id,
# ).all()
# print(f"------ organization units in {root_id!r}")
# rprint(res)

# ------------------------------------------------------------------------------
# list_accounts_for_parent
# ------------------------------------------------------------------------------
# res = aws_organizations.better_boto.list_accounts_for_parent(
#     bsm=bsm,
#     parent_id=root_id,
# ).all()
# print(f"------ accounts in {root_id!r}")
# rprint(res)

# ------------------------------------------------------------------------------
# get_org_structure
# ------------------------------------------------------------------------------
get_org_structure(bsm=bsm)
