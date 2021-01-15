from odoo import models, fields, api, _


class SocialSchoolEnrollment(models.Model):
    _name = "socialschool.enrollment"
    _description = "Social School Enrollment"
    _inherit = "mail.thread"

    name = fields.Char(
        string='Referência',
        required=True,
        copy=False,
        readonly=True,
        states={'draft': [('readonly', False)]}, index=True, default=lambda self: 'Nova')
    student_id = fields.Many2one(
        "socialschool.student",
        string="Aluno"
    )
    group_id = fields.Many2many(
        "socialschool.group",
        string="Grupo"
    )
    enrollment_course_ids = fields.One2many(
        "socialschool.enrollment.course",
        "enrollment_id"
    )
    state = fields.Selection(
        [('draft', 'Pŕe-matrícula'), ('reserved', 'Reservada'),
         ('cancel', 'Cancelada'), ('done', 'Concluída')],
        'Status', default='draft', track_visibility='onchange')
    active = fields.Boolean(default=True)

    # @api.model
    # def create(self, vals):
    #     if vals.get('name', 'Nova') == 'Nova':
    #         vals['name'] = self.env['ir.sequence'].next_by_code('socialschool.enrollment') or 'Nova'
    #     result = super(SocialSchoolEnrollment, self).create(vals)
    #     return result

    @api.multi
    def reserved_enrollment(self):
        Vacancies = self.env['socialschool.vacancie']
        for course in self.enrollment_course_ids:
            values = {
                'enrollment_id': self.id,
                'course_id': course.course_id.id,
                'student_id': self.student_id.id,
                'state': 'reserved'
            }
            Vacancies.create(values)
        self.write({'state': 'reserved'})
        return True

    @api.multi
    def done_enrollment(self):
        vacancie_id = self.env['socialschool.vacancie'].browse([self.id])
        vacancie_id.write({'state': 'done'})
        self.write({'state': 'done'})



class SocialSchoolEnrollment(models.Model):
    _name = "socialschool.enrollment.course"
    _description = "Social School Enrollment Course"

    enrollment_id = fields.Many2one(
        "socialschool.enrollment",
        string="Matrículas"
    )
    course_id = fields.Many2one(
        "socialschool.course",
        string="Cursos"
    )
    course_group = fields.Char(
        string="Grupo"
    )

    @api.onchange('course_id')
    def onchange_course(self):
        for item in self:
            item.course_group = item.course_id.group_id.name