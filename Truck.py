# Truck class for truck objects.
class Truck:
    def __init__(self, id, packages, num_of_packages, depart_time, current_time, current_address, speed, mileage):
        self.id = id
        self.packages = packages
        self.num_of_packages = num_of_packages
        self.depart_time = depart_time
        self.current_time = current_time
        self.current_address = current_address
        self.speed = speed
        self.mileage = mileage

    # Overwriting this built in python method gives the ability to display a truck's attributes. Normally if I
    # display a truck the result would be something like - <Truck.Truck object at 0x000001564105B3D0>
    def __str__(self):
        return "%s, %s, %s, %s, %s, %s" % (
            self.packages, self.num_of_packages, self.depart_time, self.current_address, self.speed,
            self.mileage)

