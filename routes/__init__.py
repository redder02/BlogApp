from flask import Blueprint

auth_routes = Blueprint('auth', __name__)
post_routes = Blueprint('post', __name__)

from .auth import *
from .posts import *
