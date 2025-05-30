# Copyright 2019 Ecosoft Co., Ltd. (http://ecosoft.co.th)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    "name": "Expense Tier Validation",
    "version": "18.0.1.0.0",
    "category": "Human Resources",
    "author": "Ecosoft, Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "website": "https://github.com/OCA/hr-expense",
    "depends": ["hr_expense", "base_tier_validation"],
    "data": ["data/ir_config_parameter.xml", "views/hr_expense_sheet_view.xml"],
    "installable": True,
    "maintainers": ["ps-tubtim"],
}
