.. _release_history:

Release and Version History
==============================================================================


Backlog (TODO)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
**Features and Improvements**

**Minor Improvements**

**Bugfixes**

**Miscellaneous**


0.3.1 (2023-03-10)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
**Features and Improvements**

- add ``OrgStructure.serialize`` and ``OrgStructure.deserialize``. now you can cache the org structure data in JSON.
- add ``OrgStructure.get_node_by_id``
- add ``OrgStructure.get_node_by_name``
- add ``Node.organization_or_account_or_organizational_unit``.
- add ``Node.parent_id``.
- add ``Node.accounts``.
- add ``Node.org_units``.
- add ``Node.all_accounts``.
- add ``Node.all_org_units``.
- add ``Node.accounts_names``.
- add ``Node.org_units_names``.
- add ``Node.all_accounts_names``.
- add ``Node.all_org_units_names``.


0.2.1 (2023-03-08)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
**Features and Improvements**

- add ``Node.iter_org_units`` and ``Node_iter_accounts`` methods.
- add ``OrgStructure`` class to represent the organization structure tree.
- drop ``get_org_structure``, add ``OrgStructure.get_org_structure`` method.
- add ``OrgStructure.visualize`` method.
- add ``OrgStructure.to_csv`` method.
- add ``OrgStructure.is_x_in_y`` method.


0.1.1 (2023-03-06)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
**Features and Improvements**

- First release
- add data model for ``Organization``, ``OrganizationUnit``, ``Account``
- add ``get_org_structure`` method to get the organization structure tree.
