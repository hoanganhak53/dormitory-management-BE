from .health import ping
from .clustering import clustering_routes
from .cluster_history import cluster_history_routes
from .thesis_data import thesis_data_routes
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

routers.append({
    'router': ping.router,
    'prefix': '/api/v1',
})

add_routes(clustering_routes, routers, [])
add_routes(cluster_history_routes, routers, [])
add_routes(thesis_data_routes, routers, [])
add_routes(user_data_routes, routers, [])
add_routes(apartment_data_routes, routers, [])
