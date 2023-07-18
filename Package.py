# Package class for package objects.
class Package:
    def __init__(self, id, delivery_address, delivery_city, delivery_state, delivery_zip, delivery_deadline, weight,
                 special_notes, delivery_status, current_location):
        self.id = id
        self.delivery_address = delivery_address
        self.delivery_city = delivery_city
        self.delivery_state = delivery_state
        self.delivery_zip = delivery_zip
        self.delivery_deadline = delivery_deadline
        self.weight = weight
        self.special_notes = special_notes
        self.delivery_status = delivery_status
        self.current_location = current_location
        self.package_delivered_timestamp = None
        self.departure_timestamp = None

    # Overwriting this built in python method gives the ability to display a package's attributes. Normally if I
    # display a package the result would be something like - <Package.Package object at 0x0000025D10579700>
    def __str__(self):
        return "%s, %s, %s, %s, %s, %s, %s, %s" % (
            self.id, self.delivery_address, self.delivery_city, self.delivery_state, self.delivery_zip,
            self.delivery_deadline, self.weight, self.delivery_status)

    # Method prints only the necessary variables when needed for the user interface.
    def print_display_options(self):
        return "%s, %s, %s, %s, %s, %s" % (
            self.delivery_address, self.delivery_city, self.delivery_state, self.delivery_zip,
            self.delivery_deadline, self.weight)
