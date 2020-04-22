from app.core import core_bp


@core_bp.route('/')
def index():
    return 'Hello, world!!!'