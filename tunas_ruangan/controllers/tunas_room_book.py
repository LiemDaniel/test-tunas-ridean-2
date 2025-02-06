from odoo import http
from odoo.http import request, Response
import json

class TunasRoomBookController(http.Controller):

    @http.route('/api/tunas_room_book/state/<int:booking_id>', type='http', auth='public', methods=['GET'], csrf=False)
    def get_booking_state(self, booking_id, **kwargs):
        try:
            # Validate booking_id is integer to prevent SQL injection
            if not isinstance(booking_id, int):
                return Response(
                    json.dumps({
                        'error': 'Invalid booking ID format'
                    }),
                    status=400,
                    content_type='application/json'
                )

            # Use ORM methods which are safe against SQL injection
            booking = request.env['tunas.room.book'].sudo().browse(int(booking_id))
            if not booking.exists():
                return Response(
                    json.dumps({
                        'error': 'Booking not found'
                    }),
                    status=404,
                    content_type='application/json'
                )

            data = {
                'state': booking.state,
                'name': booking.name,
                'order_name': booking.order_name,
                'order_date': booking.order_date.strftime('%Y-%m-%d') if booking.order_date else False,                
                'room_id': booking.room_id.id if booking.room_id else False,
                'room_name': booking.room_id.name if booking.room_id else False,
                'description': booking.description,
            }

            return Response(
                json.dumps({
                    'status': 'success',
                    'data': data
                }),
                status=200,
                content_type='application/json'
            )

        except Exception as e:
            return Response(
                json.dumps({
                    'error': str(e)
                }),
                status=500,
                content_type='application/json'
            )