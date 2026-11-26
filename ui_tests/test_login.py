import os
import re

import pytest
from playwright.sync_api import Page, expect

from ui_tests.pages.login_page import LoginPage

# Public demo credentials published on the demo site itself.
PASSWORD = os.getenv("DEMO_PASSWORD", "secret_sauce")

pytestmark = pytest.mark.ui


def test_valid_user_reaches_inventory(page: Page):
    login = LoginPage(page)
    login.open()
    login.login("standard_user", PASSWORD)
    expect(page).to_have_url(re.compile(r"/inventory"))


def test_locked_out_user_sees_error(page: Page):
    login = LoginPage(page)
    login.open()
    login.login("locked_out_user", PASSWORD)
    expect(login.error).to_be_visible()
    expect(login.error).to_contain_text("locked out")


@pytest.mark.parametrize("user, password, message", [
    ("", PASSWORD, "Username is required"),
    ("standard_user", "", "Password is required"),
    ("standard_user", "wrong_password", "do not match"),
])
def test_invalid_login_shows_error(page: Page, user, password, message):
    login = LoginPage(page)
    login.open()
    login.login(user, password)
    expect(login.error).to_contain_text(message)
