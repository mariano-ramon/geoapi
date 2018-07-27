import bson
from datetime import datetime
from decimal import Decimal
from json import dumps, loads
from uuid import uuid1

from flask import request, jsonify
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

            mongo.db.sale.update_one({"uuid": userdata['uuid']}, 
                                     {"$set": self.dump(userdata)})

        except ValidationError as e:
            return {'errors': e.messages}, 400

        return self.dump(userdata)


    def post(self):
        try:
            userdata = self.load(request)

            # REMOVE
            # userdata['uuid'] = uuid1()

            mongo.db.sale.insert_one(self.dump(userdata))
        except ValidationError as e:
            return {'errors': e.messages}, 400

        return self.dump(userdata)


    @staticmethod
    def load(request):
        Sale = SaleSchema()
        userdata = request.json
        return Sale.load(userdata)


    @staticmethod
    def dump(userdata):
        Sale = SaleSchema()
        return Sale.dump(userdata)


class UserSales(Resource):
    
    def get(self, email):
        sales = []
        try:
            data = mongo.db.sale.find({"user_email": email}, {"_id": 0})
            for sale in data:
                sales.append(sale)

        except ValidationError as e:
            return {'errors': e.messages}, 400

        return sales




api.add_resource(Sale, '/sale/<uuid>', '/sale')
api.add_resource(UserSales, '/usersales/<email>')    