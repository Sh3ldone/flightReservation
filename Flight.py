import streamlit as st
import time

MAX_FLIGHTS = 10
MAX_NAME_LENGTH = 50
PASSPORT_ID_LENGTH = 10

flights = []
total_flights = 0

passengers = []
total_passengers = 0

class Flight:
    def __init__(self, flightNumber, origin, destination, availableSeats):
        self.flightNumber = flightNumber
        self.origin = origin
        self.destination = destination
        self.availableSeats = availableSeats

class Passenger:
    def __init__(self, name, address, age, passportID, flightNumber):
        self.name = name
        self.address = address
        self.age = age
        self.passportID = passportID
        self.flightNumber = flightNumber

def loadingAnimation():
    st.write("\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\t\t\t\t\t\t\t\t\t\tLoading", end="")
    for _ in range(3):
        st.write(".", end="", flush=True)
        time.sleep(1)
    st.write("\n")

def addFlight(flightNumber, origin, destination, availableSeats):
    global total_flights
    if total_flights < MAX_FLIGHTS:
        flight = Flight(flightNumber, origin, destination, availableSeats)
        flights.append(flight)
        total_flights += 1
    else:
        st.write("Cannot add more flights. Maximum limit reached.")

def displayFlights():
    st.write("Available Flights:")
    for flight in flights:
        st.write(f"Flight {flight.flightNumber}: {flight.origin} to {flight.destination} - Available Seats: {flight.availableSeats}")
    st.write()

def bookFlight():
    name = st.text_input("Enter your name:")
    address = st.text_input("Enter your address:")
    age = st.number_input("Enter your age:", min_value=0, max_value=150, step=1)
    passportID = st.text_input("Enter your passport ID:")
    flightNumber = st.number_input("Enter the flight number:", min_value=1, max_value=MAX_FLIGHTS, step=1)

    if st.button("Book Flight"):
        global total_passengers
        for flight in flights:
            if flight.flightNumber == flightNumber:
                if flight.availableSeats > 0:
                    if len(passportID) != 9:
                        st.write("Invalid passport ID number.")
                        return
                    passenger = Passenger(name, address, age, passportID, flightNumber)
                    passengers.append(passenger)
                    flight.availableSeats -= 1
                    total_passengers += 1
                    st.write("Flight booked successfully.\n")
                    displayFlights()
                    return
                else:
                    st.write("No available seats for this flight.\n")
                    return
        st.write("Flight not found.\n")

def cancelReservation():
    name = st.text_input("Enter your name:")
    flightNumber = st.number_input("Enter the flight number of your reservation:", min_value=1, max_value=MAX_FLIGHTS, step=1)

    if st.button("Cancel Reservation"):
        global total_passengers
        for passenger in passengers:
            if passenger.name == name and passenger.flightNumber == flightNumber:
                passengers.remove(passenger)
                total_passengers -= 1
                st.write("Reservation cancelled successfully.\n")
                return
        st.write("Passenger not found or no reservation found for this flight.\n")

def displayBookedPassengers():
    st.write("\t\t\t\t                                         List of Booked Passengers:")
    isAdmin = st.radio("Are you an admin?", ("Yes", "No"))
    if isAdmin == "Yes":
        username = st.text_input("Enter username:")
        password = st.text_input("Enter password:", type="password")
        if username == "Admin123" and password == "Admin321":
            st.write("\n\n\t\t\t\t                                         List of All Passengers:")
            st.write("\n\n\t\t\t\t     ====================================================================================================\n\n")
            for passenger in passengers:
                st.write(f"\t\t\t\t     |Passenger: {passenger.name}, Age: {passenger.age}, Address: {passenger.address}, Passport ID: {passenger.passportID}, Flight Number: {passenger.flightNumber}")
            st.write("\t\t\t\t     ====================================================================================================\n")
            st.write()
        else:
            st.write("Invalid username or password. Access denied.")
    elif isAdmin == "No":
        for passenger in passengers:
            st.write(f"\t\t\t\t     |                         Passenger: {passenger.name}, Age: {passenger.age}, Flight Number: {passenger.flightNumber}")
    else:
        st.write("Invalid input.")

def main():
    loadingAnimation()

    addFlight(101, "Surigao City", "Davao City", 100)
    addFlight(102, "Surigao City", "Cebu City", 80)
    addFlight(103, "Surigao City", "Manila", 120)

    st.title("Flight Reservation System")
    menu = st.sidebar.selectbox("Menu", ["Display Available Flights", "Book a Flight", "Cancel Reservation", "Display Booked Passengers"])

    if menu == "Display Available Flights":
        displayFlights()
    elif menu == "Book a Flight":
        bookFlight()
    elif menu == "Cancel Reservation":
        cancelReservation()
    elif menu == "Display Booked Passengers":
        displayBookedPassengers()

if __name__ == "__main__":
    main()
