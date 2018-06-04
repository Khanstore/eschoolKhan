# -*- coding: utf-8 -*-

from odoo import models, fields, api

class eschoolStudent(models.Model):
    _inherit = 'op.student'
    nationality = fields.Many2one('res.country', 'Nationality', default="20")


