from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

options = webdriver.ChromeOptions()
options.add_experimental_option("detach", True)

service = Service("C:\Chrome Driver\chromedriver.exe")
driver = webdriver.Chrome(service= service, options= options)

driver.get("https://www.linkedin.com/jobs/search/?currentJobId=3471675671&f_AL=true&f_WT=2&keywords=python%20developer&refresh=true")
sign_in = driver.find_element(By.LINK_TEXT, "Sign in")
sign_in.click()
username = driver.find_element(By.CSS_SELECTOR, "div #username")
username.send_keys("hephzi2002.udo@gmail.com")
password = driver.find_element(By.CSS_SELECTOR, "div #password")
password.send_keys("C0r0na_time")
signinbtn = driver.find_element(By.CLASS_NAME, "btn__primary--large")
signinbtn.click()
time.sleep(12)
job = driver.find_element(By.CLASS_NAME, "job-card-container__link") 
job.click()
time.sleep(12)
applybtn = driver.find_element(By.CSS_SELECTOR, ".jobs-apply-button")
applybtn.click()
phone_number = "9161939448"
time.sleep(12)
number_input = driver.find_element(By.ID, "single-line-text-form-component-formElement-urn-li-jobs-applyformcommon-easyApplyFormElement-3471675671-259100257288133659-phoneNumber-nationalNumber")
number_input.send_keys(phone_number)
time.sleep(5)
continuebtn = driver.find_element(By.CSS_SELECTOR, "div .display-flex button")
continuebtn.click()
time.sleep(10)
select_resume = driver.find_element(By.CSS_SELECTOR, "div .jobs-resume-picker__resume-btn-container button")
select_resume.click()
time.sleep(10)
reviewbtn = (driver.find_elements(By.CSS_SELECTOR, "div .justify-flex-end button"))[1]
reviewbtn.click()