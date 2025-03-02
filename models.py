from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timezone

db = SQLAlchemy()

class Member(db.Model):
    __tablename__ = "members"

    id = db.Column(db.Integer, primary_key=True, index=True)
    name = db.Column(db.String, index=True)
    surname = db.Column(db.String)
    booking_count = db.Column(db.Integer, default=0)
    date_joined = db.Column(db.DateTime, default=datetime.now(timezone.utc))

    bookings = db.relationship("Booking", back_populates="member")


class Inventory(db.Model):
    __tablename__ = "inventory"

    id = db.Column(db.Integer, primary_key=True, index=True)
    title = db.Column(db.String, index=True)
    description = db.Column(db.String)
    remaining_count = db.Column(db.Integer)
    expiration_date = db.Column(db.DateTime)

    bookings = db.relationship("Booking", back_populates="inventory")


class Booking(db.Model):
    __tablename__ = "bookings"

    id = db.Column(db.Integer, primary_key=True, index=True)
    member_id = db.Column(db.Integer, db.ForeignKey("members.id"))
    inventory_id = db.Column(db.Integer, db.ForeignKey("inventory.id"))
    booking_date = db.Column(db.DateTime, default=datetime.utcnow)

    member = db.relationship("Member", back_populates="bookings")
    inventory = db.relationship("Inventory", back_populates="bookings")
