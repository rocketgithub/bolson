# -*- encoding: utf-8 -*-

from openerp import models, fields, api, _
from openerp.exceptions import UserError, ValidationError

import logging

class BolsonBolson(models.Model):
    _name = 'bolson.bolson'
    _description = 'Bolson de facturas y cheques'
    _order = 'fecha desc'

    fecha = fields.Date(string="Fecha", required=True)
    name = fields.Char(string="Descripcion", required=True)
    facturas = fields.One2many("account.invoice", "bolson_id", string="Facturas")
    cheques = fields.One2many("account.payment", "bolson_id", string="Cheques")
    company_id = fields.Many2one("res.company", string="Company", required=True, default=lambda self: self.env.user.company_id.id)
    diario = fields.Many2one("account.journal", string="Diario", required=True)
    asiento = fields.Many2one("account.move", string="Asiento")
    usuario_id = fields.Many2one("res.users", string="Usuario")
    cuenta_desajuste = fields.Many2one("account.account", string="Cuenta de desajuste")
