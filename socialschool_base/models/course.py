from odoo import models, fields, api, _


class SocialSchoolCurse(models.Model):
    _name = "socialschool.course"
    _description = "Social School Course"
    _inherit = "mail.thread"

    name = fields.Char(string="Nome")
    group_id = fields.Many2one("socialschool.group", string="Grupo")
    category_id = fields.Many2one("socialschool.course.category", string="Categoria")
    vacancies = fields.Integer(string="Vagas")
    subject_ids = fields.One2many('socialschool.course.subject', "course_id")
    active = fields.Boolean(default=True)

    hide = fields.Boolean(string="Hide", compute="_compute_hide")

    @api.depends('group_id')
    def _compute_hide(self):
        if self.group_id.type_vacancies == 'by_course':
            self.hide = True
        else:
            self.hide = False


class SocialSchoolCurseSubject(models.Model):
    _name = "socialschool.course.subject"
    _description = "Social School Subject"
    _inherit = "mail.thread"

    course_id = fields.Many2one("socialschool.course", string="Curso")
    name = fields.Char(strong="Nome")
    active = fields.Boolean(default=True)


class SocialSchoolCurseCategory(models.Model):
    _name = "socialschool.course.category"
    _description = "Social School Category"

    name = fields.Char(string="Nome")
    description = fields.Text(string="Descrição")