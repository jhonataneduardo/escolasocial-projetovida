from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class SocialSchoolStudent(models.Model):
    _inherit = "socialschool.student"

    @api.multi
    def create_student_enrollment(self):
        SocialSchoolEnrollment = self.env['socialschool.enrollment']
        values = {
            'student_id': self.id
        }
        enrollment = SocialSchoolEnrollment.create(values)
        return {
            'name': 'Matrículas....',
            'view_mode': 'form',
            'view_id': self.env.ref('socialschool_enrollment.view_socialschool_enrollment_form').id,
            'res_model': 'socialschool.enrollment',
            # 'context': "{'type':'out_invoice'}",
            'type': 'ir.actions.act_window',
            'res_id': enrollment.id,
        }