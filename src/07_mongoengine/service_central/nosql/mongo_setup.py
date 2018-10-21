import mongoengine


def global_init():
    # this is where would pass in creds and port and such
    # name= is the database db name

    # when we define our classes we will refer to the "core" connection
    # default localhost and port
    mongoengine.register_connection(alias='core', name='demo_dealership')
    # could have multiple like
    # mongoengine.register_connection(alias='analytics', name='anotherDBname')
