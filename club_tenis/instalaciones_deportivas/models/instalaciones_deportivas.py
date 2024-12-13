# -*- coding: utf-8 -*-

from odoo import models, fields, api


class instalaciones_deportivas(models.Model):
    _name = 'instalaciones.deportivas'
    _description = 'Gestión de instalaciones deportivas'

    name = fields.Char(string='Nombre de la instalación', required=True)
    facility_type = fields.Selection([
        ('tennis', 'Tenis'),
        ('padel', 'Padel'),
        ('fronton', 'Frontón'),
        ('gym', 'Gimnasio'),
        ('spa', 'Spa'),
        ('futsal', 'Futbito')
    ], string='Tipo de instalación', requires=True)

    court_number = fields.Integer(string='Número de pista')
    surface_type = fields.Selection([
        ('clay', 'Tierra Batida'),
        ('hard', 'Dura')
    ], string='Tipo de superficie')
    wall_material = fields.Selection([
        ('glass', 'Cristal'),
        ('stone', 'Piedra')
    ], string='Material de las paredes')

    image = fields.Binary(string="Imagen de la instalación", attachment=False)
    capacity = fields.Integer(string='Capacidad máxima')
    state = fields.Selection([
        ('available', 'Disponible'),
        ('maintenance', 'En mantenimiento')
    ], string='Estado', default='available')

    _sql_constraints = [
        ('unique_padel_court', 'UNIQUE(name)', 'El nombre de la pista de pádel debe ser único.'),
        ('unique_court_number', 'UNIQUE(court_number, facility_type)', 'El número de pista de tenis debe ser único.')
    ]

    def write(self, vals):
        # Si se cambia el estado a "mantenimiento", cancelar reservas activas
        if 'state' in vals and vals['state'] == 'maintenance':
            reservations = self.env['reservas.instalaciones'].sudo().search([
                ('facility_id', '=', self.id),
                ('state', '=', 'reserved')
            ])
            for reservation in reservations:
                reservations.with_context(skip_time_restriction=True).write({'state': 'cancelled'})

                # Enviar notificación por correo electrónico
                self.env['mail.mail'].create({
                    'subject': 'Reserva Cancelada',
                    'body_html': f'<p>La reserva para la instalación "{self.name}" ha sido cancelada debido a que está en mantenimiento.</p>',
                    'email_to': reservation.user_id.email,
                }).send()

        return super(instalaciones_deportivas, self).write(vals)