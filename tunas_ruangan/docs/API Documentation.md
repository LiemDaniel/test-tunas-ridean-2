openapi: 3.0.0
info:
  title: Tunas Room Booking API
  description: API untuk mendapatkan status booking ruangan di Tunas
  version: 1.0.0
servers:
  - url: http://localhost:8017
    description: Server utama
paths:
  /api/tunas_room_book/state/{booking_id}:
    get:
      summary: Get booking state
      description: Mengambil informasi status booking berdasarkan ID
      parameters:
        - name: booking_id
          in: path
          required: true
          schema:
            type: integer
          description: ID booking kamar
      responses:
        "200":
          description: Sukses mengambil data booking
          content:
            application/json:
              schema:
                type: object
                properties:
                  status:
                    type: string
                    example: success
                  data:
                    type: object
                    properties:
                      state:
                        type: string
                        example: done
                      name:
                        type: string
                        example: "John Doe"
                      order_name:
                        type: string
                        example: "Test"
                      order_date:
                        type: string
                        format: date
                        example: "2024-02-06"
                      room_id:
                        type: integer
                        example: 10
                      room_name:
                        type: string
                        example: "Meeting Room A"
                      description:
                        type: string
                        example: "Booking untuk rapat tahunan"
        "400":
          description: Format booking ID tidak valid
          content:
            application/json:
              schema:
                type: object
                properties:
                  error:
                    type: string
                    example: "Invalid booking ID format"
        "404":
          description: Booking tidak ditemukan
          content:
            application/json:
              schema:
                type: object
                properties:
                  error:
                    type: string
                    example: "Booking not found"
        "500":
          description: Kesalahan server
          content:
            application/json:
              schema:
                type: object
                properties:
                  error:
                    type: string
                    example: "Internal Server Error"
