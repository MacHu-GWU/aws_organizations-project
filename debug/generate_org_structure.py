# -*- coding: utf-8 -*-

import jsonpickle as json
from pathlib import Path

from boto_session_manager import BotoSesManager
from anytree import RenderTree
from rich import print as rprint

import aws_organizations
from aws_organizations.org_struct import OrgStructure
from aws_organizations.better_boto.org_unit import list_parents, list_children

bsm = BotoSesManager(profile_name="awshsh_infra_us_east_1")

dir_here = Path(__file__).absolute().parent
path_org_struct_tree = dir_here / "org_struct.txt"
path_org_struct_csv = dir_here / "org_struct.csv"
path_org_struct_json = dir_here / "org_struct.json"

# ------------------------------------------------------------------------------
# get_org_structure
# ------------------------------------------------------------------------------
org_struct = OrgStructure.get_org_structure(bsm=bsm)

path_org_struct_tree.write_text(org_struct.visualize())
path_org_struct_csv.write_text(org_struct.to_csv())
path_org_struct_json.write_text(json.dumps(org_struct.serialize(), indent=4))

org_struct = OrgStructure.deserialize(json.loads(path_org_struct_json.read_text()))
