from flask_app.config.mysqlconnection import connectToMySQL
import re

DATABASE='blokx_schema'


EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9._-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
PASSWORD_REGEX = re.compile(r'^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9]).{8,}$')

class User:
    def __init__(self, data):
        self.id=data['id']
        self.first_name=data['first_name']
        self.last_name=data['last_name']
        self.email=data['email']
        self.password=data['password']
        self.created_at=data['created_at']
        self.updated_at=data['updated_at']


    # C
    @classmethod
    def create(cls, data:dict) -> int:
        query="INSERT INTO users (first_name, last_name, email, password) VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s);"
        return connectToMySQL(DATABASE).query_db(query, data)

    # R
    @classmethod
    def get_one(cls, data:dict) -> list:
        query="SELECT * FROM users WHERE id=%(id)s;"
        results = connectToMySQL(DATABASE).query_db(query, data)
        if results:
            return cls(results[0])
        return False
    
    @classmethod
    def get_user_by_email(cls, data:dict) -> list:
        query = "SELECT * FROM users WHERE email=%(email)s;"
        results = connectToMySQL(DATABASE).query_db(query, data)
        if len(results)<1:
            return False
        return cls(results[0])

    @classmethod
    def get_all(cls) -> list:
        query="SELECT * FROM users;"
        results = connectToMySQL(DATABASE).query_db(query)
        if results:
            all_users = []
            for user in results:
                all_users.append(cls(user))
            return all_users
        return False

    # U
    @classmethod
    def update_one(cls, data:dict) -> None:
        query="UPDATE users SET first_name=%(first_name)s, last_name=%(last_name)s, email=%(email)s, password=%(password)s WHERE id=%(id)s;"
        return connectToMySQL(DATABASE).query_db(query, data)
    
    @classmethod
    def update_user_password(cls, data:dict) -> None:
        query="UPDATE users SET password=%(password)s WHERE id=%(id)s;"
        return connectToMySQL(DATABASE).query_db(query, data)

    # D
    @classmethod
    def delete_one(cls, data:dict) -> None:
        query="DELETE FROM users WHERE id=%(id)s;"
        return connectToMySQL(DATABASE).query_db(query, data)

    
    # ***************Validations*****************

    @staticmethod
    def validate_registration(data):
        validation_results = {
            "is_valid" : True,
            "status" : 200
        }

        # Check First Name Field
        if not data['first_name'] or len(data['first_name']) < 2:
            validation_results["is_valid"] = False
            validation_results["status"] = 400
            if "errors" not in validation_results:
                validation_results["errors"] = {}
            validation_results["errors"]["firstName"] = "First name is required"
        
        # # Check Last Name Field
        if not data['last_name'] or len(data['last_name']) < 2:
            validation_results["is_valid"] = False
            validation_results["status"] = 400
            if "errors" not in validation_results:
                validation_results["errors"] = {}
            validation_results["errors"]["lastName"] = "Last name is required"
        
        # # Check Email Field
        if not data['email'] or not EMAIL_REGEX.match(data['email']):
            validation_results["is_valid"] = False
            validation_results["status"] = 400
            if "errors" not in validation_results:
                validation_results["errors"] = {}
            validation_results["errors"]["email"] = "Please enter a valid email"

        query="SELECT email from users;"
        results = connectToMySQL(DATABASE).query_db(query)
        if results:
            for email in results:
                if data['email'] == email['email']:
                    validation_results["is_valid"] = False
                    validation_results["status"] = 400
                    if "errors" not in validation_results:
                        validation_results["errors"] = {}
                    validation_results["errors"]["email"] = "Please enter a valid email"

        # # Check Password Field
        if not data['password']:
            validation_results["is_valid"] = False
            validation_results["status"] = 400
            if "errors" not in validation_results:
                validation_results["errors"] = {}
            validation_results["errors"]["password"] = "Password is required"
        
        elif not PASSWORD_REGEX.match(data['password']):
            validation_results["is_valid"] = False
            validation_results["status"] = 400
            if "errors" not in validation_results:
                validation_results["errors"] = {}
            validation_results["errors"]["password"] = "Password must be at least 8 letters, and must include at least one lowercase letter, one uppercase letter, and one number"

        # # Check Confirm Password Field
        if not data['confirm_password']:
            validation_results["is_valid"] = False
            validation_results["status"] = 400
            if "errors" not in validation_results:
                validation_results["errors"] = {}
            validation_results["errors"]["confirm_password"] = "Please retype password"

        elif data['password'] != data['confirm_password']:
            validation_results["is_valid"] = False
            validation_results["status"] = 400
            if "errors" not in validation_results:
                validation_results["errors"] = {}
            validation_results["errors"]["confirm_password"] = "Passwords do not match"

        return validation_results
    
    @staticmethod
    def validate_login(data):
        validation_results = {
            "is_valid" : True
        }

        # Check Email Field
        if not data['email']:
            validation_results["is_valid"] = False
            validation_results["status"] = 400
            if "errors" not in validation_results:
                validation_results["errors"] = {}
            validation_results["errors"]["email"] = "Please enter your email"

        elif not EMAIL_REGEX.match(data['email']):
            validation_results["is_valid"] = False
            validation_results["status"] = 400
            if "errors" not in validation_results:
                validation_results["errors"] = {}
            validation_results["errors"]["email"] = "Please enter a valid email"
        
        # Check if email is in database
        else:
            user_in_db = User.get_user_by_email(data)
            if not user_in_db:
                validation_results["is_valid"] = False
                validation_results["status"] = 400
                if "errors" not in validation_results:
                    validation_results["errors"] = {}
                validation_results["errors"]["confirm_password"] = "Please enter a valid email"
            

        # Check password Field
        if not data['password']:
            validation_results["is_valid"] = False
            validation_results["status"] = 400
            if "errors" not in validation_results:
                validation_results["errors"] = {}
            validation_results["errors"]["password"] = "Please eenter a valid password"


        return validation_results
    
    @staticmethod
    def validate_password_change(data):
        is_valid=True
        # Check Old Password Field
        if not data['old_password']:
            validation_results["is_valid"] = False
            validation_results["status"] = 400
            if "errors" not in validation_results:
                validation_results["errors"] = {}
            validation_results["errors"]["old_password"] = "Please type your current password"
        
        # Check New Password Field
        if not data['new_password']:
            validation_results["is_valid"] = False
            validation_results["status"] = 400
            if "errors" not in validation_results:
                validation_results["errors"] = {}
            validation_results["errors"]["new_password"] = "Please enter a new password"
        
        elif not PASSWORD_REGEX.match(data['new_password']):
            validation_results["is_valid"] = False
            validation_results["status"] = 400
            if "errors" not in validation_results:
                validation_results["errors"] = {}
            validation_results["errors"]["new_password"] = "Password must be at least 8 letters, and must include at least one lowercase letter, one uppercase letter, and one number"

        # Check Confirm Password Field
        if not data['password_confirm']:
            validation_results["is_valid"] = False
            validation_results["status"] = 400
            if "errors" not in validation_results:
                validation_results["errors"] = {}
            validation_results["errors"]["confirm_password"] = "Please retype password"

        elif data['new_password'] != data['password_confirm']:
            validation_results["is_valid"] = False
            validation_results["status"] = 400
            if "errors" not in validation_results:
                validation_results["errors"] = {}
            validation_results["errors"]["confirm_password"] = "Passwords do not match"
        
        return validation_results