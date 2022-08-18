from market import db, login_manager
from market import bcrypt
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(length=30), nullable=False, unique=True)
    email_address = db.Column(db.String(length=50), nullable=False, unique=True)
    password_hash = db.Column(db.String(length=60), nullable=False)
    items = db.relationship('Item', backref='owned_user', lazy=True)
    path=db.Column(db.String(length=60), nullable=False, unique=True)

    @property
    def get_username(self):
        return self.username
    @property
    def prettier_budget(self):
        if len(str(self.budget)) >= 4:
            return f'{str(self.budget)[:-3]},{str(self.budget)[-3:]}$'
        else:
            return f"{self.budget}$"

    @property
    def password(self):
        return self.password
 

    @password.setter
    def password(self, plain_text_password):
        self.password_hash = bcrypt.generate_password_hash(plain_text_password).decode('utf-8')

    def check_password_correction(self, attempted_password):
        return bcrypt.check_password_hash(self.password_hash, attempted_password)

class Item(db.Model):
    id = db.Column(db.Integer(), primary_key=True,nullable=True, autoincrement=True)
    title = db.Column(db.String(length=30), nullable=False, unique=False)
    link = db.Column(db.String(length=1024), nullable=False, unique=False)
    postedby = db.Column(db.String(length=1024), nullable=False, unique=False)
    salary = db.Column(db.Integer(), nullable=True, unique=False)
    owner = db.Column(db.Integer(), db.ForeignKey('user.id'),nullable=True)
    def __repr__(self):
        return f'Item {self.name}'


#         Posted By: ' : [],
# 'Job Title: ' : [],
# 'Salary: ' : [],
# 'Apply Here: ': [],
# 'Job Id: ': []
