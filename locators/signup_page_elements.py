from selenium.webdriver.common.by import By

elements = {
    '_username_input': (By.ID, 'sign-username'),
    '_password_input': (By.ID, 'sign-password'),
    '_sign_up_button': (By.XPATH, '//button[text()="Sign up"]')
}
