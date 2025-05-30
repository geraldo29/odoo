============================================
Account Invoice Report Payment Extended Info
============================================

.. 
   !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
   !! This file is generated by oca-gen-addon-readme !!
   !! changes will be overwritten.                   !!
   !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
   !! source digest: sha256:c01b8475f4e323e6823c9d4dea6349b71ca527589b762171d21b9c887346e232
   !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

.. |badge1| image:: https://img.shields.io/badge/maturity-Beta-yellow.png
    :target: https://odoo-community.org/page/development-status
    :alt: Beta
.. |badge2| image:: https://img.shields.io/badge/licence-AGPL--3-blue.png
    :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
    :alt: License: AGPL-3
.. |badge3| image:: https://img.shields.io/badge/github-OCA%2Faccount--invoice--reporting-lightgray.png?logo=github
    :target: https://github.com/OCA/account-invoice-reporting/tree/18.0/account_invoice_report_payment_info
    :alt: OCA/account-invoice-reporting
.. |badge4| image:: https://img.shields.io/badge/weblate-Translate%20me-F47D42.png
    :target: https://translation.odoo-community.org/projects/account-invoice-reporting-18-0/account-invoice-reporting-18-0-account_invoice_report_payment_info
    :alt: Translate me on Weblate
.. |badge5| image:: https://img.shields.io/badge/runboat-Try%20me-875A7B.png
    :target: https://runboat.odoo-community.org/builds?repo=OCA/account-invoice-reporting&target_branch=18.0
    :alt: Try me on Runboat

|badge1| |badge2| |badge3| |badge4| |badge5|

This module extends the invoice report for adding information about the
payments.

**Table of contents**

.. contents::
   :local:

Configuration
=============

- Activate developer mode.
- Go to *Settings > Technical > Parameters > System Parameters*.
- Locate the setting with key
  "account_invoice_report_payment_info.info_pattern" or create a new one
  if not exists.
- Set a format pattern using the key available in
  \_compute_payments_widget_reconciled_info method. This module adds
  move_ref key to all those odoo core keys:

  - 'name'
  - 'journal_name'
  - 'company_name'
  - 'amount'
  - 'currency_id'
  - 'date'
  - 'partial_id'
  - 'account_payment_id'
  - 'payment_method_name'
  - 'move_id'
  - 'ref'
  - 'is_exchange'
  - 'amount_company_currency'
  - 'amount_foreign_currency'

https://github.com/odoo/odoo/blob/536df945a53edd390e8382a6e179a36668553e63/addons/account/models/account_move.py#L1371

Usage
=====

To use this module, you need to:

1. Go to **Invoicing > Customer Invoices**.
2. Select or create an validated invoice.
3. Click on button "Add credit note".
4. Select Cancel or Modify option and click on button "Add credit note".
5. Print invoice.
6. Look payment info referenced to credit note.

Bug Tracker
===========

Bugs are tracked on `GitHub Issues <https://github.com/OCA/account-invoice-reporting/issues>`_.
In case of trouble, please check there if your issue has already been reported.
If you spotted it first, help us to smash it by providing a detailed and welcomed
`feedback <https://github.com/OCA/account-invoice-reporting/issues/new?body=module:%20account_invoice_report_payment_info%0Aversion:%2018.0%0A%0A**Steps%20to%20reproduce**%0A-%20...%0A%0A**Current%20behavior**%0A%0A**Expected%20behavior**>`_.

Do not contact contributors directly about support or help with technical issues.

Credits
=======

Authors
-------

* Tecnativa

Contributors
------------

- `Tecnativa <https://www.tecnativa.com>`__:

  - Carlos Dauden
  - Carlos Roca
  - Juan Carlos Oñate

Maintainers
-----------

This module is maintained by the OCA.

.. image:: https://odoo-community.org/logo.png
   :alt: Odoo Community Association
   :target: https://odoo-community.org

OCA, or the Odoo Community Association, is a nonprofit organization whose
mission is to support the collaborative development of Odoo features and
promote its widespread use.

This module is part of the `OCA/account-invoice-reporting <https://github.com/OCA/account-invoice-reporting/tree/18.0/account_invoice_report_payment_info>`_ project on GitHub.

You are welcome to contribute. To learn how please visit https://odoo-community.org/page/Contribute.
