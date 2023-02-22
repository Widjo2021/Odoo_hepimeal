from odoo import models, fields


class HrEmployee(models.Model):
    _inherit = 'hr.employee'
    _description = 'Employee'

    ptkp_id = fields.Many2one('pph.ptkp')
    tunjangan_jabatan = fields.Integer()



class Contract(models.Model):
    _inherit = 'hr.contract'
    _description = 'Contract'

    tunjangan_jabatan = fields.Integer()
