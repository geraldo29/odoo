import re
from string import ascii_uppercase

from ach.builder import AchFile

from odoo import fields, models
from odoo.exceptions import UserError

CREDIT_AUTOMATED_RETURN = "21"
CREDIT_AUTOMATED_DEPOSIT = "22"
CREDIT_PRENOTE_DNE_ENR = "23"
CREDIT_ZERO_DOLLAR_ENTRY_WITH_ADDENDA = "24"

DEBIT_AUTOMATED_RETURN = "26"
DEBIT_AUTOMATED_PAYMENT = "27"
DEBIT_PRENOTE_DNE_ENR = "28"
DEBIT_ZERO_DOLLAR_ENTRY_WITH_ADDENDA = "29"


class AccountPaymentOrder(models.Model):
    _inherit = "account.payment.order"

    def get_file_id_mod(self):
        """
        ACH file_id_mod should be 'A' for the first of the day,
        'B' for the second and so on.
        """
        ach_transactions_today = self.env["account.payment.order"].search_count(
            [
                ("create_date", ">=", fields.Date.today()),
                ("company_partner_bank_id", "=", self.company_partner_bank_id.id),
                ("state", "in", ["generated", "uploaded"]),
                ("payment_mode_id.payment_method_id.code", "in", ["ACH-In", "ACH-Out"]),
            ]
        )
        return ascii_uppercase[ach_transactions_today]

    def ach_settings(self):
        bank = self.company_partner_bank_id.bank_id
        routing_number = bank.routing_number
        legal_id_number = self.company_id.legal_id_number
        if not legal_id_number:
            raise UserError(
                self.env._("%s does not have an EIN / SSN / BN assigned!")
                % self.company_id.name
            )

        if not routing_number:
            raise UserError(
                self.env._("%s does not have a Routing Number assigned!") % bank.name
            )
        return {
            "immediate_dest": self.company_partner_bank_id.acc_number,
            "immediate_org": routing_number,
            "immediate_dest_name": bank.name,
            "immediate_org_name": self.company_id.name,
            "company_id": legal_id_number,
        }

    def validate_banking(self, line):
        if not line.partner_bank_id.bank_id:
            raise UserError(
                self.env._("%s account number has no Bank assigned")
                % line.partner_bank_id.acc_number
            )

        if not line.partner_bank_id.bank_id.routing_number:
            raise UserError(
                self.env._("%s has no routing number specified")
                % line.partner_bank_id.bank_id.name
            )

    def validate_mandates(self, line):
        """Ensure that mandates are correctly set"""
        if not line.mandate_id:
            raise UserError(
                self.env._(
                    "Missing ACH Direct Debit mandate on the "
                    "payment line with partner %(name)s "
                    "(reference %(line_name)s).",
                    name=line.partner_id.name,
                    line_name=line.name,
                )
            )
        if line.mandate_id.state != "valid":
            raise Warning(
                self.env._(
                    "The ACH Direct Debit mandate with "
                    "reference %(unique_mandate_reference)s "
                    "for partner %(name)s has expired."
                ),
                unique_mandate_reference=line.mandate_id.unique_mandate_reference,
                name=line.mandate_id.partner_id.name,
            )
        if line.mandate_id.type == "oneoff" and line.mandate_id.last_debit_date:
            raise Warning(
                self.env._(
                    "The mandate with reference %(unique_mandate_reference)s "
                    "for partner %(name)s has type set to 'One-Off' and it has a "
                    "last debit date set to %(last_debit_date)s, so we can't use "
                    "it."
                ),
                unique_mandate_reference=line.mandate_id.unique_mandate_reference,
                name=line.mandate_id.partner_id.name,
                last_debit_date=line.mandate_id.last_debit_date,
            )

    def get_transaction_type(self, amount):
        if not amount:
            return (
                DEBIT_ZERO_DOLLAR_ENTRY_WITH_ADDENDA
                if self.payment_type == "inbound"
                else CREDIT_ZERO_DOLLAR_ENTRY_WITH_ADDENDA
            )

        return (
            DEBIT_AUTOMATED_PAYMENT
            if self.payment_type == "inbound"
            else CREDIT_AUTOMATED_DEPOSIT
        )

    def generate_ach_file(self):
        self.ensure_one()

        inbound_payment = self.payment_type == "inbound"

        file_mod = self.get_file_id_mod()
        ach_file = AchFile(file_id_mod=file_mod, settings=self.ach_settings())
        filename = (
            f"{fields.Date.today()}_{self.company_partner_bank_id.id}_{file_mod}.txt"
        )
        entries = []
        for line in self.payment_ids:
            if inbound_payment:
                self.validate_mandates(line)
            self.validate_banking(line)
            amount = line.amount
            name = re.sub("[^A-Za-z0-9]+", "", line.partner_id.name)
            note = re.sub("[^A-Za-z0-9]+", "", line.memo)
            entries.append(
                {
                    "type": self.get_transaction_type(amount=amount),
                    "routing_number": line.partner_bank_id.bank_id.routing_number,
                    "account_number": line.partner_bank_id.acc_number,
                    "amount": str(amount),
                    "name": name,
                    "addenda": [{"payment_related_info": note}],
                }
            )
        outbound_payment = self.payment_type == "outbound"
        ach_file.add_batch(
            "PPD", entries, credits=outbound_payment, debits=inbound_payment
        )
        return ach_file.render_to_string().encode("utf-8"), filename
