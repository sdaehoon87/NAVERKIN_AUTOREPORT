from selenium import webdriver
import pymysql
import time

con = pymysql.connect(host='localhost',
                      user='songking',
                      password='3779aa',
                      db='kinauto',
                      charset='utf8')
cur = con.cursor()  # 디비 커서

kin_url = 'https://kin.naver.com/qna/detail.nhn?d1id=4&dirId=4010506&docId=337605299&qb=66y07KeB7J6Q64yA7Lac&enc=utf8&section=kin&rank=4&search_sort=0&spq=0'
num = str(7)

kin_url = kin_url.split('&')
kin_url =(kin_url[0] +'&' +kin_url[1] + '&' + kin_url[2])
print(kin_url)

idchlist = []
cur.execute("SELECT idname FROM reportlist WHERE kinurl = %s",(kin_url,))
for i in cur.fetchall():
    idchlist.append(i[0])
print(idchlist)

try:
    cur.execute("SELECT id,pw FROM idlist WHERE NOT id IN ({seq})".format(seq=','.join(['%s']*len(idchlist))), idchlist)
except:
    cur.execute("SELECT id,pw FROM idlist")
idlist = cur.fetchall()

driver = webdriver.Chrome('./chromedriver.exe')
for i in idlist:
    driver.get('https://nid.naver.com/nidlogin.login')
    time.sleep(0.5)
    driver.execute_script("document.getElementsByName('id')[0].value=\'" + i[0] + "\'")
    driver.execute_script("document.getElementsByName('pw')[0].value=\'" + i[1] + "\'")
    driver.find_element_by_xpath('//*[@id="frmNIDLogin"]/fieldset/input').click()
    time.sleep(0.5)
    print(i[0])
    naverurl = driver.current_url
    if 'https://nid.naver.com/nidlogin.login' in naverurl:
        print('id, pw틀림')
        continue
    if 'https://nid.naver.com/user2/help/idRelease' in naverurl:
        print('대량생성 아이디')
        continue
    if 'https://nid.naver.com/user2/help/idSafetyRelease' in naverurl:
        print('삭제 이용 제한 아이디')
        continue

    driver.get(kin_url)
    driver.find_element_by_xpath('//*[@id="answerMenuButton{}"]'.format(num)).click()
    driver.find_element_by_xpath('//*[@id="optReport{}"]'.format(num)).click()
    time.sleep(0.5)
    driver.switch_to.window(driver.window_handles[-1])
    driver.find_element_by_xpath('//*[@id="reason0"]').click()
    time.sleep(0.5)
    driver.find_element_by_xpath('//*[@id="au_pop_footer"]/input').click()
    cur.execute("INSERT INTO reportlist (kinurl, idname) VALUES (%s,%s)", (kin_url,i[0]))
    con.commit()
    driver.close()
    driver.switch_to.window(driver.window_handles[0])