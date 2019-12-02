# -*- coding: utf-8 -*-

from odoo import models, fields, api

class estado(models.Model):
    _name = 'recharge_movil.estado'

    name = fields.Char('Nombre Estado', required=True)
    sequence = fields.Integer('Secuencia', default=10)

    fold = fields.Boolean()
