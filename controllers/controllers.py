# -*- coding: utf-8 -*-
from odoo import http

class RechargeMovil(http.Controller):
    @http.route('/recharge_movil/data/', type='json', auth='user')
    def index(self, **kw):
        recargas = http.request.env['recharge_movil.recarga'].search([])

        total_recarga, completa, bono, simple = self._total_recargas(recargas)

        m_recarga, m_completa, m_bono, m_simple = self._money_recargas(recargas)

        s_recarga, s_completa, s_bono, s_simple = self._saldo_recargas(recargas)

        n_recarga = m_recarga - s_recarga
        n_completa = m_completa - s_completa
        n_bono = m_bono - s_bono
        n_simple = m_simple - s_simple

        lineas = http.request.env['recharge_movil.cashline'].search([])
        ofertas = http.request.env['recharge_movil.oferta'].search([])

        r_linea = []

        for l in lineas:
            r_linea.append({'name': l.name, 'disponible': l.disponible, 'tipo': l.tipo_linea,'oferta': []})

        for l in r_linea:
            for o in ofertas:
                if (l['tipo'] == 1 and (o.tipo_recarga == 1 or o.tipo_recarga == 2)) or (l['tipo'] == 2 and (o.tipo_recarga == 3)):
                    l['oferta'].append({
                        'name': o.name,
                        'cant': self._calc_cant(l, o),
                        'dinero':  self._calc_dinero(l, o),
                        'saldo': self._saldo_invertido(l, o),
                        'restante': self._calc_restante(l, o)
                    })

        return {
            'total_recarga': round(total_recarga,2),
            'completa': round(completa,2),
            'bono': round(bono,2),
            'simple': round(simple,2),

            'm_recarga': round(m_recarga,2),
            'm_completa': round(m_completa,2),
            'm_bono': round(m_bono,2),
            'm_simple': round(m_simple,2),

            's_recarga': round(s_recarga,2),
            's_completa': round(s_completa,2),
            's_bono': round(s_bono,2),
            's_simple': round(s_simple,2),

            'n_recarga': round(n_recarga,2),
            'n_completa': round(n_completa,2),
            'n_bono': round(n_bono,2),
            'n_simple': round(n_simple,2),
            'lineas': r_linea
        }

    def _calc_restante(self, l, o):
        if o.tipo_recarga == 2:
            return 'Retornado: $ ' + str(round(l['disponible'] - self._saldo_invertido(l, o), 2))
        else:
            return '$ ' + str(round(l['disponible'] - self._saldo_invertido(l, o), 2))

    def _saldo_invertido(self, l, o):
        c = self._calc_cant(l, o)

        if o.tipo_recarga == 3:
            return round(c * (o.saldo + 0.20), 2)
        elif o.tipo_recarga == 2:
            return round(c * (o.saldo - o.saldo_retorno), 2)
        else:
            return round(c * o.saldo, 2)

    def _calc_cant(self, l, o):
        if o.tipo_recarga == 3:
            return int(l['disponible'] / (o.saldo + 0.20))
        else:
            return int(l['disponible'] / o.saldo)

    def _calc_dinero(self, l, o):
        return round(self._calc_cant(l, o) * o.precio)

    def _total_recargas(self, records):
        total = 0
        completa = 0
        bono = 0
        simple = 0

        for R in records:
            if R.is_this_week == 1 and R.estado.id != 1:
                total = total + 1

                if R.oferta.tipo_recarga == 1:
                    completa = completa + 1

                if R.oferta.tipo_recarga == 2:
                    bono = bono + 1

                if R.oferta.tipo_recarga == 3:
                    simple = simple + 1

        return total, completa, bono, simple

    def _money_recargas(self, records):
        total = 0.00
        completa = 0.0
        bono = 0.00
        simple = 0.00

        for R in records:
            if R.is_this_week == 1 and R.estado.id == 3:
                total = total + R.precio

                if R.oferta.tipo_recarga == 1:
                    completa = completa + R.precio

                if R.oferta.tipo_recarga == 2:
                    bono = bono + R.precio

                if R.oferta.tipo_recarga == 3:
                    simple = simple + R.precio

        return total, completa, bono, simple

    def _saldo_recargas(self, records):
        total = 0.00
        t = 0.00
        completa = 0.00
        bono = 0.00
        simple = 0.00

        for R in records:
            if R.is_this_week == 1 and R.estado.id != 1:
                if R.tipo_recarga == 2:
                    total = total + (R.saldo - R.oferta.saldo_retorno)
                else:
                    total = total + R.saldo

                if R.tipo_recarga == 3:
                    t = t + 1

                if R.oferta.tipo_recarga == 1:
                    completa = completa + R.saldo

                if R.oferta.tipo_recarga == 2:
                    if R.estado.id == 3:
                        bono = bono + (R.saldo - R.oferta.saldo_retorno)

                    if R.estado.id == 2:
                        bono = bono + R.saldo

                if R.oferta.tipo_recarga == 3:
                    simple = simple + R.saldo

        t = t * 0.2
        return total + t, completa, bono, simple + t
