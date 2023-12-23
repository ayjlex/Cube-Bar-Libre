from cocktails_site import db, bcrypt, login_manager
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(length=30), nullable=False, unique=True)
    password_hash = db.Column(db.String(length=60), nullable=False)
    cocktails = db.relationship('Cocktail', backref='user', lazy=True)

    @property
    def password(self):
        return self.password

    @password.setter
    def password(self, plain_password):
        self.password_hash = bcrypt.generate_password_hash(plain_password).decode('utf-8')

    def check_password(self, attempted_password):
        return bcrypt.check_password_hash(self.password_hash, attempted_password)


class Cocktail(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(length=30), nullable=False)
    description = db.Column(db.String(length=700), nullable=False)
    ingredients = db.relationship('Ingredient', backref='cocktail', lazy=True)
    is_user_cocktail = db.Column(db.Boolean, default=True)
    user_id = db.Column(db.Integer(), db.ForeignKey('user.id'))


class Ingredient(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(length=30), nullable=False)
    cocktail_id = db.Column(db.Integer(), db.ForeignKey('cocktail.id'))
