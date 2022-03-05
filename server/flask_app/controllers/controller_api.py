from flask_app import app
from flask import request, jsonify
from flask_bcrypt import Bcrypt
from flask_cors import CORS
from flask_jwt_extended import create_access_token, jwt_required, JWTManager, get_jwt_identity, set_access_cookies, unset_jwt_cookies, current_user

from flask_app.models.model_user import User

app.config['JWT_TOKEN_LOCATION'] = ['cookies']
app.config["JWT_SECRET_KEY"] = "keep it secret. keep it safe."
jwt = JWTManager(app)
CORS(app, supports_credentials=True)

bcrypt = Bcrypt(app)

# ------------------------------------------------------------
# -------------------AUTHENTICATION ROUTES--------------------
# ------------------------------------------------------------

# -------------------------REGISTER---------------------------
@app.route('/api/createUser', methods=['POST'])
def users_register():
    content = request.get_json()
    # print(content)
    validation_results = User.validate_registration(content)
    if not validation_results['is_valid']:
        response = jsonify(validation_results)
        return response

    password_hash = bcrypt.generate_password_hash(content['password'])
    data = {
        **content,
        "password": password_hash
    }
    new_user = User.create(data)
    
    access_token = create_access_token(identity=new_user)
    response = jsonify(validation_results)
    response.headers.add('Access-Control-Allow-Origin', 'http://localhost:3000')
    response.headers.add('Access-Control-Allow-Credentials', 'true')
    set_access_cookies(response, access_token)

    return response, 200


# ------------------------LOGIN----------------------------
@app.route('/api/users/login', methods=['POST'])
def users_login():
    content = request.get_json()
    validation_results = User.validate_login(content)

    if not validation_results['is_valid']:
        return validation_results
    
    user_in_db = User.get_user_by_email(content)

    if not user_in_db:
        validation_results["status"] = 400
        if "errors" not in validation_results:
            validation_results["errors"] = {}
        validation_results["errors"]["login"] = "Invalid Email/Password"

        return validation_results
    
    if not bcrypt.check_password_hash(user_in_db.password, content['password']):
        validation_results["status"] = 400
        if "errors" not in validation_results:
            validation_results["errors"] = {}
        validation_results["errors"]["login"] = "Invalid Email/Password"
        return validation_results

    validation_results['user'] = {}
    validation_results['user']['id'] = user_in_db.id
    validation_results['user']['first_name'] = user_in_db.first_name
    validation_results['user']['last_name'] = user_in_db.last_name

    access_token = create_access_token(identity=user_in_db.id)
    response = jsonify(validation_results)
    response.headers.add('Access-Control-Allow-Origin', 'http://localhost:3000')
    response.headers.add('Access-Control-Allow-Credentials', 'true')
    set_access_cookies(response, access_token)

    return response, 200


# -----------------------LOGOUT--------------------------
@app.route("/api/logout")
def logout():
    response = jsonify({'logout': True})
    unset_jwt_cookies(response)
    return response, 200