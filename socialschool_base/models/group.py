from odoo import models, fields, api, _


class SocialSchoolGroup(models.Model):
    _name = "socialschool.group"
    _description = "Social School Group"

    name = fields.Char(string="Nome")
    parent_id = fields.Many2one("socialschool.group.config", string="Grupo Pai")
    type_vacancies = fields.Selection([
        ('by_group', 'Por Grupo'),
        ('by_course', 'Por Curso'),
        ('unlimited', 'Ilimitada')
    ], string="Tipo de Vagas")
    number_vacancies = fields.Integer(string="Número de Vagas")
    periods = fields.Selection([
        ('morning', 'Manhã'),
        ('afternoon', 'Tarde'),
        ('fulltime', 'Integral')
    ])
    faculty_id = fields.Many2one("socialschool.faculty", string="Orientador(a)")