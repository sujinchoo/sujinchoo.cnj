from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Lead(db.Model):
    __tablename__ = "leads"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    company = db.Column(db.String(150))
    phone = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120))

    interest = db.Column(db.String(50), nullable=False)  # 1ton, 25_35_ton, cold, ev 등
    fleet_size = db.Column(db.String(50))
    message = db.Column(db.Text)

    source = db.Column(db.String(50), default="website")  # website / linkedin / etc
    status = db.Column(db.String(20), default="new")      # new / contacted / meeting / proposal / closed

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )

    def __repr__(self):
        return f"<Lead {self.id} {self.name}>"
