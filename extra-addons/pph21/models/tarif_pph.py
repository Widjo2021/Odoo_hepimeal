from odoo import models, fields


class tarif_pph(models.Model):
    _name = 'tarif.pph'
    _description = 'Settinf Tarif PPH'

    name = fields.Char()
    min_nominal = fields.Integer()
    max_nominal = fields.Integer()