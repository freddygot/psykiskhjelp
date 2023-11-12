from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Psychologist(db.Model):
    __tablename__ = 'psychologist'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    address = db.Column(db.String(300))
    country = db.Column(db.String(50))
    language = db.Column(db.String(50))
    email = db.Column(db.String(120), unique=True)
    phone_number = db.Column(db.String(30), unique=True)
    profile_picture = db.Column(db.String(300))
    bio = db.Column(db.Text)
    gender_categories = db.Column(db.String(50))
    status = db.Column(db.String(50))

    def __repr__(self):
        return f'<Psychologist {self.name}>'
