from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class SocialSchoolStudent(models.Model):
    _name = "socialschool.student"
    _description = "Social School Student"
    _inherit = "mail.thread"
    _inherits = {"res.partner": "partner_id"}

    first_name = fields.Char('Nome', size=128, translate=True)
    last_name = fields.Char('Sobrenome', size=128, translate=True)
    birth_date = fields.Date('Data de Nascimento')
    gender = fields.Selection([
        ('m', 'Masculino'),
        ('f', 'Feminino')
    ], 'Gênero', required=True, default='m')
    nationality = fields.Many2one('res.country', 'Nacionalidade')
    emergency_contact = fields.Many2one('res.partner', 'Contatos de Emergência')
    health_ids = fields.Many2many("socialschool.student.health", string="Questões de saúde")
    partner_id = fields.Many2one('res.partner', 'Partner', required=True, ondelete="cascade")
    user_id = fields.Many2one('res.users', 'User', ondelete="cascade")
    active = fields.Boolean(default=True)

    @api.onchange('first_name', 'last_name')
    def _onchange_name(self):
        self.name = str(self.first_name) + " " + str(self.last_name)

    @api.multi
    @api.constrains('birth_date')
    def _check_birthdate(self):
        for record in self:
            if record.birth_date > fields.Date.today():
                raise ValidationError(_(
                    "A data de nascimento não pode ser posterior à data atual!"))

    @api.multi
    def create_student_user(self):
        user_group = self.env.ref("base.group_portal") or False
        users_res = self.env['res.users']
        for record in self:
            if not record.user_id:
                user_id = users_res.create({
                    'name': record.name,
                    'partner_id': record.partner_id.id,
                    'login': record.email,
                    'groups_id': user_group,
                    # 'is_student': True,
                    'tz': self._context.get('tz')
                })
                record.user_id = user_id


class SocialSchoolStudentHealth(models.Model):
    _name = "socialschool.student.health"
    _description = "Social School Student Health"

    type = fields.Selection([
        ('psychological', 'Psicológico'),
        ('physicist', 'Físico')
    ], string="Tipo")
    medication_use = fields.Boolean(string="Usa medicamento contínuo?")
    description = fields.Text(string="Descrição")

