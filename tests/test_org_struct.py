# -*- coding: utf-8 -*-

import os
import pytest
from boto_session_manager import BotoSesManager
from aws_organizations.org_struct import (
    ROOT_NODE_NAME,
    NodeTypeEnum,
    OrgStructure,
)

IS_CI = "CI" in os.environ


@pytest.mark.skipif(IS_CI, reason="This test is not meant to run in CI")
def _run_test_case(org_struct: OrgStructure):
    # --------------------------------------------------------------------------
    # Root node
    # --------------------------------------------------------------------------
    root = org_struct.root
    assert (
        root.id == root.obj.id
    )  # root.id is the root_id, root.obj.id is the organization id
    assert root.name == ROOT_NODE_NAME
    assert root.type == NodeTypeEnum.ROOT.value

    assert org_struct.root_id == root.obj.root_id
    assert root.is_root is True
    assert root.obj.is_org() is True

    # --------------------------------------------------------------------------
    # Iterate account, ou
    # --------------------------------------------------------------------------
    assert len(root.accounts) == 1
    assert root.accounts[0].name == "awshsh-root"

    assert len(root.all_accounts) == 6
    assert len(root.all_org_units) == 4

    assert len(root.accounts) == len(root.accounts_names)
    assert len(root.org_units) == len(root.org_units_names)
    assert len(root.all_accounts) == len(root.all_accounts_names)
    assert len(root.all_org_units) == len(root.all_org_units_names)

    # --------------------------------------------------------------------------
    # is X in Y
    # --------------------------------------------------------------------------
    root_id = org_struct.root_id
    root_node = org_struct.get_node_by_id(root_id)
    org = root_node.obj

    for y in [root_id, root_node, org]:
        for x_node in [
            org_struct.get_node_by_name("infra"),
            org_struct.get_node_by_name("awshsh-infra"),
        ]:
            assert org_struct.is_x_in_y(x_node, y) is True
            assert org_struct.is_x_in_y(x_node.id, y) is True
            assert org_struct.is_x_in_y(x_node.obj, y) is True

    assert (
        org_struct.is_x_in_y(
            org_struct.get_node_by_name("awshsh-app-dev"),
            org_struct.get_node_by_name("ml"),
        )
        is False
    )


def _run_visualize(org_struct: OrgStructure):
    org_struct.visualize()
    org_struct.to_csv()
    # print(org_struct.visualize())
    # print(org_struct.to_csv())


def test():
    print("")
    bsm = BotoSesManager(profile_name="awshsh_infra_us_east_1")

    org_struct = OrgStructure.get_org_structure(bsm=bsm)
    _run_test_case(org_struct)
    _run_visualize(org_struct)

    org_struct_data = org_struct.serialize()
    org_struct_parsed = OrgStructure.deserialize(org_struct_data)
    _run_test_case(org_struct_parsed)


if __name__ == "__main__":
    from aws_organizations.tests import run_cov_test

    run_cov_test(__file__, "aws_organizations.org_struct", preview=False)
