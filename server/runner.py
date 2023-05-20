from app.create_flask_app import create_app, register_blueprints

FlaskApp = create_app()
register_blueprints(FlaskApp)
