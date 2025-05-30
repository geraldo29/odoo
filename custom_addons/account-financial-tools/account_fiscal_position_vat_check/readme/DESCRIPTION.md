With this module, when a user tries to validate a customer invoice or
refund with a fiscal position that requires VAT, Odoo blocks the
validation of the invoice if the customer doesn't have a VAT number in
Odoo.

![Block on invoice validation if partner's VAT is missing](static/description/vat_check_invoice_validation.png)

In the European Union (EU), when an EU company sends an invoice to
another EU company in another country, it can invoice without VAT (most
of the time) but the VAT number of the customer must be displayed on the
invoice.
