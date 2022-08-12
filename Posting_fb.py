#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
import pickle
import os
import time
from random import randint

    
url = 'https://m.facebook.com/'
email = ""
password = ""
text_post = "Example text post"
rand_rause = randint(7, 15)
gecko_options = webdriver.FirefoxOptions()
gecko_options.add_argument("--headless")
browser = webdriver.Firefox(options=gecko_options)
wait = WebDriverWait(browser, 10)


def login(email, password):
    email_input = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="m_login_email"]')))
    email_input.send_keys(email)
    password_input = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="m_login_password"]')))
    password_input.send_keys(password)
    login_button = wait.until(EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div/div[2]/div[1]/div/div/div[2]/div/div[3]/form/div[5]/div[1]/button')))
    login_button.click()
    wait.until(EC.url_changes(url))
    time.sleep(1)
    try:
        wait.until(EC.visibility_of_element_located((By.XPATH, "/html/body/div[1]/div/div[2]/div/div[1]/div/div/div/div[3]/div/div[1]/div/div/a")))
        next_button = wait.until(EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div/div[2]/div/div[1]/div/div/div/div[3]/div/div[1]/div/div/a')))
        next_button.click()
    except:
        pass


def new_post(text_post):
    try:
        wait.until(EC.visibility_of_element_located((By.XPATH, "/html/body/div[1]/div/div[4]/div/div[1]/div/div[3]/div/div[1]/div/div[2]/div")))
        input_place = wait.until(EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div/div[4]/div/div[1]/div/div[3]/div/div[1]/div/div[2]/div')))
        place_ = input_place.find_element_by_xpath('..')
        place_.click()
        time.sleep(4)
    except:
        print('Input place not found')
        return False
    try:
        button = wait.until(EC.visibility_of_element_located((By.XPATH, '/html/body/div[2]/div[1]/div/div[2]/div[1]/div/div[5]/div[3]/div/div/button')))
        button = button.find_element_by_xpath('..')
        text_area = browser.find_element_by_xpath('//*[@id="uniqid_1"]')
        text_area.send_keys(text_post)
        time.sleep(4)
    except:
        print('Text area not found')
        return False
    post_btn = browser.find_element_by_xpath('/html/body/div[2]/div[1]/div/div[2]/div/div/div[5]/div[3]/div/div/button')
    post_btn.click()


if __name__ == '__main__':

    if not os.path.exists('geckodriver.exe'):
        print('Geckodriver not found, please download it from https://github.com/mozilla/geckodriver/releases')
        exit()

    if not os.path.exists('community_list.txt'):
        with open('community_list.txt', 'w') as f:
            f.write('')
            f.close()

    if len(email) < 5 or len(password) < 5:
        print('Wrong email or password, please change it in 12 and 13 lines')
        exit()


    #Check if list of communities is empty
    with open('community_list.txt', 'r', encoding="utf-8") as f:
        comm = f.readlines()
        if not comm:
            print('Community list is empty, please add a grous to the list, like this: \nhttps://m.facebook.com/groups/<group_name>\n')
            exit()

    browser.get(url)
    #Check if cookie.pkl exists
    if not os.path.exists('cookie.pkl'):
        login(email, password)
        print("Logged in")
        with open('cookie.pkl', 'wb') as f:
            pickle.dump(browser.get_cookies(), f)
    else:
        with open('cookie.pkl', 'rb') as f:
            cookies = pickle.load(f)
        for cookie in cookies:
            browser.add_cookie(cookie)
        print("Cookies added")
    
    for c in comm:
        print(f"Posting in {c}")
        browser.get(c)
        print(f"Waiting {rand_rause} seconds...")
        time.sleep(rand_rause)
        if new_post(text_post):
            print(f"Post in {c} successful")
        else:
            print(f"Post in {c} fiailed")


    browser.quit()
