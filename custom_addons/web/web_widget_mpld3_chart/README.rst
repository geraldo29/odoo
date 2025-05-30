======================
Web Widget mpld3 Chart
======================

.. 
   !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
   !! This file is generated by oca-gen-addon-readme !!
   !! changes will be overwritten.                   !!
   !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
   !! source digest: sha256:0eb1a67d1e1a31cce1fa49b4f4d8224def69ef757defdb96dba62154c4a6a0d4
   !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

.. |badge1| image:: https://img.shields.io/badge/maturity-Beta-yellow.png
    :target: https://odoo-community.org/page/development-status
    :alt: Beta
.. |badge2| image:: https://img.shields.io/badge/licence-LGPL--3-blue.png
    :target: http://www.gnu.org/licenses/lgpl-3.0-standalone.html
    :alt: License: LGPL-3
.. |badge3| image:: https://img.shields.io/badge/github-OCA%2Fweb-lightgray.png?logo=github
    :target: https://github.com/OCA/web/tree/18.0/web_widget_mpld3_chart
    :alt: OCA/web
.. |badge4| image:: https://img.shields.io/badge/weblate-Translate%20me-F47D42.png
    :target: https://translation.odoo-community.org/projects/web-18-0/web-18-0-web_widget_mpld3_chart
    :alt: Translate me on Weblate
.. |badge5| image:: https://img.shields.io/badge/runboat-Try%20me-875A7B.png
    :target: https://runboat.odoo-community.org/builds?repo=OCA/web&target_branch=18.0
    :alt: Try me on Runboat

|badge1| |badge2| |badge3| |badge4| |badge5|

This module adds the possibility to insert mpld3 charts into Odoo
standard views. This is an interactive D3js-based viewer which brings
matplotlib graphics to the browser.

If you want to see some samples of mpld3's capabilities follow this
`link <http://mpld3.github.io/>`__.

**Table of contents**

.. contents::
   :local:

Installation
============

You need to install the python mpld3 library:

::

   pip install mpld3

Usage
=====

To insert a mpld3 chart in a view proceed as follows:

1. You should inherit from abstract class abstract.mpld3.parser:

   ::

      _name = 'res.partner'
      _inherit = ['res.partner', 'abstract.mpld3.parser']

2. Import the required libraries:

   ::

      import matplotlib.pyplot as plt

3. Declare a json computed field like this:

   ::

      mpld3_chart = fields.Json(
          string='Mpld3 Chart',
          compute='_compute_mpld3_chart',
      )

4. In its computed method do:

   ::

      def _compute_mpld3_chart(self):
          for rec in self:
              # Design your mpld3 figure:
              plt.scatter([1, 10], [5, 9])
              figure = plt.figure()
              rec.mpld3_chart = self.convert_figure_to_json(figure)

5. In the view, add something like this wherever you want to display
   your mpld3 chart:

   ::

      <div>
          <field name="mpld3_chart" widget="mpld3_chart" nolabel="1"/>
      </div>

Bug Tracker
===========

Bugs are tracked on `GitHub Issues <https://github.com/OCA/web/issues>`_.
In case of trouble, please check there if your issue has already been reported.
If you spotted it first, help us to smash it by providing a detailed and welcomed
`feedback <https://github.com/OCA/web/issues/new?body=module:%20web_widget_mpld3_chart%0Aversion:%2018.0%0A%0A**Steps%20to%20reproduce**%0A-%20...%0A%0A**Current%20behavior**%0A%0A**Expected%20behavior**>`_.

Do not contact contributors directly about support or help with technical issues.

Credits
=======

Authors
-------

* ForgeFlow

Contributors
------------

- Jordi Ballester Alomar <jordi.ballester@forgeflow.com>
- Christopher Ormaza <chris.ormaza@forgeflow.com>

Other credits
-------------

- This module uses the library
  `mpld3 <https://github.com/mpld3/mpld3>`__ which is under the
  open-source BSD 3-clause "New" or "Revised" License. Copyright (c)
  2013, Jake Vanderplas
- This module uses the library `BeautifulSoup
  4 <https://pypi.org/project/beautifulsoup4/>`__ which is under the
  open-source MIT License. Copyright (c) 2014, Leonard Richardson
- Odoo Community Association (OCA)

Maintainers
-----------

This module is maintained by the OCA.

.. image:: https://odoo-community.org/logo.png
   :alt: Odoo Community Association
   :target: https://odoo-community.org

OCA, or the Odoo Community Association, is a nonprofit organization whose
mission is to support the collaborative development of Odoo features and
promote its widespread use.

.. |maintainer-JordiBForgeFlow| image:: https://github.com/JordiBForgeFlow.png?size=40px
    :target: https://github.com/JordiBForgeFlow
    :alt: JordiBForgeFlow
.. |maintainer-ThiagoMForgeFlow| image:: https://github.com/ThiagoMForgeFlow.png?size=40px
    :target: https://github.com/ThiagoMForgeFlow
    :alt: ThiagoMForgeFlow

Current `maintainers <https://odoo-community.org/page/maintainer-role>`__:

|maintainer-JordiBForgeFlow| |maintainer-ThiagoMForgeFlow| 

This module is part of the `OCA/web <https://github.com/OCA/web/tree/18.0/web_widget_mpld3_chart>`_ project on GitHub.

You are welcome to contribute. To learn how please visit https://odoo-community.org/page/Contribute.
