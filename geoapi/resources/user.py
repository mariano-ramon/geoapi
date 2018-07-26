from flask import request
from flask_restful import Resource
from marshmallow import ValidationError

from geoapi import api
from geoapi.db import mongo
from geoapi.db.schema import UserSchema

class User(Resource):

    def get(self, email):
        try:
            user = mongo.db.user.find_one({"email": email})
            if not user:
                raise ValidationError('no user with that email', fields=['email'])

        except ValidationError as e:
            return {'errors': e.messages}, 400

        return self.dump(user)

    def put(self):
        try:
            userdata = self.load(request)
            user = mongo.db.user.find_one({"email": userdata['email']})
            if not user:
                raise ValidationError('no user with that email', fields=['email'])

            mongo.db.user.update({"email": userdata['email']}, 
                                {"$set": self.dump(userdata)})

        except ValidationError as e:
            return {'errors': e.messages}, 400

        return self.dump(user)


    def post(self):
        try:
            userdata = self.load(request)
            if mongo.db.user.find_one({'email':userdata['email']}):
                raise ValidationError('mail already used', fields=['email'])

            user = mongo.db.user.insert_one(self.dump(userdata))


        except ValidationError as e:
            return {'errors': e.messages}, 400

        return self.dump(user)


    @staticmethod
    def load(request):
        User = UserSchema()
        userdata = request.json
        if 'name' in userdata and userdata['name'] == '':
            raise ValidationError('name cannot be empty')
        if 'last_name' in userdata and userdata['last_name'] == '':
            raise ValidationError('last name cannot be empty')
        return User.load(request.json)


    @staticmethod
    def dump(user):
        User = UserSchema()
        return User.dump(user)


class UserList(Resource):
    def get(self):
        return users


api.add_resource(User, '/user/<email>', '/user')
api.add_resource(UserList, '/users/')