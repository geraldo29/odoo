# © 2017 Akretion (Alexis de Lattre <alexis.delattre@akretion.com>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    "name": "Agreement",
    "summary": "Adds an agreement object",
    "version": "18.0.1.0.0",
    "category": "Contract",
    "author": "Akretion, "
    "Yves Goldberg (Ygol Internetwork), "
    "Odoo Community Association (OCA)",
    "website": "https://github.com/OCA/agreement",
    "license": "AGPL-3",
    "depends": ["mail"],
    "data": [
        "security/ir.model.access.csv",
        "security/agreement_security.xml",
        "views/agreement.xml",
        "views/agreement_type.xml",
        "views/agreement_menu.xml",
    ],
    "demo": ["demo/demo.xml"],
    "development_status": "Beta",
    "maintainers": [
        "ygol",
        "alexis-via",
    ],
    "installable": True,
}
