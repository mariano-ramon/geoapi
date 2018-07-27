from marshmallow import Schema, ValidationError
from marshmallow.fields import Str, Decimal, DateTime, Email, Boolean, Nested, Float, String

from geoapi.db import mongo



def is_enabled(email):
    user = mongo.db.user.find_one({"email": email})

    if not user or 'enabled' not in user or not user['enabled']:
        raise ValidationError("User is disabled or doesn't exists")


class SaleSchema(Schema):
    _id = String()
    uuid = Str()
    user_email = Email(validate=is_enabled, required=True)
    amount = Float() #TODO change to Decimal(2)
    date = DateTime(format="%Y-%m-%d %H:%M")
    enabled = Boolean()

class UserSchema(Schema):
    email = Email(required=True)
    name = Str()
    last_name = Str()
    address = Str()
    enabled = Boolean()
    sales = Nested(SaleSchema, many=True)
    # class Meta:
    #     fields = ("email", "name", "last_name")

