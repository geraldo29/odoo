=================
Sales product set
=================

.. 
   !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
   !! This file is generated by oca-gen-addon-readme !!
   !! changes will be overwritten.                   !!
   !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
   !! source digest: sha256:2f7beee55c7bf24a53bdf20c9eaa6dec4098d084c0bdb197a8b3702fae33e2a1
   !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

.. |badge1| image:: https://img.shields.io/badge/maturity-Beta-yellow.png
    :target: https://odoo-community.org/page/development-status
    :alt: Beta
.. |badge2| image:: https://img.shields.io/badge/licence-AGPL--3-blue.png
    :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
    :alt: License: AGPL-3
.. |badge3| image:: https://img.shields.io/badge/github-OCA%2Fsale--workflow-lightgray.png?logo=github
    :target: https://github.com/OCA/sale-workflow/tree/18.0/sale_product_set
    :alt: OCA/sale-workflow
.. |badge4| image:: https://img.shields.io/badge/weblate-Translate%20me-F47D42.png
    :target: https://translation.odoo-community.org/projects/sale-workflow-18-0/sale-workflow-18-0-sale_product_set
    :alt: Translate me on Weblate
.. |badge5| image:: https://img.shields.io/badge/runboat-Try%20me-875A7B.png
    :target: https://runboat.odoo-community.org/builds?repo=OCA/sale-workflow&target_branch=18.0
    :alt: Try me on Runboat

|badge1| |badge2| |badge3| |badge4| |badge5|

A **product set** is a list of products which end customers aren't
aware, this list is defined by sales manager.

This module aims to load a product set in a sales order though a wizard.
The product set is a list of products and quantities that gets inserted
as separate sales order lines.

After a *product set* is added to the sales order, each line can be
updated or removed as any other sales order lines.

**Table of contents**

.. contents::
   :local:

Usage
=====

- Define a *product set* as sales manager:

  - choose products
  - for each product, define a quantity.
  - for each product (if Discounts setting is active), define a discount
    or leave default value
  - Sort *set* lines, this order will be the default when added into the
    quotation

- Then you can remove or update added lines as any other sales order
  lines.

|Sale order|

.. |Sale order| image:: https://raw.githubusercontent.com/sale_product_set/static/description/sale_order.png

Bug Tracker
===========

Bugs are tracked on `GitHub Issues <https://github.com/OCA/sale-workflow/issues>`_.
In case of trouble, please check there if your issue has already been reported.
If you spotted it first, help us to smash it by providing a detailed and welcomed
`feedback <https://github.com/OCA/sale-workflow/issues/new?body=module:%20sale_product_set%0Aversion:%2018.0%0A%0A**Steps%20to%20reproduce**%0A-%20...%0A%0A**Current%20behavior**%0A%0A**Expected%20behavior**>`_.

Do not contact contributors directly about support or help with technical issues.

Credits
=======

Authors
-------

* Anybox

Contributors
------------

- Clovis Nzouendjou <clovis@anybox.fr>
- Pierre Verkest <pverkest@anybox.fr>
- Denis Leemann <denis.leemann@camptocamp.com>
- Simone Orsi <simone.orsi@camptocamp.com>
- Souheil Bejaoui <souheil.bejaoui@acsone.eu>
- Adria Gil Sorribes <adria.gil@forgeflow.com>
- Phuc (Tran Thanh) <phuc@trobz.com>
- Manuel Regidor <manuel.regidor@sygel.es>
- `Tecnativa <https://www.tecnativa.com>`__:

  - Pilar Vargas
  - Juan Carlos Oñate

- Nils Coenen <nils.coenen@nico-solutions.de>

Other credits
-------------

The development of this module has been financially supported by:

- Camptocamp

Maintainers
-----------

This module is maintained by the OCA.

.. image:: https://odoo-community.org/logo.png
   :alt: Odoo Community Association
   :target: https://odoo-community.org

OCA, or the Odoo Community Association, is a nonprofit organization whose
mission is to support the collaborative development of Odoo features and
promote its widespread use.

This module is part of the `OCA/sale-workflow <https://github.com/OCA/sale-workflow/tree/18.0/sale_product_set>`_ project on GitHub.

You are welcome to contribute. To learn how please visit https://odoo-community.org/page/Contribute.
