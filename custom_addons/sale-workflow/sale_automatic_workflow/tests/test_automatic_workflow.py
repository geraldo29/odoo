# Copyright 2014 Camptocamp SA (author: Guewen Baconnier)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from datetime import timedelta
from unittest import mock

from freezegun import freeze_time

from odoo import fields
from odoo.tests import tagged

from .common import TestAutomaticWorkflowMixin, TestCommon


@tagged("post_install", "-at_install")
class TestAutomaticWorkflow(TestCommon, TestAutomaticWorkflowMixin):
    def setUp(self):
        super().setUp()
        self.env = self.env(
            context=dict(
                self.env.context,
                tracking_disable=True,
                # Compatibility with sale_automatic_workflow_job: even if
                # the module is installed, ensure we don't delay a job.
                # Thus, we test the usual flow.
                queue_job__no_delay=True,
            )
        )

    def test_01_full_automatic(self):
        workflow = self.create_full_automatic()
        sale = self.create_sale_order(workflow)
        self.assertEqual(sale.state, "draft")
        self.assertEqual(sale.workflow_process_id, workflow)
        self.run_job()
        self.assertEqual(sale.state, "sale")
        self.assertTrue(sale.invoice_ids)
        invoice = sale.invoice_ids
        self.assertEqual(invoice.state, "posted")

    def test_02_onchange(self):
        team_1 = self.env.ref("sales_team.crm_team_1")
        team_2 = self.env.ref("sales_team.team_sales_department")
        workflow = self.create_full_automatic(override={"team_id": team_1.id})
        sale = self.create_sale_order(workflow)
        self.assertEqual(sale.team_id, team_1)
        workflow2 = self.create_full_automatic(override={"team_id": team_2.id})
        sale.workflow_process_id = workflow2.id
        self.assertEqual(sale.team_id, team_2)

    @freeze_time("2025-1-1")
    def test_03_date_invoice_from_sale_order(self):
        workflow = self.create_full_automatic()
        # date_order on sale.order is date + time
        # invoice_date on account.move is date only
        last_week_time = fields.Datetime.now() - timedelta(days=7)
        override = {"date_order": last_week_time}
        sale = self.create_sale_order(workflow, override=override)
        self.assertEqual(sale.date_order, last_week_time)
        self.run_job()
        self.assertTrue(sale.invoice_ids)
        invoice = sale.invoice_ids
        self.assertEqual(invoice.invoice_date, last_week_time.date())
        self.assertEqual(invoice.workflow_process_id, sale.workflow_process_id)

    def test_04_create_invoice_from_sale_order(self):
        workflow = self.create_full_automatic()
        sale = self.create_sale_order(workflow)
        line = sale.order_line[0]
        # Make sure this addon works properly in regards to it.
        mock_path = "odoo.addons.sale.models.sale_order.SaleOrder._create_invoices"
        workflow.invoice_service_delivery = True
        line.qty_delivered_method = "manual"
        with mock.patch(mock_path) as mocked:
            sale._create_invoices()
            mocked.assert_called()
        self.assertEqual(line.qty_delivered, 1.0)

    def test_05_invoice_from_picking_with_service_product(self):
        workflow = self.create_full_automatic()
        product_service = self.env["product.product"].create(
            {
                "name": "Remodeling Service",
                "categ_id": self.env.ref("product.product_category_3").id,
                "standard_price": 40.0,
                "list_price": 90.0,
                "type": "service",
                "uom_id": self.env.ref("uom.product_uom_hour").id,
                "uom_po_id": self.env.ref("uom.product_uom_hour").id,
                "description": "Example of product to invoice on order",
                "default_code": "PRE-PAID",
                "invoice_policy": "order",
            }
        )
        product_uom_hour = self.env.ref("uom.product_uom_hour")
        override = {
            "order_line": [
                (
                    0,
                    0,
                    {
                        "name": "Prepaid Consulting",
                        "product_id": product_service.id,
                        "product_uom_qty": 1,
                        "product_uom": product_uom_hour.id,
                    },
                )
            ]
        }
        sale = self.create_sale_order(workflow, override=override)
        self.run_job()
        self.assertTrue(sale.invoice_ids)
        invoice = sale.invoice_ids
        self.assertEqual(invoice.workflow_process_id, sale.workflow_process_id)

    def test_06_journal_on_invoice(self):
        sale_journal = self.env["account.journal"].search(
            [("type", "=", "sale")], limit=1
        )
        new_sale_journal = self.env["account.journal"].create(
            {"name": "TTSA", "code": "TTSA", "type": "sale"}
        )

        workflow = self.create_full_automatic()
        sale = self.create_sale_order(workflow)
        self.run_job()
        self.assertTrue(sale.invoice_ids)
        invoice = sale.invoice_ids
        self.assertEqual(invoice.journal_id.id, sale_journal.id)

        workflow = self.create_full_automatic(
            override={"property_journal_id": new_sale_journal.id}
        )
        sale = self.create_sale_order(workflow)
        self.run_job()
        self.assertTrue(sale.invoice_ids)
        invoice = sale.invoice_ids
        self.assertEqual(invoice.journal_id.id, new_sale_journal.id)

    def test_no_copy(self):
        workflow = self.create_full_automatic()
        sale = self.create_sale_order(workflow)
        self.run_job()
        invoice = sale.invoice_ids
        self.assertTrue(sale.workflow_process_id)
        self.assertTrue(invoice.workflow_process_id)
        sale2 = sale.copy()
        invoice2 = invoice.copy()
        self.assertFalse(sale2.workflow_process_id)
        self.assertFalse(invoice2.workflow_process_id)

    def test_automatic_sale_order_confirmation_mail(self):
        workflow = self.create_full_automatic()
        workflow.send_order_confirmation_mail = True
        sale = self.create_sale_order(workflow)
        previous_message_ids = sale.message_ids
        self.run_job()
        self.assertEqual(sale.state, "sale")
        new_messages = self.env["mail.message"].search(
            [
                ("id", "in", sale.message_ids.ids),
                ("id", "not in", previous_message_ids.ids),
            ]
        )
        self.assertTrue(
            new_messages.filtered(
                lambda x: x.subtype_id == self.env.ref("mail.mt_comment")
            )
        )

    def test_create_payment_with_invoice_currency_id(self):
        workflow = self.create_full_automatic()
        pricelist_id = self.env["product.pricelist"].create(
            {
                "name": "default_pricelist",
                "currency_id": 1,
            }
        )
        product_service = self.env["product.product"].create(
            {
                "name": "Remodeling Service",
                "categ_id": self.env.ref("product.product_category_3").id,
                "standard_price": 40.0,
                "list_price": 90.0,
                "type": "service",
                "uom_id": self.env.ref("uom.product_uom_hour").id,
                "uom_po_id": self.env.ref("uom.product_uom_hour").id,
                "description": "Example of product to invoice on order",
                "default_code": "PRE-PAID",
                "invoice_policy": "order",
            }
        )
        product_uom_hour = self.env.ref("uom.product_uom_hour")
        override = {
            "pricelist_id": pricelist_id.id,
            "order_line": [
                (
                    0,
                    0,
                    {
                        "name": "Prepaid Consulting",
                        "product_id": product_service.id,
                        "product_uom_qty": 1,
                        "product_uom": product_uom_hour.id,
                    },
                )
            ],
        }
        sale = self.create_sale_order(workflow, override=override)
        self.run_job()
        self.assertTrue(sale.invoice_ids)
        invoice = sale.invoice_ids
        self.assertEqual(invoice.state, "posted")
        payment_id = self.env["automatic.workflow.job"]._register_payment_invoice(
            invoice
        )
        self.assertTrue(payment_id)
        self.assertEqual(invoice.currency_id.id, payment_id.currency_id.id)
