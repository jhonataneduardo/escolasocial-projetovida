from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class SocialSchooParent(models.Model):
    _name = "socialschool.parent"
    _description = "Social School Parent"
    _inherit = "mail.thread"
    _inherits = {"res.partner": "partner_id"}

    first_name = fields.Char('Nome', size=128, translate=True)
    last_name = fields.Char('Sobrenome', size=128, translate=True)
    birth_date = fields.Date('Data de Nascimento')
    gender = fields.Selection([
        ('m', 'Masculino'),
        ('f', 'Feminino')
    ], 'Gênero', required=True, default='m')
    parent_type = fields.Selection([
        ('p', 'Pai'),
        ('m', 'Mãe'),
        ('i', 'Irmão'),
        ('t', 'Tio'),
        ('a', 'Avô/Avó'),
        ('pm', 'Primo'),
        ('o', 'Outro')
    ], 'Grau Parentesco', required=True)
    is_legal_responsible = fields.Selection([
        ('s', 'Sim'),
        ('n', 'Não')
    ], string='É o responsável legal do aluno(a)?', required=True)
    in_same_house = fields.Selection([
        ('s', 'Sim'),
        ('n', 'Não')
    ], string='Moram da mesma casa?', required=True)
    profession = fields.Many2one('socialschool.profession', string="Profissão")
    nationality = fields.Many2one('res.country', 'Nacionalidade')
    rg = fields.Char(string="RG")
    cpf = fields.Char(string="CPF")
    partner_id = fields.Many2one('res.partner', 'Partner', required=True, ondelete="cascade")
    user_id = fields.Many2one('res.users', 'User', ondelete="cascade")
    student_id = fields.Many2one('socialschool.student', string="Parentes")
    description = fields.Text(string="Observação")
    active = fields.Boolean(default=True)

    @api.onchange('first_name', 'last_name')
    def _onchange_name(self):
        self.name = str(self.first_name) + " " + str(self.last_name)


class SocialSchoolStudent(models.Model):
    _inherit = "socialschool.student"

    parent_ids = fields.One2many('socialschool.parent', 'student_id', string="Alunos(as)")