# -*- coding: utf-8 -*-

if __name__ == "__main__":
    from aws_organizations.tests import run_cov_test

    run_cov_test(__file__, "aws_organizations", is_folder=True, preview=False)
