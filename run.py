import os
import time
from playwright.sync_api import Page
import yaml

if not os.path.isdir('./ScreenShots'):
    os.makedirs('./ScreenShots')


def open_file(path: str):
    with open(path, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)


try:
    config = open_file('../.config/test.yml')
except FileNotFoundError:
    config = open_file('../.config/default.yml')


def login(page: Page):
    page.goto(f'{config["url"]}')
    page.wait_for_load_state('networkidle')
    page.click('//*[@id="app"]/main/div/div[1]/div/p/span[3]')
    page.query_selector(
        '#app > div.modal.v--modal-overlay.scrollable > div > div.v--modal-box.v--modal > form > div.normal-signin > div:nth-child(1) > div.input > input[type=text]').fill('alice')
    page.query_selector(
        '#app > div.modal.v--modal-overlay.scrollable > div > div.v--modal-box.v--modal > form > div.normal-signin > div:nth-child(2) > div.input > input[type=password]').fill('alice1234')
    page.keyboard.press('Enter')
    time.sleep(3)
    return page


def test_create_user(page: Page):
    page.goto(f'{config["url"]}')
    page.wait_for_load_state('networkidle')
    page.click('//*[@id="app"]/main/div/div[1]/div/p/span[1]')
    # アカウント登録
    page.query_selector(
        '#app > div.modal.v--modal-overlay.scrollable > div > div.v--modal-box.v--modal > form > div:nth-child(1) > div.input > input[type=text]').fill('alice')
    page.query_selector(
        '#app > div.modal.v--modal-overlay.scrollable > div > div.v--modal-box.v--modal > form > div:nth-child(2) > div.input > input[type=password]').fill('alice1234')
    page.query_selector(
        '#app > div.modal.v--modal-overlay.scrollable > div > div.v--modal-box.v--modal > form > div:nth-child(3) > div.input > input[type=password]').fill('alice1234')
    page.query_selector('#app > div.modal.v--modal-overlay.scrollable > div > div.v--modal-box.v--modal > form > button').click()
    time.sleep(3)
    page.screenshot(path="./ScreenShots/register_user.png")


def test_login(page: Page):
    page = login(page)
    page.screenshot(path="./ScreenShots/login.png")


def test_note(page: Page):
    page = login(page)
    page.click('#app > div.header.header > div > div.main > div > div.right > div.note > button')
    time.sleep(2)
    page.query_selector(
        'body > div.mk-window.mk-post-form-window > div.main > div > div > div > div > div > div.content > div > textarea').fill('Hello Ayuskey')
    page.click('body > div.mk-window.mk-post-form-window > div.main > div > div > div > div > div > button.dmtdnykelhudezerjlfpbhgovrgnqqgr.submit.primary.round')
    time.sleep(3)
    page.screenshot(path="./ScreenShots/note.png")
