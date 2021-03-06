from odoo import models, fields, api, _


class SocialSchoolVacancieMove(models.Model):
    _name = "socialschool.vacancie.move"
    _description = "Social School Vacancies Moves"

    enrollment_id = fields.Many2one(
        "socialschool.enrollment",
        string="Matrículas"
    )
    course_id = fields.Many2one(
        "socialschool.course",
        string="Cursos"
    )
    student_id = fields.Many2one(
        "socialschool.student",
        string="Aluno"
    )
    company_id = fields.Many2one(
        'res.company', 'Empresa',
        default=lambda self: self.env['res.company']._company_default_get('socialschool.vacancie.move'),
        index=True, required=True
    )
    state = fields.Selection([
        ('reserved', 'Reservada'),
        ('cancel', 'Cancelada'),
        ('done', 'Concluída')],
        string="Status", copy=False, default="draft", index=True, readonly=True)