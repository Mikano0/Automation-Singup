Gym Class Booking Automation

Automatically book or join waitlists for gym classes using Python and Selenium.

What It Does

Logs into your gym account.

Finds Tuesday and Thursday classes at 6:00 PM.

Books available classes or joins waitlists.

Shows a summary of what was booked or waitlisted.

Verifies bookings on the “My Bookings” page.

Pops up a message when done.

Requirements

Python 3.8+

Google Chrome + Chromedriver

Python packages:

selenium

tkinter (comes with Python)

Install Selenium with:

pip install selenium

Setup

Download the script.

Open the script and update your account info:

ACCOUNT_EMAIL = "your_email@example.com"
ACCOUNT_PASSWORD = "your_password"
GYM_URL = "https://appbrewery.github.io/gym/"


Make sure Chromedriver is installed and matches your Chrome version.

How to Run

Run the script with Python:

python gym_booking.py


The script will:

Open Chrome.

Log in.

Find the classes.

Book or join waitlists.

Show a summary in the console.

Pop up a notification when done.
