from odoo import models, fields, api

ROOM_TYPE = [
    ('meeting_room_kecil', 'Meeting Room Kecil'),
    ('meeting_room_besar', 'Meeting Room Besar'),
    ('aula', 'Aula'),
]

ROOM_LOCATION = [
    ('1a', '1A'),
    ('1b', '1B'),
    ('1c', '1C'),
    ('2a', '2A'),
    ('2b', '2B'),
    ('2c', '2C'),
]

class TunasRoom(models.Model):
    _name = 'tunas.room'
    _description = 'Master Data Ruangan'

    name = fields.Char(string='Nama Ruangan', required=True)
    room_type = fields.Selection(
        selection=ROOM_TYPE,
        string='Tipe Ruangan',
        required=True
    )
    room_location = fields.Selection(
        selection=ROOM_LOCATION,
        string='Lokasi Ruangan',
        required=True
    )
    room_image = fields.Binary(string='Foto Ruangan', required=True)
    room_capacity = fields.Integer(string='Kapasitas Ruangan', required=True)
    description = fields.Char(string='Keterangan')

    @api.constrains('name')
    def _check_name(self):
        for rec in self:
            domain = [('name', '=', rec.name)]
            duplicated_name = self.search(domain)
            if duplicated_name:
                raise ValidationError("Room name already exists!") 