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
    ], 'Gender', required=True)
    nationality = fields.Many2one('res.country', 'Nacionalidade')
    emergency_contact = fields.Many2one(
        'res.partner', 'Contato de Emergência')
    login = fields.Char(
        'Login', related='partner_id.user_id.login', readonly=1)
    last_login = fields.Datetime('Latest Connection', readonly=1,
                                 related='partner_id.user_id.login_date')
    emp_id = fields.Many2one('hr.employee', 'HR Employee')
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

    @api.multi
    def create_employee(self):
        for record in self:
            vals = {
                'name': record.name,
                'country_id': record.nationality.id,
                'gender': record.gender,
                'address_home_id': record.partner_id.id
            }
            emp_id = self.env['hr.employee'].create(vals)
            record.write({'emp_id': emp_id.id})
            record.partner_id.write({'supplier': True, 'employee': True})