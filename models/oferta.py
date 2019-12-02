# -*- coding: utf-8 -*-

from odoo import models, fields, api

tipo_r = ['', 'Completa', 'Bono', 'Recarga Simple']

class oferta(models.Model):
    _name = 'recharge_movil.oferta'

    name = fields.Char(compute='_compute_name', string="Oferta")

    tipo_recarga = fields.Selection(selection=[(1, 'Completa'),(2, 'Bono'),(3, 'Recarga Simple')], required=True, string="Tipo de Recarga")

    company_currency = fields.Many2one('res.currency')

    precio = fields.Monetary(string="Precio a cobrar", required=True, currency_field='company_currency')

    saldo = fields.Monetary(string="Saldo a enviar", required=True, currency_field='company_currency')

    saldo_retorno = fields.Monetary(string="Saldo de Retorno", currency_field='company_currency', default=0)

    @api.one
    def _compute_name(self):
        if self.tipo_recarga == 3:
            self.name = tipo_r[self.tipo_recarga] + ' ' + str(self.precio) + ' -> ' + str(self.saldo)

        if self.tipo_recarga == 2:
            self.name = tipo_r[self.tipo_recarga] + ' ' + str(self.precio) + ' -> ' + 'BONO y R: ' + str(self.saldo_retorno)

        if self.tipo_recarga == 1:
            self.name = tipo_r[self.tipo_recarga] + ' ' + str(self.precio) + ' -> ' + str(self.saldo) + ' + BONO'
