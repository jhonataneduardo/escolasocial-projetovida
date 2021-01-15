from odoo import models, fields, api, _


class SocialSchooProfession(models.Model):
    _name = "socialschool.profession"
    _description = "Social School Profession"

    name = fields.Char(string="Nome")

    # TODO: Criar um demo pra popular a tabela na instalação.