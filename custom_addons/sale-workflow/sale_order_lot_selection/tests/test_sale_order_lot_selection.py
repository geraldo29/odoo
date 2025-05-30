# © 2015 Agile Business Group
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo.tests import TransactionCase


class TestSaleOrderLotSelection(TransactionCase):
    @classmethod
    def setUpClass(cls):
        """
        Set up a sale order a particular lot.

        I confirm it, transfer the delivery order and check lot on picking

        Set up a sale order with two lines with different products and lots.

        I confirm it, transfer the delivery order and check lots on picking

        """
        super().setUpClass()
        cls.prd_cable = cls.env.ref("stock.product_cable_management_box")
        cls.prd_cable.tracking = "lot"
        cls.product_46 = cls.env.ref("product.product_product_13")
        cls.product_12 = cls.env.ref("product.product_product_12")
        cls.supplier_location = cls.env.ref("stock.stock_location_suppliers")
        cls.customer_location = cls.env.ref("stock.stock_location_customers")
        cls.stock_location = cls.env.ref("stock.stock_location_stock")
        cls.product_model = cls.env["product.product"]
        cls.lot_model = cls.env["stock.lot"]
        cls.lot_cable = cls.env.ref("sale_order_lot_selection.lot_cable_demo")
        cls.sale = cls.env.ref("sale_order_lot_selection.sale_order_demo")

    def _retrieve_stock_quantity(self, product, lot, location):
        return product.with_context(lot_id=lot.id, location=location.id).qty_available

    def test_00_stock_available_wrong_lot(self):
        # We should not be able to reserve if some stock is available but with another
        # lot
        self._update_stock_quantity(self.prd_cable, self.lot_cable, 1)
        other_lot = self.env["stock.lot"].create(
            {
                "name": "test2",
                "product_id": self.prd_cable.id,
                "company_id": self.env.ref("base.main_company").id,
            }
        )
        self._update_stock_quantity(self.prd_cable, other_lot, 1)
        self.sale.action_confirm()
        self.sale.picking_ids.action_assign()
        # one of 2 moves should be reserved
        available_move = self.sale.picking_ids.move_ids.filtered(
            lambda m: m.state == "assigned"
        )
        unavailable_move = self.sale.picking_ids.move_ids.filtered(
            lambda m: m.state == "confirmed"
        )
        self.assertEqual(len(available_move), 1)
        self.assertEqual(len(unavailable_move), 1)

    def _update_stock_quantity(self, product, lot, qty):
        self.env["stock.quant"]._update_available_quantity(
            product, self.stock_location, lot_id=lot, quantity=qty
        )

    def test_01_several_lines_with_same_lot(self):
        """You may want split your order in several lines
        even if lot/product are the same
        use cases: price is different or any shipping information
        """
        self._update_stock_quantity(self.prd_cable, self.lot_cable, 10)
        self.sale.action_confirm()

    def test_02_sale_order_lot_selection(self):
        # INIT stock of products to 0
        picking_out = self.env["stock.picking"].create(
            {
                "picking_type_id": self.env.ref("stock.picking_type_out").id,
                "location_id": self.stock_location.id,
                "location_dest_id": self.customer_location.id,
            }
        )
        self.env["stock.move"].create(
            {
                "name": self.product_12.name,
                "product_id": self.product_12.id,
                "product_uom_qty": self.product_12.qty_available,
                "product_uom": self.product_12.uom_id.id,
                "picking_id": picking_out.id,
                "location_id": self.stock_location.id,
                "location_dest_id": self.customer_location.id,
            }
        )
        self.env["stock.move"].create(
            {
                "name": self.product_46.name,
                "product_id": self.product_46.id,
                "product_uom_qty": self.product_46.qty_available,
                "product_uom": self.product_46.uom_id.id,
                "picking_id": picking_out.id,
                "location_id": self.stock_location.id,
                "location_dest_id": self.customer_location.id,
            }
        )
        picking_out.action_confirm()
        picking_out.action_assign()
        picking_out._action_done()

        self.product_46.write({"tracking": "lot", "type": "consu"})
        self.product_12.write({"tracking": "lot", "type": "consu"})

        # make products enter
        picking_in = self.env["stock.picking"].create(
            {
                "partner_id": self.env.ref("base.res_partner_1").id,
                "picking_type_id": self.env.ref("stock.picking_type_in").id,
                "location_id": self.supplier_location.id,
                "location_dest_id": self.stock_location.id,
            }
        )
        self.env["stock.move"].create(
            {
                "name": self.prd_cable.name,
                "product_id": self.prd_cable.id,
                "product_uom_qty": 1,
                "product_uom": self.prd_cable.uom_id.id,
                "picking_id": picking_in.id,
                "location_id": self.supplier_location.id,
                "location_dest_id": self.stock_location.id,
            }
        )
        self.env["stock.move"].create(
            {
                "name": self.product_12.name,
                "product_id": self.product_12.id,
                "product_uom_qty": 1,
                "product_uom": self.product_12.uom_id.id,
                "picking_id": picking_in.id,
                "location_id": self.supplier_location.id,
                "location_dest_id": self.stock_location.id,
            }
        )
        self.env["stock.move"].create(
            {
                "name": self.product_46.name,
                "product_id": self.product_46.id,
                "product_uom_qty": 2,
                "product_uom": self.product_46.uom_id.id,
                "picking_id": picking_in.id,
                "location_id": self.supplier_location.id,
                "location_dest_id": self.stock_location.id,
            }
        )
        for move in picking_in.move_ids:
            self.assertEqual(move.state, "draft", "Wrong state of move line.")
        picking_in.action_confirm()
        for move in picking_in.move_ids:
            self.assertEqual(move.state, "assigned", "Wrong state of move line.")
        lot10 = False
        lot11 = False
        lot12 = False
        for move in picking_in.move_ids_without_package:
            if move.product_id == self.prd_cable:
                lot10 = self.lot_model.create(
                    {
                        "name": "0000010",
                        "product_id": self.prd_cable.id,
                        "product_qty": move.product_qty,
                        "company_id": self.env.company.id,
                    }
                )
                move.move_line_ids.write(
                    {"lot_id": lot10.id, "quantity": move.product_qty}
                )
            if move.product_id == self.product_46:
                lot11 = self.lot_model.create(
                    {
                        "name": "0000011",
                        "product_id": self.product_46.id,
                        "product_qty": move.product_qty,
                        "company_id": self.env.company.id,
                    }
                )
                move.move_line_ids.write(
                    {"lot_id": lot11.id, "quantity": move.product_qty}
                )
            if move.product_id == self.product_12:
                lot12 = self.lot_model.create(
                    {
                        "name": "0000012",
                        "product_id": self.product_12.id,
                        "product_qty": move.product_qty,
                        "company_id": self.env.company.id,
                    }
                )
                move.move_line_ids.write(
                    {"lot_id": lot12.id, "quantity": move.product_qty}
                )
        picking_in.button_validate()

        # check quantities
        lot10_qty_available = self._retrieve_stock_quantity(
            self.prd_cable, lot10, self.stock_location
        )
        self.assertEqual(lot10_qty_available, 1)
        lot11_qty_available = self._retrieve_stock_quantity(
            self.product_46, lot11, self.stock_location
        )
        self.assertEqual(lot11_qty_available, 2)
        lot12_qty_available = self._retrieve_stock_quantity(
            self.product_12, lot12, self.stock_location
        )
        self.assertEqual(lot12_qty_available, 1)

        # create order
        self.order1 = self.env["sale.order"].create(
            {"partner_id": self.env.ref("base.res_partner_1").id}
        )
        self.sol1 = self.env["sale.order.line"].create(
            {
                "name": "sol1",
                "order_id": self.order1.id,
                "lot_id": lot10.id,
                "product_id": self.prd_cable.id,
                "product_uom_qty": 1,
            }
        )
        self.order2 = self.env["sale.order"].create(
            {"partner_id": self.env.ref("base.res_partner_1").id}
        )
        self.sol2a = self.env["sale.order.line"].create(
            {
                "name": "sol2a",
                "order_id": self.order2.id,
                "lot_id": lot11.id,
                "product_id": self.product_46.id,
                "product_uom_qty": 1,
            }
        )
        self.sol2b = self.env["sale.order.line"].create(
            {
                "name": "sol2b",
                "order_id": self.order2.id,
                "lot_id": lot12.id,
                "product_id": self.product_12.id,
                "product_uom_qty": 1,
            }
        )
        self.order3 = self.env["sale.order"].create(
            {"partner_id": self.env.ref("base.res_partner_1").id}
        )
        self.sol3 = self.env["sale.order.line"].create(
            {
                "name": "sol_test_1",
                "order_id": self.order3.id,
                "lot_id": lot10.id,
                "product_id": self.prd_cable.id,
                "product_uom_qty": 1,
            }
        )
        self.order4 = self.env["sale.order"].create(
            {"partner_id": self.env.ref("base.res_partner_1").id}
        )
        self.sol4 = self.env["sale.order.line"].create(
            {
                "name": "sol4",
                "order_id": self.order4.id,
                "lot_id": lot11.id,
                "product_id": self.product_46.id,
                "product_uom_qty": 2,
            }
        )

        # confirm orders
        self.order1.action_confirm()
        picking = self.order1.picking_ids

        picking_move_line_ids = picking.move_ids_without_package[0].move_line_ids
        picking_move_line_ids[0].quantity = 1
        picking_move_line_ids[0].location_id = self.stock_location
        picking.button_validate()

        # put back the lot because it is removed by onchange
        self.sol3.lot_id = lot10.id
        # I'll try to confirm it to check lot reservation:
        # lot10 was delivered by order1
        lot10_qty_available = self._retrieve_stock_quantity(
            self.prd_cable, lot10, self.stock_location
        )
        self.order3.action_confirm()
        self.assertEqual(self.order3.state, "sale")
        # products are not available for reservation (lot unavailable)
        self.assertEqual(self.order3.picking_ids[0].state, "confirmed")

        # onchange remove lot_id, we put it back
        self.sol2a.lot_id = lot11.id
        self.order2.action_confirm()
        picking = self.order2.picking_ids
        picking.action_assign()

        picking.move_ids_without_package.mapped("move_line_ids").write({"quantity": 1})
        picking.button_validate()

        # check quantities
        lot10_qty_available = self._retrieve_stock_quantity(
            self.prd_cable, lot10, self.stock_location
        )
        self.assertEqual(lot10_qty_available, 0)
        lot11_qty_available = self._retrieve_stock_quantity(
            self.product_46, lot11, self.stock_location
        )
        self.assertEqual(lot11_qty_available, 1)
        lot12_qty_available = self._retrieve_stock_quantity(
            self.product_12, lot12, self.stock_location
        )
        self.assertEqual(lot12_qty_available, 0)
        # I'll try to confirm it to check lot reservation:
        # lot11 has 1 availability and order4 has quantity 2
        self.order4.action_confirm()
        self.assertEqual(self.order4.state, "sale")
        # products are reserved
        self.assertEqual(self.order4.picking_ids[0].state, "assigned")
