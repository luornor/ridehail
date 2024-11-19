import random
from datetime import datetime
from threading import Thread
from time import sleep
from utilities.messaging import send_whatsapp_message


def start_ride_simulation(user, ride, session):
    """
    Simulates the progression of a ride with timed updates.
    """
    statuses = ["Driver on the way", "Driver arrived", "Trip started", "Trip completed"]
    time_intervals = [5, 5, 5]  # seconds between updates

    for index, status in enumerate(statuses[:-1]):
        sleep(time_intervals[index])
        ride.status = status
        session.commit()
        send_whatsapp_message(user.phone_number, f"Update: {status}")

    # Final status update and fare calculation
    ride.status = statuses[-1]
    ride.timestamp = datetime.now()
    ride.fare_estimate = f"${random.randint(10, 50)}"
    session.commit()
    send_whatsapp_message(
        user.phone_number,
        f"Your ride is completed. Fare: {ride.fare_estimate}. Thank you!",
    )


def process_user_command(session, user, command, request):
    """
    Process user commands based on their state and input.
    """
    if user.state == "awaiting_name":
        user.name = command.capitalize()
        user.state = "ready"
        session.commit()
        return f"Thank you, {user.name}. You can now book rides by typing 'book'."

    if command == "book":
        user.state = "awaiting_location"
        session.commit()
        return "Please share your current location to begin booking."

    if user.state == "awaiting_location":
        location = request.values.get('Latitude') + ',' + request.values.get('Longitude')
        ride = Ride(user_id=user.id, pickup_location=location, status="requested")
        session.add(ride)
        user.state = "ride_in_progress"
        session.commit()

        # Simulate driver assignment
        ride.driver_name = random.choice(["Alex", "Jordan", "Taylor"])
        ride.car_details = random.choice(["Toyota - ABC123", "Honda - XYZ789"])
        session.commit()

        # Start ride simulation in a new thread
        simulation_thread = Thread(target=start_ride_simulation, args=(user, ride, session))
        simulation_thread.start()

        return f"Ride confirmed! Driver {ride.driver_name} is on the way."

    return "Command not recognized. Please type 'help' for options."
