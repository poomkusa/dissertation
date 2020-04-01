#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 24 16:20:33 2020

@author: poom
"""

import requests
from bs4 import BeautifulSoup

# Fill in your details here to be posted to the login form.
payload = {
    'email': 'seanhayesipg%40gmail.com',
    'password': '1Poomaman%407',
    'remember_me': 'true',
    'from': 'email_login',
#    'airlock_id': '',
    'origin_url': 'https%3A%2F%2Fwww.airbnb.com%2Fusers%2Fshow%2F169512344',
#    'page_controller_action_pair':  ''
}
# Use 'with' to ensure the session context is closed after use.
with requests.Session() as s:
    p = s.post('https://www.airbnb.com/authenticate', data=payload)
    # An authorised request.
    r = s.get("https://www.airbnb.com/users/show/169512344")
    html_page = BeautifulSoup(r.text, "html.parser")
    picture_selector = 'img._1mgxxu3'
    pic = html_page.select(picture_selector)
    for image in pic:
        print(image["src"]) #src = source