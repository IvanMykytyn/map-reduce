
from flask import Flask
from config import Config
from ManagementServer.constants import DATABASE_URI
from ManagementServer.models.db_config import db
from ManagementServer.routes.snippet_route import snippet_route
from ManagementServer.routes.file_route import file_route
# from ManagementServer.routes.auth_route import auth_route
from ManagementServer.routes.data_node_route import data_node_route


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URI
    db.init_app(app)

    app.register_blueprint(data_node_route, name='data_node_route', url_prefix='/data-node')
    app.register_blueprint(file_route, name='file_route', url_prefix='/file')
    app.register_blueprint(snippet_route, name='snippet_route', url_prefix='/snippet')

    return app


if __name__ == '__main__':
    management_app = create_app()
    management_app.run(port=5030, debug=True)

# python app.py --port 5001
