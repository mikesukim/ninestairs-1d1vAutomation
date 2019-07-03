#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException
from openpyxl import load_workbook
import datetime
import types
from selenium.webdriver.common.keys import Keys

###개인랩탑
# driver = webdriver.Chrome('/Library/Python/2.7/site-packages/selenium/webdriver/common/chromedriver')
###회사
driver = webdriver.Chrome('/Users/Michael/Documents/chromedriver')

##### 관리자 페이지 로그인후 노티스 추가 버튼 클릭까지
driver.get("https://pms.ninestairs.co.kr/secret-center-9stairs/pacemaker/notice/")
idTextField = driver.find_element_by_id('id_username')
pwTextField = driver.find_element_by_id('id_password')
id_for_naverBlog = "mikesungunkim@gmail.com"
password_for_naverBlog = "socialPW"
idTextField.send_keys(id_for_naverBlog)
pwTextField.send_keys(password_for_naverBlog)
pwTextField.submit()

###### 엑셀 에서 데이터 불러오기
wb = load_workbook("Michael's 1d1v material.xlsx" , data_only=True)
ws = wb['Sheet1']

noticeList = []

rows = iter(ws.rows)
next(rows)
for row in rows:

	title = row[7].value
	description = row[8].value
	link = row[9].value
	start_date = row[3].value
	end_date = row[4].value
	start_date_In_str = "{:%Y-%m-%d}".format(start_date)
	end_date_In_str = "{:%Y-%m-%d}".format(end_date)
	start_time = row[5].value
	start_time_In_str = "{:%H:%M:%S}".format(start_time)
	end_time = row[6].value
	end_time_In_str = "{:%H:%M:%S}".format(end_time)

	elementList = [		title,
						description,
						link,
						start_date_In_str,							
						start_time_In_str,
						start_date_In_str,							
						start_time_In_str,
						end_date_In_str,
						end_time_In_str
										]
	noticeList.append(elementList)


def _convert(param):
    if isinstance(param, str):
        return param.decode('utf-8')
    else:
        return param


#### 페이지에서 제일 상단에 등록되어 있는 노티스의 날짜 가지고 오기.
postedNoticeDate = driver.find_element_by_xpath('//*[@id="result_list"]/tbody/tr[1]/td[3]')
postedNoticeDateStartDate = postedNoticeDate.text.split(" ")[0]



#### noticeList에 등록되어 있는 날짜의 노티스가 있는지 확인.
#### 존재 한다면, 그 noticeList에서 그 전 노티스들은 제거.
index = 1
for notice in noticeList:

	if postedNoticeDateStartDate == notice[5]:
		noticeList = noticeList[index:]
		break

	index += 1

	

###### 노티스 페이지에 올리기
for notice in noticeList:

	button = driver.find_element_by_xpath("//a[@class='addlink']")
	button.click()

	titleTextfield = driver.find_element_by_id('id_title')
	for x in range(0, 13):
		titleTextfield.send_keys(Keys.BACKSPACE)
	titleTextfield.send_keys(_convert(notice[0]))
	descriptionTextfield = driver.find_element_by_id('id_description')
	descriptionTextfield.send_keys(_convert(notice[1]))
	linkTextfield = driver.find_element_by_id('id_link')
	if notice[2] is not None:
		linkTextfield.send_keys(_convert(notice[2]))
	releaseDateTextField = driver.find_element_by_id('id_release_date_0')
	releaseDateTextField.send_keys(_convert(notice[3]))
	releaseTimeTextField = driver.find_element_by_id('id_release_date_1')
	releaseTimeTextField.send_keys(_convert(notice[4]))
	startDateTextField = driver.find_element_by_id('id_start_date_0')
	startDateTextField.send_keys(_convert(notice[5]))
	startTimeTextField = driver.find_element_by_id('id_start_date_1')
	startTimeTextField.send_keys(_convert(notice[6]))
	endDateTextField = driver.find_element_by_id('id_end_date_0')
	endDateTextField.send_keys(_convert(notice[7]))
	endTimeTextField = driver.find_element_by_id('id_end_date_1')
	endTimeTextField.send_keys(_convert(notice[8]))
	popupCheckbox = driver.find_element_by_id('id_popup')
	popupCheckbox.click()

	summitBtn = driver.find_element_by_xpath('//*[@id="notice_form"]/div/div/input[1]')
	summitBtn.click()






