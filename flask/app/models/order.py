from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy_utils import PhoneNumber
from app.models.user import User
from app import db

class Order(db.Model):
    """
    Order Flask-SQLAlchemy Model
    Represents objects contained in the orders table
    """

    __tablename__ = "orders"
  
    id = db.Column(db.Integer, primary_key=True)
    weight = db.Column(db.Float, nullable=False)
    sender_address = db.Column(db.String(240), nullable=False)
    sender_phone_number = db.Column(db.String(120), nullable=False)
    receiver_address = db.Column(db.String(240), nullable=False)
    receiver_email = db.Column(db.String(120), nullable=False)
    order_status = db.Column(db.String())
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'),
        nullable=False)
    user = db.relationship('User',
        backref=db.backref('orders', lazy=True))

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def __repr__(self):
        return (
            f"**Order** "
            f"id: {self.id} "
            f"weight: {self.weight} "
            f"sender_address: {self.sender_address}"
            f"sender_phone_number: {self.sender_phone_number}"
            f"receiver_address: {self.receiver_address}"
            f"receiver_email: {self.receiver_email}"
            f"order_status: {self.order_status}"
            f"**Order** "
        )

    @classmethod
    def find_by_id(cls, user_id, _id):
        user = User.find_by_id(user_id)
        return cls.query.filter_by(user_id = user.id, id = _id).first()
    
    @classmethod
    def find_all(cls, user_id):
        user = User.find_by_id(user_id)
        return cls.query.filter_by(user_id = user.id).all()
