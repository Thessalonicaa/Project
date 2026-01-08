from database import Car
from datetime import datetime

__all__ = ['Car']

# Car model

class Car:
    """Car model"""
    
    def __init__(self, brand, model, year, price, description, license_plate, 
                 seller_username, business_name, images=None):
        self.brand = brand
        self.model = model
        self.year = year
        self.price = price
        self.description = description
        self.license_plate = license_plate
        self.seller_username = seller_username
        self.business_name = business_name
        self.images = images or []
        self.created_at = datetime.now()
    
    def to_dict(self):
        """Convert to dictionary"""
        return {
            'brand': self.brand,
            'model': self.model,
            'year': self.year,
            'price': self.price,
            'description': self.description,
            'license_plate': self.license_plate,
            'seller_username': self.seller_username,
            'business_name': self.business_name,
            'images': self.images,
            'created_at': self.created_at
        }
