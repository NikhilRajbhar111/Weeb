from flask import Flask

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'advadofhkodhca'

    from .routes import routes  # Change this line to import 'routes' instead of 'views'
    app.register_blueprint(routes, url_prefix='/')

    # Import and register the custom filter
    from .filters import clean_title
    app.jinja_env.filters['clean_title'] = clean_title

    return app
