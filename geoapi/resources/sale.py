from datetime import datetime
from json import dumps
from uuid import uuid1

from flask import request
from flask_restful import Resource
from marshmallow import ValidationError

from geoapi import api
from geoapi.db import mongo
from geoapi.db.schema import SaleSchema

class Sale(Resource):

    def get(self, uuid):
        try:
            sale = mongo.db.sale.find_one({"uuid": uuid})
            if not uuid:
                raise ValidationError('no sale with that id', fields=['uuid'])

        except ValidationError as e:
            return {'errors': e.messages}, 400

        return self.dump(sale)


    def put(self):
        try:
            userdata = self.load(request)
            sale = mongo.db.sale.find_one({"uuid": userdata['uuid']})
            if not sale:
                raise ValidationError('no sale with that id', fields=['uuid'])

            if ['amount','uuid','date'] in userdata:
                raise ValidationError('sales can only be enabled/disabled')

            mongo.db.sa;e.update_one({"uuid": userdata['uuid']}, 
                                     {"$set": self.dump(userdata)})

        except ValidationError as e:
            return {'errors': e.messages}, 400

        return self.dump(userdata)


    def post(self):
        try:
            userdata = self.load(request)

            if 'uuid' in userdata:
                raise ValidationError("uuid can't be manually set")

            userdata['uuid'] = uuid1()

            sale = mongo.db.sale.insert_one(self.dump(userdata))
        except ValidationError as e:
            return {'errors': e.messages}, 400

        return self.dump(sale)


    @staticmethod
    def load(request):
        Sale = SaleSchema()
        userdata = request.json
        if not 'amount' in userdata or userdata['amount'] == '':
            raise ValidationError('amount cannot be empty')
        if 'date' in userdata:
            raise ValidationError("date can't be manually set")


        return Sale.load(request.json)


    @staticmethod
    def dump(userdata):
        Sale = SaleSchema()
        return Sale.dump(userdata)


class UserSales(Resource):
    def get(self, todo_id):
        return 

    def put(self, todo_id):
        todos[todo_id] = request.form['data']
        return {todo_id: todos[todo_id]}


api.add_resource(Sale, '/sale/<uuid>', '/sale')
api.add_resource(UserSales, '/usersales/<email>')    