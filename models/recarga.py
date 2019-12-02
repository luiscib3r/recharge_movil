# -*- coding: utf-8 -*-

from odoo import models, fields, api

from odoo.exceptions import ValidationError

class recarga(models.Model):
    _name = 'recharge_movil.recarga'

    name = fields.Char(compute='_compute_name')

    provedor = fields.Many2one('recharge_movil.provedor', string="Provider")

    phone_number = fields.Char(string='Número de Teléfono')

    fecha_recarga = fields.Date(string="Fecha de recarga", required=True, default=fields.Date.today)

    oferta = fields.Many2one('recharge_movil.oferta', required=True)

    company_currency = fields.Many2one('res.currency')

    precio = fields.Monetary(string="Precio a cobrar", required=True, currency_field='company_currency', readonly=True, compute='_compute_precio')

    saldo = fields.Monetary(string="Saldo a enviar", required=True, currency_field='company_currency', readonly=True, compute='_compute_saldo')

    estado = fields.Many2one('recharge_movil.estado', string="Estado", required=True, ondelete='restrict', track_visibility='onchange', index=True, default=0, group_expand='_read_group_stage_ids')

    linea = fields.Many2one('recharge_movil.cashline', string="Línea de recarga", required=True)

    tipo_linea = fields.Integer(compute='_compute_tipo_linea')

    linea_retorno = fields.Many2one('recharge_movil.cashline', string="Línea de retorno", domain=[('tipo_linea', '=', 2)])

    tipo_recarga = fields.Integer(compute='_compute_tipo_recarga')

    is_this_week = fields.Integer(compute='_compute_is_this_week', string="Esta semana")

    @api.one
    def _compute_is_this_week(self):
        this_day = fields.Date.today()
        this_day_n = this_day.weekday()
        lunes = this_day - this_day.resolution * this_day_n
        domingo = this_day + this_day.resolution * (6 - this_day_n)

        if (self.fecha_recarga >= lunes and self.fecha_recarga <= domingo):
            self.is_this_week = 1
        else:
            self.is_this_week = 0


    @api.one
    def _compute_tipo_recarga(self):
        self.tipo_recarga = self.oferta.tipo_recarga

    @api.one
    def _compute_tipo_linea(self):
        if self.oferta.tipo_recarga > 2:
            self.tipo_linea = 2
        else:
            self.tipo_linea = 1

    @api.model
    def create(self, vals):
        oferta = self.env['recharge_movil.oferta'].browse(vals['oferta'])

        linea = self.env['recharge_movil.cashline'].browse(vals['linea'])

        if oferta.tipo_recarga > 2:
            saldo = oferta.saldo + 0.2
        else:
            saldo = oferta.saldo

        disponible = linea.disponible - linea.comprometido

        if saldo > disponible:
            raise ValidationError("Está tratando de asignar una recarga a una línea que no posee suficiente saldo")
            record = False;
        else:
            record = super(recarga, self).create(vals)

        return record

    @api.model
    def _read_group_stage_ids(self,stages,domain,order):
        stage_ids = self.env['recharge_movil.estado'].search([])
        return stage_ids

    @api.onchange('oferta')
    def _onchange_oferta(self):
        self.precio = self.oferta.precio
        self.saldo = self.oferta.saldo

        self._compute_tipo_linea()
        self._compute_tipo_recarga()

    @api.one
    @api.depends('oferta')
    def _compute_precio(self):
        self.precio = self.oferta.precio

    @api.one
    @api.depends('oferta')
    def _compute_saldo(self):
        self.saldo = self.oferta.saldo

    @api.one
    def _compute_name(self):
        try:
            self.name = self.provedor.name + ' ' + str(self.fecha_recarga)
        except Exception:
            self.name = '_' + ' ' + str(self.fecha_recarga)
