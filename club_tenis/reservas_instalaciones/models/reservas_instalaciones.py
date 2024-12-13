from odoo import models, fields, api
from datetime import timedelta, datetime
from odoo.exceptions import ValidationError
import pytz

class ReservasInstalaciones(models.Model):
    _name = 'reservas.instalaciones'
    _description = 'Reservas de Instalaciones'

    name = fields.Char(string='Reserva', required=True)
    user_id = fields.Many2one('res.users', string='Usuario', required=True, default=lambda self: self.env.user)
    facility_id = fields.Many2one('instalaciones.deportivas', string='Instalación', required=True)
    start_datetime = fields.Datetime(string='Fecha y Hora de Inicio', required=True)
    end_datetime = fields.Datetime(string='Fecha y Hora de Fin', required=True)
    state = fields.Selection([
        ('reserved', 'Reservado'),
        ('cancelled', 'Cancelado'),
        ('completed', 'Completado')
    ], string='Estado', default='reserved')

    @api.onchange('start_datetime')
    def _onchange_end_datetime(self):
        """Establece automáticamente el tiempo de fin a 1 hora y 30 minutos después de la hora de inicio."""
        if self.start_datetime:
            self.end_datetime = self.start_datetime + timedelta(hours=1, minutes=30)

    @api.constrains('start_datetime', 'end_datetime')
    def _check_reservation_conflict(self):
        """Verifica las restricciones de las reservas."""
        for record in self:
            # Verificar si la instalación está en mantenimiento
            if record.facility_id.state == 'maintenance':
                raise ValidationError(f"No se puede reservar la instalación '{record.facility_id.name}' porque está en mantenimiento.")

            # Convertir las fechas a la zona horaria del servidor/usuario
            user_tz = pytz.timezone(self.env.user.tz or 'UTC')
            start_datetime_utc = pytz.utc.localize(record.start_datetime)
            end_datetime_utc = pytz.utc.localize(record.end_datetime)
            start = start_datetime_utc.astimezone(user_tz)
            end = end_datetime_utc.astimezone(user_tz)

             # Obtener la fecha actual en la zona horaria del usuario
            today = fields.Date.context_today(record)
            today_datetime = datetime.combine(today, datetime.min.time())  # Fecha actual con hora 00:00
            today_utc = pytz.utc.localize(today_datetime)  # Localizar como UTC
            today_local = today_utc.astimezone(user_tz)

            # Restricción de reservas solo para hoy, mañana y pasado mañana
            if start < today_local:
                raise ValidationError("No puedes reservar para días pasados.")
            
            max_date = today_local + timedelta(days=2)
            if start.date() > max_date.date():
                raise ValidationError("Solo puedes reservar para hoy, mañana o pasado mañana.")


            # Horarios permitidos
            weekday_start_hour = 8  # 8:00 AM
            weekday_end_hour = 23  # 11:00 PM
            sunday_end_hour = 14  # 2:00 PM

            if start.weekday() == 6:  # Domingo
                if not (weekday_start_hour <= start.hour < sunday_end_hour and
                        weekday_start_hour <= end.hour <= sunday_end_hour):
                    raise ValidationError("Los domingos el horario permitido es de 8:00 a 14:00.")
            else:  # De lunes a sábado
                if not (weekday_start_hour <= start.hour < weekday_end_hour and
                        weekday_start_hour <= end.hour <= weekday_end_hour):
                    raise ValidationError("El horario permitido es de 8:00 a 23:00 de lunes a sábado.")

            # Validar horas exactas permitidas
            allowed_hours = [8, 9.5, 11, 12.5, 14, 15.5, 17, 18.5, 20, 21.5]  # Horas permitidas
            start_hour_decimal = start.hour + start.minute / 60
            if start_hour_decimal not in allowed_hours:
                raise ValidationError("Solo se pueden reservar las siguientes horas: "
                                      "8:00, 9:30, 11:00, 12:30, 14:00, 15:30, 17:00, 18:30, 20:00, 21:30.")

            # Definir la capacidad máxima según el tipo de instalación
            max_allowed = record.facility_id.capacity

            # Buscar todas las reservas en el mismo rango de horas para la misma instalación
            reservations = self.env['reservas.instalaciones'].sudo().search([
                ('id', '!=', record.id),
                ('facility_id', '=', record.facility_id.id),
                ('start_datetime', '<', record.end_datetime),
                ('end_datetime', '>', record.start_datetime),
                ('state', '=', 'reserved'),  # Solo conflictos con reservas activas
            ])

            # Verificar si la cantidad de reservas actuales supera la capacidad máxima
            current_reservations_count = len(reservations)
            if current_reservations_count >= max_allowed:
                raise ValidationError(f"{record.facility_id.name} ya ha alcanzado el numero maximo de reservas en este horario.")

    @api.model
    def create(self, vals):
        """Sobrescribe el método create para evitar la creación de reservas con estado 'completado'."""
        if vals.get('state') == 'completed':
            raise ValidationError("No puedes crear una reserva con estado 'Completado'.")
        reservation = super(ReservasInstalaciones, self).create(vals)
        reservation._check_reservation_conflict()  # Verificar conflictos después de crear
        return reservation

    def write(self, vals):
        """Sobrescribe el método write para controlar restricciones de modificación."""
        for reservation in self:
            # Omitir validaciones si el contexto indica que se están cancelando automáticamente
            if self._context.get('skip_time_restriction', False) and 'state' in vals and vals['state'] == 'cancelled':
                continue

            if reservation.state == 'completed':
                raise ValidationError("No se puede modificar una reserva que ya ha sido completada.")
            
            start_datetime = fields.Datetime.from_string(reservation.start_datetime)
            if start_datetime < fields.Datetime.now() and not self._context.get('is_cron', False):
                raise ValidationError("No puedes modificar reservas de horas o días pasados.")
            
            # Verificar si la reserva se está cancelando
            if 'state' in vals and vals['state'] == 'cancelled':
                user_tz = pytz.timezone(self.env.user.tz or 'UTC')
                now_utc = fields.Datetime.now()
                now_local = pytz.utc.localize(now_utc).astimezone(user_tz)

                start_local = reservation.start_datetime.astimezone(user_tz)
                time_until_start = start_local - now_local

                if time_until_start < timedelta(hours=1, minutes=30):
                    raise ValidationError("No puedes cancelar una reserva menos de 1 hora y 30 minutos antes de que empiece.")
                
            # Si se actualizan campos, verificar conflictos
            if 'start_datetime' in vals or 'end_datetime' in vals or 'facility_id' in vals:
                new_vals = reservation.copy_data(vals)[0]  # Simular los cambios
                temp_reservation = self.new(new_vals)
                temp_reservation._check_reservation_conflict()
        
        return super(ReservasInstalaciones, self).write(vals)

    def auto_complete_reservations(self):
        """Actualiza automáticamente el estado de las reservas que ya han finalizado."""
        now = fields.Datetime.now()
        expired_reservations = self.search([
            ('end_datetime', '<', now),
            ('state', '=', 'reserved')
        ])
        for reservation in expired_reservations:
            reservation.with_context(is_cron=True).write({'state': 'completed'})