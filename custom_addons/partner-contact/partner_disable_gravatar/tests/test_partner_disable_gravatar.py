# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo.tests import Form, common


class TestPartnerDisableGravatar(common.TransactionCase):
    def test_disable_gravatar(self):
        with Form(self.env["res.partner"]) as f1:
            f1.name = "Support Gravatar"
            f1.email = "support@gravatar.com"
        self.assertFalse(f1.image_1920)
