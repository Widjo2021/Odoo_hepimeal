from odoo import models, fields, api, _
from odoo.exceptions import UserError


class SuratKerja(models.Model):
    _name = 'surat.kerja'

    name = fields.Char(readonly=True, copy=False)
    employee_id = fields.Many2one('hr.employee')
    date_from = fields.Datetime()
    date_to = fields.Datetime()
    description = fields.Text()
    state = fields.Selection([
        ('ongoing', 'Sedang Berjalan'),
        ('done', 'Selesai')
    ], default="ongoing")
    word_hours = fields.Float(compute='_compute_worked_hours', store=True)
    surat_jalan_employee_id = fields.One2many('surat.jalan.detil.employee', 'surat_jalan_id')
    detil_attendance_line_id = fields.One2many('detil.employee.attendance', 'surat_kerja_id')
    default_attendance = fields.Char(compute='compute_default_attendance')

    def compute_default_attendance(self):
        for line in self:
            line.default_attendance = 'a'
            line.detil_attendance_line_id = False

            attendancess = []
            for lines in line.surat_jalan_employee_id:
                date = str(str(lines.date_from).split(' ')[0]).split('-')[0] + "-" + \
                       str(str(lines.date_from).split(' ')[0]).split('-')[1] + "-" + \
                       str(str(lines.date_from).split(' ')[0]).split('-')[2]
                if lines.date_from and lines.employee_id:

                    id = []
                    self._cr.execute("SELECT * FROM hr_attendance WHERE check_in::date = '" + str(
                        date) + "' and employee_id = " + str(lines.employee_id.id))
                    attd = self._cr.dictfetchall()
                    for attd_id in attd:
                        id.append(attd_id['id'])

                    attendance = self.env['hr.attendance'].search([('id', 'in', id)])
                    for atte_line in attendance:
                        check_out = atte_line.check_out
                        if not atte_line.check_out:
                            check_out = atte_line.check_in
                        delta = check_out - atte_line.check_in

                        data = {
                            'employee_id': lines.employee_id.id,
                            'check_in': atte_line.check_in,
                            'check_out': atte_line.check_out,
                            'work_hours': delta.total_seconds() / 3600.0,
                            'surat_kerja_id': line.id
                        }
                        attendancess.append([0, 0, data])
            line.detil_attendance_line_id = attendancess



    def action_done(self):
        for line in self:
            for lines in line.surat_jalan_employee_id:
                if lines.long_working_hours_approved <= 0.0:
                    if lines.long_working_hours > line.word_hours:
                        line.long_working_hours_approved = line.word_hours
                    else:
                        line.long_working_hours_approved = line.long_working_hours
                lines.state = 'approved'
            line.state = 'done'

    @api.depends('date_from', 'date_to')
    def _compute_worked_hours(self):
        for line in self:
            if line.date_to:
                delta = line.date_to - line.date_from
                line.word_hours = delta.total_seconds() / 3600.0
            else:
                line.word_hours = False

    # @api.onchange('date_from')
    # def onchange_date_from(self):
    #     for line in self:
    #         if line.date_from:
    #             delta = line.date_to - line.date_from
    #             line.word_hours = delta.total_seconds() / 3600.0
    #
    # @api.onchange('date_to')
    # def onchange_date_to(self):
    #     for line in self:
    #         if line.date_to:
    #             delta = line.date_from - line.date_to
    #             line.word_hours = delta.total_seconds() / 3600.0

    @api.model
    def create(self, vals):
        vals['name'] = self.env['ir.sequence'].next_by_code('surat.kerja') or '/'
        return super(SuratKerja, self).create(vals)


class SuratJalanDetilEmployee(models.Model):
    _name = 'surat.jalan.detil.employee'

    employee_id = fields.Many2one('hr.employee')
    date_from = fields.Datetime()
    date_to = fields.Datetime()
    word_hours = fields.Float()
    state = fields.Selection([
        ('draft', 'Draft'),
        ('approved', 'Approved')
    ], default="draft")
    long_working_hours = fields.Float(compute="compute_long_working_hours")
    long_working_hours_approved = fields.Float()
    surat_jalan_id = fields.Many2one('surat.jalan')

    def compute_long_working_hours(self):
        for line in self:
            # date = str(line.date_from).split(' ')[0]
            date = str(str(line.date_from).split(' ')[0]).split('-')[0] + "-" + str(str(line.date_from).split(' ')[0]).split('-')[1] + "-" + str(str(line.date_from).split(' ')[0]).split('-')[2]
            print(date)
            long_working_hours = 0.0
            if line.date_from and line.employee_id:

                id = []
                self._cr.execute("SELECT * FROM hr_attendance WHERE check_in::date = '"+ str(date) +"' and employee_id = "+str(line.employee_id.id))
                attd = self._cr.dictfetchall()
                for attd_id in attd:
                    id.append(attd_id['id'])

                attendance = self.env['hr.attendance'].search([('id', 'in', id)])

                for lines in attendance:
                    check_out = lines.check_out
                    if not lines.check_out:
                        check_out = lines.check_in
                    delta = check_out - lines.check_in
                    long_working_hours += delta.total_seconds() / 3600.0
            line.long_working_hours = long_working_hours
            #if line.long_working_hours > line.word_hours:
            #    line.long_working_hours_approved = line.word_hours
            #else:
            #    line.long_working_hours_approved = line.long_working_hours


class DetilEmployeeAttendance(models.Model):
    _name = 'detil.employee.attendance'

    employee_id = fields.Many2one('hr.employee')
    check_in = fields.Datetime()
    check_out = fields.Datetime()
    work_hours = fields.Float()
    surat_kerja_id = fields.Many2one('surat.kerja')
