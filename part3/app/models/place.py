from app.extensions import db
from sqlalchemy import ForeignKey
from .baseclass import BaseModel

# Association table for many-to-many relationship between Place and Amenity
place_amenity = db.Table('place_amenity',
    db.Column('place_id', db.String(36), db.ForeignKey('places.id'), primary_key=True),
    db.Column('amenity_id', db.String(36), db.ForeignKey('amenities.id'), primary_key=True)
)

class Place(BaseModel):
    __tablename__ = 'places'

    title = db.Column(db.String(120), nullable=False)
    description = db.Column(db.String(500), nullable=True)
    price = db.Column(db.Float, nullable=False)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    owner_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)

    reviews = db.relationship('Review', backref='place', lazy=True)
    amenities = db.relationship('Amenity', secondary=place_amenity, lazy='subquery',
                               backref=db.backref('places', lazy=True))

    def __init__(self, title, price, latitude, longitude, owner_id,
                 description="", amenities=None, id=None):
        super().__init__(id=id)
        # Cast numeric values to correct types before validating
        try:
            price = float(price)
            latitude = float(latitude)
            longitude = float(longitude)
        except (ValueError, TypeError):
            raise ValueError("Price, latitude, and longitude must be numbers")

        if not title:
            raise ValueError("Title cannot be empty")
        if price <= 0:
            raise ValueError("Price must be a positive number")
        if not (-90 <= latitude <= 90):
            raise ValueError("Latitude must be between -90 and 90")
        if not (-180 <= longitude <= 180):
            raise ValueError("Longitude must be between -180 and 180")

        self.title = title
        self.description = description
        self.price = price
        self.latitude = latitude
        self.longitude = longitude
        self.owner_id = owner_id
        self.amenities = amenities or []

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "price": self.price,
            "latitude": self.latitude,
            "longitude": self.longitude,
            "owner_id": self.owner_id,
            "owner": self.owner.to_dict() if self.owner else None,
            "reviews": [review.to_dict() for review in self.reviews],
            "amenities": [amenity.to_dict() for amenity in self.amenities]
        }
