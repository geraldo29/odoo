=============
Filter Button
=============

.. 
   !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
   !! This file is generated by oca-gen-addon-readme !!
   !! changes will be overwritten.                   !!
   !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
   !! source digest: sha256:ca8b5898e3d8f183bcf7575688c5858938135a593f03f422767e69367be33984
   !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

.. |badge1| image:: https://img.shields.io/badge/maturity-Beta-yellow.png
    :target: https://odoo-community.org/page/development-status
    :alt: Beta
.. |badge2| image:: https://img.shields.io/badge/licence-AGPL--3-blue.png
    :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
    :alt: License: AGPL-3
.. |badge3| image:: https://img.shields.io/badge/github-OCA%2Fweb-lightgray.png?logo=github
    :target: https://github.com/OCA/web/tree/18.0/web_filter_header_button
    :alt: OCA/web
.. |badge4| image:: https://img.shields.io/badge/weblate-Translate%20me-F47D42.png
    :target: https://translation.odoo-community.org/projects/web-18-0/web-18-0-web_filter_header_button
    :alt: Translate me on Weblate
.. |badge5| image:: https://img.shields.io/badge/runboat-Try%20me-875A7B.png
    :target: https://runboat.odoo-community.org/builds?repo=OCA/web&target_branch=18.0
    :alt: Try me on Runboat

|badge1| |badge2| |badge3| |badge4| |badge5|

This module allows to add some selected filters as buttons in the header
control panel.

**Table of contents**

.. contents::
   :local:

Use Cases / Context
===================

This developement is aimed to ease the filter access for touch screens
users.

Configuration
=============

To show a filter in the header of the views, it should have the a
``context`` attribute with the key ``shown_in_panel``.

.. code:: xml

   <filter
       string="My filter"
       name="my_filter"
       domain="[('active', '!=', False)]"
       context="{'shown_in_panel': True}"
   >

This will show the filter in the header with its name. You can customize
the button adding an icon or with a custom name passing an object to
that key:

.. code:: python

   {'shown_in_panel': {'icon': 'fa-thumbs-up', 'name': 'Ok'}}

You might be interested in leaving just the icon. In that case, set an
empty string on the ``name`` property:

.. code:: python

   {'shown_in_panel': {'icon': 'fa-thumbs-up', 'name': ''}}

You could also want to add a hotkey. In such case add the ``hotkey``
property:

.. code:: python

   {'shown_in_panel': {'icon': 'fa-thumbs-up', 'hotkey': 'F'}}

You can show filter, groups or even favorites.

Usage
=====

In a search view with header filter buttons, you'll see a filter icon
(funnel). Use it to unfold the filters.

There's a demo implementation in ``Apps`` and you can play around
following the *Configure* section.

Known issues / Roadmap
======================

- Group filters by kind
- As we use the ``context`` attribute, the inheritance could be limiting
  in some cases. Keep it in mind or use
  ``base_view_inheritance_extension`` if you want to use proper context
  inheritance.
- Another nice to have would be to be able to hide the filters in the
  filter list to be able to show them just in the header, although
  there's not a straigh forward way to do it and it could lead to side
  effects.

Bug Tracker
===========

Bugs are tracked on `GitHub Issues <https://github.com/OCA/web/issues>`_.
In case of trouble, please check there if your issue has already been reported.
If you spotted it first, help us to smash it by providing a detailed and welcomed
`feedback <https://github.com/OCA/web/issues/new?body=module:%20web_filter_header_button%0Aversion:%2018.0%0A%0A**Steps%20to%20reproduce**%0A-%20...%0A%0A**Current%20behavior**%0A%0A**Expected%20behavior**>`_.

Do not contact contributors directly about support or help with technical issues.

Credits
=======

Authors
-------

* Tecnativa

Contributors
------------

- `Tecnativa <https://tecnativa.com>`__

  - David Vidal

Maintainers
-----------

This module is maintained by the OCA.

.. image:: https://odoo-community.org/logo.png
   :alt: Odoo Community Association
   :target: https://odoo-community.org

OCA, or the Odoo Community Association, is a nonprofit organization whose
mission is to support the collaborative development of Odoo features and
promote its widespread use.

This module is part of the `OCA/web <https://github.com/OCA/web/tree/18.0/web_filter_header_button>`_ project on GitHub.

You are welcome to contribute. To learn how please visit https://odoo-community.org/page/Contribute.
