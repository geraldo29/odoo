# Copyright 2019 Tecnativa - Ernesto Tejeda
# Copyright 2024 Moduon Team S.L. <info@moduon.team>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class SaleOrderLinePriceHistory(models.TransientModel):
    _name = "sale.order.line.price.history"
    _description = "Sale order line price history"

    @api.model
    def _default_partner_id(self):
        line_id = self.env.context.get("active_id")
        return self.env["sale.order.line"].browse(line_id).order_partner_id.id

    @api.model
    def _default_product_id(self):
        line_id = self.env.context.get("active_id")
        return self.env["sale.order.line"].browse(line_id).product_id.id

    sale_order_line_id = fields.Many2one(
        comodel_name="sale.order.line",
        string="Sale order line",
        default=lambda self: self.env.context.get("active_id"),
    )
    product_id = fields.Many2one(
        comodel_name="product.product",
        string="Product",
        default=_default_product_id,
    )
    partner_id = fields.Many2one(
        comodel_name="res.partner",
        string="Customer",
        default=_default_partner_id,
    )
    line_ids = fields.One2many(
        comodel_name="sale.order.line.price.history.line",
        inverse_name="history_id",
        string="History lines",
        readonly=True,
    )
    include_quotations = fields.Boolean(
        help="Include quotations lines in the sale history",
    )
    include_commercial_partner = fields.Boolean(
        string="Include commercial entity",
        default=True,
        help="Include commercial entity and its contacts in the sale history",
    )

    @api.onchange("partner_id", "include_quotations", "include_commercial_partner")
    def _onchange_partner_id(self):
        self.line_ids = False
        states = ["sale", "done"]
        if self.include_quotations:
            states += ["draft", "sent"]
        domain = [
            ("product_id", "=", self.product_id.id),
            ("state", "in", states),
        ]
        if self.partner_id:
            if self.include_commercial_partner:
                domain += [
                    (
                        "order_partner_id",
                        "child_of",
                        self.partner_id.commercial_partner_id.ids,
                    )
                ]
            else:
                domain += [("order_partner_id", "child_of", self.partner_id.ids)]

        vals = []
        sol_limit = (
            self.env["ir.config_parameter"]
            .sudo()
            .get_param("sale_order_line_price_history.order_line_limit", default="20")
        )
        order_lines = self.env["sale.order.line"].search(domain, limit=int(sol_limit))
        order_lines -= self.sale_order_line_id
        for order_line in order_lines:
            vals.append(
                (
                    0,
                    False,
                    {
                        "sale_order_line_id": order_line.id,
                        "history_sale_order_line_id": self.sale_order_line_id.id,
                        "history_id": self.id,
                    },
                )
            )
        self.line_ids = vals


class SaleOrderLinePriceHistoryline(models.TransientModel):
    _name = "sale.order.line.price.history.line"
    _description = "Sale order line price history line"
    _order = "sale_order_date_order desc"

    history_id = fields.Many2one(
        comodel_name="sale.order.line.price.history",
        string="History",
    )
    target_sale_order_line_id = fields.Many2one(
        comodel_name="sale.order.line",
        related="history_id.sale_order_line_id",
    )
    history_sale_order_line_id = fields.Many2one(
        comodel_name="sale.order.line",
        string="history sale order line",
    )
    sale_order_line_id = fields.Many2one(
        comodel_name="sale.order.line",
    )
    order_id = fields.Many2one(
        related="sale_order_line_id.order_id",
    )
    order_state = fields.Selection(
        related="order_id.state",
    )
    partner_id = fields.Many2one(
        related="sale_order_line_id.order_partner_id",
    )
    sale_order_date_order = fields.Datetime(
        related="sale_order_line_id.order_id.date_order",
    )
    product_uom_qty = fields.Float(
        related="sale_order_line_id.product_uom_qty",
    )
    price_unit = fields.Float(
        related="sale_order_line_id.price_unit",
    )
    discount = fields.Float(
        related="sale_order_line_id.discount",
    )

    def _prepare_set_price_history_vals(self):
        """Hook method to prepare the values to update the
        sales order line in context.

        This method is invoke by action_set_price method in this model.
        """
        self.ensure_one()
        return {"price_unit": self.price_unit, "discount": self.discount}

    def action_set_price(self):
        if self.history_sale_order_line_id and self.sale_order_line_id:
            self.history_sale_order_line_id.write(
                self._prepare_set_price_history_vals()
            )
        else:
            raise ValidationError(
                _("Not found historical sale order line for this action!")
            )
