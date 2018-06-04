# -*- coding: utf-8 -*-
from odoo import http

# class Next(http.Controller):
#     @http.route('/next/next/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/next/next/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('next.listing', {
#             'root': '/next/next',
#             'objects': http.request.env['next.next'].search([]),
#         })

#     @http.route('/next/next/objects/<model("next.next"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('next.object', {
#             'object': obj
#         })