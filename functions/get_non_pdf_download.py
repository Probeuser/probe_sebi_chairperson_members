from log import log
import traceback
import sys
import time
import pandas as pd
from datetime import datetime
import re
import pyautogui
from bs4 import BeautifulSoup
from config import sebi_config
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchWindowException
from selenium.common.exceptions import TimeoutException,WebDriverException




def get_non_pdf_download(pdf_link,driver,name,index):
 try:    

    # Navigate to your web page
    driver.get(pdf_link)
    print("pdf_link ======",pdf_link,name,index)
    time.sleep(10)
    print_button = driver.find_element(By.XPATH, '//*[@id="member-wrapper"]/section[2]/h1/div/ul/li[7]/a')
    print_button.click()
    print("print button clicked=====")
    time.sleep(15)


    # Get handles of all currently open windows
    all_windows = driver.window_handles

    # Switch to the new window
    new_window = [window for window in all_windows if window != driver.current_window_handle][0]
    print("new window =======",new_window)
    driver.switch_to.window(new_window)

    

    try:
        WebDriverWait(driver, 30).until(EC.visibility_of_element_located((By.XPATH, "//html/body/print-preview-app")))
        
        # Find the print-preview-app element using XPath
        print_preview_app = driver.find_element(By.XPATH, "//html/body/print-preview-app")
        
        if print_preview_app :
            shadow_element = driver.execute_script('return arguments[0].shadowRoot.querySelector("print-preview-sidebar").shadowRoot.querySelector("#container").querySelector("print-preview-destination-settings").shadowRoot.querySelector("print-preview-destination-select").shadowRoot.querySelector("print-preview-settings-section > div").querySelector(".md-select")', print_preview_app)

            # Print the shadow element
            print(shadow_element)
            if shadow_element:
                # print("Shadow element found:", shadow_element.tag_name)
                # print("HTML of the located element:", shadow_element.get_attribute('outerHTML'))
                shadow_element.click()
                time.sleep(10)
                select = Select(shadow_element)
                time.sleep(10)
                select.select_by_value('Save as PDF/local/')
                shadow_element.click()
                time.sleep(10)
                # Find the print-preview-app element using XPath
                print_preview_app = driver.find_element(By.XPATH, "//html/body/print-preview-app")
                if print_preview_app :
                    shadow_element = driver.execute_script('return arguments[0].shadowRoot.querySelector("print-preview-sidebar").shadowRoot.querySelector("print-preview-button-strip").shadowRoot.querySelector(".controls").querySelector(".action-button")', print_preview_app)
                    # Print the shadow element
                    print("save button",shadow_element)
                    if shadow_element:
                        # print("Shadow element found:", shadow_element.tag_name)
                        # print("HTML of the located element:", shadow_element.get_attribute('outerHTML'))
                        shadow_element.click()
                        time.sleep(10)
                        # file_name_with_path = fr"C:\Users\devadmin\sebi_final_script\chairperson_members\pdfdownload\chairperson_members_{name}_{index}.pdf"
                        file_name_with_path = fr"C:\inetpub\wwwroot\Sebi_apiproject\pdfdownload\co_{name}_{index}.pdf"
                        print(file_name_with_path)
                        pyautogui.write(file_name_with_path)
                        time.sleep(5)
                        pyautogui.press('enter')
                        time.sleep(5)

                        return f"co_{name}_{index}.pdf"
                else:
                    print("Shadow element save not found.")
            else:
                print("Shadow element select not found.")

    except TimeoutException:
        print("Timeout waiting for print preview to load.")
        return None
    except WebDriverException as e:
        print("An error occurred:", e)
        return None
    driver.switch_to.window(driver.window_handles[0])
    driver.quit()
 except NoSuchWindowException as e:
        print("Error: NoSuchWindowException -", e)
        # browser = webdriver.Chrome(options=chrome_options)
        # browser.get(url)
        return "Nan"
