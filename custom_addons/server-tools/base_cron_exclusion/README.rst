===================
Base Cron Exclusion
===================

.. 
   !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
   !! This file is generated by oca-gen-addon-readme !!
   !! changes will be overwritten.                   !!
   !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
   !! source digest: sha256:e2cf1e9e142b4df25319ffe32517d93d3df441b7a8564b97d3c17784bab99f6c
   !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

.. |badge1| image:: https://img.shields.io/badge/maturity-Production%2FStable-green.png
    :target: https://odoo-community.org/page/development-status
    :alt: Production/Stable
.. |badge2| image:: https://img.shields.io/badge/licence-LGPL--3-blue.png
    :target: http://www.gnu.org/licenses/lgpl-3.0-standalone.html
    :alt: License: LGPL-3
.. |badge3| image:: https://img.shields.io/badge/github-OCA%2Fserver--tools-lightgray.png?logo=github
    :target: https://github.com/OCA/server-tools/tree/18.0/base_cron_exclusion
    :alt: OCA/server-tools
.. |badge4| image:: https://img.shields.io/badge/weblate-Translate%20me-F47D42.png
    :target: https://translation.odoo-community.org/projects/server-tools-18-0/server-tools-18-0-base_cron_exclusion
    :alt: Translate me on Weblate
.. |badge5| image:: https://img.shields.io/badge/runboat-Try%20me-875A7B.png
    :target: https://runboat.odoo-community.org/builds?repo=OCA/server-tools&target_branch=18.0
    :alt: Try me on Runboat

|badge1| |badge2| |badge3| |badge4| |badge5|

This module extends the functionality of scheduled actions to allow you
to select the ones that should not run simultaneously.

**Table of contents**

.. contents::
   :local:

Usage
=====

To use this module, you need to:

1. Go to *Settings > Technical > Automation > Scheduled Actions*.
2. In the form view go to the tab *Mutually Exclusive Scheduled
   Actions*.
3. Fill it with the actions that should be blocked while running the
   action you are editing. Note that this is mutual and the selected
   actions will block the initial action when running.

Bug Tracker
===========

Bugs are tracked on `GitHub Issues <https://github.com/OCA/server-tools/issues>`_.
In case of trouble, please check there if your issue has already been reported.
If you spotted it first, help us to smash it by providing a detailed and welcomed
`feedback <https://github.com/OCA/server-tools/issues/new?body=module:%20base_cron_exclusion%0Aversion:%2018.0%0A%0A**Steps%20to%20reproduce**%0A-%20...%0A%0A**Current%20behavior**%0A%0A**Expected%20behavior**>`_.

Do not contact contributors directly about support or help with technical issues.

Credits
=======

Authors
-------

* ForgeFlow

Contributors
------------

- Christopher Ormaza <chris.ormaza@forgeflow.com>
- Lois Rilo <lois.rilo@forgeflow.com>
- Jordi Ballester <jordi.ballester@forgeflow.com>
- Bhavesh Odedra <bodedra@opensourceintegrators.com>
- `Trobz <https://trobz.com>`__:

  - Do Anh Duy <duyda@trobz.com>

Other credits
-------------

The migration of this module from 17.0 to 18.0 was financially supported
by Camptocamp

Maintainers
-----------

This module is maintained by the OCA.

.. image:: https://odoo-community.org/logo.png
   :alt: Odoo Community Association
   :target: https://odoo-community.org

OCA, or the Odoo Community Association, is a nonprofit organization whose
mission is to support the collaborative development of Odoo features and
promote its widespread use.

.. |maintainer-LoisRForgeFlow| image:: https://github.com/LoisRForgeFlow.png?size=40px
    :target: https://github.com/LoisRForgeFlow
    :alt: LoisRForgeFlow
.. |maintainer-ChrisOForgeFlow| image:: https://github.com/ChrisOForgeFlow.png?size=40px
    :target: https://github.com/ChrisOForgeFlow
    :alt: ChrisOForgeFlow

Current `maintainers <https://odoo-community.org/page/maintainer-role>`__:

|maintainer-LoisRForgeFlow| |maintainer-ChrisOForgeFlow| 

This module is part of the `OCA/server-tools <https://github.com/OCA/server-tools/tree/18.0/base_cron_exclusion>`_ project on GitHub.

You are welcome to contribute. To learn how please visit https://odoo-community.org/page/Contribute.
