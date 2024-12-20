# models.py

import pytz

from config import db, ma

class Trail(db.Model):
    __tablename__ = "Trails"
    __table_args__ = {'schema': 'CW2'}
    TrailID = db.Column(db.Integer, primary_key=True)
    TrailName = db.Column(db.String(32), unique=True)
    TrailSummary = db.Column(db.String(32))
    TrailDescription = db.Column(db.String(32))
    Difficulty = db.Column(db.String(32))
    Location = db.Column(db.String(32))
    Length = db.Column(db.Integer)
    ElevationGain = db.Column(db.Integer)
    RouteType = db.Column(db.String(32))
    OwnerID = db.Column(db.Integer)


class TrailSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Trail
        load_instance = True
        sql_session = db.session



trail_schema = TrailSchema()
trails_schema = TrailSchema(many=True)
