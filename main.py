import tkinter as tk
from gui import SancharSaathiGUI
from form_filler import fill_sanchar_saathi_form
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

def submit_form(data):
    # Set up the Chrome driver
    options = webdriver.ChromeOptions()
    options.add_argument('--start-maximized')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
    
    try:
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)
        
        # Call the form filler function with both driver and data
        fill_sanchar_saathi_form(driver, data)
        
        # Keep the browser open
        input("Press Enter to close the browser...")
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        # You might want to show this error message in the GUI as well
    finally:
        # Close the driver only after user input
        if 'driver' in locals():
            driver.quit()

if __name__ == "__main__":
    root = tk.Tk()
    app = SancharSaathiGUI(root, submit_form)
    root.mainloop()