# Copyright 2017-2020 Onestein (<https://www.onestein.eu>)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models
from odoo.exceptions import UserError


class SaleOrder(models.Model):
    _inherit = "sale.order"

    active = fields.Boolean(copy=False, default=True)

    def toggle_active(self):
        if self.filtered(
            lambda so: not so.locked and so.state != "cancel" and so.active
        ):
            raise UserError(
                self.env._("Only 'Locked' or 'Canceled' orders can be archived")
            )
        return super().toggle_active()
