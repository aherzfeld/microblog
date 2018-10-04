from flask import Blueprint

# args = name of blueprint, name of base module
bp = Blueprint('errors', __name__)


from app.errors import handlers
