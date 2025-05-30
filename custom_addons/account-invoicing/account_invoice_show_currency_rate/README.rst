==================================
Account Invoice Show Currency Rate
==================================

.. 
   !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
   !! This file is generated by oca-gen-addon-readme !!
   !! changes will be overwritten.                   !!
   !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
   !! source digest: sha256:d7f1cb233310876e1c3d7aedd0128a89137a0c8d1162c1d3393e8e64ffc0f8f0
   !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

.. |badge1| image:: https://img.shields.io/badge/maturity-Beta-yellow.png
    :target: https://odoo-community.org/page/development-status
    :alt: Beta
.. |badge2| image:: https://img.shields.io/badge/licence-AGPL--3-blue.png
    :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
    :alt: License: AGPL-3
.. |badge3| image:: https://img.shields.io/badge/github-OCA%2Faccount--invoicing-lightgray.png?logo=github
    :target: https://github.com/OCA/account-invoicing/tree/18.0/account_invoice_show_currency_rate
    :alt: OCA/account-invoicing
.. |badge4| image:: https://img.shields.io/badge/weblate-Translate%20me-F47D42.png
    :target: https://translation.odoo-community.org/projects/account-invoicing-18-0/account-invoicing-18-0-account_invoice_show_currency_rate
    :alt: Translate me on Weblate
.. |badge5| image:: https://img.shields.io/badge/runboat-Try%20me-875A7B.png
    :target: https://runboat.odoo-community.org/builds?repo=OCA/account-invoicing&target_branch=18.0
    :alt: Try me on Runboat

|badge1| |badge2| |badge3| |badge4| |badge5|

Odoo computes the currency rate applied on invoices, as well as for
journal items. However, these rates are simply computed based on the
currency rates that are configured in the system.

This module ensures that for posted entries the currency rates are
computed taking into account the actual amounts in the specific
currency. This ensures that the correct rates are displayed when an
invoice was posted with a different rate configuration, or if the user
manually changed the amount in currency.

**Table of contents**

.. contents::
   :local:

Configuration
=============

Enable the option for multiple currencies in your instance:

1. Go to Invoicing > Configuration > Settings > Currencies >
   Multi-Currencies
2. Go to any draft invoice
3. Change the invoice currency
4. The proper currency rate, based on the invoice date and the selected
   currency, will be shown.
5. Add any invoice line.
6. Odoo has already generated the journal item lines with the rate
   applied, so the currency rate shown is get from the division between
   the amount in currency by the amount in company currency.

Some rates must be defined (and be distinct to 1.0) for currencies
different from the company default.

1. Go to Invoicing > Configuration > Currencies and go to EUR
2. Go to Rates smart-button
3. Update 01/01/2010 record and change rate to 1.5

Usage
=====

To use this module, you need to:

1. Go to Invoicing > Customer > Invoice
2. Create Invoice and set Currency distinct to company currency (EUR for
   example)
3. Rate account show according to currency defined.

Bug Tracker
===========

Bugs are tracked on `GitHub Issues <https://github.com/OCA/account-invoicing/issues>`_.
In case of trouble, please check there if your issue has already been reported.
If you spotted it first, help us to smash it by providing a detailed and welcomed
`feedback <https://github.com/OCA/account-invoicing/issues/new?body=module:%20account_invoice_show_currency_rate%0Aversion:%2018.0%0A%0A**Steps%20to%20reproduce**%0A-%20...%0A%0A**Current%20behavior**%0A%0A**Expected%20behavior**>`_.

Do not contact contributors directly about support or help with technical issues.

Credits
=======

Authors
-------

* Tecnativa

Contributors
------------

- `Tecnativa <https://www.tecnativa.com>`__:

  - Pedro M. Baeza
  - Víctor Martínez

- `ForgeFlow <https://www.forgeflow.com>`__:

  - Jordi Masvidal

Maintainers
-----------

This module is maintained by the OCA.

.. image:: https://odoo-community.org/logo.png
   :alt: Odoo Community Association
   :target: https://odoo-community.org

OCA, or the Odoo Community Association, is a nonprofit organization whose
mission is to support the collaborative development of Odoo features and
promote its widespread use.

.. |maintainer-victoralmau| image:: https://github.com/victoralmau.png?size=40px
    :target: https://github.com/victoralmau
    :alt: victoralmau

Current `maintainer <https://odoo-community.org/page/maintainer-role>`__:

|maintainer-victoralmau| 

This module is part of the `OCA/account-invoicing <https://github.com/OCA/account-invoicing/tree/18.0/account_invoice_show_currency_rate>`_ project on GitHub.

You are welcome to contribute. To learn how please visit https://odoo-community.org/page/Contribute.
