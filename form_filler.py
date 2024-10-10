from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time

def fill_sanchar_saathi_form(driver, data):
    wait = WebDriverWait(driver, 20)  # 20 seconds timeout

    try:
        driver.get("https://sancharsaathi.gov.in/sfc/Home/sfc-complaint.jsp")

        # Wait for page to load
        wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))

        # Select medium of communication
        medium_select = Select(wait.until(EC.presence_of_element_located((By.ID, "sfc-medium"))))
        medium_select.select_by_visible_text(data['medium'])

        # Select fraud category
        category_select = Select(wait.until(EC.presence_of_element_located((By.ID, "sfc-category"))))
        category_select.select_by_visible_text(data['category'])

        # Handle medium-specific fields
        if data['medium'] == 'Call':
            wait.until(EC.presence_of_element_located((By.ID, "suspected-number"))).send_keys(data.get('suspected_number', ''))
        elif data['medium'] == 'SMS':
            sms_type = wait.until(EC.presence_of_element_located((By.ID, "sms-without-shortcode" if data['sms_type'] == 'without_header' else "sms-with-shortcode")))
            sms_type.click()
            
            if data['sms_type'] == 'without_header':
                wait.until(EC.presence_of_element_located((By.ID, "suspected-number"))).send_keys(data.get('sms_suspected_number', ''))
            else:
                wait.until(EC.presence_of_element_located((By.ID, "suspected-shortcode"))).send_keys(data.get('sms_suspected_header', ''))

            # Fill SMS CTA and URL if provided
            if 'sms_cta' in data:
                wait.until(EC.presence_of_element_located((By.ID, "sms-cta"))).send_keys(data['sms_cta'])
            if 'sms_cta_url' in data:
                wait.until(EC.presence_of_element_located((By.ID, "sms-cta-url"))).send_keys(data['sms_cta_url'])
        elif data['medium'] == 'WhatsApp':
            whatsapp_type = wait.until(EC.presence_of_element_located((By.ID, "whatsapp-call" if data['whatsapp_type'] == 'call' else "whatsapp-text")))
            whatsapp_type.click()
            wait.until(EC.presence_of_element_located((By.ID, "suspected-whatsapp-number"))).send_keys(data.get('suspected_whatsapp_number', ''))

        # Fill in other details
        wait.until(EC.presence_of_element_located((By.ID, "sfc-date-input"))).send_keys(data['date'])
        wait.until(EC.presence_of_element_located((By.ID, "sfc-time-input"))).send_keys(data['time'])
        wait.until(EC.presence_of_element_located((By.ID, "sfc-remarks"))).send_keys(data['complaint_details'])
        wait.until(EC.presence_of_element_located((By.ID, "first-name"))).send_keys(data['first_name'])
        wait.until(EC.presence_of_element_located((By.ID, "last-name"))).send_keys(data.get('last_name', ''))
        wait.until(EC.presence_of_element_located((By.ID, "mobile"))).send_keys(data['mobile_number'])

        # Check the declaration checkbox
        declaration_checkbox = wait.until(EC.element_to_be_clickable((By.ID, "declaration")))
        declaration_checkbox.click()

        print("Form filled successfully. Please review and submit manually.")

    except Exception as e:
        print(f"An error occurred while filling the form: {str(e)}")
    finally:
        # Don't close the driver here, let the user decide when to close it
        print("Please close the browser manually when you're done.")