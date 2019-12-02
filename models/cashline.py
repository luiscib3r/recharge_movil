# -*- coding: utf-8 -*-

from odoo import models, fields, api

class cashline(models.Model):
    _name = 'recharge_movil.cashline'

    name = fields.Char('Línea', required=True, unique=True)

    company_currency = fields.Many2one('res.currency')

    saldo = fields.Monetary(string="Saldo", required=True, currency_field='company_currency')

    tipo_linea = fields.Selection(selection=[(1, 'Exterior'), (2, 'Móvil')], required=True, string="Tipo de línea")

    disponible = fields.Monetary(string="Disponible", compute='_compute_disponible', currency_field='company_currency')

    bono = fields.Monetary(string="Retorno de Bono", compute='_compute_bono', currency_field='company_currency')

    realizada = fields.Integer(string="Recargas realizadas", compute='_compute_realizada')

    pendiente = fields.Integer(string="Recargas pendientes", compute='_compute_pendiente')

    comprometido = fields.Monetary(string="Saldo comprometido", compute='_compute_comprometido', currency_field='company_currency')

    recaudado = fields.Monetary(string="Dinero recaudado", compute='_compute_recaudado', currency_field='company_currency')

    gastado = fields.Monetary(string="Saldo gastado", compute='_compute_gastado', currency_field='company_currency')

    @api.multi
    def _compute_bono(self):
        for r in self:
            recargas = r.env['recharge_movil.recarga'].search([('linea_retorno', '=', r.id), ('estado', '!=', 1)])

            sum = 0
            for R in recargas:
                if R.is_this_week == 1:
                    sum = sum + R.oferta.saldo_retorno

            r.bono = sum


    @api.multi
    def _compute_disponible(self):
        for r in self:
            recargas = r.env['recharge_movil.recarga'].search([('linea', '=', r.id), ('estado', '!=', 1)])
            r.disponible = r.saldo + r.bono - self._sum_saldo(recargas)

    def _sum_saldo(self, records):
        sum = 0.0

        for r in records:
            if r.is_this_week == 1:
                sum = sum + r.saldo
                if r.tipo_linea == 2:
                    sum = sum + 0.20

        return sum

    def _sum_money(self, records):
        sum = 0.0

        for r in records:
            if r.is_this_week == 1:
                sum = sum + r.precio

        return sum

    @api.multi
    def _compute_realizada(self):
        for r in self:
            realizada = 0
            recargas = r.env['recharge_movil.recarga'].search([('linea', '=', r.id), ('estado', '!=', 4), ('estado', '!=', 1)])

            for R in recargas:
                if R.is_this_week == 1:
                    realizada = realizada + 1

            r.realizada = realizada

    @api.multi
    def _compute_pendiente(self):
        for r in self:
            pendiente = 0
            recargas = r.env['recharge_movil.recarga'].search([('linea', '=', r.id), ('estado', '=', 1)])
            for R in recargas:
                if R.is_this_week == 1:
                    pendiente = pendiente + 1

            r.pendiente = pendiente

    @api.multi
    def _compute_comprometido(self):
        for r in self:
            recargas = r.env['recharge_movil.recarga'].search([('linea', '=', r.id), ('estado', '=', 1)])
            r.comprometido = self._sum_saldo(recargas)

    @api.multi
    def _compute_recaudado(self):
        for r in self:
            recargas = r.env['recharge_movil.recarga'].search([('linea', '=', r.id), ('estado', '=', 3)])
            r.recaudado = self._sum_money(recargas)

    @api.multi
    def _compute_gastado(self):
        for r in self:
            recargas = r.env['recharge_movil.recarga'].search([('linea', '=', r.id), ('estado', '!=', 1)])

            r.gastado = self._sum_saldo(recargas)
