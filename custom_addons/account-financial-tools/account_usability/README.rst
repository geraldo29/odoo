==========================================
Account - Missing Menus & Saxon Accounting
==========================================

.. 
   !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
   !! This file is generated by oca-gen-addon-readme !!
   !! changes will be overwritten.                   !!
   !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
   !! source digest: sha256:ec2f84093090a05babdbbe997869edd9fff239c374e7ad107aae618b4d2dcad2
   !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

.. |badge1| image:: https://img.shields.io/badge/maturity-Beta-yellow.png
    :target: https://odoo-community.org/page/development-status
    :alt: Beta
.. |badge2| image:: https://img.shields.io/badge/licence-AGPL--3-blue.png
    :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
    :alt: License: AGPL-3
.. |badge3| image:: https://img.shields.io/badge/github-OCA%2Faccount--financial--tools-lightgray.png?logo=github
    :target: https://github.com/OCA/account-financial-tools/tree/18.0/account_usability
    :alt: OCA/account-financial-tools
.. |badge4| image:: https://img.shields.io/badge/weblate-Translate%20me-F47D42.png
    :target: https://translation.odoo-community.org/projects/account-financial-tools-18-0/account-financial-tools-18-0-account_usability
    :alt: Translate me on Weblate
.. |badge5| image:: https://img.shields.io/badge/runboat-Try%20me-875A7B.png
    :target: https://runboat.odoo-community.org/builds?repo=OCA/account-financial-tools&target_branch=18.0
    :alt: Try me on Runboat

|badge1| |badge2| |badge3| |badge4| |badge5|

This module extends the Odoo CE account module to add all the missing or
hidden things that are hidden and available only on EE version.

1) This module adds all missing menu entries and views for the
   **Account** module.

   - Bank Statements
   - Cash Registers
   - Account Tags
   - Account Groups
   - Chart of Account Templates
   - Account Templates
   - Tax Templates
   - Fiscal Position Templates

2) This module also enables the option to enable or disable Anglo-Saxon
   accounting in the Chart of Account Template form view and in the
   Invoicing Settings.
3) In Odoo CE, the group 'Show Full Accounting Features' is hidden. With
   that module, the group is selectable in the user form view. Also the
   group "Billing / xxx" are renamed into "Accounting / yyy" to fit with
   the EE terms.
4) Rename the main menu 'Billing' into 'Accounting' to fit with EE
   naming.

**Table of contents**

.. contents::
   :local:

Development
===========

**Detailled Module Category Changes (ir.module.category)**

- base.module_category_accounting_accounting

*CE Without that module* -> Complete Name : Invoicing

*CE With that module / EE* -> Complete Name: **Accounting**

**Detailled Groups Changes (res.groups)**

- account.group_account_invoice

*CE Without that module* -> Complete Name : Invoicing / Billing ->
Parent Category : base.module_category_accounting_accounting -> Implies
: base.group_user

*CE With that module / EE* -> Complete Name: **Accounting** / Billing

- account.group_account_readonly

*CE Without that module* -> Complete Name : Technical / Show Accounting
Features - Readonly -> Parent : base.module_category_hidden -> Implies :
base.group_user

*CE With that module / EE* -> name: **Accounting / Read-only** -> Parent
Category: **base.module_category_accounting_accounting**

- account.group_account_user

*CE Without that module* -> Complete Name : Technical / Show Full
Accounting Features -> Parent : base.module_category_hidden -> Implies :
account.group_account_invoice, account.group_account_readonly

*CE With that module / EE* -> name: **Accounting / Bookkeeper** ->
Parent Category: **base.module_category_accounting_accounting**

- account.group_account_manager

*CE Without that module* -> Complete Name : Invoicing / Billing
Administrator -> Parent : base.module_category_accounting_accounting ->
Implies : account.group_account_invoice

*CE With that module / EE* -> name: **Accounting / Accountant** ->
Implies : **account.group_account_user**

Known issues / Roadmap
======================

- Add a form view for the model ``account.bank.statement`` as Odoo SA
  privatized in EE the form view in V16.0.

Bug Tracker
===========

Bugs are tracked on `GitHub Issues <https://github.com/OCA/account-financial-tools/issues>`_.
In case of trouble, please check there if your issue has already been reported.
If you spotted it first, help us to smash it by providing a detailed and welcomed
`feedback <https://github.com/OCA/account-financial-tools/issues/new?body=module:%20account_usability%0Aversion:%2018.0%0A%0A**Steps%20to%20reproduce**%0A-%20...%0A%0A**Current%20behavior**%0A%0A**Expected%20behavior**>`_.

Do not contact contributors directly about support or help with technical issues.

Credits
=======

Authors
-------

* GRAP
* Akretion

Contributors
------------

- Sylvain LE GAL <https://twitter.com/legalsylvain>
- Raf Ven <raf.ven@dynapps.be>
- Alexis de Lattre <alexis.delattre@akretion.com>
- Álvaro Trius <alvaro.trius@forgeflow.com>
- [APSL-Nagarro](https://apsl.tech):

  - Antoni Marroig <amarroig@apsl.net>

Maintainers
-----------

This module is maintained by the OCA.

.. image:: https://odoo-community.org/logo.png
   :alt: Odoo Community Association
   :target: https://odoo-community.org

OCA, or the Odoo Community Association, is a nonprofit organization whose
mission is to support the collaborative development of Odoo features and
promote its widespread use.

.. |maintainer-legalsylvain| image:: https://github.com/legalsylvain.png?size=40px
    :target: https://github.com/legalsylvain
    :alt: legalsylvain

Current `maintainer <https://odoo-community.org/page/maintainer-role>`__:

|maintainer-legalsylvain| 

This module is part of the `OCA/account-financial-tools <https://github.com/OCA/account-financial-tools/tree/18.0/account_usability>`_ project on GitHub.

You are welcome to contribute. To learn how please visit https://odoo-community.org/page/Contribute.
