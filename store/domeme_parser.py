import re
import time
import random
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup as bs

class Domeme:
    driver = None

    def __init__(self):
        self.domeme_login()

    def driver_get(self, page_url):
        return_value = True
        try:
            self.driver.get(page_url)
        except TimeoutException:
            depth_print("도매매 사이트 출력 TimeoutException 발생")
            return_value = False
        self.rand_sleep()
        return return_value

    def domeme_login(self):
        depth_print("로그인 시도")
        self.options = webdriver.ChromeOptions()
        self.options.add_argument('--ignore-certificate-errors')
        self.options.add_argument('--ignore-ssl-errors')
        # self.options.page_load_strategy = 'none'
        self.driver = webdriver.Chrome(r'C:\Users\한치\mnec\store\chromedriver', chrome_options=self.options)
        # self.driver.set_page_load_timeout(100)
        # self.driver = webdriver.Chrome(r'C:\Users\한치\mnec\store\chromedriver')
        # driver = webdriver.PhantomJS('C:\Users\한치\mnec\store\phantomjs')

        self.driver_get('https://domemedb.domeggook.com/index/')
        self.js_click(self.driver_find_xpath('//*[@id="pup_topen"]/div[1]'), "7일간 보지않기 버튼")
        self.driver.find_element_by_xpath("//a[text()='로그인']").click()

        self.driver.find_element_by_name("id").send_keys('um0205')
        self.rand_sleep()
        self.driver.find_element_by_name("pass").send_keys('bu8232MxvxPQX!7')
        self.rand_sleep()
        self.driver.find_element_by_xpath('//*[@id="formLogin"]/input[7]').click()
        self.rand_sleep()
        depth_print("로그인 성공")

    def get_item_info(self, item_id, depth=0):
        depth_print("아이템 정보 요청 받음 ("+str(item_id)+")", depth=depth+1)
        self.driver_get('http://domeme.domeggook.com/s/'+str(item_id))
        soup = self.get_soup()

        if soup and not soup.select('#lEmpty'):
            item_dict = {}
            try:
                item_dict['name'] = soup.select('#lInfoItemTitle')[0].text
            except:
                item_dict['name'] = ""
            try:
                item_dict['price'] = soup.select('div.lItemPrice')[0].text
            except:
                item_dict['price'] = soup.select('td.lSelected')[0].text
            item_dict['domeme_price'] = item_dict['price'].replace('원','').replace(',','')
            item_dict['domeme_id'] = item_id

            recommand_tr = soup.select('#lInfoBody > div.lInfoBody.lInfoRow.lSelected > table > tbody > tr:nth-child(2)')
            recommand_th = recommand_tr[0].find_all('th')
            recommand_td = recommand_tr[0].find_all('td')
            if recommand_th[0].text == "준수조건":
                p = re.compile('최저단가\s+([0-9]+)')
                m = p.search(recommand_td[0].text.replace(',',''))
                if m and m.group():
                    depth_print(m.group(), depth=depth+1)
                    item_dict['domeme_row_price'] = float(m.group(1))
                else:
                    item_dict['domeme_row_price'] = -1
            else:
                item_dict['domeme_row_price'] = -1
            
            # option_names = soup.select('button.pSelectUIBtn')
            # option_prices = soup.select('button.pSelectUIBtn > label:nth-child(1)')

            # options = []
            # for index in range(len(option_names)):
            #     options.append([option_names[index], option_prices[index]])

            # item_dict['options'] = options

            return item_dict
        else:
            return None

    def get_item_list(self, domemeno_list):
        item_list = []
        for domemeno in domemeno_list:
            item_list.append(get_item_info(domemeno))
        return item_list
        
    def smart_send_item_db(self):
        self.driver_get('https://domemedb.domeggook.com/index/item/safeDbList.php?folder=default')
        self.driver.find_element_by_xpath('//*[@id="allSel"]/label').click()
        self.rand_sleep()
        self.driver_get('https://domemedb.domeggook.com/index/popup_sender/popup_setBulkProduct.php?i_type=safeDown')
        self.driver.find_element_by_xpath('//*[@id="mkForm"]').submit()
        self.rand_sleep()

        soup = self.get_soup()
        if soup:
            send_list = soup.select('#swList > table > tbody > tr')

            self.driver.find_element_by_xpath('/html/body/div/div[1]/div/div[3]/div[7]/button').click()
            self.rand_sleep()
            return True
        else:
            return False
        
    def rand_sleep(self):
        return time.sleep(random.random() * 1 + 1)

    def goto_soldout_page(self):
        self.driver_get('https://domemedb.domeggook.com/index/sender/sender_productList.php?&status=SOLDOUT')

    def soldout_list(self):
        self.goto_soldout_page()

        soup = self.get_soup()
        if soup:
            name_list = soup.select('#mkForm > table > tbody > tr:nth-child(even) > td:nth-child(3) > div.main_cont_text1.b > a')
            price_list = soup.select('#mkForm > table > tbody > tr:nth-child(even) > td:nth-child(3) > div:nth-child(4) > strong')
            domeme_id = soup.select('#mkForm > table > tbody > tr:nth-child(even) > td:nth-child(6)')
            domeme_status = soup.select('#mkForm > table > tbody > tr:nth-child(even) > td:nth-child(7) > span')
            store_no = soup.select('#mkForm > table > tbody > tr:nth-child(odd) > td.al')
        else:
             ('데이터 리스트를 가져오지 못함')

        soldout_list = []
        for index in range(len(name_list)):
            soldout_dict = {}
            soldout_dict['name'] = name_list[index].text
            soldout_dict['price'] = price_list[index].text
            soldout_dict['domeme_id'] = domeme_id[index].text[4:]
            soldout_dict['domeme_status'] = domeme_status[index].text
            soldout_dict['store_no'] = store_no[index].text
            soldout_list.append(soldout_dict)

        return soldout_list

    def clear_soldout(self):
        self.goto_soldout_page()
        self.driver.find_element_by_xpath('//*[@id="mkForm"]/table/tbody/tr[1]/th[1]/div/label').click()
        self.rand_sleep()
        self.driver.find_element_by_xpath('/html/body/div[1]/div[2]/table/tbody/tr/td/button[2]').click()
        self.rand_sleep()
        alert = self.driver.switch_to.alert
        alert.accept()
        self.rand_sleep()
        alert = self.driver.switch_to.alert
        alert.accept()
        self.rand_sleep()

    def get_soup(self, depth=0):
        result = None
        try:
            result = bs(self.driver.page_source, 'html.parser')
        except TimeoutException:
            depth_print(self.driver.page_source, depth=depth+1)
        return result

    def driver_find_xpath(self, target):
        try:
            element = self.driver.find_element_by_xpath(target)
        except:
            element = None
        return element

    def js_click(self, element, text=None, depth=0):
        if element:
            if text:
                depth_print(text+" 클릭", depth=depth+1)
            self.driver.execute_script("arguments[0].click();", element)
            self.rand_sleep()
        
def depth_print(input_str, depth=0):
    indent = ""
    for i in range(depth):
        indent += "  "
    print(indent + "[Domeme] " + input_str)

if __name__ == "__main__":
    domeme = Domeme()
    domeme.smart_send_item_db()


# import requests
# import re

# LOGIN_INFO = {
#     'id': 'um0205',
#     'pass': 'bu8232MxvxPQX!7',
#     'save': '1',    
# }

# with requests.Session() as session:
#     main_page = session.get('https://domemedb.domeggook.com/index/', verify=False)
#     html = main_page.text
#     soup = bs(html, 'html.parser')
#     login_url = soup.select('#loggedOut1_1 > a')[0].get('href')
#     print(login_url)

#     regex = re.compile('\?back=(?P<back>\S+)')
#     matchobj = regex.search(login_url)
#     back = matchobj.group("back")

#     login_page = session.get('http://domeme.domeggook.com/main/member/mem_formLogin.php?back='+back)
#     html = login_page.text
#     soup = bs(html, 'html.parser')
    
#     LOGIN_INFO = {**LOGIN_INFO, **{'back': back}}
#     print(LOGIN_INFO)

#     login_req = session.post('https://domeggook.com/main/member/mem_ing.php', data=LOGIN_INFO)
#     print(login_req.status_code)

#     req = session.get('http://domeme.domeggook.com/s/10225500')
#     req.encoding = 'euc-kr'

#     html = req.text
#     header = req.headers
#     status = req.status_code
#     is_ok = req.ok

#     soup = bs(html, 'html.parser')

#     price = soup.select('#lInfoBody > div.lInfoBody.lInfoRow.lSelected > table > tbody > tr.lInfoAmt > td > div > div')
#     for p in price:
#         print(p.text)