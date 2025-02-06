from odoo import api, fields, models
from odoo.addons.tunas_ruangan.models.tunas_room import ROOM_LOCATION, ROOM_TYPE
from odoo.exceptions import ValidationError

class TunasRoomBook(models.Model):
    _name = 'tunas.room.book'
    _description = 'Room Booking'

    name = fields.Char(string='Nomor Pemesanan', default='/', required=True)
    name_sequence = fields.Char(string='Nomor Sequence')
    room_id = fields.Many2one('tunas.room', string='Ruangan', required=True)
    order_name = fields.Char(string='Nama Pemesanan', required=True)
    order_date = fields.Date(string='Tanggal Pemesanan', default=fields.Datetime.now)
    state = fields.Selection([
        ('draft', 'Draft'),
        ('ongoing', 'On Going'),
        ('done', 'Done'),
        ('cancel', 'Cancelled')
    ], string='Status', default='draft')
    description = fields.Text(string='Catatan Pemesanan')

    def action_draft(self):
        self.ensure_one()
        if self.state in ['done', 'cancel']:
            self.state = 'draft'

    def action_ongoing(self):
        self.ensure_one()
        if self.state == 'draft':
            self.state = 'ongoing'

    def action_done(self):
        self.ensure_one()
        if self.state == 'ongoing':
            self.state = 'done'

    def action_cancel(self):
        self.ensure_one()
        if self.state == 'draft':
            self.state = 'cancel'

    @api.model
    def create(self, vals):
        if vals.get('name', '/') == '/':
            room = self.env['tunas.room'].browse(vals.get('room_id', False))
            sequence = self.env['ir.sequence'].next_by_code('tunas.room.book.sequence') or '/'
            vals['name_sequence'] = sequence
            vals['name'] = f"{dict(ROOM_TYPE)[room.room_type]}/{dict(ROOM_LOCATION)[room.room_location]}/{sequence}"        
        return super(TunasRoomBook, self).create(vals)

    @api.constrains('order_date')
    def _check_order_date(self):
        for rec in self:
            if rec.order_date < fields.Date.today():
                raise ValidationError("Order date cannot be in the past!")

    @api.constrains('room_id', 'order_date')
    def _check_room_availability(self):
        for rec in self:
            domain = [
                ('room_id', '=', rec.room_id.id),
                ('order_date', '=', rec.order_date),
                ('state', 'in', ['draft', 'ongoing']),
                ('id', '!=', rec.id)
            ]
            existing_booking = self.search(domain)
            if existing_booking:
                raise ValidationError(f"Room {rec.room_id.name} is already booked for this date and time!")

    @api.constrains('order_name')
    def _check_order_name(self):
        for rec in self:
            domain = [('order_name', '=', rec.order_name), ('id', '!=', rec.id)]
            duplicated_order_name = self.search(domain)
            if duplicated_order_name:
                raise ValidationError("Order name already exists!")