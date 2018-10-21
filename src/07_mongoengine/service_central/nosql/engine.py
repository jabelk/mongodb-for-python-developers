import uuid
import mongoengine

# sub docs, embeded can only work thru parent
class Engine(mongoengine.EmbeddedDocument):
    horsepower = mongoengine.IntField(required=True)
    liters = mongoengine.FloatField(required=True)
    mpg = mongoengine.FloatField(required=True)
    serial_number = mongoengine.StringField(
        # leaving dashes in to distinguish between dummy VIN #
        default=lambda: str(uuid.uuid4())
    )
