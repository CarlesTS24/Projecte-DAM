# -*- coding: utf-8 -*-
# from odoo import http


# class ReservasInstalaciones(http.Controller):
#     @http.route('/reservas_instalaciones/reservas_instalaciones', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/reservas_instalaciones/reservas_instalaciones/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('reservas_instalaciones.listing', {
#             'root': '/reservas_instalaciones/reservas_instalaciones',
#             'objects': http.request.env['reservas_instalaciones.reservas_instalaciones'].search([]),
#         })

#     @http.route('/reservas_instalaciones/reservas_instalaciones/objects/<model("reservas_instalaciones.reservas_instalaciones"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('reservas_instalaciones.object', {
#             'object': obj
#         })
