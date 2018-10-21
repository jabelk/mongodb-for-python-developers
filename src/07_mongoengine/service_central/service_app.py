# this is what starts the mongo, calling dir nosql to not name conflict
# for mongodb
import nosql.mongo_setup as mongo_setup
# now defining data models using mongoengine classes, class Car(mongoengine.Document)
from nosql.car import Car

# sub docs, embeded can only work thru parent, engine
# class Engine(mongoengine.EmbeddedDocument):
from nosql.engine import Engine
from nosql.servicehistory import ServiceHistory


def main():
    print_header()
    # config mongo just calls mongo_setup which calls the mongo db init
    config_mongo()
    # if need to update schema to old existing db entries having old schema
    # update_doc_versions()
    user_loop()


# only run once to fix, use mark as changed to force save
# example if an existing car did not have vin number
# sql would have had to do sql migration big deal

# noinspection PyProtectedMember
# def update_doc_versions():
#     for car in Car.objects():
#         car._mark_as_changed('vi_number')
#         car.save()


def print_header():
    print('----------------------------------------------')
    print('|                                             |')
    print('|           SERVICE CENTRAL v.02              |')
    print('|               demo edition                  |')
    print('|                                             |')
    print('----------------------------------------------')
    print()


def config_mongo():
    mongo_setup.global_init()


def user_loop():
    while True:
        print("Available actions:")
        print(" * [a]dd car")
        print(" * [l]ist cars")
        print(" * [p]oorly serviced")
        print(" * perform [s]ervice")
        print(" * e[x]it")
        print()
        ch = input("> ").strip().lower()
        if ch == 'a':
            add_car()
        elif ch == 'l':
            list_cars()
        elif ch == 's':
            service_car()
        elif ch == 'p':
            show_poorly_serviced_cars()
        elif not ch or ch == 'x':
            print("Goodbye")
            break


def add_car():
    model = input("What is the model? ")
    make = 'Ferrari'  # input("What is the make? ")
    year = int(input("Year built? "))

    # instantiate Car model from nosql.car.py
    # each attribute below has data constraints by the types given

    car = Car()
    car.year = year
    car.make = make
    car.model = model
    # video also has (early on)
    # car.mileage (float)l
    # car.vin

    # create subdocument list within the car class
    # dummy values
    engine = Engine()
    engine.horsepower = 590
    engine.mpg = 22
    engine.liters = 4.0

    # associate the engine to the car, embedding it

    car.engine = engine

    # save to the DB, since mongo does not have transactionsa
    car.save()


# queries against mongo


def list_cars():
    # could filter as well after .objects

    cars = Car.objects().order_by("-year")
    for car in cars:
        print("{} -- {} with vin {} (year {})".format(
            car.make, car.model, car.vi_number, car.year))
        print("{} of service records".format(len(car.service_history)))
        # since service history is a list since embedded on a car
        for s in car.service_history:
            print("  * ${:,.0f} {}".format(s.price, s.description))
    print()


def find_car():
    print("TODO: find_car")


def service_car():
    # vin = input("What is the VIN of the car to service? ")

    # this will grab a list of cars back, get the first one back,
    # get the car or none
    # instead also could have
    # could do objects(filter=

    # car = Car.objects(vi_number=vin).first()
    # if not car:
    #     print("Car with VIN {} not found!".format(vin))
    #     return
    #
    # service = ServiceHistory()
    # service.price = float(input("What is the price? "))
    # service.description = input("What type of service is this? ")
    # service.customer_rating = int(input("How happy is our customer? [1-5] "))
    #
    # car.service_history.append(service)
    # car.save()

    vin = input("What is the VIN of the car to service? ")
    service = ServiceHistory()
    service.price = float(input("What is the price? "))
    service.description = input("What type of service is this? ")
    service.customer_rating = int(input("How happy is our customer? [1-5] "))

    updated = Car.objects(vi_number=vin).update_one(push__service_history=service)
    if updated == 0:
        print("Car with VIN {} not found!".format(vin))
        return


def show_poorly_serviced_cars():
    level = int(input("What max level of satisfaction are we looking for? [1-5] "))
    # { "service_history.customer_rating": {$lte: level} }
    cars = Car.objects(service_history__customer_rating__lte=level)
    for car in cars:
        print("{} -- {} with vin {} (year {})".format(
            car.make, car.model, car.vi_number, car.year))
        print("{} of service records".format(len(car.service_history)))
        for s in car.service_history:
            print("  * Satisfaction: {} ${:,.0f} {}".format(
                s.customer_rating, s.price, s.description))
    print()


if __name__ == '__main__':
    main()
