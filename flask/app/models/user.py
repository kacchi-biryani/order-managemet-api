from app import db
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model):
    """
    User Flask-SQLAlchemy Model
    Represents objects contained in the users table
    """

    __tablename__ = "users"
  
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    address = db.Column(db.String(240), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def __repr__(self):
        return (
            f"**User** "
            f"id: {self.id} "
            f"name: {self.name} "
            f"address: {self.address}"
            f"email: {self.email}"
            f"**User** "
        )

    @classmethod
    def find_by_email(cls, email):
        return cls.query.filter_by(email = email).first()

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(id = _id).first()
