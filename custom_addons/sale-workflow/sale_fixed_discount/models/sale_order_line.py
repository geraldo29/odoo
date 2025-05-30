# Copyright 2017-20 ForgeFlow S.L.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models
from odoo.exceptions import ValidationError
from odoo.tools.float_utils import float_compare, float_round


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    discount_fixed = fields.Float(
        string="Discount (Fixed)",
        digits="Product Price",
        help="Fixed amount discount.",
    )

    @api.constrains("discount_fixed", "discount")
    def _check_discounts(self):
        """Check that the fixed discount and the discount percentage are consistent."""
        for line in self:
            if line.discount_fixed and line.discount:
                currency = line.currency_id
                calculated_fixed_discount = float_round(
                    line._get_discount_from_fixed_discount(),
                    precision_rounding=currency.rounding,
                )

                if (
                    float_compare(
                        calculated_fixed_discount,
                        line.discount,
                        precision_rounding=currency.rounding,
                    )
                    != 0
                ):
                    raise ValidationError(
                        self.env._(
                            "The fixed discount %(fixed)s does not match the calculated"
                            "discount %(discount)s %%."
                            "Please correct one of the discounts.",
                            fixed=line.discount_fixed,
                            discount=line.discount,
                        )
                    )

    def _prepare_base_line_for_taxes_computation(self, **kwargs):
        """Prior to calculating the tax toals for a line, update the discount value
        used in the tax calculation to the full float value. Otherwise, we get rounding
        errors in the resulting calculated totals.

        For example:
            - price_unit = 750.0
            - discount_fixed = 100.0
            - discount = 13.33
            => price_subtotal = 650.03

        :return: A python dictionary.
        """
        self.ensure_one()

        # Accurately pass along the fixed discount amount to the tax computation method.
        if self.discount_fixed:
            return self.env["account.tax"]._prepare_base_line_for_taxes_computation(
                self,
                **{
                    "tax_ids": self.tax_id,
                    "quantity": self.product_uom_qty,
                    "partner_id": self.order_id.partner_id,
                    "currency_id": self.order_id.currency_id
                    or self.order_id.company_id.currency_id,
                    "rate": self.order_id.currency_rate,
                    "discount": self._get_discount_from_fixed_discount(),
                    **kwargs,
                },
            )

        return super()._prepare_base_line_for_taxes_computation(**kwargs)

    @api.depends("discount_fixed", "price_unit")
    def _compute_discount(self):
        lines_with_discount_fixed = self.filtered(lambda sol: sol.discount_fixed)
        for line in lines_with_discount_fixed:
            line.discount = line._get_discount_from_fixed_discount()
        return super(
            SaleOrderLine, self - lines_with_discount_fixed
        )._compute_discount()

    def _get_discount_from_fixed_discount(self):
        """Calculate the discount percentage from the fixed discount amount."""
        self.ensure_one()
        if not self.discount_fixed:
            return 0.0

        return (
            (self.price_unit != 0)
            and ((self.discount_fixed) / self.price_unit) * 100
            or 0.00
        )

    def _prepare_invoice_line(self, **optional_values):
        res = super()._prepare_invoice_line(**optional_values)
        res.update({"discount_fixed": self.discount_fixed})
        return res
