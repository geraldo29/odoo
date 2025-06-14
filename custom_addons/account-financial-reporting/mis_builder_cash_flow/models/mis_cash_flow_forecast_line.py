# Copyright 2019 ADHOC SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class MisCashFlowForecastLine(models.Model):
    _name = "mis.cash_flow.forecast_line"
    _description = "MIS Cash Flow Forecast Line"

    date = fields.Date(required=True, index=True)
    account_id = fields.Many2one(
        comodel_name="account.account",
        string="Account",
        required=True,
        help="The account of the forecast line is only for informative purpose",
    )
    partner_id = fields.Many2one(comodel_name="res.partner", string="Partner")
    name = fields.Char(required=True, default="/")
    balance = fields.Float(required=True)
    company_ids = fields.Many2many(
        "res.company",
        string="Companies",
        required=True,
        default=lambda self: self.env.companies,
        index=True,
    )

    @api.constrains("company_ids", "account_id")
    def _check_company_ids_account_id(self):
        for line in self:
            if line.account_id.company_ids and not (
                line.company_ids & line.account_id.company_ids
            ):
                raise ValidationError(
                    _(
                        "The forecast line companies must overlap with the "
                        "account's companies."
                    )
                )
