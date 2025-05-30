# Copyright 2013-2014 Camptocamp SA - Guewen Baconnier
# © 2016 Eficent Business and IT Consulting Services S.L.
# © 2016 Serpent Consulting Services Pvt. Ltd.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).


from odoo import api, fields, models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    warehouse_id = fields.Many2one(
        "stock.warehouse",
        string="Default Warehouse",
        readonly=True,
        help="If no source warehouse is selected on line, "
        "this warehouse is used as default. ",
    )


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    @api.depends(
        "route_id", "order_id.warehouse_id", "product_packaging_id", "product_id"
    )
    def _compute_warehouse_id(self):
        """compute the warehouse for the lines only
        if it has not already been set."""
        lines = self.filtered(lambda rec: not rec.warehouse_id)
        return super(SaleOrderLine, lines)._compute_warehouse_id()

    def _prepare_procurement_group_vals(self):
        vals = super()._prepare_procurement_group_vals()
        # for compatibility with sale_quotation_sourcing
        if self._get_procurement_group_key()[0] == 10:
            if self.warehouse_id:
                vals["name"] += "/" + self.warehouse_id.name
        return vals

    def _prepare_procurement_values(self, group_id=False):
        """Prepare specific key for moves or other components
        that will be created from a stock rule
        comming from a sale order line. This method could be
        override in order to add other custom key that could
        be used in move/po creation.
        """
        values = super()._prepare_procurement_values(group_id)
        self.ensure_one()
        if self.warehouse_id:
            values["warehouse_id"] = self.warehouse_id
        return values

    def _get_procurement_group_key(self):
        """Return a key with priority to be used to regroup lines in multiple
        procurement groups

        """
        priority = 10
        key = super()._get_procurement_group_key()
        # Check priority
        if key[0] >= priority:
            return key
        wh_id = (
            self.warehouse_id.id if self.warehouse_id else self.order_id.warehouse_id.id
        )
        return priority, wh_id
