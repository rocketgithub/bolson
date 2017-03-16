# -*- encoding: utf-8 -*-

from openerp import models, fields, api, _
from openerp.exceptions import UserError, ValidationError

class AccountBankStatement(models.Model):
    _inherit = 'account.bank.statement'

    bolson_id = fields.Many2one("bolson.bolson", string="Liquidacion", ondelete='restrict')
