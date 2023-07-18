# Diego Rodriguez | Student ID: 010097404

# Imports.
import time

from colorama import Fore
import datetime
import sys

import CSVReader
from MyHashMap import MyHashMap
from Package import Package
from Truck import Truck

# Truck speed will always be the same
TRUCK_SPEED = 18

# Locations for each CSV file.
address_file_location = 'Data/Address_File.csv'
distance_file_location = 'Data/Distance_File.csv'
package_file_location = 'Data/Package_File.csv'

# String address for main hub.
main_hub_address = '4001 South 700 East'

# Package #9 correct address. Will be updated at 10:20.
package9_correct_address = '410 S State St'

# HashMap
package_hash = MyHashMap()

# Reading in address distance, and package CSV files, then returning list.
address_file = CSVReader.read_csv_file_to_list(address_file_location)
distance_file = CSVReader.read_csv_file_to_list(distance_file_location)
package_file = CSVReader.read_csv_file_to_list(package_file_location)

# Creating a new package object for each package in CSV file.
# Then adding each new package into package HashMap.
# Space - O(N)       Time - O(N)
for index, package in enumerate(package_file):  # Looping through each line in package csv file.
    # Creating package attributes.
    id = package[0]
    delivery_address = package[1]
    delivery_city = package[2]
    delivery_state = package[3]
    delivery_zip = package[4]
    delivery_deadline = package[5]
    weight = package[6]
    special_notes = package[7]
    delivery_status = 'AT THE HUB'
    current_location = main_hub_address
    # Creating new package with data read from package CSV file.
    new_package = Package(id, delivery_address, delivery_city, delivery_state, delivery_zip, delivery_deadline, weight,
                          special_notes, delivery_status, current_location)
    # Inserting each new package into package HashMap. Setting index to match package ID.
    package_hash.insert(index + 1, new_package)

# 116.2 total miles loading the packages this way.
# Creating lists of packages that each truck will carry, aka manually loading them.
truck1_package_ids = [1, 2, 4, 5, 13, 14, 15, 16, 17, 19, 20, 29, 32, 31, 33, 40]
truck2_package_ids = [3, 6, 12, 18, 21, 22, 23, 24, 26, 27, 30, 35, 36, 38, 39]
truck3_package_ids = [7, 8, 9, 10, 11, 25, 28, 34, 37]

# Adding each package into each truck list of packages using each truck package id list.
truck1_packages = [package_hash.lookup(id) for id in truck1_package_ids]
truck2_packages = [package_hash.lookup(id) for id in truck2_package_ids]
truck3_packages = [package_hash.lookup(id) for id in truck3_package_ids]

# Creating 3 truck objects below, for each truck.
# Using the lists of packages previously created to manually load each truck with each list.
date_time_truck1 = datetime.datetime(2023, 5, 7, 8, 0, 0)
date_time_truck2 = datetime.datetime(2023, 5, 7, 9, 5, 0)

truck1 = Truck(1, truck1_packages, len(truck1_packages), date_time_truck1,
               date_time_truck1, main_hub_address, TRUCK_SPEED, 0)
truck2 = Truck(2, truck2_packages, len(truck2_packages), date_time_truck2,
               date_time_truck2, main_hub_address, TRUCK_SPEED, 0)
truck3 = Truck(3, truck3_packages, len(truck3_packages), None,
               None, main_hub_address, TRUCK_SPEED, 0)


# Returns the address index from Address_File.csv using an address.
# This will be used with other methods to get the distance between two addresses.
# Space - O(1)       Time - O(N)
def get_address_index(address):
    for a in address_file:  # Looping through each address in address CSV file.
        if address == a[2]:
            return int(a[0])  # Returning address index if address provided matches an address in file.


# Returns building name of address using address index.
# For example, giving method a street like '1060 Dalton Ave S' will return 'International Peace Gardens'.
# Space - O(1)       Time - O(N)
def get_address_name(add_street):
    for a in address_file:  # Looping through each address in address CSV file.
        if add_street == a[2]:
            return a[1]  # Returning name of building.


# Returns the distance from two address indexes using the Distance_File.csv.
def get_distance(add_index1, add_index2):
    distance = distance_file[add_index1][add_index2]  # Getting the distance from first index and second index.
    if distance == '':  # If distance is '' (blank) means we need to flip the row and col.
        distance = distance_file[add_index2][add_index1]
    return float(distance)  # Returning distance.


# Main function for the package delivery simulation that uses the greedy algorithm.
# Space - O(N^3)       Time - O(N^3)
def run_simulation(truck):
    # This makes sure truck 3 does not leave until truck 1 returns. Since truck 1 returns to main hub first.
    if truck.id == 3:
        truck.depart_time = truck1.current_time  # Setting truck 3 depart time to time when truck 1 returned back.
        truck.current_time = truck1.current_time  # Setting truck 3 current time to time when truck 1 returned back.

    packages = list(truck.packages)  # List of all packages in truck.
    addresses = []  # List of every address for each package.
    wrong_address_changed = False  # Variable becomes true once wrong address is changed at 10:20.

    # Space - O(N)       Time - O(N)
    for p in packages:  # Adding each package address into list of addresses.
        addresses.append(p.delivery_address)
        p.delivery_status = 'EN ROUTE'  # Setting delivery status to 'EN ROUTE', packages are now being delivered.
        p.departure_timestamp = truck.current_time.time()  # Package departure time is now trucks current time.

    # Stores total driving time for truck.
    total_driving_time = 0

    # Setting closest distance to first address in list to compare with.
    # Variable will be updated when a closer distance is found.
    closest_distance = get_distance(get_address_index(truck.current_address), get_address_index(addresses[0]))

    # Setting the next package to deliver to first package in list.
    # Variable will be updated when closest distance is found.
    next_package_to_deliver = packages[0]

    # Loop will run until list of addresses is empty.
    print(f"{Fore.BLUE}{truck.current_time.time()} -- Truck {truck.id} has now begun delivering packages")
    while len(addresses) > 0:
        # Using greedy algorithm to find the closest address to current truck location from list of address.
        # Space - O(N^2)         Time - O(N^2)
        for index, address in enumerate(addresses):  # Looping through each address in list of addresses.
            # If time is 10:20. Will change package #9 address which is in truck 3 to correct address.
            if truck.current_time.time() >= datetime.time(hour=10, minute=20, second=0) \
                    and not wrong_address_changed and truck.id == 3:
                # Space - O(N)       Time - O(N)
                # print(addresses)
                for p in packages:  # Looping through packages in truck 3.
                    if p.id == '9':  # Package #9.
                        p.delivery_address = package9_correct_address  # Setting package #9 to correct address.
                        addresses[1] = package9_correct_address  # Updating list of addresses with correct address.
                wrong_address_changed = True  # Wrong address has been changed.

            current_address = truck.current_address  # Current truck address.
            next_address = address  # First delivery address from list of addresses.

            # Getting address indexes of current address and next address. This will be used to calculate the distance.
            current_address_index = get_address_index(current_address)
            next_address_index = get_address_index(next_address)

            # Calculating distance between current truck address and next delivery address.
            current_distance = get_distance(current_address_index, next_address_index)

            # If distance for current package is less than or equal to current closest distance found.
            if current_distance <= closest_distance:
                closest_distance = current_distance  # Closest distance will now be set to that distance.
                # Next package to deliver will now be set to package that has the current delivery address.
                next_package_to_deliver = packages[index]
            else:  # Continues with loop if above condition is not met.
                continue

        # End of for loop. Setting distance to the closest distance found.
        current_distance = closest_distance

        # Package has been delivered. Updating truck status information.
        next_package_to_deliver.delivery_status = 'DELIVERED'

        # Calculating the total time it took to drive to each location and total time spent driving.
        driving_time = (current_distance / truck.speed) * 60
        total_driving_time += (current_distance / truck.speed) * 60

        # Getting timedelta variable of minutes spent driving to deliver current package.
        time_change = datetime.timedelta(minutes=driving_time)
        # Updating truck variables.
        truck.current_time += time_change  # Adding time spent driving for current package to current truck time.
        truck.current_address = next_package_to_deliver.delivery_address  # Setting new current address.
        truck.mileage += current_distance  # Adding distance spent driving for current package to total mileage.

        # Printing delivery information.
        current_address_name = get_address_name(next_package_to_deliver.delivery_address)
        print(f"{Fore.GREEN}{truck.current_time.time()} -- Package {next_package_to_deliver.id}, has been delivered to "
              f"'{current_address_name}'")

        # Setting the timestamp when the package has been delivered.
        next_package_to_deliver.package_delivered_timestamp = truck.current_time.time()

        # No longer need current package/address from each list.
        packages.remove(next_package_to_deliver)
        addresses.remove(next_package_to_deliver.delivery_address)
        time.sleep(0.05)

        # Resetting closest distance variable.
        if len(addresses) > 0:
            closest_distance = get_distance(get_address_index(truck.current_address), get_address_index(addresses[0]))

    # Calculating distance to main hub from current distance.
    final_distance_to_main_hub = get_distance(
        get_address_index(truck.current_address), get_address_index(main_hub_address))
    # Returning truck back to main hub.
    current_address_name = get_address_name(main_hub_address)
    print(f"Truck {truck.id} returning to '{current_address_name}'")

    # Adding distance back to main hub to total mileage, and setting new current address.
    truck.mileage += final_distance_to_main_hub
    truck.current_address = main_hub_address

    # Calculating final truck driving time variables.
    total_driving_time += (final_distance_to_main_hub / truck.speed) * 60
    driving_time = (final_distance_to_main_hub / truck.speed) * 60
    # Updating truck current time to time when back at main hub.
    time_change = datetime.timedelta(minutes=driving_time)
    truck.current_time += time_change

    # Truck has returned back to main hub.
    print(f"{Fore.BLUE}{truck.current_time.time()} -- Truck {truck.id} has returned to '{current_address_name}'")
    print()

    # Rounding mileage number.
    truck.mileage = round(truck.mileage, 2)


# Method is used to print out metrics for each truck.
def print_truck_metrics(truck):
    # Getting necessary truck time/miles information.
    truck_drive_time = round((truck.mileage / truck.speed), 2)  # Total drive time in hours.
    truck_miles_driven = round(truck.mileage, 2)  # Total miles driven.
    truck_return_time = truck.current_time.time()  # Truck return time.

    # Printing out truck metrics.
    print()
    print(f"{Fore.MAGENTA}Truck {truck.id} metrics:")
    print(f"{Fore.LIGHTWHITE_EX}-----------------------------------")
    print(f"{Fore.YELLOW}Departure Time: {truck.depart_time.time()}")
    print(f"Return Time: {truck_return_time}")
    print(f"Drive Time: {truck_drive_time} hours")
    print(f"Total Distance: {truck_miles_driven} miles")
    time.sleep(0.1)


# Method is used to display program options.
# User is able to view package status and information.
def display_program_options():
    # Loop will run until user decides to quit.
    while True:
        # Printing out program options.
        print()
        print()
        print(f"{Fore.CYAN}Program Options:")
        print(f"{Fore.LIGHTWHITE_EX}Select '1' to View status report of a specific package at a specified time")
        print("Select '2' to Check delivery status of all packages at a specified time")
        print("Select '3' to View total mileage by trucks")
        print("Select 'q' to End Program")
        try:  # If user selects one of the following options.
            user_input = input("Enter your option -- ").lower()
            if user_input == '1':  # Printing out status report of package at a specified time.
                try:
                    # Getting package ID.
                    package_id_to_check = input("Please enter a package ID -- ")
                    # Getting time to check status of package and converting it to appropriate form.
                    time_to_check = input("Please enter a time (in military format HH:MM) -- ")
                    (h, m) = time_to_check.split(":")
                    converted_time_to_check = datetime.time(int(h), int(m))
                    # Getting package using package ID.
                    package_to_check = package_hash.lookup(int(package_id_to_check))
                    # Getting delivery status for package.
                    if converted_time_to_check < package_to_check.departure_timestamp:
                        print(f"{Fore.RED}{package_to_check.id}, AT THE HUB, {package_to_check.print_display_options()}")
                    elif package_to_check.departure_timestamp <= converted_time_to_check < package_to_check.package_delivered_timestamp:
                        print(f"{Fore.YELLOW}{package_to_check.id}, EN ROUTE, {package_to_check.print_display_options()}")
                    else:
                        print(f"{Fore.GREEN}{package_to_check.id}, DELIVERED "
                              f"({package_to_check.package_delivered_timestamp}), {package_to_check.print_display_options()}")
                except (TypeError, ValueError, None):  # User entered a wrong id/time.
                    print("You entered a wrong Package ID/Time. Please start over and select a program option")
            elif user_input == '2':  # Printing out status reports of all package at a specified time.
                try:
                    # Getting time to check status of package and converting it to appropriate form.
                    time_to_check = input("Please enter a time (in military format HH:MM) -- ")
                    (h, m) = time_to_check.split(":")
                    converted_time_to_check = datetime.time(int(h), int(m))
                    # Looping through every package id.
                    for package_id in range(1, 41):
                        # Getting package.
                        package_to_check = package_hash.lookup(package_id)
                        # Getting delivery status for package.
                        if converted_time_to_check < package_to_check.departure_timestamp:
                            print(f"{Fore.RED}{package_id}, AT THE HUB, {package_to_check.print_display_options()} ")
                        elif package_to_check.departure_timestamp <= converted_time_to_check < package_to_check.package_delivered_timestamp:
                            print(f"{Fore.YELLOW}{package_id}, EN ROUTE, {package_to_check.print_display_options()}")
                        else:
                            print(f"{Fore.GREEN}{package_id}, DELIVERED "
                                  f"({package_to_check.package_delivered_timestamp}), {package_to_check.print_display_options()}")
                except (TypeError, ValueError):  # User entered a wrong time.
                    print("You entered a wrong Time. Please start over and select a program option")
            elif user_input == '3':  # Printing out metrics for each truck (mileage, time).
                # Getting truck mileage/time information.
                total_mileage = round(truck1.mileage + truck2.mileage + truck3.mileage, 2)
                total_time = (total_mileage / 18) * 60
                total_time_hours = round((total_mileage / 18))
                total_time_minutes = round(total_time % 60)
                # Printing truck metrics.
                print_truck_metrics(truck1)
                print_truck_metrics(truck2)
                print_truck_metrics(truck3)
                print()
                print(
                    f"{Fore.RED}Combined mileage for all trucks (including returning back to Main Hub): {total_mileage} miles")
                print(
                    f"Total time driven for all trucks (including returning back to Main Hub): ({total_time_hours}) "
                    f"hours & ({total_time_minutes}) minutes")
            elif user_input == 'q':  # User decides to quit program.
                print('Good bye!')
                # Exiting program.
                sys.exit()
            else:
                raise TypeError  # Raises this error when user enters a wrong option.
        except (TypeError, ValueError):  # Type Error if user entered a wrong option.
            print('Please enter a correct option.')
            print()


# Main class handles the user input and execution of program.
class Main:
    # Printing program startup text.
    print(f"{Fore.CYAN}Welcome to DSA II Package Delivery Simulation!")
    print(f"{Fore.LIGHTWHITE_EX}Select 'd' to Begin Delivery Simulation.")
    print("Select 'q' to Quit Program.")
    # Loop will run until user decides to quit.
    while True:
        try:  # Getting user input.
            user_input = (input("Enter your option -- ")).lower()
            if user_input == 'd':  # Beginning package delivery information.
                print(f"{Fore.CYAN}Beginning simulation...")
                # Calling simulation method for each truck.
                run_simulation(truck1)
                run_simulation(truck2)
                run_simulation(truck3)
                print(f"{Fore.CYAN}Delivery complete for all trucks!")
                # Displaying program options after simulation is complete.
                display_program_options()
                break
            elif user_input == 'q':  # User decided to quit program.
                print('Good bye!')
                break
            else:
                raise TypeError  # Raises this error when user enters a wrong option.
        except TypeError:  # Type Error if user entered a wrong option.
            print('Please enter a correct option.')
            print()
