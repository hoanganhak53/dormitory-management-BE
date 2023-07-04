from .user import user_data_routes
from .apartment import apartment_data_routes

def add_routes(routes, routers, tags):
    prefix = '/api/v1'
    for route in routes:
        routers.append({
            'router': route,
            'tags': tags,
            'prefix': prefix
        })

routers = []

add_routes(user_data_routes, routers, [])
add_routes(apartment_data_routes, routers, [])
