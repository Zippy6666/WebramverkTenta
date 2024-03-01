from flask_sqlalchemy import SQLAlchemy
from flask_security import SQLAlchemyUserDatastore, UserMixin, RoleMixin
import requests, json
from faker import Faker

db = SQLAlchemy()

# Definiera modeller för användare och roller
roles_users = db.Table('roles_users',
    db.Column('user_id', db.Integer(), db.ForeignKey('user.id')),
    db.Column('role_id', db.Integer(), db.ForeignKey('role.id'))
)

class Role(db.Model, RoleMixin):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    email_confirmed_at = db.Column(db.DateTime()) 
    password = db.Column(db.String(255))
    active = db.Column(db.Boolean())
    fs_uniquifier = db.Column(db.String(255), unique=True, nullable=False)  # Lägg till denna rad
    roles = db.relationship('Role', secondary=roles_users, backref=db.backref('user', lazy='dynamic'))

# Sätt upp Flask-Security
user_datastore = SQLAlchemyUserDatastore(db, User, Role)

    
class Product(db.Model):
    __tablename__= "Products"
    ProductID = db.Column(db.Integer, primary_key=True)
    ProductName = db.Column(db.String(100), unique=False, nullable=False)
    Color = db.Column(db.String(40), unique=False, nullable=False)
    Created = db.Column(db.DateTime, unique=False, nullable=False)
    LastBought = db.Column(db.DateTime, unique=False, nullable=True)
    ImageUrl = db.Column(db.String(100), unique=False, nullable=False)
    Rating = db.Column(db.Float, unique=False, nullable=False)
    RatingCount = db.Column(db.Integer, unique=False, nullable=False)
    CategoryName = db.Column(db.String(40), unique=False, nullable=False)
    Price = db.Column(db.Integer, unique=False, nullable=False)

def create_user():

    if not Role.query.first():
        user_datastore.create_role(name='Admin')
        user_datastore.create_role(name='User')
    db.session.commit()

    if not User.query.first():
        user_datastore.create_user(email='test@example.com', password='password', roles=['Admin','User'])
        user_datastore.create_user(email='c@c.com', password='password', roles=['User'])
        user_datastore.create_user(email='d@d.com', password='password', roles=['Admin'])
        db.session.commit()


def seedData():
    create_user()
    # jkdasjkdajkdas
    antal =  Product.query.count()


    if antal < 1:
        url = requests.get("https://fakestoreapi.com/products")
        text = url.text
        data = json.loads(text)
        
        fake = Faker()
        for prod in data:
            dat1 = fake.past_date("-365d")
            dat2 = fake.past_date("-365d")
            if dat1 > dat2:
                d = dat1
                dat1 = dat2
                dat2 = d
            product = Product()
            product.ProductName = prod['title']
            product.Color = fake.color_name()
            product.ImageUrl = prod['image']
            product.Price = prod['price']
            product.Created = dat1
            product.LastBought = dat2
            product.CategoryName = prod['category']
            product.Rating = prod['rating']['rate']
            product.RatingCount =prod['rating']['count']

            db.session.add(product)
        db.session.commit()        


    

