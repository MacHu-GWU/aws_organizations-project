# -*- coding: utf-8 -*-

import jsonpickle as json
from pathlib import Path

from boto_session_manager import BotoSesManager

from aws_organizations.org_struct import OrgStructure

bsm = BotoSesManager(profile_name="esc_admin_us_east_1")

dir_here = Path(__file__).absolute().parent
path_org_struct_tree = dir_here / "org_struct.txt"
path_org_struct_csv = dir_here / "org_struct.csv"
path_org_struct_json = dir_here / "org_struct.json"
path_org_struct_mermaid = dir_here / "org_struct.md"

# ------------------------------------------------------------------------------
# get_org_structure
# ------------------------------------------------------------------------------
org_struct = OrgStructure.get_org_structure(bsm=bsm)

path_org_struct_tree.write_text(org_struct.visualize())
path_org_struct_csv.write_text(org_struct.to_csv())
path_org_struct_json.write_text(json.dumps(org_struct.serialize(), indent=4))
path_org_struct_mermaid.write_text(org_struct.to_mermaid())

org_struct = OrgStructure.deserialize(json.loads(path_org_struct_json.read_text()))
