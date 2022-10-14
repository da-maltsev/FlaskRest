from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from main import app

db = SQLAlchemy()
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///project.db"
db.init_app(app)
ma = Marshmallow(app)

class Advertise(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    description = db.Column(db.String)
    created_at = db.Column(db.Date)
    author = db.Column(db.String)

class AdvertiseSchema(ma.Schema):
    class Meta:
        fields = ("id", "title", "description", "created_at", "author")
        model = Advertise

advertise_schema = AdvertiseSchema()
advertise_schemas = AdvertiseSchema(many=True)