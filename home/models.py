from home import db,login_manager
from itsdangerous import URLSafeTimedSerializer as Serializer
from  flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model,UserMixin):
    id=db.Column(db.Integer,primary_key=True)
    first_name=db.Column(db.String(20),nullable=False)
    last_name=db.Column(db.String(20),nullable=False)
    email=db.Column(db.String(120),unique=True,nullable=False)
    password=db.Column(db.String(60),nullable=False)

    def get_reset_token(self,expires_sec=1800):
        s=Serializer(app.config['SECRET_KEY'],expires_sec)
        return s.dumps({'user_id':self.id}).decode('utf-8')
    
    @staticmethod
    def verify_reset_token(token):
        s=Serializer(app.config['SECRET_KEY'])
        try:
            user_id=s.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)

    def __repr__(self):
        return f"User('{self.first_name}','{self.last_name}','{self.email}')"

class Product(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(20),nullable=False)
    cost=db.Column(db.Float,nullable=False)
    category=db.Column(db.String(20),nullable=False)
    brand=db.Column(db.String(20),nullable=False)
    retail_price=db.Column(db.Float,nullable=False)
    department=db.Column(db.String(20),nullable=False)
    sku=db.Column(db.String(20),nullable=False)
    distribution_center_id=db.Column(db.String(20),nullable=False)

    def __repr__(self):
        return f"Product('{self.name}','{self.cost}','{self.category}','{self.brand}')"
