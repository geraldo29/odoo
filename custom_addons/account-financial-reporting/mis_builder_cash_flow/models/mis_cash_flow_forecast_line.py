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
    company_id = fields.Many2one(
        "res.company",
        string="Company",
        required=True,
        default=lambda self: self.env.company,
        index=True,
    )

    @api.constrains("company_id", "account_id")
    def _check_company_id_account_id(self):
        for line in self:
            # In Odoo 18, account.account uses company_ids (Many2many)
            # Check if the forecast line's company is in the account's companies
            if (
                line.account_id.company_ids 
                and line.company_id not in line.account_id.company_ids
            ):
                raise ValidationError(
                    _(
                        "The forecast line company must be one of the "
                        "account's companies."
                    )
                )

    @api.onchange("company_id")
    def _onchange_company_id(self):
        """Filter accounts based on the selected company"""
        if self.company_id:
            return {
                "domain": {
                    "account_id": [
                        ("company_ids", "in", self.company_id.id)
                    ]
                }
            }
