# Copyright 2020 Tecnativa - Carlos Dauden
# Copyright 2020 Tecnativa - Pedro M. Baeza
# Copyright 2022 Tecnativa - Víctor Martínez
# Copyright 2023 Amitaujas
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from lxml import etree

from odoo import api, models
from odoo.tools.translate import _


class Base(models.AbstractModel):
    _inherit = "base"

    @api.model
    def _add_custom_filters(self, res, custom_filters):
        """
        Add custom filter fields to the view architecture.

        This method modifies the XML architecture of a view by injecting custom filter
        fields at specific positions. For each custom filter, it attempts to place the
        field after a specified field (if position_after is defined) or after the last
        field in the view.

        Args:
            res (dict): The view data dictionary containing the architecture
            custom_filters (recordset): Custom filter records to be added to the view

        Returns:
            dict: The modified view data with custom filters injected
        """
        arch = etree.fromstring(res["arch"])
        for custom_filter in custom_filters:
            node = False
            if custom_filter.position_after:
                node = arch.xpath(
                    _("//field[@name='%s']") % custom_filter.position_after
                )
            if not node:
                node = arch.xpath("//field[last()]")
            if node:
                elem = etree.Element(
                    "field",
                    {"name": custom_filter.expression, "string": custom_filter.name},
                )
                node[0].addnext(elem)
        res["arch"] = etree.tostring(arch)
        return res

    @api.model
    def get_view(self, view_id=None, view_type="form", **options):
        """Inject fields field in search views."""
        res = super().get_view(view_id, view_type, **options)
        if view_type == "search":
            custom_filters = self.env["ir.ui.custom.field.filter"].search(
                [("model_name", "=", res.get("model"))]
            )
            if custom_filters:
                res = self._add_custom_filters(res, custom_filters)
        return res

    @api.model
    def get_views(self, views, options=None):
        """Inject fake field definition for having custom filters available."""
        res = super().get_views(views, options)
        if self._name not in res["models"]:
            res["models"][self._name] = {}
        custom_filters = self.env["ir.ui.custom.field.filter"].search(
            [("model_name", "=", self._name)]
        )
        for custom_filter in custom_filters:
            field = custom_filter._get_related_field()
            # Safeguard: Ensure the related field exists before processing.
            # This check is necessary because a custom filter might reference
            # a field that no longer exists or is misconfigured. In such cases,
            # we skip the filter to avoid runtime errors.
            if not field:
                continue
            field_name = custom_filter.expression
            res["models"][self._name][field_name] = field.get_description(self.env)
            # Force these properties to prevent the field from appearing in the UI
            res["models"][self._name][field_name]["selectable"] = False
            res["models"][self._name][field_name]["sortable"] = False
            res["models"][self._name][field_name]["store"] = False
        return res
