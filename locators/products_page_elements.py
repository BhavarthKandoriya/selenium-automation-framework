from selenium.webdriver.common.by import By

elements = {
    '_logged_in_username': (By.ID, 'nameofuser'),
    '_product_link': (By.XPATH, '(//div[@id="tbodyid"]//div[1]//a[1])[1]'),
    '_add_to_cart_link': (By.XPATH, '//a[text()="Add to cart"]')
}
