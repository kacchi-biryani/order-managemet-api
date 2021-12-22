from flask_marshmallow import Marshmallow

ma = Marshmallow()

class UserSchema(ma.Schema):
    """
    User Marshmallow Schema
    Marshmallow schema used for loading/dumping Users
    """
    class Meta:
        # Fields to expose
        fields = ('id', 'name', 'address' ,'email')

    # Smart hyperlinking
    _links = ma.Hyperlinks(
        {
            "self": ma.URLFor("user_detail", values=dict(id="<id>")),
            "collection": ma.URLFor("users"),
        }
    )
