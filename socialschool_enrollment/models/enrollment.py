from odoo import models, fields, api, _
from odoo.exceptions import Warning


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

    @api.model
    def create(self, vals):
        if vals.get('name', 'Nova') == 'Nova':
            vals['name'] = self.env['ir.sequence'].next_by_code('socialschool.enrollment') or 'Nova'
        result = super(SocialSchoolEnrollment, self).create(vals)
        return result

    @api.multi
    def _check_vacancies(self, course):
        if course.group_id.type_vacancies == 'by_group':
            course_vacancies = course.group_id.number_vacancies
        elif course.group_id.type_vacancies == 'by_course':
            course_vacancies = course.vacancies
        else:
            course_vacancies = 1000000

        vacancie_moves = self.env['socialschool.vacancie.move'].search([
            ('course_id', '=', course.id),
            ('company_id', '=', self.env.user.company_id.id),
            ('state', 'in', ['reserved', 'done'])])

        if len(vacancie_moves) == course_vacancies:
            raise Warning('Não há mais vagas disponíveis para o curso {}'.format(course.name))

        return True


    @api.multi
    def reserved_enrollment(self):
        if len(self.enrollment_course_ids) == 0:
            raise Warning('Nenhum curso selecionado.')
        Vacancies = self.env['socialschool.vacancie.move']
        for course in self.enrollment_course_ids:
            self._check_vacancies(course.course_id)
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
        vacancie_id = self.env['socialschool.vacancie.move'].search([('enrollment_id', '=', self.id)])
        vacancie_id.write({'state': 'done'})
        self.write({'state': 'done'})



class SocialSchoolEnrollmentCourse(models.Model):
    _name = "socialschool.enrollment.course"
    _description = "Social School Enrollment Course"

    enrollment_id = fields.Many2one(
        "socialschool.enrollment",
        string="Matrículas",
        ondelete='cascade'
    )
    course_id = fields.Many2one(
        "socialschool.course",
        string="Cursos",
        ondelete='restrict'
    )
    course_group = fields.Char(
        string="Grupo"
    )

    @api.onchange('course_id')
    def onchange_course(self):
        for item in self:
            item.course_group = item.course_id.group_id.name