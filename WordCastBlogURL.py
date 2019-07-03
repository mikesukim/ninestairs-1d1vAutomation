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
	

###개인랩탑
# driver = webdriver.Chrome('/Library/Python/2.7/site-packages/selenium/webdriver/common/chromedriver')
###회사
driver = webdriver.Chrome('/Users/Michael/Documents/chromedriver')



driver.get("https://nid.naver.com/nidlogin.login?mode=form&url=https://blog.naver.com/9stairs/221220305155")

idTextField = driver.find_element_by_id('id')
pwTextField = driver.find_element_by_id('pw')
driver.find_element_by_xpath("//a[@class='sp h_logo']")

id_for_naverBlog = "9stairs"
password_for_naverBlog = "9stairs337"

idTextField.send_keys(id_for_naverBlog)
pwTextField.send_keys(password_for_naverBlog)

pwTextField.submit()

wait = WebDriverWait(driver, 300)
wait.until(EC.frame_to_be_available_and_switch_to_it((By.NAME,'mainFrame')))


button = driver.find_element_by_xpath("//a[@class='col _checkBlock _rosRestrict']")
button.click()

#### 예약글 버튼 클릭
wait = WebDriverWait(driver, 10)
wait.until(EC.frame_to_be_available_and_switch_to_it((By.NAME,'mainFrame')))
driver.find_element_by_id('prePostLayerShower').click()


#### 마지막 예약글 테이블로 이동
#### 예약글들의 ID 뽑아오기 
element = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//a[@class='next_end']")))
element.click()
time.sleep(1)
elements = driver.find_elements_by_xpath("//*[@class='title _returnFalse _loadReserve _Se']")

#### 각 예약글들 위한 ID 리스트
IDlist = []

#### 예약글 테이블에서 모든 예약글들의 고유 ID를 가져와 저장.
for elem in elements:
	ID = elem.get_attribute("id")
	IDlist.append(ID)

IDlist.reverse()

### 다음 예약글 테이블로 버튼 클릭(5 -> 4)

element = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//*[@id='prepost_list_paging']/strong")))
page_num = int(element.text)
page_number = page_num

#### 현재에는, 예약글 테이블이 5페이지 이하인 경우만 작동됨이 확인. 
#### 5 페이지 이상일때 작동되는지 확인해봐야 함.
#### 모든 예약글의 고유 ID 가져오기 (4 -> 3 -> 2 -> 1)
while page_num > 1 :

	xpath = "//*[@id='prepost_list_paging']/a[{}]" .format(page_num)
	element = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, xpath)))
	element.click()

	time.sleep(1)
	elements = driver.find_elements_by_xpath("//*[@class='title _returnFalse _loadReserve _Se']")
	elements.reverse()

	for element in elements:
		ID = element.get_attribute("id")
		IDlist.append(ID)
		

	page_num = page_num - 1
	

print("예약된 글 개수 = {}" .format(len(IDlist)))


#### 마지막 예약글 테이블로 이동
element = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//a[@class='next_end']")))
element.click()
time.sleep(1)

### 글 URL 가져오기
for ID in IDlist:

	time.sleep(1)
	##### 이 부분에서 페이지 변경!
	try:
		WebDriverWait(driver, 2).until(EC.visibility_of_element_located((By.ID, ID))).click()
		
	except TimeoutException:
		xpath = "//*[@id='prepost_list_paging']/a[{}]" .format(page_number)
		element = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, xpath)))
		element.click()
		WebDriverWait(driver, 2).until(EC.visibility_of_element_located((By.ID, ID))).click()
		page_number = page_number - 1
	
	window_before = driver.window_handles[0]
	driver.switch_to_alert().accept()

	driver.switch_to_window(window_before)

	wait = WebDriverWait(driver, 10)
	wait.until(EC.frame_to_be_available_and_switch_to_it((By.NAME,'mainFrame')))

	element = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//a[@id='btn_preview']")))
	element.click()

	WebDriverWait(driver, 20).until(EC.number_of_windows_to_be(2))
	driver.switch_to.window(driver.window_handles[1])
	
	time.sleep(1)

	url = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//a[@class='fil5 pcol2']")))
	title = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//span[@class='pcol1 itemSubjectBoldfont']")))
	

	####성공!!!!!
	print("URL = %s TITLE = %s"%(url.text, title.text))

	driver.close()

	driver.switch_to_window(driver.window_handles[0])

	wait = WebDriverWait(driver, 10)
	wait.until(EC.frame_to_be_available_and_switch_to_it((By.NAME,'mainFrame')))
	driver.find_element_by_id('prePostLayerShower').click()



driver.quit()




#### 현재 예약글 URL 과 TITLE이 겹쳐서 나오는 경우가 있음.







