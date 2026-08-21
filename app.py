from flask import Flask
from views import views
from database import db

app = Flask(__name__)
app.secret_key = 'This_key_will_save_session_of_user'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///project.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


@app.url_defaults
def supply_static_fallback(endpoint, values):
    """Keep catalogue pages usable when an older database row has no image path."""
    if endpoint == "static" and not values.get("filename"):
        values["filename"] = "background.png"

db.init_app(app)
app.register_blueprint(views)

if __name__ == "__main__":
    with app.app_context():
        db.create_all()

    app.run(host='0.0.0.0', port=3000, debug=True, use_reloader=True)
