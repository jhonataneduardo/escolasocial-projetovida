from odoo import models, fields, api, _


class SocialSchoolParent(models.Model):
    _name = "socialschool.parent"
    _description = "Social School Parent"
    _inherit = "mail.thread"
    _inherits = {"res.partner": "partner_id"}

    name = fields.Char(string="Nome")
    student_ids = fields.Many2many('socialschool.student', string='Estudante(s)')
    partner_id = fields.Many2one('res.partner', 'Partner', required=True, ondelete="cascade")
    user_id = fields.Many2one('res.users', 'User', ondelete="cascade")
    active = fields.Boolean(default=True)


class SocialSchoolStudent(models.Model):
    _inherit = "socialschool.student"

    parent_ids = fields.Many2many('socialschool.parent', string='Parent')

    def get_parent(self):
        action = self.env.ref('socialschool_parent.act_open_op_parent_view').read()[0]
        action['domain'] = [('student_ids', 'in', self.ids)]
        return action