import os
from playwright.sync_api import Page

BASE_URL = os.getenv("UI_BASE_URL", "https://www.saucedemo.com")


class LoginPage:
    """Page object for the login screen: locators and actions live here, not in tests."""

    def __init__(self, page: Page):
        self.page = page
        self.username = page.get_by_placeholder("Username")
        self.password = page.get_by_placeholder("Password")
        self.login_button = page.get_by_role("button", name="Login")
        self.error = page.locator('[data-test="error"]')

    def open(self):
        self.page.goto(BASE_URL)

    def login(self, user: str, password: str):
        self.username.fill(user)
        self.password.fill(password)
        self.login_button.click()
