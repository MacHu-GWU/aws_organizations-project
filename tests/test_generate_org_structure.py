# -*- coding: utf-8 -*-

import os
import pytest

from boto_session_manager import BotoSesManager
from aws_organizations.org_struct import OrgStructure


IS_CI = "CI" in os.environ


@pytest.mark.skipif(IS_CI, reason="This test is not meant to run in CI")
def test():
    bsm = BotoSesManager(profile_name="awshsh_root_us_east_1")

    org_struct = OrgStructure.get_org_structure(bsm=bsm)

    org_struct.visualize()
    org_struct.to_csv()

    assert org_struct.is_x_in_y("393783141457", "r-rkp6") is True
    assert org_struct.is_x_in_y("393783141457", org_struct.get_node("r-rkp6")) is True
    assert (
        org_struct.is_x_in_y("393783141457", org_struct.get_node("r-rkp6").obj) is True
    )
    assert org_struct.is_x_in_y("393783141457", "r-rkp6") is True
    assert (
        org_struct.is_x_in_y(
            org_struct.get_node("393783141457"), org_struct.get_node("r-rkp6")
        )
        is True
    )
    assert (
        org_struct.is_x_in_y(
            org_struct.get_node("393783141457").obj, org_struct.get_node("r-rkp6").obj
        )
        is True
    )

    assert org_struct.is_x_in_y("393783141457", "ou-rkp6-cxgi4leg") is True
    assert org_struct.is_x_in_y("393783141457", "ou-rkp6-vq6m3h5y") is False

    for ou in org_struct.root.iter_org_units():
        print(org_struct.get_node(ou.id))

    for acc in org_struct.root.iter_accounts():
        print(org_struct.get_node(acc.id))


if __name__ == "__main__":
    import os

    basename = os.path.basename(__file__)
    pytest.main([basename, "-s", "--tb=native"])
