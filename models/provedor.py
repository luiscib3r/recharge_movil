# -*- coding: utf-8 -*-

from odoo import models, fields, api

class provedor(models.Model):
    _name = 'recharge_movil.provedor'

    name = fields.Char(unique=True, required=True, string="Nombre")

    company_currency = fields.Many2one('res.currency')

    debe = fields.Monetary(string="Debe", currency_field='company_currency', compute='_compute_debe')

    @api.one
    def _compute_debe(self):
        recargas = self.env['recharge_movil.recarga'].search([('provedor', '=', self.id), ('estado', '=', 2)])

        self.debe = self._sum_money(recargas)

    def _sum_money(self, records):
        sum = 0.0

        for r in records:
            sum = sum + r.precio

        return sum
