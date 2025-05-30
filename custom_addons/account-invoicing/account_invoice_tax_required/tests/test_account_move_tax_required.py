# Copyright 2016 - Tecnativa - Angel Moya <odoo@tecnativa.com>
# Copyright 2024 - Tecnativa - Pedro M. Baeza
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import exceptions
from odoo.fields import Command
from odoo.tests import tagged

from odoo.addons.account.tests.common import AccountTestInvoicingCommon


@tagged("post_install", "-at_install")
class TestAccountInvoiceTaxRequired(AccountTestInvoicingCommon):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.account_invoice = cls.env["account.move"]
        cls.account_journal = cls.env["account.journal"]
        cls.journal = cls.account_journal.create(
            {"code": "test", "name": "test", "type": "sale"}
        )
        cls.partner = cls.env.ref("base.res_partner_3")

        cls.account_account = cls.env["account.account"]
        cls.account_rec1_id = cls.account_account.create(
            dict(
                code="20000",
                name="customer account",
                account_type="asset_receivable",
                reconcile=True,
            )
        )
        cls.product_product = cls.env["product.product"]
        cls.product = cls.product_product.create(
            {
                "name": "Test",
                "categ_id": cls.env.ref("product.product_category_all").id,
                "standard_price": 50,
                "list_price": 100,
                "type": "service",
                "uom_id": cls.env.ref("uom.product_uom_unit").id,
                "uom_po_id": cls.env.ref("uom.product_uom_unit").id,
                "description": "Test",
            }
        )

        invoice_line_data = [
            Command.create(
                {
                    "product_id": cls.product.id,
                    "quantity": 10.0,
                    "account_id": cls.account_account.search(
                        [
                            (
                                "account_type",
                                "=",
                                "income",
                            )
                        ],
                        limit=1,
                    ).id,
                    "name": "product test 5",
                    "price_unit": 100.00,
                    "tax_ids": False,
                },
            )
        ]

        cls.invoice = cls.account_invoice.create(
            dict(
                name="Test Customer Invoice",
                journal_id=cls.journal.id,
                partner_id=cls.partner.id,
                invoice_line_ids=invoice_line_data,
                move_type="out_invoice",
            )
        )

        cls.tax_waiting_account = cls.env["account.account"].create(
            {
                "name": "TAX_WAIT",
                "code": "TWAIT",
                "account_type": "liability_current",
                "reconcile": True,
            }
        )

        cls.tax_cash_basis = cls.env["account.tax"].create(
            {
                "name": "cash basis 20%",
                "type_tax_use": "purchase",
                "amount": 20,
                "tax_exigibility": "on_payment",
                "cash_basis_transition_account_id": cls.tax_waiting_account.id,
            }
        )

    def test_exception(self):
        """Validate invoice without tax must raise exception"""
        with self.assertRaises(exceptions.RedirectWarning):
            self.invoice.with_context(test_tax_required=True).action_post()

    def test_mass_validation(self):
        wizard = (
            self.env["validate.account.move"]
            .with_context(
                test_tax_required=True,
                active_model="account.move",
                active_ids=self.invoice.ids,
            )
            .create({})
        )
        with self.assertRaises(exceptions.RedirectWarning):
            wizard.validate_move()

    def test_without_exception(self):
        """Validate invoice without tax must raise exception"""
        self.invoice.invoice_line_ids[0].tax_ids = [(4, self.tax_cash_basis.id)]
        self.invoice.with_context(test_tax_required=True).action_post()
