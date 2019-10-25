from selenium import webdriver
from selenium.webdriver.common.alert import Alert
import pymysql
import time

con = pymysql.connect(host='121.143.107.49',
                      user='songking',
                      password='3779aa',
                      db='kinauto',
                      charset='utf8')
cur = con.cursor()  # 디비 커서
cur.execute("SELECT id,pw FROM idlist")
idlist = cur.fetchall()

for i in idlist:
    driver = webdriver.Chrome('./chromedriver.exe')
    driver.get('https://nid.naver.com/nidlogin.login')
    time.sleep(0.5)
    driver.execute_script("document.getElementsByName('id')[0].value=\'" + i[0] + "\'")
    driver.execute_script("document.getElementsByName('pw')[0].value=\'" + i[1] + "\'")
    driver.find_element_by_xpath('//*[@id="frmNIDLogin"]/fieldset/input').click()
    time.sleep(0.5)
    driver.get('https://kin.naver.com/qna/detail.nhn?d1id=4&dirId=4010506&docId=337604773&qb=66y07KeB7J6Q64yA7Lac&enc=utf8&section=kin&rank=1&search_sort=0&spq=0')
    driver.find_element_by_xpath('//*[@id="answerMenuButton1"]').click()
    driver.find_element_by_xpath('//*[@id="optReport1"]').click()
    print(driver.window_handles)
    driver.switch_to.window(driver.window_handles[-1])
    time.sleep(3)
    try:
        driver.find_element_by_xpath('//*[@id="reason0"]').click()
        time.sleep(3)
        driver.find_element_by_xpath('//*[@id="au_pop_footer"]/input').click()
        driver.close()
    except:
        time.sleep(3)
        da = Alert(driver)
        da.accept()
        driver.close()

    break