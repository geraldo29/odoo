# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
# Copyright 2021 Ecosoft Co., Ltd (http://ecosoft.co.th)

from odoo import models


class SaleAdvancePaymentInv(models.TransientModel):
    _inherit = "sale.advance.payment.inv"

    def _prepare_invoice_values(self, order, so_line, accounts):
        res = super()._prepare_invoice_values(order, so_line, accounts)
        if order.type_id.journal_id:
            res["journal_id"] = order.type_id.journal_id.id
        if order.type_id:
            res["sale_type_id"] = order.type_id.id
        return res
