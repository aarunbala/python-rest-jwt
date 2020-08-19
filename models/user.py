from db import db

class UserModel(db.Model):
    """class to maintain User data"""
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80))
    password = db.Column(db.String(80))
    user_role = db.Column(db.String(10))

    def __init__(self, username, password, user_role):
        self.username = username
        self.password = password
        self.user_role = user_role

    def json(self):
        return {
            'id': self.id,
            'username': self.username,
            'user_role': self.user_role
            }

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def find_by_username(cls, username):
        return cls.query.filter_by(username=username).first()

    @classmethod
    def find_by_userid(cls, userid):
        return cls.query.filter_by(id=userid).first()

    @classmethod
    def find_by_userrole(cls, user_role):
        return cls.query.filter_by(user_role-user_role)

    @classmethod
    def find_all(cls):
        return cls.query.all()
