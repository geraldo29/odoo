# Copyright 2013-2014 Camptocamp SA - Guewen Baconnier
# © 2016 Eficent Business and IT Consulting Services S.L.
# © 2016 Serpent Consulting Services Pvt. Ltd.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo.addons.base.tests.common import BaseCommon


class TestSaleSourcedByLine(BaseCommon):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.sale_order_model = cls.env["sale.order"]
        cls.sale_order_line_model = cls.env["sale.order.line"]
        cls.stock_move_model = cls.env["stock.move"]
        cls.stock_warehouse_model = cls.env["stock.warehouse"]

        # Refs
        cls.customer = cls.env.ref("base.res_partner_2")
        cls.product_1 = cls.env.ref("product.product_product_27")
        cls.product_2 = cls.env.ref("product.product_product_24")
        cls.warehouse0 = cls.env.ref("stock.warehouse0")
        cls.warehouse1 = cls.stock_warehouse_model.create(
            {"name": "Test Warehouse", "code": "TWH"}
        )

    def test_sales_order_multi_source(self):
        so = self.sale_order_model.create(
            {
                "partner_id": self.customer.id,
            }
        )
        self.sale_order_line_model.create(
            {
                "product_id": self.product_1.id,
                "product_uom_qty": 8,
                "warehouse_id": self.warehouse1.id,
                "order_id": so.id,
            }
        )
        self.sale_order_line_model.create(
            {
                "product_id": self.product_2.id,
                "product_uom_qty": 8,
                "warehouse_id": self.warehouse0.id,
                "order_id": so.id,
            }
        )
        # confirm quotation
        so.action_confirm()
        self.assertEqual(
            len(so.picking_ids),
            2,
            f"2 delivery orders expected. Got {len(so.picking_ids)} instead",
        )
        for line in so.order_line:
            self.assertEqual(
                line.procurement_group_id.name,
                line.order_id.name + "/" + line.warehouse_id.name,
                "The name of the procurement group is not " "correct.",
            )
            moves = self.stock_move_model.search(
                [("group_id", "=", line.procurement_group_id.id)]
            )
            for move in moves:
                self.assertEqual(
                    move.group_id,
                    line.procurement_group_id,
                    "The group in the stock move does not "
                    "match with the procurement group in "
                    "the sales order line.",
                )
                self.assertEqual(
                    move.picking_id.group_id,
                    line.procurement_group_id,
                    "The group in the stock picking does "
                    "not match with the procurement group "
                    "in the sales order line.",
                )

    def test_sales_order_no_source(self):
        so = self.sale_order_model.create(
            {
                "partner_id": self.customer.id,
                "warehouse_id": self.warehouse1.id,
            }
        )
        self.sale_order_line_model.create(
            {"product_id": self.product_1.id, "product_uom_qty": 8, "order_id": so.id}
        )
        self.sale_order_line_model.create(
            {"product_id": self.product_2.id, "product_uom_qty": 8, "order_id": so.id}
        )
        # confirm quotation
        so.action_confirm()
        self.assertEqual(
            len(so.picking_ids),
            1,
            f"1 delivery order expected. Got {len(so.picking_ids)} instead",
        )

    def test_sale_order_source(self):
        so = self.sale_order_model.create(
            {
                "partner_id": self.customer.id,
            }
        )
        self.sale_order_line_model.create(
            {
                "product_id": self.product_1.id,
                "product_uom_qty": 8,
                "warehouse_id": self.warehouse1.id,
                "order_id": so.id,
            }
        )
        self.sale_order_line_model.create(
            {
                "product_id": self.product_2.id,
                "product_uom_qty": 8,
                "warehouse_id": self.warehouse0.id,
                "order_id": so.id,
            }
        )
        # confirm quotation
        so.action_confirm()
        for line in so.order_line:
            moves = self.stock_move_model.search(
                [("group_id", "=", line.procurement_group_id.id)]
            )
            for move in moves:
                self.assertEqual(
                    move.warehouse_id,
                    line.warehouse_id,
                    "The warehouse in the stock move does not "
                    "match with the Sales order line.",
                )
