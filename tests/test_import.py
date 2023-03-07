# -*- coding: utf-8 -*-

import pytest
from pytest import raises, approx


def test():
    import aws_organizations

    # low level
    _ = aws_organizations.better_boto.ParentTypeEnum
    _ = aws_organizations.better_boto.Parent
    _ = aws_organizations.better_boto.ChildTypeEnum
    _ = aws_organizations.better_boto.Child
    _ = aws_organizations.better_boto.AccountStatusEnum
    _ = aws_organizations.better_boto.AccountJoinedMethodEnum
    _ = aws_organizations.better_boto.Account
    _ = aws_organizations.better_boto.OrganizationUnit
    _ = aws_organizations.better_boto.Organization

    _ = aws_organizations.better_boto.list_parents
    _ = aws_organizations.better_boto.list_children
    _ = aws_organizations.better_boto.get_root_id
    _ = aws_organizations.better_boto.list_organizational_units_for_parent
    _ = aws_organizations.better_boto.list_accounts_for_parent

    _ = aws_organizations.better_boto.describe_organization

    # high level
    _ = aws_organizations.get_org_structure


if __name__ == "__main__":
    import os

    basename = os.path.basename(__file__)
    pytest.main([basename, "-s", "--tb=native"])
