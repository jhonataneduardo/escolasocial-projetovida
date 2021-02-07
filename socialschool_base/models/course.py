from odoo import models, fields, api, _


class SocialSchoolCurse(models.Model):
    _name = "socialschool.course"
    _description = "Social School Course"
    _inherit = "mail.thread"

    name = fields.Char(string="Nome")
    group_id = fields.Many2one("socialschool.group", string="Grupo", ondelete='restrict')
    category_id = fields.Many2one("socialschool.course.category", string="Categoria")
    vacancies = fields.Integer(string="Vagas")
    subject_ids = fields.One2many('socialschool.course.subject', "course_id")
    faculty_id = fields.Many2one("socialschool.faculty", string="Professore Responsável")
    active = fields.Boolean(default=True)
    available_vacancies = fields.Integer(string="Vagas Disponíveis", compute="_compute_available_vacancies")

    hide = fields.Boolean(string="Hide", compute="_compute_hide")

    @api.depends('group_id')
    def _compute_hide(self):
        if self.group_id.type_vacancies == 'by_course':
            self.hide = True
        else:
            self.hide = False

    def _compute_available_vacancies(self):
        VacancieMoves = self.env['socialschool.vacancie.move']
        for course in self:
            if course.group_id.type_vacancies == 'by_group':
                course_vacancies = course.group_id.number_vacancies
            elif course.group_id.type_vacancies == 'by_course':
                course_vacancies = course.vacancies
            else:
                course_vacancies = 1000000

            vacancie_moves = VacancieMoves.search([
                ('course_id', '=', course.id),
                ('company_id', '=', self.env.user.company_id.id),
                ('state', 'in', ['reserved', 'done'])])
            course.available_vacancies = course_vacancies - len(vacancie_moves)
        return True




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