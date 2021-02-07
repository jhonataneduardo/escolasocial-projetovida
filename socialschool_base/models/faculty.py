from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class SocialSchookFaculty(models.Model):
    _name = "socialschool.faculty"
    _description = "Social School Faculty"
    _inherit = "mail.thread"
    _inherits = {"res.partner": "partner_id"}

    partner_id = fields.Many2one('res.partner', 'Partner',
                                 required=True, ondelete="cascade")
    first_name = fields.Char('Nome', size=128, translate=True)
    last_name = fields.Char('Sobrenome', size=128, required=True)
    birth_date = fields.Date('Data de aniversário', required=True)
    gender = fields.Selection([
        ('male', 'Masculino'),
        ('female', 'Feminino')
    ], 'Sexo', required=True)
    nationality = fields.Many2one('res.country', 'Nacionalidade')
    login = fields.Char(
        'Login', related='partner_id.user_id.login', readonly=1)
    last_login = fields.Datetime('Latest Connection', readonly=1,
                                 related='partner_id.user_id.login_date')
    activity_ids = fields.One2many(
        "socialschool.faculty.activity",
        "faculty_id",
        string="Atividades")
    active = fields.Boolean(default=True)

    @api.multi
    @api.constrains('birth_date')
    def _check_birthdate(self):
        for record in self:
            if record.birth_date > fields.Date.today():
                raise ValidationError(_(
                    "Birth Date can't be greater than current date!"))

    @api.onchange('first_name', 'last_name')
    def _onchange_name(self):
        self.name = str(self.first_name) + " " + str(self.last_name)


class SocialSchookFacultyActivity(models.Model):
    _name = "socialschool.faculty.activity"

    faculty_id = fields.Many2one(
        "socialschool.faculty",
        string="Atividades")
    day = fields.Selection([
        ('monday', 'Segunda-feira'),
        ('tuesday', 'Terça-feira'),
        ('wednesday', 'Quarta-feira'),
        ('thursday', 'Quinta-feira'),
        ('friday', 'Sexta-feira'),
        ('saturday', 'Sábado'),
        ('sunday', 'Domingo')
    ], string="Dia da Semana")
    start_time = fields.Float(
        string="Horário de Entrada")
    end_time = fields.Float(
        string="Horário de Saída")
    course_ids = fields. Many2many(
        "socialschool.course",
        string="Cursos/Oficinas")
    description = fields.Text(
        string="Descrição")