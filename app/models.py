from app import db
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
class Favorite:
    def __init__(self):
        self.favorites_by_user = {}

    def add_favorite(self, user_id, location):
        if user_id not in self.favorites_by_user:
            self.favorites_by_user[user_id] = []
        if location not in self.favorites_by_user[user_id]:
            self.favorites_by_user[user_id].append(location)

    def get_favorites(self, user_id):
        return self.favorites_by_user.get(user_id, [])
    
favorites = Favorite()