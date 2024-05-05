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
                 (name TEXT, address TEXT, age INTEGER, passportID TEXT, flightNumber INTEGER,
                  parentName TEXT, parentContact TEXT, parentEmail TEXT)''')

    MAX_FLIGHTS = 10

except sqlite3.Error as e:
    st.error(f"SQLite error: {e}")

def addFlight(flightNumber, origin, destination, availableSeats):
    try:
        # Check if flight number already exists
        c.execute("SELECT flightNumber FROM flights WHERE flightNumber = ?", (flightNumber,))
        existing_flight = c.fetchone()
        if not existing_flight:  # Only add if the flight doesn't already exist
            # Insert new flight record
            c.execute('''INSERT INTO flights (flightNumber, origin, destination, availableSeats) 
                         VALUES (?, ?, ?, ?)''', (flightNumber, origin, destination, availableSeats))
            conn.commit()
            st.success("Flight added successfully.")
    except sqlite3.Error as e:
        st.error(f"An error occurred: {e}")

def bookFlight(name, address, age, passportID, flightNumber, parent_name=None, parent_contact=None, parent_email=None):
    try:
        if age < 18:
            st.info("Since you are below 18 years old, we need some information from your parents.")
            parent_name = st.text_input("Enter the name of your parent:")
            parent_contact = st.text_input("Enter the contact number of your parent:")
            parent_email = st.text_input("Enter the email address of your parent:")
            
            # Check if all parent information is provided
            if not (parent_name and parent_contact and parent_email):
                st.warning("Please provide all required information of your parent.")
                return
        else:
            parent_name = None
            parent_contact = None
            parent_email = None

        # Only mark the flight as booked and decrement available seats if all required information is provided
        c.execute('''INSERT INTO passengers (name, address, age, passportID, flightNumber, parentName, parentContact, parentEmail) 
                     VALUES (?, ?, ?, ?, ?, ?, ?, ?)''', 
                     (name, address, age, passportID, flightNumber, parent_name, parent_contact, parent_email))
                     
        c.execute('''UPDATE flights SET availableSeats = availableSeats - 1 WHERE flightNumber = ?''', (flightNumber,))
        conn.commit()
        st.success("Flight booked successfully.")
    except sqlite3.Error as e:
        st.error(f"Error booking flight: {e}")



def displayBookedPassengers():
    try:
        st.write("List of Booked Passengers:")
        for row in c.execute("SELECT * FROM passengers"):
            passenger_info = f"Passenger: {row[0]}, Age: {row[2]}, Address: {row[1]}, Passport ID: {row[3]}, Flight Number: {row[4]}"
            if row[5]:  # If parent information exists
                parent_info = f"Parent Name: {row[5]}, Contact: {row[6]}, Email: {row[7]}"
                passenger_info += f", {parent_info}"
            st.write(passenger_info)
    except sqlite3.Error as e:
        st.error(f"Error displaying booked passengers: {e}")

# The rest of the code remains unchanged...




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
