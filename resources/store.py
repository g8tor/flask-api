from flask_restful import Resource, reqparse
from models.store import StoreModel
from flask_jwt import jwt_required


class Store(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('name',
        type=str,
        required=True,
        help="This field is required")

    @jwt_required()
    def get(self, name):

        store = StoreModel.find_by_name(name)
        if store:
            return store.json(), 200

        return {'message': "Store not found"},404


    def post(self, name):

        if StoreModel.find_by_name(name):
            msg = "A store with the name '{}' already exists"
            return {'message': msg.format(name) }, 400 #Bad Request

        store = StoreModel(name)
        try:
            store.save_to_db()
        except:
            return {'message': 'An error occured inserting item'}, 500

        return store.json(), 201

    def delete(self, name):
        store = StoreModel.find_by_name(name)
        if store is None:
            msg = "No store named '{}' exist"
            return {'message': msg.format(name) }, 400 #Bad Request

        store.delete_from_db()
        return {'message': 'Store {} deleted'.format(store.name)}


class StoreList(Resource):

    def get(self):
        try:
            stores = [store.json() for store in StoreModel.query.all()]
            return {'stores': stores}, 200
        except Exception as e:
            raise(e)
            return {'message': "Error retrieving stores"}, 500
