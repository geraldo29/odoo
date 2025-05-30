# © 2016 Opener B.V. (<https://opener.am>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from odoo import api, fields, models
from odoo.exceptions import AccessError
from odoo.tools.translate import _


class ResUsers(models.Model):
    _inherit = "res.users"

    technical_features = fields.Boolean(
        compute="_compute_technical_features", inverse="_inverse_technical_features"
    )
    show_technical_features = fields.Boolean(
        string="Show field Technical Features",
        compute="_compute_show_technical_features",
        help=(
            "Whether to display the technical features field in the user "
            "preferences."
        ),
    )

    @api.depends("groups_id")
    def _compute_show_technical_features(self):
        """Only display the technical features checkbox in the user
        preferences if the user has access to them"""
        for user in self:
            user.show_technical_features = user.has_group("base.group_no_one")

    @api.depends("groups_id")
    def _compute_technical_features(self):
        for user in self:
            user.technical_features = user.has_group(
                "base_technical_features.group_technical_features"
            )

    def _inverse_technical_features(self):
        """Map boolean field value to group membership, but checking
        access"""
        group = self.env.ref("base_technical_features.group_technical_features")
        for user in self:
            if self.env.ref("base.group_no_one") not in user.groups_id:
                raise AccessError(
                    _("The user does not have access to technical " "features.")
                )
        if user.technical_features:
            self.sudo().write({"groups_id": [(4, group.id)]})
        else:
            self.sudo().write({"groups_id": [(3, group.id)]})

    @property
    def SELF_READABLE_FIELDS(self):
        return super().SELF_READABLE_FIELDS + [
            "technical_features",
            "show_technical_features",
        ]

    @property
    def SELF_WRITEABLE_FIELDS(self):
        return super().SELF_WRITEABLE_FIELDS + ["technical_features"]
