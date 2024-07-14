# seed.py

from app import app, db
from models import Plant

with app.app_context():
    db.create_all()

    if not Plant.query.first():
        plants = [
            Plant(name='Aloe', image='./images/aloe.jpg', price=11.50, is_in_stock=True),
            Plant(name='Basil', image='./images/basil.jpg', price=5.99, is_in_stock=True),
            Plant(name='Cactus', image='./images/cactus.jpg', price=7.50, is_in_stock=True)
        ]
        db.session.add_all(plants)
        db.session.commit()
