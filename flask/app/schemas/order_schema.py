from flask_marshmallow import Marshmallow

ma = Marshmallow()

class OrderSchema(ma.Schema):
    """
    Order Marshmallow Schema
    Marshmallow schema used for loading/dumping Orders
    """
    class Meta:
        # Fields to expose
        fields = ('id', 'weight', 'sender_address', 'sender_phone_number', \
            'receiver_address', 'receiver_email', 'order_status')

    # Smart hyperlinking
    _links = ma.Hyperlinks(
        {
            "self": ma.URLFor("order_detail", values=dict(id="<id>")),
            "collection": ma.URLFor("orders"),
        }
    )
