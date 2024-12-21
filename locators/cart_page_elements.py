from selenium.webdriver.common.by import By

elements = {
    '_place_order_button': (By.XPATH, '//button[text()="Place Order"]'),
    '_name_input': (By.ID, 'name'),
    '_creditcard_input': (By.ID, 'card'),
    '_purchase_button': (By.XPATH, '//button[text()="Purchase"]'),
    '_success_alert': (By.XPATH, '//div[contains(@class,"sweet-alert")]//p')
}
