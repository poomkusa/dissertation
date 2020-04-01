# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import bs4
import requests

#ดึงข้อมูลจากเว็บที่เราสนใจ
r = requests.get("https://www.wongnai.com/restaurants/sushimasa")
#เช็คข้อมูล
r.text
#แปลงเป็น type bs4.BeautifulSoup
html_page = bs4.BeautifulSoup(r.text, "html.parser")
print(html_page)
type(html_page)
#ทำให้ source ดูได้ง่ายขึ้น
print(html_page.prettify())
#ถ้า tag ที่เราได้มาเว้นด้วย spacebar เราจะแทนด้วย . ลงไปแทนนะครับ เช่น span. sc-1u6e7er-1 cvVMHV จะต้องใช้เป็น span. sc-1u6e7er-1.cvVMHV
selector = 'span._2qDKIyMmA-jMRyfxACZWt6'
#เลือกตัวเดียว(ตัวแรกที่พบ) .select_one() หรือจะดึงออกมาทุกตัวเลย .select()
price = html_page.select_one(selector)
price
price.text


picture_selector = 'img.e9lydh-0.glafeS.sc-1yqvox6-15.uvlFd'
pic = html_page.select(picture_selector)
pic
for image in pic:
    print(image["src"]) #src = source
   
    
#ดึงข้อมูลจากเว็บที่เราสนใจ
r = requests.get("https://www.airbnb.com/users/show/169512344")
#เช็คข้อมูล
r.text
#แปลงเป็น type bs4.BeautifulSoup
html_page = bs4.BeautifulSoup(r.text, "html.parser")
print(html_page)
type(html_page)
#ทำให้ source ดูได้ง่ายขึ้น
print(html_page.prettify())
#ถ้า tag ที่เราได้มาเว้นด้วย spacebar เราจะแทนด้วย . ลงไปแทนนะครับ เช่น span. sc-1u6e7er-1 cvVMHV จะต้องใช้เป็น span. sc-1u6e7er-1.cvVMHV
selector = 'div._910j1c5'
#เลือกตัวเดียว(ตัวแรกที่พบ) .select_one() หรือจะดึงออกมาทุกตัวเลย .select()
country = html_page.select_one(selector)
country
country.text
