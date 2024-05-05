import streamlit as st
import sqlite3

# Connect to SQLite database
try:
    conn = sqlite3.connect('flight_reservation.db')
    c = conn.cursor()

    # Create flights table if not exists
    c.execute('''CREATE TABLE IF NOT EXISTS flights 
                 (flightNumber INTEGER PRIMARY KEY, origin TEXT, destination TEXT, availableSeats INTEGER)''')

    # Create passengers table if not exists
    c.execute('''CREATE TABLE IF NOT EXISTS passengers 
                 (name TEXT, address TEXT, age INTEGER, passportID TEXT, flightNumber INTEGER)''')

    MAX_FLIGHTS = 10

except sqlite3.Error as e:
    st.error(f"SQLite error: {e}")

def addFlight(flightNumber, origin, destination, availableSeats):
    try:
        c.execute('''INSERT INTO flights (flightNumber, origin, destination, availableSeats) 
                     VALUES (?, ?, ?, ?)''', (flightNumber, origin, destination, availableSeats))
        conn.commit()
    except sqlite3.IntegrityError:
        st.warning(f"Flight {flightNumber} already exists in the database.")

def displayFlights():
    try:
        st.write("Available Flights:")
        for row in c.execute("SELECT * FROM flights"):
            st.write(f"Flight {row[0]}: {row[1]} to {row[2]} - Available Seats: {row[3]}")
    except sqlite3.Error as e:
        st.error(f"Error displaying flights: {e}")

def bookFlight(name, address, age, passportID, flightNumber):
    try:
        c.execute('''INSERT INTO passengers (name, address, age, passportID, flightNumber) 
                     VALUES (?, ?, ?, ?, ?)''', (name, address, age, passportID, flightNumber))
        c.execute('''UPDATE flights SET availableSeats = availableSeats - 1 WHERE flightNumber = ?''', (flightNumber,))
        conn.commit()
    except sqlite3.Error as e:
        st.error(f"Error booking flight: {e}")

def displayBookedPassengers():
    try:
        st.write("List of Booked Passengers:")
        for row in c.execute("SELECT * FROM passengers"):
            st.write(f"Passenger: {row[0]}, Age: {row[2]}, Address: {row[1]}, Passport ID: {row[3]}, Flight Number: {row[4]}")
    except sqlite3.Error as e:
        st.error(f"Error displaying booked passengers: {e}")

def main():
    try:
        st.title("Flight Reservation System")
        addFlight(1001, "Surigao City", "Davao City", 100)
        addFlight(1002, "Surigao City", "Cebu City", 80)
        addFlight(1003, "Surigao City", "Manila", 120)

        menu = st.sidebar.selectbox("Menu", ["Display Available Flights", "Book a Flight", "Display Booked Passengers"])

        if menu == "Display Available Flights":
            displayFlights()
        elif menu == "Book a Flight":
            name = st.text_input("Enter your name:")
            address = st.text_input("Enter your address:")
            age = st.number_input("Enter your age:", min_value=0, max_value=150, step=1)
            passportID = st.text_input("Enter your passport ID:")
            flightNumber = st.number_input("Enter the flight number:", min_value=1001, max_value=1000 + MAX_FLIGHTS, step=1, format="%d")
            if st.button("Book Flight"):
                bookFlight(name, address, age, passportID, flightNumber)
                st.success("Flight booked successfully.")
        elif menu == "Display Booked Passengers":
            displayBookedPassengers()

    except Exception as e:
        st.error(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
