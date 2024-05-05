import streamlit as st
import time

MAX_FLIGHTS = 10
MAX_NAME_LENGTH = 50
PASSPORT_ID_LENGTH = 10

flights = []
total_flights = 0

passengers = []
total_passengers = 0

def loading_animation():
    st.write("\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\t\t\t\t\t\t\t\t\t\tLoading")
    for _ in range(3):
        st.write(".")
        time.sleep(1)
    st.write("\n")

class Flight:
    def __init__(self, flight_number, origin, destination, available_seats):
        self.flight_number = flight_number
        self.origin = origin
        self.destination = destination
        self.available_seats = available_seats

class Passenger:
    def __init__(self, name, address, age, passport_id, flight_number):
        self.name = name
        self.address = address
        self.age = age
        self.passport_id = passport_id
        self.flight_number = flight_number

def add_flight(flight_number, origin, destination, available_seats):
    global total_flights
    if total_flights < MAX_FLIGHTS:
        flights.append(Flight(flight_number, origin, destination, available_seats))
        total_flights += 1
    else:
        st.write("Cannot add more flights. Maximum limit reached.")

def display_flights():
    st.write("Available Flights:")
    for flight in flights:
        st.write(f"Flight {flight.flight_number}: {flight.origin} to {flight.destination} - Available Seats: {flight.available_seats}")

def book_flight(name, address, age, passport_id, flight_number):
    global total_passengers
    for flight in flights:
        if flight.flight_number == flight_number:
            if flight.available_seats > 0:
                passengers.append(Passenger(name, address, age, passport_id, flight_number))
                flight.available_seats -= 1
                total_passengers += 1
                st.write("Flight booked successfully.")
                display_flights()
                return
            else:
                st.write("No available seats for this flight.")
                return
    st.write("Flight not found.")

def cancel_reservation(name, flight_number):
    global total_passengers
    for passenger in passengers:
        if passenger.name == name and passenger.flight_number == flight_number:
            passengers.remove(passenger)
            total_passengers -= 1
            st.write("Reservation cancelled successfully.")
            return
    st.write("Passenger not found or no reservation found for this flight.")

def display_booked_passengers():
    is_admin = st.radio("Are you an admin?", ("Yes", "No"))
    if is_admin == "Yes":
        username = st.text_input("Enter username:")
        password = st.text_input("Enter password:", type="password")
        if username == "Admin123" and password == "Admin321":
            st.write("\n\n\t\t\t\t                                         List of All Passengers:")
            st.write("\n\n\t\t\t\t     ====================================================================================================\n\n")
            for passenger in passengers:
                st.write(f"\t\t\t\t     |Passenger: {passenger.name}, Age: {passenger.age}, Address: {passenger.address}, Passport ID: {passenger.passport_id}, Flight Number: {passenger.flight_number}")
            st.write("\t\t\t\t     ====================================================================================================\n")
        else:
            st.write("Invalid username or password. Access denied.")
    elif is_admin == "No":
        for passenger in passengers:
            st.write(f"\t\t\t\t     |                         Passenger: {passenger.name}, Age: {passenger.age}, Flight Number: {passenger.flight_number}")

def main():
    loading_animation()

    add_flight(101, "Surigao City", "Davao City", 100)
    add_flight(102, "Surigao City", "Cebu City", 80)
    add_flight(103, "Surigao City", "Manila", 120)

    while True:
        choice = st.radio(
            "SURIGAO DEL NORTE STATE UNIVERSITY\nFLIGHT RESERVATION SYSTEM",
            ("Display Available Flights", "Book a Flight", "Cancel Reservation", "Display Booked Passengers", "Exit"),
            key="choice"  # Unique key for this radio widget
        )

        if choice == "Display Available Flights":
            display_flights()
        elif choice == "Book a Flight":
            display_flights()
            name = st.text_input("Enter your name:", key="name")  # Unique key for this text input widget
            address = st.text_input("Enter your address:", key="address")  # Unique key for this text input widget
            age = st.number_input("Enter your age:", key="age")  # Unique key for this number input widget
            passport_id = st.text_input("Enter your passport ID:", key="passport_id")  # Unique key for this text input widget
            flight_number = st.number_input("Enter the flight number:", key="flight_number")  # Unique key for this number input widget
            book_flight(name, address, age, passport_id, flight_number)
        elif choice == "Cancel Reservation":
            name = st.text_input("Enter your name:", key="cancel_name")  # Unique key for this text input widget
            flight_number = st.number_input("Enter the flight number of your reservation:", key="cancel_flight_number")  # Unique key for this number input widget
            cancel_reservation(name, flight_number)
        elif choice == "Display Booked Passengers":
            display_booked_passengers()
        elif choice == "Exit":
            st.write("Exiting...")
            break

if __name__ == "__main__":
    main()

