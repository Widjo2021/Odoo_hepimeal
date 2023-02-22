from odoo import models, fields, api, _


class IjinJamKerja(models.Model):
    _name = 'ijin.jam.kerja'

    name = fields.Char(readonly=True, copy=False)
    employee_id = fields.Many2one('hr.employee')
    date_from = fields.Datetime()
    date_to = fields.Datetime()
    duration = fields.Float(compute='_compute_worked_hours', store=True)
    description = fields.Text()
    date = fields.Date()
    state = fields.Selection([
        ('draft', 'Draft'),
        ('approved', 'Approved')
    ], default='draft')

    @api.depends('date_from', 'date_to')
    def _compute_worked_hours(self):
        for line in self:
            if line.date_to:
                delta = line.date_to - line.date_from
                line.duration = delta.total_seconds() / 3600.0
            else:
                line.duration = False

    def action_approved(self):
        for line in self:
            line.state = 'approved'

    @api.model
    def create(self, vals):
        vals['name'] = self.env['ir.sequence'].next_by_code('ijin.jam.kerja') or '/'
        return super(IjinJamKerja, self).create(vals)

