from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.common.exceptions import NoSuchElementException
import os
import tkinter as tk
from tkinter import messagebox


ACCOUNT_EMAIL = "YOUR EMAIL"
ACCOUNT_PASSWORD = "YOUR PASSWORD"
GYM_URL = "https://appbrewery.github.io/gym/"

booked_count = 0
waitlist_count = 0
already_booked_count = 0
total_classes = 0
processed_classes = []
succesfull_books = 0


chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach", True)

user_data_dir = os.path.join(os.getcwd(), "chrome_profile")
chrome_options.add_argument(f"--user-data-dir={user_data_dir}")

driver = webdriver.Chrome(options=chrome_options)
driver.get(GYM_URL)

wait = WebDriverWait(driver, 5)


login_btn = wait.until(ec.element_to_be_clickable((By.ID, "login-button")))
login_btn.click()

email = wait.until(ec.visibility_of_element_located((By.ID, "email-input")))
email.send_keys(ACCOUNT_EMAIL)

password = driver.find_element(By.ID, "password-input")
password.send_keys(ACCOUNT_PASSWORD)

submit_btn = driver.find_element(By.ID, "submit-button")
submit_btn.click()

wait.until(ec.presence_of_element_located((By.ID, "schedule-page")))

class_cards = driver.find_elements(By.CSS_SELECTOR, value='[id^="class-card"]')

class_cards = driver.find_elements(By.CSS_SELECTOR, '[id^="class-card"]')

for card in class_cards:
    day_group = card.find_element(By.XPATH, "./ancestor::div[contains(@id, 'day-group-')]")
    day_title = day_group.find_element(By.TAG_NAME, 'h2').text
    if "Tue" in day_title or "Thu" in day_title:
        time_text = card.find_element(By.CSS_SELECTOR, value="p[id^='class-time-']").text
        if "6:00 PM" in time_text:
            class_name = card.find_element(By.CSS_SELECTOR, "h3[id^='class-name-']").text
            button = card.find_element(By.CSS_SELECTOR, value="button[id^='book-button-']")
            class_info = f"{class_name} on {day_title}"

            if button.text  == "Booked":
                print(f"Already booked: {class_info} ")
                already_booked_count += 1
            elif button.text == "Waitlisted":
                print(f"Already waitlisted: {class_info} ")
                already_booked_count += 1
            elif button.text == "Book Class":  
                button.click()
                print(f"✓ Booked: {class_info}")
                booked_count += 1 
                processed_classes.append(f"[New Booking] {class_info}")
            elif button.text == "Join Waitlist":
                button.click()
                print(f"Joined waitlist for: {class_info}")
                waitlist_count += 1
                processed_classes.append(f"[New Waitlist] {class_info}")
            total_classes += 1        

print("--- Booking Summary ---")
print(f"Classes booked: {booked_count}")
print(f"Waitlists joined: {waitlist_count}")
print(f"Already booked/Waitlisted: {already_booked_count}")
print(f"Total Tuesday & Thursday 6pm classes processed: {total_classes}")

my_bookings = driver.find_element(By.XPATH, value=' //*[@id="my-bookings-link"]')
my_bookings.click()

wait.until(ec.presence_of_element_located((By.ID, "my-bookings-page")))

confirmed_books = driver.find_elements(By.ID, value="confirmed-bookings-section")
confirmed_waitslists = driver.find_elements(By.ID, value="waitlist-section")

print("--- VERIFYING ON MY BOOKINGS PAGE ---")
try:
    for book in confirmed_books:
        book_data = f"{class_name}"
        print(f"✓ Verified: {book_data}")
        succesfull_books += 1

    for waitlist in confirmed_waitslists:
        waitlist_data = f"{class_name}"
        print(f"✓ Verified: {waitlist_data} (Waitlist)")
        succesfull_books += 1
except NoSuchElementException:
    pass
    

print("--- VERIFICATION RESULT ---")
print(f"Expected {total_classes} bookings")
print(f"Found {succesfull_books} Bookings")

if total_classes == succesfull_books:
    print("✅ SUCCESS: All bookings verified!")
else:
    print(f"❌ MISMATCH: Missing {total_classes - succesfull_books} bookings ")


print("--- Detailed class list ---")
for class_detail in processed_classes:
    print(f"{class_detail}")

root = tk.Tk()
root.withdraw()  
messagebox.showinfo("Automation Complete", "Press OK to close the browser...")

driver.quit()
