# Copyright 2015 Pedro M. Baeza <pedro.baeza@serviciosbaeza.com>
# Copyright 2016 Vicent Cubells <vicent.cubells@tecnativa.com>
# Copyright 2017 David Vidal <david.vidal@tecnativa.com>
# Copyright 2018 Duc Dao Dong <duc.dd@komit-consulting.com>
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo.tests import common


class TestSaleOrderPriceRecalculation(common.TransactionCase):
    def setUp(self):
        super().setUp()
        # Enable group_discount_per_so_line for admin user
        group = self.env.ref("sale.group_discount_per_so_line")
        group.users = [(4, self.env.user.id)]
        self.partner = self.env["res.partner"].create({"name": "Test partner"})
        uom_id = self.env.ref("uom.product_uom_kgm")
        self.product = self.env["product.product"].create(
            {
                "name": "Jacket - Color: Black - Size: XL",
                "uom_id": uom_id.id,
                "uom_po_id": uom_id.id,
            }
        )
        self.pricelist = self.env["product.pricelist"].create(
            {
                "name": "Test pricelist",
                "item_ids": [
                    (
                        0,
                        0,
                        {
                            "applied_on": "3_global",
                            "compute_price": "formula",
                            "base": "list_price",
                        },
                    ),
                ],
            }
        )
        self.sale_order = self.env["sale.order"].create(
            {
                "partner_id": self.partner.id,
                "partner_invoice_id": self.partner.id,
                "partner_shipping_id": self.partner.id,
                "pricelist_id": self.pricelist.id,
            }
        )
        line_vals = {
            "product_id": self.product.id,
            "product_template_id": self.product.product_tmpl_id.id,
            "name": self.product.name,
            "product_uom_qty": 1.0,
            "product_uom": self.product.uom_id.id,
            "price_unit": self.product.lst_price,
            "order_id": self.sale_order.id,
        }
        self.sale_order_line = self.env["sale.order.line"].create(line_vals)

    def test_name_recalculation(self):
        self.sale_order_line.price_unit = 150.0
        initial_price = self.sale_order_line.price_unit
        self.assertEqual(self.sale_order_line.name, self.product.name)
        self.sale_order_line.name = "Custom Jacket"
        self.sale_order.action_update_names()
        self.assertNotEqual("Custom Jacket", self.sale_order_line.name)
        # Check the price wasn't reset
        self.assertEqual(initial_price, self.sale_order_line.price_unit)
