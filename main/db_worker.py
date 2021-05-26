from flask_login import UserMixin

from main import db, manager


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    u_name = db.Column(db.String(32))
    u_surname = db.Column(db.String(32))
    u_phone = db.Column(db.String(32), nullable=False)
    u_password = db.Column(db.String(64), nullable=False)
    u_src = db.Column(db.String(128))
    u_city = db.Column(db.String(32))
    u_age = db.Column(db.Integer)
    u_about = db.Column(db.String(140))
    u_gender = db.Column(db.String(6))


class Photo(db.Model):
    photo_id = db.Column(db.Integer, primary_key=True)
    p_src = db.Column(db.String(128), nullable=False)
    p_user = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    u_user = db.relationship("User", backref=db.backref('photos', lazy=True))


class Message(db.Model):
    message_id = db.Column(db.Integer, primary_key=True)
    m_datetime = db.Column(db.String(48), nullable=False)
    m_to_user = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    u_to_user = db.relationship("User", foreign_keys=[m_to_user])
    m_from_user = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    u_from_user = db.relationship('User', foreign_keys=[m_from_user])
    m_text = db.Column(db.Text, nullable=False)


class Match(db.Model):
    match_id = db.Column(db.Integer, primary_key=True)
    mt_status = db.Column(db.Integer, nullable=False)
    mt_to_user = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    u_to_user = db.relationship("User", foreign_keys=[mt_to_user])
    mt_from_user = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    u_from_user = db.relationship('User', foreign_keys=[mt_from_user])


@manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)
