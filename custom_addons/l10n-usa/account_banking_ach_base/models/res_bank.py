from stdnum.us import rtn

from odoo import api, fields, models
from odoo.exceptions import ValidationError


class ResBank(models.Model):
    _inherit = "res.bank"

    routing_number = fields.Char()

    @api.constrains("routing_number")
    def validate_routing_number(self):
        if not self.routing_number or not self.country:
            return
        country_code = self.country.code
        if country_code == "US":
            try:
                rtn.validate(self.routing_number)
            except Exception:
                raise ValidationError(  # noqa: B904
                    self.env._("%s is not a valid US routing number!")
                    % self.routing_number
                )
        elif country_code == "CA":
            if len(self.routing_number) != 8 or not self.routing_number.is_digit():
                raise ValidationError(
                    self.env._("%s is not a valid Canadian routing number!")
                    % self.routing_number
                )
