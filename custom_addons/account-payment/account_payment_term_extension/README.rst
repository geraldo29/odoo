======================
Payment Term Extension
======================

.. 
   !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
   !! This file is generated by oca-gen-addon-readme !!
   !! changes will be overwritten.                   !!
   !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
   !! source digest: sha256:117c24bfceb4532d84c40254649a45acdc39bd64dd8684feadd25f86fe8d5781
   !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

.. |badge1| image:: https://img.shields.io/badge/maturity-Beta-yellow.png
    :target: https://odoo-community.org/page/development-status
    :alt: Beta
.. |badge2| image:: https://img.shields.io/badge/licence-AGPL--3-blue.png
    :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
    :alt: License: AGPL-3
.. |badge3| image:: https://img.shields.io/badge/github-OCA%2Faccount--payment-lightgray.png?logo=github
    :target: https://github.com/OCA/account-payment/tree/18.0/account_payment_term_extension
    :alt: OCA/account-payment
.. |badge4| image:: https://img.shields.io/badge/weblate-Translate%20me-F47D42.png
    :target: https://translation.odoo-community.org/projects/account-payment-18-0/account-payment-18-0-account_payment_term_extension
    :alt: Translate me on Weblate
.. |badge5| image:: https://img.shields.io/badge/runboat-Try%20me-875A7B.png
    :target: https://runboat.odoo-community.org/builds?repo=OCA/account-payment&target_branch=18.0
    :alt: Try me on Runboat

|badge1| |badge2| |badge3| |badge4| |badge5|

This module extends the functionality of payment terms to:

- select "Percent (untaxed amount)" type in lines for using the base
  amount instead of the total (with taxes) one.
- support rounding, months and weeks on payment term lines
- allow to set more than one day of payment in payment terms
- if a payment term date is a holiday, it is postponed to a selected
  date
- allow to apply a chronological order on lines

  - for example, with a payment term which contains 2 lines

    - on standard, the due date of all lines is calculated from the
      invoice date
    - with this feature, the due date of the second line is calculated
      from the due date of the first line

**Table of contents**

.. contents::
   :local:

Configuration
=============

To configure the Payment Terms and see the new options on the Payment
Term Lines, you need to:

1. Go to the menu Invoicing > Configuration > Invoicing > Payment Terms.

To use multiple payment days, define for each payment term line which
payment days apply, separated by spaces, commas or dashes. To use
holidays, insert the holiday and the date payment terms will be
postponed to.

To modify the type of delay options available in the payment terms, you
need to:

1. Go to the menu Invoicing > Configuration > Settings > Payment Terms.
2. Choose an option from:

   - Days
   - Days and Weeks
   - Days and Months
   - Days, Weeks and Months

Usage
=====

Go to **Invoicing > Customers > Invoices** and edit any invoice or
create a new one.

Select any payment term and set a date in invoice.

You must see the due date based on this payment term.

Known issues / Roadmap
======================

This module is not compatible with cash rounding

Bug Tracker
===========

Bugs are tracked on `GitHub Issues <https://github.com/OCA/account-payment/issues>`_.
In case of trouble, please check there if your issue has already been reported.
If you spotted it first, help us to smash it by providing a detailed and welcomed
`feedback <https://github.com/OCA/account-payment/issues/new?body=module:%20account_payment_term_extension%0Aversion:%2018.0%0A%0A**Steps%20to%20reproduce**%0A-%20...%0A%0A**Current%20behavior**%0A%0A**Expected%20behavior**>`_.

Do not contact contributors directly about support or help with technical issues.

Credits
=======

Authors
-------

* Camptocamp
* Tecnativa
* Agile Business Group

Contributors
------------

- Yannick Vaucher <yannick.vaucher@camptocamp.com>
- Alexis de Lattre <alexis.delattre@akretion.com>
- Julien Coux <julien.coux@camptocamp.com>
- Simone Rubino <simone.rubino@agilebg.com>
  (`www.agilebg.com <http://www.agilebg.com>`__)
- \`Tecnativa <https://www.tecnativa.com>\`:

  - Pedro M. Baeza
  - Vicent Cubells
  - Víctor Martínez

- \`Domatix <https://domatix.com>\`:

  - Carlos Martínez

- \`Sygel <https://sygel.es>\`:

  - Manuel Regidor

- \`Trobz <https://trobz.com>\`:

  - Hoang <hoang@trobz.com>

- Anaïs López <anais.lopez@forgeflow.com>
- Marco Colombo <marco.colombo@phi.technology>

Other credits
-------------

The migration of this module from 17.0 to 18.0 was financially supported
by THERA S.R.L.

Maintainers
-----------

This module is maintained by the OCA.

.. image:: https://odoo-community.org/logo.png
   :alt: Odoo Community Association
   :target: https://odoo-community.org

OCA, or the Odoo Community Association, is a nonprofit organization whose
mission is to support the collaborative development of Odoo features and
promote its widespread use.

This module is part of the `OCA/account-payment <https://github.com/OCA/account-payment/tree/18.0/account_payment_term_extension>`_ project on GitHub.

You are welcome to contribute. To learn how please visit https://odoo-community.org/page/Contribute.
