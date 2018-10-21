import uuid
import mongoengine

from nosql.engine import Engine
from nosql.servicehistory import ServiceHistory

# allows load / save / query documents
# also maps id to _id ObjectId()


class Car(mongoengine.Document):
    # even though Mongo itself does not have types
    # types are enforced through mongoengine classes below

    # required being true at mongoengine level
    model = mongoengine.StringField(required=True)
    make = mongoengine.StringField(required=True)
    year = mongoengine.IntField(required=True)
    mileage = mongoengine.FloatField(default=0.0)
    # auto generate the VIN number
    # uuid4, creates a vin number, taking out the -, to make a long dummy
    vi_number = mongoengine.StringField(
        default=lambda: str(uuid.uuid4()).replace('-', ''))

    # what is the sub document? it is engine
    # can add (required=true as weel
    engine = mongoengine.EmbeddedDocumentField(Engine)

    # should the car be embedded in service history or vice versa?
    # do we want that embedded data with us most of the time?
    # so we almost always want service history associated with the car
    # means embed as an array in the car
    # is the set bounded and small?
    # it gets worked on only a little bit

    # it is not just a single document embedded, what kind of things
    # are in it? it is a list of service history

    service_history = mongoengine.EmbeddedDocumentListField(ServiceHistory)

    # special dict, mapping back to mongo_setup.py
    #  mongoengine.register_connection(alias='core', name='demo_dealership')
    # core mapped to below from setup, core being that you might want
    # multiple DBs covering core stuff, analytics stuff, etc
    # core is the connection info, cars is the name of the collection within
    # that DB
    meta = {
        'db_alias': 'core',
        'collection': 'cars',
    }
