from flask_restful import Resource, reqparse
from app.schemas.order_schema import OrderSchema
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models.user import User
from app.models.order import Order

order_schema = OrderSchema()
orders_schema = OrderSchema(many=True)

class OrderResource(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('weight', 
        type =  float,
        required = True,
        help = "this field can't be left blank!"
    )
    parser.add_argument('sender_address', 
        type =  str,
        required = True,
        help = "this field can't be left blank!"
    )
    parser.add_argument('sender_phone_number', 
        type =  str,
        required = True,
        help = "this field can't be left blank!"
    )
    parser.add_argument('order_status', 
        type =  str,
        required = True,
        help = "this field can't be left blank!"
    )

    @jwt_required()
    def get(self, id=None):
        email = get_jwt_identity()
        user = User.find_by_email(email)
        if not id:
            orders = Order.find_all(user.id)
            return orders_schema.dump(orders)

        try:
            order = Order.find_by_id(user.id, id)
            return order_schema.dump(order)
        except:
            return {"message" : "Not found"}, 404

    @jwt_required()
    def post(self):
        email = get_jwt_identity()
        current_user = User.find_by_email(email)
        data = OrderResource.parser.parse_args()
        data['user_id'] = current_user.id
        data['receiver_address'] = current_user.address
        data['receiver_email'] = email
        order = Order(**data)

        try:
            order.save_to_db()
            
        except:
            return {'message' : "An error occurred while inserting an order"}, 500 
            
        return order_schema.dump(order), 201

    @jwt_required()
    def _get_all_orders(self):
        email = get_jwt_identity()
        user = User.find_by_email(email)
        orders = Order.find_all(user.id)

        if orders:
            return orders_schema.dump(orders)
        return {"message" : "Orders not found"}, 404
