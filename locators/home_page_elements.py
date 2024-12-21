from selenium.webdriver.common.by import By

elements = {
    '_log_in_link': (By.ID, 'login2'),
    '_log_in_button': (By.XPATH, '//button[text()="Log in"]'),
    '_username_input': (By.ID, 'loginusername'),
    '_password_input': (By.ID, 'loginpassword')
}
