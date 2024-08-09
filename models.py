from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Campaign(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    links = db.relationship('Link', backref='campaign', lazy=True)

class Link(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    campaign_id = db.Column(db.Integer, db.ForeignKey('campaign.id'), nullable=False)
    url = db.Column(db.String(200), nullable=False)

class Click(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    link_id = db.Column(db.Integer, db.ForeignKey('link.id'), nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False)
    ip_address = db.Column(db.String(45), nullable=False)
    link = db.relationship('Link', backref=db.backref('clicks', lazy=True))

class Conversion(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    click_id = db.Column(db.Integer, db.ForeignKey('click.id'), nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False)
    revenue = db.Column(db.Float, nullable=False)
    click = db.relationship('Click', backref=db.backref('conversions', lazy=True))
