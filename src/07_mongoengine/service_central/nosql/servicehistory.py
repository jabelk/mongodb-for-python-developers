import mongoengine
import datetime

# should the car be embedded in service history or vice versa?
# do we want that embedded data with us most of the time?
# so we almost always want service history associated with the car
# means embed as an array in the car
# is the set bounded and small?
# it gets worked on only a little bit



class ServiceHistory(mongoengine.EmbeddedDocument):
    # leaving off the datetime.now(), to make sure when called it will have time
    date = mongoengine.DateTimeField(default=datetime.datetime.now)
    description = mongoengine.StringField()
    price = mongoengine.FloatField()
    customer_rating = mongoengine.IntField(min_value=1, max_value=5)

