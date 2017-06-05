from flask_restful import Resource, reqparse
from flask_jwt import jwt_required

from models.item import ItemModel

class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price',
        type=float,
        required=True,
        help="This field is required")
    parser.add_argument('store_id',
        type=int,
        required=True,
        help="Every item needs a store_id")

    @jwt_required()
    def get(self, name):

        item = ItemModel.find_by_name(name)
        if item:
            return item.json(), 200

        return {'message': "No item by that name exists"},404


    def post(self, name):

        if ItemModel.find_by_name(name):
            msg = "An item with name '{}' already exists".format(name)
            return {'message': msg }, 400 #Bad Request

        data = Item.parser.parse_args()
        item = ItemModel(name, data.get('price'), data.get('store_id'))
        try:
            item.save_to_db()
        except:
            return {'message': 'An error occured inserting item'}, 500

        return item.json(), 201

    def delete(self, name):
        item = ItemModel.find_by_name(name)
        if item is None:
            msg = "An item with name '{}' does not exist".format(name)
            return {'message': msg }, 400 #Bad Request

        item.delete_from_db()
        return {'message': 'Item {} deleted'.format(item.name)}

    def put(self, name):

        data = Item.parser.parse_args()

        item = ItemModel.find_by_name(name)
        if item is None:
            item = ItemModel(name, **data)
        else:
            item.price = data.get('price')
            item.store_id = data.get('store_id')
        try:
            item.save_to_db()
        except:
            action = "inserting" if item is None else "updating"
            return {'message': 'An error occured {} item'.format(action)}, 500

        return item.json()


class ItemList(Resource):

    def get(self):
        try:
            items = [item.json() for item in ItemModel.query.all()]
            return {'items': items}, 200
        except Exception as e:
            raise(e)
            return {'message': "Error retrieving items"}, 500
