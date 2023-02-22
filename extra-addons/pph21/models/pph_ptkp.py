from odoo import models, fields


class pph_ptkp(models.Model):
    _name = 'pph.ptkp'
    _description = 'Setting PTKP PPH 21'

    name = fields.Char()
    nominal = fields.Integer()
    currency_id = fields.Many2one('res.currency')
    keterangan = fields.Text()