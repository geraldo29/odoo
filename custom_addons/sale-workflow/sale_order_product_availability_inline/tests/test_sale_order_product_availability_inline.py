# Copyright 2018 Tecnativa - Ernesto Tejeda
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.tests import Form, TransactionCase


class TestSaleOrderProductAvailabilityInline(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.obj_product = cls.env["product.product"]
        cls.obj_partner = cls.env["res.partner"]
        cls.obj_quant = cls.env["stock.quant"]
        cls.partner = cls.obj_partner.create({"name": "Partner test - sopai"})
        cls.product = cls.obj_product.create(
            {
                "name": "Test Product - sopai",
                "type": "consu",
                "is_storable": True,
                "default_code": "PRODSOPAI",
            }
        )
        cls.warehouse1 = cls.env["stock.warehouse"].create(
            {"name": "Warehouse test - sopai", "code": "AI1"}
        )
        cls.warehouse2 = cls.env["stock.warehouse"].create(
            {"name": "Warehouse test - sopai2", "code": "AI2"}
        )
        cls.obj_quant.create(
            {
                "location_id": cls.warehouse1.lot_stock_id.id,
                "product_id": cls.product.id,
                "inventory_quantity": 10,
            }
        ).action_apply_inventory()

        cls.obj_quant.create(
            {
                "location_id": cls.warehouse2.lot_stock_id.id,
                "product_id": cls.product.id,
                "inventory_quantity": 20,
            }
        ).action_apply_inventory()

    def test_sale_order_product_rec_name(self):
        self.assertEqual(
            self.product.with_context(warehouse_id=self.warehouse1.id).free_qty,
            10.0,
        )
        self.env.ref("product.decimal_product_uom").write({"digits": 3})
        sale_order_form = Form(
            self.env["sale.order"].with_context(
                warehouse_id=self.warehouse1.id, so_product_stock_inline=True
            )
        )
        with sale_order_form.order_line.new() as line_form:
            line_form.product_id = self.product
            self.assertTrue(
                line_form.product_id.display_name.endswith("(10.000 Units)")
            )
            self.assertFalse(line_form.name.endswith("(10.000 Units)"))
