from selenium import webdriver
import pymysql
import time

con = pymysql.connect(host='121.143.107.49',
                      user='songking',
                      password='3779aa',
                      db='kinauto',
                      charset='utf8')
cur = con.cursor()  # 디비 커서

kin_url = 'https://kin.naver.com/qna/detail.nhn?d1id=4&dirId=4010503&docId=329909070&qb=7ZaH7IK066Gg&enc=utf8&section=kin&rank=1&search_sort=0&spq=0'


kin_url = kin_url.split('&')
kin_url =(kin_url[0] +'&' +kin_url[1] + '&' + kin_url[2])
print(kin_url)

idchlist = []
cur.execute("SELECT idname FROM reportlist WHERE kinurl = %s",(kin_url,))
for i in cur.fetchall():
    idchlist.append(i[0])
print(idchlist)

cur.execute("SELECT id,pw FROM idlist WHERE NOT id IN ({seq})".format(seq=','.join(['%s']*len(idchlist))), idchlist)
idlist = cur.fetchall()

driver = webdriver.Chrome('./chromedriver.exe')
for i in idlist:
    driver.get('https://nid.naver.com/nidlogin.login')
    time.sleep(0.5)
    driver.execute_script("document.getElementsByName('id')[0].value=\'" + i[0] + "\'")
    driver.execute_script("document.getElementsByName('pw')[0].value=\'" + i[1] + "\'")
    driver.find_element_by_xpath('//*[@id="frmNIDLogin"]/fieldset/input').click()
    time.sleep(0.5)
    driver.get('https://kin.naver.com/qna/detail.nhn?d1id=4&dirId=4010503&docId=329909070&qb=7ZaH7IK066Gg&enc=utf8&section=kin&rank=1&search_sort=0&spq=0')
    driver.find_element_by_xpath('//*[@id="answerMenuButton4"]').click()
    driver.find_element_by_xpath('//*[@id="optReport4"]').click()
    print(i[0])
    time.sleep(0.5)
    driver.switch_to.window(driver.window_handles[-1])
    driver.find_element_by_xpath('//*[@id="reason0"]').click()
    time.sleep(0.5)
    driver.find_element_by_xpath('//*[@id="au_pop_footer"]/input').click()
    cur.execute("INSERT INTO reportlist (kinurl, idname) VALUES (%s,%s)", (kin_url,i[0]))
    con.commit()
    driver.close()
    driver.switch_to.window(driver.window_handles[0])