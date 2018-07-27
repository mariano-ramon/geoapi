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

            if any(x not in userdata for x in ['name','last_name']):
                raise ValidationError('both name and last name are required')

            user = mongo.db.user.insert_one(self.dump(userdata))


        except ValidationError as e:
            return {'errors': e.messages}, 400

        return self.dump(userdata)


    @staticmethod
    def load(request):
        User = UserSchema()
        data = request.json
        if 'name' in data and data['name'] == '':
            raise ValidationError('name cannot be empty')
        if 'last_name' in data and data['last_name'] == '':
            raise ValidationError('last name cannot be empty')
        return User.load(request.json)


    @staticmethod
    def dump(data):
        User = UserSchema()
        return User.dump(data)


class UserList(Resource):
    def get(self):
        users = []
        try:
            data = mongo.db.users.find({"_id": 0})
            for user in data:
                sales.append(user)

        except ValidationError as e:
            return {'errors': e.messages}, 400

        return users


api.add_resource(User, '/user/<email>', '/user')
api.add_resource(UserList, '/users')