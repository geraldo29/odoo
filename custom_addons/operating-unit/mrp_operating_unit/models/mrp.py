# Copyright 2019 ForgeFlow S.L.
# Copyright 2019 Serpent Consulting Services Pvt. Ltd.
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).
from odoo import api, fields, models
from odoo.exceptions import ValidationError


class MrpProduction(models.Model):
    _inherit = "mrp.production"

    operating_unit_id = fields.Many2one(
        "operating.unit",
        "Operating Unit",
        readonly=True,
        default=lambda self: self.env["res.users"]._get_default_operating_unit(
            self._uid
        ),
    )

    @api.constrains("operating_unit_id", "location_src_id", "location_dest_id")
    def _check_location_operating_unit(self):
        for mo in self:
            # no operating unit on mo but on locations
            no_mo_ou = not mo.operating_unit_id and (
                mo.location_src_id.operating_unit_id
                or mo.location_dest_id.operating_unit_id
            )
            # operating unit on mo but not on locations
            different_ou = mo.operating_unit_id and (
                mo.operating_unit_id != mo.location_src_id.operating_unit_id
                or mo.operating_unit_id != mo.location_dest_id.operating_unit_id
            )

            if no_mo_ou or different_ou:
                raise ValidationError(
                    self.env._(
                        "The Operating Unit of the Manufacturing Order must match "
                        "with that of the Raw Materials and Finished Product "
                        "Locations."
                    )
                )

    @api.onchange("operating_unit_id")
    def _onchange_operating_unit_id(self):
        """Change locations according to the warehouse of the operating unit."""
        if self.operating_unit_id:
            # Take first warehouse with the current operating unit
            wh = self.env["stock.warehouse"].search(
                [("operating_unit_id", "=", self.operating_unit_id.id)], limit=1
            )
            picking_type_id = (
                self.env["stock.picking.type"].search(
                    [
                        ("code", "=", "mrp_operation"),
                        ("company_id", "=", self.company_id.id),
                        ("warehouse_id", "=", wh.id),
                    ],
                    limit=1,
                )
                if wh
                else False
            )
            if picking_type_id:
                self.picking_type_id = picking_type_id
