from flask_restx import Namespace

from app.api.v1.users import api as users_ns
from app.api.v1.amenities import api as amenities_ns


def init_app(api):
    api.add_namespace(users_ns, path='/api/v1/users')
    api.add_namespace(amenities_ns, path='/api/v1/amenities')
