# -*- coding: utf-8 -*-
# from odoo import http


# class InstalacionesDeportivas(http.Controller):
#     @http.route('/instalaciones_deportivas/instalaciones_deportivas', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/instalaciones_deportivas/instalaciones_deportivas/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('instalaciones_deportivas.listing', {
#             'root': '/instalaciones_deportivas/instalaciones_deportivas',
#             'objects': http.request.env['instalaciones_deportivas.instalaciones_deportivas'].search([]),
#         })

#     @http.route('/instalaciones_deportivas/instalaciones_deportivas/objects/<model("instalaciones_deportivas.instalaciones_deportivas"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('instalaciones_deportivas.object', {
#             'object': obj
#         })
