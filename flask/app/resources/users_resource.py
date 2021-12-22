from flask_restful import Resource, reqparse
from flask_jwt_extended import (create_access_token, create_refresh_token, jwt_required, get_jwt_identity, get_jwt)
from app.models.user import User, UserSchema

user_schema = UserSchema()
users_schema = UserSchema(many=True)

class UserRegistration(Resource):
    """
    UserRegistration POST method to register Users
    :return: access_token and refresh_token, 201 HTTP status code
    """
    parser = reqparse.RequestParser()
    parser.add_argument('name', 
        type =  str,
        required = True,
        help = "this field can't be left blank!"
    )
    parser.add_argument('address', 
        type =  str,
        required = True,
        help = "this field can't be left blank!"
    )
    parser.add_argument('email', 
        type =  str,
        required = True,
        help = "this field can't be left blank!"
    )
    parser.add_argument('password', 
        type =  str,
        required = True,
        help = "this field can't be left blank!"
    )

    def post(self):
        data = UserRegistration.parser.parse_args()
        if User.find_by_email(data['email']):
            return {"message": "User with this email address already exist"}, 400

        user = User()
        user.name = data['name']
        user.address = data['address']
        user.email = data['email']
        user.set_password(data['password'])

        try:
            user.save_to_db()
            access_token = create_access_token(identity = data['email'])
            refresh_token = create_refresh_token(identity = data['email'])
            return {
                'message': 'User {} was created successfully'.format(data['email']),
                'access_token': access_token,
                'refresh_token': refresh_token
                }, 201
        except:
            return {'message': 'Something went wrong'}, 500

class UserLogin(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('email', 
        type =  str,
        required = True,
        help = "this field can't be left blank!"
    )
    parser.add_argument('password', 
        type =  str,
        required = True,
        help = "this field can't be left blank!"
    )
    def post(self):
        """
        UserLogin POST method to authenticate Users
        :return: access_token and refresh_token, 200 HTTP status code
        """
        data = UserLogin.parser.parse_args()
        user = User.find_by_email(data['email'])

        if not user:
            return {'message': 'User {} doesn\'t exist'.format(data['email'])}
        
        if user.check_password(data['password']):
            access_token = create_access_token(identity = data['email'])
            refresh_token = create_refresh_token(identity = data['email'])
            return {
                'message': 'Logged in as {}'.format(user.email),
                'access_token': access_token,
                'refresh_token': refresh_token
                }
        else:
            return {'message': 'Wrong credentials'}, 403

class UsersResource(Resource):
    @jwt_required()
    def get(self):
        """
        UsersResource GET method. Retrieves one user and requires a valid access_token
        :return: User, 200 HTTP status code
        """
        email = get_jwt_identity()
        user = User.find_by_email(email)
        print(user)
        if user:
            return user_schema.dump(user)
        return {"message" : "user not found"}, 404
