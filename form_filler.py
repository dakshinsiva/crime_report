from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from config import CHROME_DRIVER_PATH
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

def fill_sanchar_saathi_form(data):
    options = webdriver.ChromeOptions()
    options.add_argument('--start-maximized')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
    
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    wait = WebDriverWait(driver, 20)  # 20 seconds timeout

    try:
        driver.get("https://sancharsaathi.gov.in/sfc/Home/sfc-complaint.jsp")

        # Wait for page to load
        wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))

        # Fill in the fields that can be automated
        try:
            # Select medium of communication
            medium_select = Select(wait.until(EC.presence_of_element_located((By.ID, "sfc-medium"))))
            medium_select.select_by_visible_text(data['medium'])

            # Select fraud category
            category_select = Select(wait.until(EC.presence_of_element_located((By.ID, "sfc-category"))))
            category_select.select_by_visible_text(data['category'])

            # Fill in other details
            fields = {
                "suspected-number": data.get('suspected_number', ''),
                "sfc-date-input": data['date'],
                "sfc-time-input": data['time'],
                "sfc-remarks": data['complaint_details'],
                "first-name": data['first_name'],
                "last-name": data.get('last_name', ''),
                "mobile": data.get('mobile_number', '')
            }

            for field, value in fields.items():
                if value:  # Only fill if value is provided
                    try:
                        element = wait.until(EC.presence_of_element_located((By.ID, field)))
                        element.clear()  # Clear any existing text
                        element.send_keys(value)
                    except TimeoutException:
                        print(f"Could not find or interact with field: {field}")

            # Handle SMS-specific fields if medium is SMS
            if data['medium'] == 'SMS':
                sms_type = wait.until(EC.presence_of_element_located((By.ID, "sms-without-shortcode")))
                sms_type.click()
                
                sms_cta = wait.until(EC.presence_of_element_located((By.ID, "sms-cta")))
                sms_cta.clear()
                sms_cta.send_keys(data.get('sms_cta', ''))
                
                sms_cta_url = wait.until(EC.presence_of_element_located((By.ID, "sms-cta-url")))
                sms_cta_url.clear()
                sms_cta_url.send_keys(data.get('sms_cta_url', ''))

            # Handle WhatsApp-specific fields if medium is WhatsApp
            elif data['medium'] == 'WhatsApp':
                whatsapp_type = wait.until(EC.presence_of_element_located((By.ID, "whatsapp-call")))
                whatsapp_type.click()
                
                whatsapp_number = wait.until(EC.presence_of_element_located((By.ID, "suspected-whatsapp-number")))
                whatsapp_number.clear()
                whatsapp_number.send_keys(data.get('suspected_whatsapp_number', ''))

        except Exception as e:
            print(f"An error occurred while filling the form: {str(e)}")

        print("Basic information filled. Please complete the remaining fields manually.")
        print("Don't forget to upload the screenshot, complete any CAPTCHA or OTP verification, and check the declaration checkbox.")

        # Keep the browser open for manual completion
        input("Press Enter when you've completed the form manually...")

    except Exception as e:
        print(f"An error occurred: {str(e)}")
    finally:
        driver.quit()