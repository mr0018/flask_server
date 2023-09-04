from app import db  # Import db from the app package


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.String(50),  nullable=False)
    last_name = db.Column(db.String(50),  nullable=False)
    email = db.Column(db.String(80), unique=True, nullable=False)
    phone = db.Column(db.String(20), nullable=True)
    password = db.Column(db.String(120), nullable=False)

    def to_json(self):
        return {
            'id': self.id,
            'full_name': f"{self.first_name} {self.last_name}",
            'first_name': self.first_name,
            'last_name': self.last_name,
            'email': self.email,
            'phone': self.phone,
            # 'password': self.password
        }
