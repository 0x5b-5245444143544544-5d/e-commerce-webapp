from flask_login import UserMixin
import backend.database as database

db = database.Database().get()

class User(UserMixin):
    id = None
    email = "",
    password = ""
    is_seller = False
    is_active = False

    def get_user_by_id(self, user_id):
        result = db['user_info'].find_one(id=user_id)
        self.id = result['id']
        self.email = result['email']
        self.password = result['password']
        self.is_seller = bool(result['is_seller'])
        self.is_active = True
        return self
    
    def get_user_by_email(self, email):
        result = db['user_info'].find_one(email=email)
        if result:
            self.id = result['id']
            self.email = result['email']
            self.password = result['password']
            self.is_seller = bool(result['is_seller'])
            self.is_active = True
            return self
        
        return None

