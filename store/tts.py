import time
import random
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from bs4 import BeautifulSoup as bs

class Tts:
    driver = None

    url_state = -1

    STATE_KEYWORD_PAGE = 0

    KEYWORD_URL = 'https://text-to-speech.imtranslator.net/speech.asp?dir=ko'

    def __init__(self):
        self.tts_login()

    def tts_login(self, depth=0):
        self.driver = webdriver.Chrome(r'C:\Users\한치\mnec\store\chromedriver')
        return True

    def tts_execute(self, text):
        self.driver.get(KEYWORD_URL)
        textarea_element = self.driver.driver_find_xpath('//*[@id="text"]')
        self.clear_and_send_element(textarea_element, text)
        self.js_click_with_xpath('//*[@id="ttsgo"]')

    def driver_find_xpath(self, target, target_name="", try_count=1, depth=0):
        for i in range(int(try_count)):
            if i > 0:
                if target_name:
                    naver_depth_print("driver_find_xpath 함수가 "+target_name+"을 "+str(i)+"번째 찾는중", depth=depth+1)
                else:
                    naver_depth_print("driver_find_xpath 함수가 "+target+"을 "+str(i)+"번째 찾는중", depth=depth+1)
            element = None
            try:
                element = self.driver.find_element_by_xpath(target)
                break
            except NoSuchElementException:
                element = None
            except UnexpectedAlertPresentException:
                # 아래의 swtich_to.alert에서 아직 alert창을 찾지못해서 NoAlertPresentException이 발생함
                # 해결하기위해서 WebDriverWait을 사용해서 alert창을 기다려보기로 함
                self.check_alert_and_accept(depth=depth+1)
            except NoAlertPresentException:
                naver_depth_print("NoAlertPresentException occur", depth=depth+1)
            time.sleep(0.5)
        if not element:
            if target_name:
                naver_depth_print("driver_find_xpath 함수가 "+target_name+"을 찾지못함", depth=depth+1)
            else:
                naver_depth_print("driver_find_xpath 함수가 "+target+"을 찾지못함", depth=depth+1)
        return element

    def clear_and_send_element(self, element, input_str, target_name=None, depth=0):
        if element:
            if target_name:
                naver_depth_print(target_name+" 비우고 내용 '"+input_str+"' 보냄", depth=depth+1)
            element.clear()
            self.rand_sleep()
            element.send_keys(str(input_str))
            self.rand_sleep()

    def js_click_with_xpath(self, xpath, target_name=None, depth=0, try_count=-1):
        naver_depth_print("js_click_with_xpath call", depth=depth+1)
        result = False
        count = 0
        while 1:
            naver_depth_print(str(count+1)+" try", depth=depth+1)
            element = self.driver_find_xpath(xpath, target_name=target_name, depth=depth+1)
            if element:
                self.js_click(element, target_name=target_name, depth=depth+1)
                return True 
            count = count + 1
            if try_count > 0:
                if count > try_count:
                    return False
                    
    def js_click(self, element, target_name=None, depth=0):
        result = False
        if element:
            self.driver.execute_script("arguments[0].click();", element)
            self.rand_sleep()
            result = True
        if target_name:
            naver_depth_print(target_name+" 클릭 ("+str(result)+")", depth=depth+1)
        return result

if __name__ == "__main__":
    # naver = Naver()
    # domeme = Domeme()

    # i = 0
    # unset_list = naver.get_sale_unset_item_list()
    # for item in unset_list:
    #     print("아이템 "+str(i)+"/"+str(len(unset_list)))
    #     naver.set_price(item, domeme.get_item_info(item_dict['domeme_id']))
    #     i = i + 1
    calc_price(41100)

