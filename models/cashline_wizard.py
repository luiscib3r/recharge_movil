from odoo import models, fields, api

from odoo.exceptions import Warning

class cashline_wizard(models.TransientModel):
    _name = 'recharge_movil.cashline_wizard'

    company_currency = fields.Many2one('res.currency')

    asaldo = fields.Monetary(string="Cantidad saldo recargado", required=True, currency_field='company_currency')

    @api.one
    def recarga(self):
        line_id = self.env.context.get('active_id')

        linea = self.env['recharge_movil.cashline'].browse(line_id)

        linea.saldo = linea.saldo + self.asaldo
