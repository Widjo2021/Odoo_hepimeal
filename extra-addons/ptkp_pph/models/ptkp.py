from odoo import models, fields, api,_


class PTKP(models.Model):
    _name = 'ptkp.ptkp'

    name = fields.Char()
    nominal = fields.Float()


class ResPartner(models.Model):
    _inherit = 'res.partner'

    ptkp_id = fields.Many2one('ptkp.ptkp')


class HREmployee(models.Model):
    _inherit = 'hr.employee'

    ptkp_id = fields.Many2one('ptkp.ptkp')
