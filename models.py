# models.py

import pytz
from marshmallow_sqlalchemy import fields

from config import db, ma

#Link Tables
class TrailFeatures(db.Model):
    __tablename__ = "TrailFeature"
    __table_args__ = {'schema': 'CW2'}

    TrailID = db.Column(db.Integer, db.ForeignKey('CW2.Trails.TrailID'), primary_key=True)
    FeatureID = db.Column(db.Integer, db.ForeignKey('CW2.Feature.FeatureID'), primary_key=True)


class TrailLocationPt(db.Model):
    __tablename__ = "TrailLocationPt"
    __table_args__ = {'schema': 'CW2'}

    TrailID = db.Column(db.Integer, db.ForeignKey('CW2.Trails.TrailID'), primary_key=True)
    LocationPointID = db.Column(db.Integer, db.ForeignKey('CW2.LocationPoint.LocationPointID'), primary_key=True)


#Main tables
class Feature(db.Model):
    __tablename__ = "Feature"
    __table_args__ = {'schema': 'CW2'}

    FeatureID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    TrailFeature = db.Column(db.String(32))

    trail = db.relationship(
        "Trail", 
        secondary="CW2.TrailFeature",
        cascade="all, save-update",
        single_parent=True,
        order_by="desc(Trail.TrailName)", 
        back_populates="features")


class LocationPoint(db.Model):
    __tablename__ = "LocationPoint"
    __table_args__ = {'schema': 'CW2'}

    LocationPointID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Latitude = db.Column(db.Integer)
    Longitude = db.Column(db.Integer)
    Description = db.Column(db.String(32))

    trail = db.relationship(
        "Trail", 
        secondary="CW2.TrailLocationPt",
        cascade="all, save-update",
        single_parent=True,
        order_by="desc(Trail.TrailName)", 
        back_populates="locationpoints")


class Trail(db.Model):
    __tablename__ = "Trails"
    __table_args__ = {'schema': 'CW2'}
    TrailID = db.Column(db.Integer, primary_key=True)
    TrailName = db.Column(db.String(32), unique=True)
    TrailSummary = db.Column(db.String)
    TrailDescription = db.Column(db.String)
    Difficulty = db.Column(db.String(32))
    Location = db.Column(db.String(32))
    Length = db.Column(db.Integer)
    ElevationGain = db.Column(db.Integer)
    RouteType = db.Column(db.String(32))
    OwnerID = db.Column(db.Integer, db.ForeignKey("CW2.Users.UserID"))

    owner = db.relationship(
        "User", 
        backref="Trails", 
    )


    features = db.relationship(
        "Feature",
        secondary="CW2.TrailFeature", 
        cascade="all, delete, delete-orphan",
        single_parent=True,
        order_by="desc(Feature.FeatureID)",
        back_populates="trail")

    locationpoints = db.relationship(
        "LocationPoint",
        secondary="CW2.TrailLocationPt", 
        cascade="all, delete, delete-orphan",
        single_parent=True,
        order_by="desc(LocationPoint.LocationPointID)",
        back_populates="trail")


class User(db.Model):
    __tablename__ = "Users"
    __table_args__ = {'schema': 'CW2'}

    UserID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Email_Address = db.Column(db.String(32))
    Role = db.Column(db.String(32))

    trails = db.relationship(
        "Trail", 
        backref="Users",
        cascade="all, delete, delete-orphan",
        single_parent=True,
        order_by="desc(Trail.TrailName)",
        )

#Schema
class FeatureSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Feature
        load_instance = True
        sql_session = db.session
        include_fk = True

class LocationPointSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = LocationPoint
        load_instance = True
        sql_session = db.session
        include_fk = True

class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User
        load_instance = True
        sql_session = db.session
        include_fk = True
    trails = fields.Nested('TrailSchema', many=True,  exclude=('owner',))


class TrailSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Trail
        load_instance = True
        sql_session = db.session
        include_relationship = True
        include_fk = True
    features = fields.Nested('FeatureSchema', many=True)
    locationpoints = fields.Nested('LocationPointSchema', many=True)
    owner = fields.Nested('UserSchema')


trail_schema = TrailSchema()
trails_schema = TrailSchema(many=True)

feature_schema = FeatureSchema()
locationpt_schema = LocationPointSchema()

users_schema = UserSchema(many=True)
user_schema = UserSchema()

