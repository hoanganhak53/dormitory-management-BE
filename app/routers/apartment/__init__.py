from . import apartment, room_type, room, registration, student_room

apartment_data_routes = [
    apartment.route,
    room_type.route,
    room.route,
    registration.route,
    student_room.route
]