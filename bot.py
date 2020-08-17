from selenium import webdriver
from selenium.webdriver.support.ui import Select
from twilio.rest import Client
from time import sleep
from sys import exit, argv
from os import environ

PAGE_TIMEOUT = 3
HAMBURGER_BUTTON_DELAY = 5
HOME_PAGE_DELAY = 5

LOGIN_PAGE = "https://secure.dol.wa.gov/home/"
CREDENTIALS = {
    "username": environ["DOL_USERNAME"],
    "password": environ["DOL_PASSWORD"],
    "email": environ["EMAIL"],
    "phone_number": environ["PHONE_NUMBER"]
}

TWILIO_CREDENTIALS = {
    "from_num": environ["FROM_NUM"],
    "to_num": environ["TO_NUM"],
    "account_sid": environ["ACCOUNT_SID"],
    "auth_token": environ["AUTH_TOKEN"]
}


SCHEDULE_AN_APPT_BUTTON = "l_k-v-4"
SCHEDULE_A_NEW_APPT_BUTTON = "d-i"
NEXT_BUTTON = "d-__NextStep"
I_WANT_TO_DROP_DOWN = "d-l1"
ENHANCED_LICENSE_OPTION_IDX = 2
EMAIL_FIELD = "d-w2"
CONFIRM_EMAIL_FIELD = "d-x2"
CELL_PHONE_NUM_FIELD = "d-03"
GUEST_DROP_DOWN = "d-93"
NO_GUEST_OPTION_IDX = 1
OFFICE_DROP_DOWN = "d-14"
SEE_AVAILABLE_APPTS_BUTTON = "d-24"
SELECT_APPT_TIME_TABLE = "container_c-01"
HAMBURGER_BUTTON = "ManagerMenuLink"
HAMBURGER_BUTTON_HOME_OPTION = "MenuLinkHome"


def send_text(msg):
    client = Client(TWILIO_CREDENTIALS["account_sid"],
                    TWILIO_CREDENTIALS["auth_token"])

    client.messages.create(
            to=TWILIO_CREDENTIALS["to_num"],
            from_=TWILIO_CREDENTIALS["from_num"],
            body=msg)

def click_into_new_page(element, page_timeout=PAGE_TIMEOUT):
    element.click()
    sleep(page_timeout)

def login_home_page(driver):
    driver.get(LOGIN_PAGE)
    
    element = driver.find_element_by_id("username")
    element.send_keys(CREDENTIALS["username"])
    
    element = driver.find_element_by_id("password")
    element.send_keys(CREDENTIALS["password"])

    element = driver.find_element_by_id("btnLogin")
    click_into_new_page(element)

def click_next_button(driver):
    element = driver.find_element_by_id(NEXT_BUTTON)
    click_into_new_page(element)

def fill_out_contact_form(driver):
    element = driver.find_element_by_id(EMAIL_FIELD)
    element.send_keys(CREDENTIALS["email"])
    
    element = driver.find_element_by_id(CONFIRM_EMAIL_FIELD)
    element.send_keys(CREDENTIALS["email"])
    
    element = driver.find_element_by_id(CELL_PHONE_NUM_FIELD)
    element.send_keys(CREDENTIALS["phone_number"])

def fill_out_guest_form(driver):
    select = Select(driver.find_element_by_id(GUEST_DROP_DOWN))
    select.select_by_index(NO_GUEST_OPTION_IDX)

def select_office_location(driver, location):
    select = Select(driver.find_element_by_id(OFFICE_DROP_DOWN))
    options = select.options
    for idx, option in enumerate(options):
        if option.text != location: continue

        select.select_by_index(idx)
        return True
    
    print(f'Cannot find "{location}" on office dropdown form!')
    return False

def go_to_home_page(driver):
    element = driver.find_element_by_class_name(HAMBURGER_BUTTON)
    element.click()
    sleep(HAMBURGER_BUTTON_DELAY)

    element = driver.find_element_by_class_name(HAMBURGER_BUTTON_HOME_OPTION)
    element.click()
    sleep(HOME_PAGE_DELAY)

def location_has_appts(driver, location):
    element = driver.find_element_by_id(SELECT_APPT_TIME_TABLE)
    class_name = element.get_attribute("class")
    return "Hidden" not in class_name

def main():
    locations = argv[1:]
    if len(locations) == 0:
        print(f'Usage: python3 bot.py <location_1> ... <location_n>')
        exit(1)

    driver = webdriver.Firefox('./')
    login_home_page(driver)

    for location in locations:
        element = driver.find_element_by_id(SCHEDULE_AN_APPT_BUTTON)
        click_into_new_page(element)

        element = driver.find_element_by_id(SCHEDULE_A_NEW_APPT_BUTTON)
        click_into_new_page(element)
        click_next_button(driver)

        select = Select(driver.find_element_by_id(I_WANT_TO_DROP_DOWN))
        select.select_by_index(ENHANCED_LICENSE_OPTION_IDX)

        click_next_button(driver)
        click_next_button(driver)

        fill_out_contact_form(driver)
        click_next_button(driver)

        fill_out_guest_form(driver)
        click_next_button(driver)

        if not select_office_location(driver, location):
            go_to_home_page(driver)
            continue

        element = driver.find_element_by_id(SEE_AVAILABLE_APPTS_BUTTON)
        click_into_new_page(element)

        if location_has_appts(driver, location):
            msg = f'"{location}" has spots!'
            send_text(msg)

        go_to_home_page(driver)

    driver.close()

if __name__ == "__main__":
    main()

