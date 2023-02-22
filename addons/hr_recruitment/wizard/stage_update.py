from odoo import models, fields
from odoo.exceptions import UserError


class StageUpdate(models.Model):
    _name = "recruitment.stage.update"

    stages = fields.Many2one('hr.recruitment.stage')

    def update_stages(self):
        dt_recruiter = self._context.get('active_ids')
        check = []
        for key, data in enumerate(dt_recruiter):
            items = self.env['hr.applicant'].search([('id', '=', data)])
            check.append(int(items.stage_id))

        if len(set(check)) > 1:
            raise UserError('Stages Harus Sama')

        for key, data in enumerate(dt_recruiter):
            items = self.env['hr.applicant'].search([('id', '=', data)])
            for item in items:
                item.write({
                    'stage_id': self.stages.id
                })

