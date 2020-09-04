import sys
import time
import random
from pygame import mixer
from contextlib import suppress
from selenium import webdriver
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, UnexpectedAlertPresentException, NoAlertPresentException, TimeoutException
from bs4 import BeautifulSoup as bs
from selenium.webdriver.common.keys import Keys

class Naver:
    driver = None
    is_mixer_init = False

    url_state = -1
    url_edit_id = -1

    STATE_NONE = 0
    STATE_LOGIN_PAGE = 1
    STATE_EDIT_PAGE = 2

    LOGIN_URL = 'https://sell.smartstore.naver.com/#/login'
    LOGIN_BUTTON_XPATH = '//*[@id="log.login"]'
    LOGIN_NAVER_ID_LOGIN_BUTTON_XPATH = '/html/body/ui-view[1]/div[3]/div/div/div/form/div[1]/ul/li[2]/a'

    ORIGIN_SALE_PRICE_OFFSET = 970

    ORIGIN_ITEM_ID_TEXTAREA_XPATH = '//*[@id="seller-content"]/ui-view/div/ui-view[1]/div[2]/form/div[1]/div/ul/li[1]/div/div/div[2]/textarea'
    ORIGIN_ITEM_SEARCH_BUTTON_XPATH = '//*[@id="seller-content"]/ui-view/div/ui-view[1]/div[2]/form/div[2]/div/button[1]'
    ORIGIN_ITEM_MODIFY_BUTTON_XPATH = '//*[@id="seller-content"]/ui-view/div/ui-view[2]/div[1]/div[2]/div[3]/div/div/div/div/div[3]/div[1]/div/div[2]/span/button'

    def __init__(self):
        self.naver_login()

    def play_sound(self, file_path):
        if self.is_mixer_init is False:
            mixer.init()
            self.is_mixer_init = True
        mixer.music.load(file_path)
        mixer.music.play()

    def set_url_state(self, state, edit_id=-1):
        url_state = state
        url_edit_id = edit_id

    def driver_get(self, page_url, depth=0, sleep_time=3):
        naver_depth_print(str(page_url)+" 주소로 페이지 이동 시도")
        return_value = True
        try:
            if page_url == self.driver.current_url:
                self.driver.refresh()
            else:
                self.driver.get(page_url)
        except TimeoutException:
            print("네이버 페이지 타임 아웃 발생")
            # self.driver.send_keys(Keys.ESCAPE)
            return_value = False
        except UnexpectedAlertPresentException:
            # 아래의 swtich_to.alert에서 아직 alert창을 찾지못해서 NoAlertPresentException이 발생함
            # 해결하기위해서 WebDriverWait을 사용해서 alert창을 기다려보기로 함
            self.check_alert_and_accept(depth=depth+1)
            self.driver.get(page_url)
        self.rand_sleep(default=sleep_time)
        return return_value

    def naver_login(self, depth=0):
        naver_depth_print("로그인 시도")
        self.options = webdriver.ChromeOptions()
        self.options.add_argument('--ignore-certificate-errors')
        self.options.add_argument('--ignore-ssl-errors')
        # self.options.page_load_strategy = 'eager'
        self.driver = webdriver.Chrome(r'C:\Users\한치\mnec\store\chromedriver', chrome_options=self.options)
        # self.driver = webdriver.Chrome(r'C:\Users\한치\mnec\store\chromedriver')
        # self.driver.DesiredCapabilities.Chrome["unexpectedAlertBehaviour"] = "accept"
        # driver = webdriver.PhantomJS('C:\Users\한치\mnec\store\phantomjs')
        position = self.driver.get_window_position() # returns {'y', 'x'} coordinates
        self.driver.set_window_position(position['x'] + 1280, position['y'])

        self.driver_get(self.LOGIN_URL)
        self.set_url_state(self.STATE_LOGIN_PAGE)
        self.rand_sleep()
        self.driver_find_xpath(self.LOGIN_NAVER_ID_LOGIN_BUTTON_XPATH).click()
        self.rand_sleep()
        self.driver_find_name("id", depth=depth+1).send_keys('um0205')
        self.rand_sleep()
        self.driver_find_name("pw", depth=depth+1).send_keys('2hZQ8LBh.w^fTKq')
        self.rand_sleep()
        self.driver_find_xpath(self.LOGIN_BUTTON_XPATH).click()
        self.rand_sleep()

    def search_with_domeme_id(self, item_dict, depth=0):
        naver_depth_print("get_naver_id_from_domeme_id call (domeme_id:"+str(item_dict['domeme_id'])+")", depth=depth+1)
        self.goto_product_list(depth=depth+1)
        self.js_click_with_xpath('//*[@id="seller-content"]/ui-view/div/ui-view[1]/div[2]/form/div[1]/div/ul/li[1]/div/div/div[1]/div/div[2]/label/input', target_name='판매자상품코드 라디오 버튼', depth=depth+1)
        self.send_element(self.driver_find_xpath(self.ORIGIN_ITEM_ID_TEXTAREA_XPATH), str(item_dict['domeme_id']), "도매매 아이템 번호 "+str(item_dict['domeme_id']), depth=depth+1)
        self.js_click_with_xpath(self.ORIGIN_ITEM_SEARCH_BUTTON_XPATH, target_name="아이템 검색 버튼", depth=depth+1)

    def get_naver_id_from_domeme_id(self, item_dict, depth=0):
        self.search_with_domeme_id(item_dict, depth=depth+1)
        naver_ids = self.selectStorefarmChannelProductNoInOriginList()
        assert len(naver_ids) > 0
        naver_depth_print("최상단 네이버 상품 번호: "+str(naver_ids[0]))
        item_dict['naver_id'] = naver_ids[0]

    def set_main_category(self, item_dict, depth=0):
        new_item_dict = item_dict.copy()

        assert new_item_dict is not item_dict

        self.search_item(new_item_dict)
        result = False
        while not result:
            no_data_element = self.driver_find_xpath('//*[@id="seller-content"]/ui-view/div/ui-view[2]/div[1]/div[2]/div[3]/div/div/div/div/div[6]/div/div/div/p', depth=depth+1)
            if no_data_element and no_data_element.text == "데이터가 존재하지 않습니다.":
                naver_depth_print("삭제된 아이템 복사 중단", depth=depth+1)
                break
            copy_button_element = self.driver_find_xpath('//*[@id="seller-content"]/ui-view/div/ui-view[2]/div[1]/div[2]/div[3]/div/div/div/div/div[3]/div[1]/div[1]/div[3]/span/button', depth=depth+1, target_name="복사 버튼")
            if copy_button_element:
                result = True
                self.js_click(copy_button_element, '복사 버튼', depth=depth+1)
                self.js_click(self.driver_find_xpath('/html/body/div[1]/div/div/div[3]/div/button'), "KC인증 확인 버튼", depth=depth+1)

        # 복사 버튼 클릭 성공
        if result == True:
            new_item_dict['naver_edit_id'] = self.get_edit_id_from_url()
            self.js_click_with_xpath('//*[@id="productForm"]/ng-include/ui-view[3]/div/div[2]/div/div/div/category-search/div[1]/div[1]/div/label[2]', target_name='카테고리명 선택', depth=depth+1)
            (result, new_item_dict) = self.set_category_in_item_page(new_item_dict, depth=depth+1, start_index=0)
            if result == 1:
                naver_depth_print("원본 아이템 제거", depth=depth+1)
                self.save_item_page(depth=depth+1, try_count=5)

                cert_category = self.driver_find_xpath('/html/body/div[1]/div/div/div[2]/div[2]/strong', target_name='인증 필수 카테고리', depth=depth+1)
                if cert_category:
                    naver_depth_print("인증 실패로 관련 아이템 전체 제거", depth=depth+1)
                    return (-1, new_item_dict)
                else:
                    self.js_click_with_xpath('//*[@id="seller-content"]/ui-view/div/ui-view[2]/div[1]/div[2]/div[1]/div[1]/div/div[1]/button', target_name='선택 삭제', depth=depth+1)
                    self.js_click_with_xpath('/html/body/div[1]/div/div/div[2]/div/span[2]/button', target_name='삭제 확인', depth=depth+1)
                    self.js_click_with_xpath('/html/body/div[1]/div/div/div[1]/button', target_name='일괄변경 결과 닫기', depth=depth+1)
                    self.get_naver_id_from_domeme_id(new_item_dict, depth=depth+1)
                return (True, new_item_dict)
            elif result == -1:
                naver_depth_print("관련 아이템 전체 제거", depth=depth+1)
                return (result, new_item_dict)
            else:
                new_item_dict = None
                self.cancel_item_page(depth=depth+1)
                return (0, new_item_dict)
        else:
            new_item_dict = None
            return (0, new_item_dict)

    def set_category_in_item_page_with_data(self, score_str, category_str, start_index=1, depth=0):
        recommand_category_string = category_str.split('>')
        category_score = format(int(score_str), "04d")

        modify = False
        for index in range(4):
            if index < start_index:
                continue #대분류는 복사해서 새로 생성해야함
            elif len(recommand_category_string) < index + 1:
                category_tab = self.driver_find_xpath('//*[@id="productForm"]/ng-include/ui-view[3]/div/div[2]/div/div[1]/div/category-search/div[3]/div['+str(index+1)+']/ul', target_name=(str(index+1)+"번째 분류탭"), try_count=5, depth=depth+1)
                tab_category_elements = category_tab.find_elements(By.TAG_NAME, 'a')
                if len(tab_category_elements) == 1 and tab_category_elements[0].text == '세분류':
                    return 1
                else:
                    return 0
            else:
                # 상위 분류가 변경되면 하위도 새로 세팅해야되는 경우가 대부분임. 
                # 세팅을 시작했으면 하위도 다 세팅함.
                if int(category_score[index]) > 0 or modify: 
                    modify = True
                    category_tab = self.driver_find_xpath('//*[@id="productForm"]/ng-include/ui-view[3]/div/div[2]/div/div[1]/div/category-search/div[3]/div['+str(index+1)+']/ul', target_name=(str(index+1)+"번째 분류탭"), try_count=5, depth=depth+1)
                    tab_category_elements = category_tab.find_elements(By.TAG_NAME, 'a')
                    for e in tab_category_elements:
                        if e.text == recommand_category_string[index]:
                            self.js_click(e, str(index+1)+"번째 탭의 "+e.text+" 카테고리", depth=depth+1)
            category_permission = self.driver_find_xpath('/html/body/div/div/div/div[1]/p[2]/strong', target_name='카테고리 등록권한창', try_count=5, depth=depth+1)
            if category_permission:
                print(category_permission.text)
            if category_permission:
                self.js_click_with_xpath('/html/body/div/div/div/div[1]/button/span', target_name='권한창 닫기', depth=depth+1)
                self.js_click_with_xpath('//*[@id="seller-content"]/ui-view/div[3]/div[2]/div[2]/button', target_name='취소 버튼', depth=depth+1)
                self.check_alert_and_accept(depth=depth+1)
                return -1
        return 1

    def driver_get_text_with_xpath(target, target_name='', try_count=1, depth=0):
        element = self.driver_find_xpath(target, target_name=target_name, try_count=try_count, depth=depth+1)
        if element:
            return element.text
        else:
            return ''

    def set_category_in_item_page(self, item_dict, depth=0, start_index=1):
        naver_depth_print("set_category_in_item_page call", depth=depth+1)

        result = self.set_category_in_item_page_with_data(item_dict['category_score'], item_dict['category_recommand'], start_index=start_index, depth=depth+1)
        if result == 1:
            naver_depth_print("추천 카테고리 성공", depth=depth+1)
            item_dict['category_score'] = 0
            item_dict['category_current'] = item_dict['category_recommand']
            return (1, item_dict)
        else:
            naver_depth_print("추천 카테고리 실패 ("+str(result)+")", depth=depth+1)
            if result == -1:
                return (-1, None)
                    
        for category in item_dict['category_list']:
            if category == item_dict['category_recommand']:
                naver_depth_print('추천 카테고리로 사용됨', depth=depth+1)
                continue
            else:
                result = self.set_category_in_item_page_with_data("9999", category, start_index=start_index, depth=depth+1)
                if result == 1:
                    item_dict['category_score'] = 0
                    item_dict['category_current'] = category
                    return (1, item_dict)
                else:
                    naver_depth_print("카테고리 실패 ("+str(result)+")", depth=depth+1)
                    if result == -1:
                        return (-1, None)
        return (0, None)                

    def set_recommand_category(self, item_dict, depth=0):
        naver_depth_print("set_recommand_category 콜", depth=depth+1)
        result = True
        (temp_result, item_dict) = self.goto_item_page(item_dict, depth=0)
        result = result and temp_result

        if item_dict and self.set_category_in_item_page(item_dict, depth=depth+1, start_index=1) == 1:          
            self.get_category_data_list(item_dict, depth=depth+1)
            self.save_item_page(depth=depth+1)
            return (result, item_dict)
        else:
            return (False, None)

    def get_category_data_list(self, item_dict, depth=0):
        naver_depth_print('get_category_data_list call', depth=depth+1)
        category_strong_element = self.driver_find_xpath('//*[@id="productForm"]/ng-include/ui-view[3]/div/div[2]/div/div[1]/div/p[1]/strong', try_count=10)
        if category_strong_element:
            #naver_depth_print(category_strong_element.text, depth=depth+1)
            category_list = category_strong_element.text.split('>')
            #naver_depth_print(str(category_list), depth=depth+1)
            item_dict['naver_category'] = category_list
        else:
            item_dict['naver_category'] = None
        naver_depth_print('get_category_data_list result: '+str(item_dict['naver_category']), depth=depth+1)

    def get_category(self, item_dict, depth=0, with_save=True):
        naver_depth_print("get_category 콜", depth=depth+1)
        result = True
        (temp_result, item_dict) = self.goto_item_page(item_dict, depth=depth+1)
        result = result and temp_result

        if result and item_dict:
            self.get_category_data_list(item_dict, depth=depth+1)
            if with_save:
                self.save_item_page(depth=depth+1)

        naver_depth_print("get_category result: "+str((True, item_dict)), depth=depth+1)
        return (True, item_dict)

    def get_item_list(self, depth=0, load_page=0, load_count=0):
        self.goto_product_list(depth=depth+1)
        
        page = 1
        target_page = 1
        total_list = []
        total_domeme_ids = []
        if self.get_pagenation_element(11):
            target_page = 11
            naver_depth_print("오른쪽 다음 페이지 버튼이 존재해서 반복적으로 수행", depth=depth+1)
        while self.get_pagenation_element(target_page):
            if load_page != 0 and page != load_page:
                page = page + 1
                continue

            if page > 1:
                self.js_click(self.get_pagenation_element(target_page), "페이지 "+str(target_page)+" 버튼")
            else:
                naver_depth_print(str(page)+ " 페이지 처리 시작", depth=depth+1)

            tab = 1
            naver_depth_print("페이지 "+str(page)+" 탭 "+str((tab))+" 데이터 로드", depth=depth+1)
            data_count = self.scroll_down_to_next_data(len(total_list), depth=depth+1)
            if data_count == 0:
                break
            self.append_no_and_price_pair(total_domeme_ids, total_list)
            naver_depth_print("로드된 데이터 수: "+str(len(total_list)), depth=depth+1)  
            tab = tab + 1

            last_count = len(total_list)
            while tab <= 5:
                naver_depth_print("페이지 "+str(page)+" 탭 "+str((tab))+" 데이터 로드", depth=depth+1)
                data_count = self.scroll_down_to_next_data(len(total_list), depth=depth+1)
                if data_count == 0:
                    break
                self.append_no_and_price_pair(total_domeme_ids, total_list)
                naver_depth_print("로드된 데이터 수: "+str(len(total_list)), depth=depth+1)
                tab = tab + 1
                
            if load_count != 0 and load_count < len(total_list):
                break

            if load_page != 0 and page == load_page:
                break

            page = page + 1

            if target_page == 11 and page > 2:
                target_page = 12

        naver_depth_print("seller sale price unsetted list count:" + str(len(total_list)), depth=depth+1)

        return total_list

    def get_sale_unset_item_list(self, except_list=[], depth=0, page=0, load_count=0):
        total_list = self.get_item_list(depth=depth+1, load_page=page, load_count=load_count)

        unset_list = []
        dup_count = 0
        count = 0
        for item in total_list:
            if int(item['domeme_id']) in except_list:
                dup_count = dup_count + 1
            else:
                unset_list.append(item)
                count = count + 1
        
        naver_depth_print("total count = "+str(count) + " dup count: "+str(dup_count), depth=depth+1)

        return unset_list

    def naver_info_list_to_dict(self, title, domeme_id, naver_id, naver_price, naver_sale):
        return {'title':str(title),
                'domeme_id':str(domeme_id), 
                'domeme_price':0, # str(domeme_prices[index]), 
                'naver_id':str(naver_id),
                'naver_price':self.replace_price(str(naver_price)),
                'naver_sale':self.replace_price(str(naver_sale))}

    def get_origin_info_list(self):
        domeme_ids = self.selectSellerManagementCodeInOriginList()
        naver_ids = self.selectStorefarmChannelProductNoInOriginList()
        titles = self.selectItemTitleInOriginList()
        naver_prices = self.selectSalePriceInOriginList()
        naver_sales = self.selectSellerImmediateDiscountInOriginList()
        return (titles, domeme_ids, naver_ids, naver_prices, naver_sales)

    def append_no_and_price_pair(self, check_list, unset_list):
        (titles, domeme_ids, naver_ids, naver_prices, naver_sales) = self.get_origin_info_list()
        
        for index in range(len(domeme_ids)):
            if not domeme_ids[index] in check_list:
                item_dict = self.naver_info_list_to_dict(titles[index], domeme_ids[index], naver_ids[index], naver_prices[index], naver_sales[index])
                unset_list.append(item_dict)
                check_list.append(domeme_ids[index])

    def scroll_down_to_next_data(self, last_index, depth=0):
        scroll_gap = 800
        scroll_top = 40 * (last_index % 100)
        scroll_dir = 0

        start_index = last_index
        end_index = last_index + 20
        naver_depth_print("target index "+str(start_index)+" ~ "+str(end_index), depth=depth+1)

        success_count = 0

        max_top = 0
        max_count = 0

        while scroll_gap > 10:
            scroll_top = scroll_top + (scroll_gap * scroll_dir)
            self.scroll_down_in_origin_list(scroll_top, depth=depth+1)

            temp_dir = 0
            success_count = 0
            for row in self.selectLeftContainerInOriginList():
                if start_index > int(row['row-id']):
                    temp_dir = 1
                elif end_index < int(row['row-id']):
                    temp_dir = -1
                else:
                    success_count = success_count + 1
                

            if success_count > max_count:
                max_top = scroll_top
                max_count = success_count
            else:
                if temp_dir != 0:
                    scroll_dir = temp_dir
                scroll_gap = scroll_gap / 2

            if success_count >= 20:
                break

        if max_top != scroll_top:
            self.scroll_down_in_origin_list(max_top, depth=depth+1)

        return max_count
        

    def scroll_down_in_origin_list(self, top, depth=0):
        naver_depth_print("origin list top:"+str(top), depth=depth+1)
        self.driver.execute_script('document.querySelector("#seller-content > ui-view > div > ui-view:nth-child(2) > div.panel.panel-seller > div.panel-body > div.seller-grid-area > div > div > div > div > div.ag-body-viewport.ag-layout-normal.ag-row-no-animation").scrollTop = ' + str(top))
        time.sleep(3)

    def scrollLeft(self, left_offset):
        while self.driver_find_xpath('//*[@id="seller-content"]/ui-view/div/ui-view[2]/div[1]/div[2]/div[3]/div/div/div/div/div[5]/div[2]', "수평 스크롤바") is None:
            time.sleep(1)
        self.driver.execute_script('document.querySelector("#seller-content > ui-view > div > ui-view:nth-child(2) > div.panel.panel-seller > div.panel-body > div.seller-grid-area > div > div > div > div > div.ag-body-horizontal-scroll > div.ag-body-horizontal-scroll-viewport").scrollLeft = '+str(left_offset))
        self.rand_sleep()

    def replace_price(self, price):
        return price.replace('원','').replace(',','')

    def selectSalePriceInOriginList(self):
        self.scrollLeft(self.ORIGIN_SALE_PRICE_OFFSET)
        sale_price_list = []
        for div in self.selectRightContainerInOriginList("salePrice"):
            sale_price_list.append(self.replace_price(div.get_text()))
        return sale_price_list

    def selectItemTitleInOriginList(self):
        self.scrollLeft(80)
        title_list = []
        for div in self.selectRightContainerInOriginList("productName"):
            title_list.append(div.get_text())
        return title_list

    def selectSellerImmediateDiscountInOriginList(self):
        self.scrollLeft(1190)
        seller_immediate_discount_list = []
        for div in self.selectRightContainerInOriginList("sellerImmediateDiscount"):
            for a in div.find_all("a"):
                seller_immediate_discount_list.append(self.replace_price(a.get_text()))
        return seller_immediate_discount_list

    def selectStorefarmChannelProductNoInOriginList(self):
        storefarm_channel_product_no_list = []
        for div in self.selectLeftContainerInOriginList("storefarmChannelProductNo"):
            for a in div.find_all("a"):
                storefarm_channel_product_no_list.append(a.get_text())
        return storefarm_channel_product_no_list

    def selectSellerManagementCodeInOriginList(self):
        seller_management_code_list = []
        for div in self.selectLeftContainerInOriginList("sellerManagementCode"):
            seller_management_code_list.append(div.get_text())
        return seller_management_code_list

    def selectRightContainerInOriginList(self, col_id=None):
        soup = self.get_soup()
        if col_id:
            return soup.find_all(class_="ag-cell", attrs={"col-id": str(col_id)})
        else:
            return soup.select('#seller-content > ui-view > div > ui-view:nth-child(2) > div.panel.panel-seller > div.panel-body > div.seller-grid-area > div > div > div > div > div.ag-body-viewport.ag-layout-normal.ag-row-no-animation > div.ag-center-cols-clipper > div > div > div.ag-row')
        
    def selectLeftContainerInOriginList(self, col_id=None):
        soup = self.get_soup()
        if col_id:
            return soup.find_all(class_="ag-cell", attrs={"col-id": str(col_id)})
        else:
            return soup.select('#seller-content > ui-view > div > ui-view:nth-child(2) > div.panel.panel-seller > div.panel-body > div.seller-grid-area > div > div > div > div > div.ag-body-viewport.ag-layout-normal.ag-row-no-animation > div.ag-pinned-left-cols-container > div.ag-row')

    def soup_test_print(self, file_name, soup_list):
        i = 0
        f = open(file_name, 'w', encoding='UTF8')
        for soup in soup_list: 
            temp_str = file_name + " " + str(i) + "번째 아이템 시작 \n["
            if str(type(soup)) == "<class 'bs4.element.Tag'>":
                temp_str += str(soup.prettify())
            else:
                temp_str += str(soup) 
            temp_str += "] " + file_name + " " + str(i) + "번째 아이템 끝"
            f.write(temp_str)
            i = i + 1
        f.close()

    def check_alert_and_accept(self, depth=0, result=True):
        naver_depth_print("check_alert_and_accept", depth=depth+1)
        try:
            WebDriverWait(self.driver, 5).until(EC.alert_is_present())
            alert = Alert(self.driver)
            if alert:
                if result:
                    alert.accept()
                else:
                    alert.dismiss()
        # except TimeoutException:
        #     naver_depth_print('wrong value in row . Please check the value', depth=depth+1)
        # except NoAlertPresentException:     
        #     naver_depth_print('alert is not present yet, waiting for some time', depth=depth+1)
        except:
            naver_depth_print("Unexpected error: " + str(sys.exc_info()[0]), depth=depth+1)


    def goto_product_list(self, depth=0):
        naver_depth_print("리스트 페이지로 이동", depth=depth+1)
        result = False
        while not result:
            with suppress(UnexpectedAlertPresentException): self.driver_get('https://sell.smartstore.naver.com/#/products/origin-list')
            self.check_alert_and_accept(depth=depth+1)
            naver_depth_print("페이지 종료시 알람 끄기", depth=depth+1)
            if self.js_click(self.driver_find_xpath('//*[@id="seller-content"]/ui-view/div/ui-view[1]/div[1]/ul/li[1]/a', "전체 물건 버튼", depth=depth+1, try_count=10), "전체 물건 버튼", depth=depth+1):
                result = True
        self.rand_sleep()

    def get_soup(self):
        return bs(self.driver.page_source, 'html.parser')
        
    def rand_sleep(self, default=1, rand=1):
        return time.sleep(random.random() * rand + default)

    def set_price(self, item_dict, goto_page=True, depth=0):
        if item_dict['price_state'] > 0:
            naver_depth_print("domeme no: "+str(item_dict['domeme_id']), depth=depth+1)
            naver_depth_print("naver no: "+str(item_dict['naver_id']), depth=depth+1)
            naver_depth_print("domeme name: "+item_dict['title'], depth=depth+1)
            naver_depth_print("domeme price: "+str(item_dict['domeme_price']), depth=depth+1)
            domeme_final_price = item_dict['domeme_price'] * item_dict['minimum_count']
            naver_depth_print("갯수 포함 도매매 가격:"+str(domeme_final_price), depth=depth+1)
            no_margin_price = domeme_final_price / ( 1 - 0.03 )
            naver_depth_print("노마진 가격: "+str(no_margin_price), depth=depth+1)
            margin_price = domeme_final_price * ( 1.15 + ( random.random() * 0.15 ) )
            margin_percent = (1 - (domeme_final_price / margin_price))*100
            naver_depth_print("마진 가격: "+str(margin_price) + " 마진율: "+ str(margin_percent)+"%", depth=depth+1)
            sale_price = round(margin_price * ( 0.5 * random.random() + 0.05 ), -1)
            naver_depth_print("세일 추가값: " + str(sale_price), depth=depth+1)
            naver_price = round(margin_price + sale_price, -1)
            naver_depth_print("네이버 판매가: "+str(naver_price), depth=depth+1)

        if goto_page:
            (result, item_dict) = self.goto_item_page(item_dict)
        else:
            (result, item_dict) = self.goto_item_page(item_dict, with_search=False)

        if result:
            self.clear_and_send_element(self.driver_find_name("product.name"), item_dict['title'], "상품명 입력창")

            self.js_click(self.driver_find_xpath('//*[@id="productForm"]/ng-include/ui-view[16]/div[1]/div'), "배송 탭 열기 버튼", depth=depth+1)
            self.js_click(self.driver_find_xpath('//*[@id="productForm"]/ng-include/ui-view[16]/div[1]/div[2]/div/div[7]/div[2]/div[4]/div/div/div/label[2]/input'),
                          "배송 선결제 버튼", depth=depth+1)

            if self.driver_find_xpath('//*[@id="productForm"]/ng-include/ui-view[22]/div/div[2]/div/div[2]/div/div[2]/ng-include/div/div[1]/div/div[2]', "스마트스토어전용 상품명 값 입력 태그", depth=depth+1):
                self.js_click(self.driver_find_xpath('//*[@id="productForm"]/ng-include/ui-view[22]/div/div[2]/div/div[2]/div/div[2]/ng-include/div/div[1]/div/div[1]/div/label/input'), "스마트스토어전용 상품명 미사용", depth=depth+1)
            # 상세 페이지 smart editor로 변환하기 수행
            xpath_list = ['//*[@id="productForm"]/ng-include/ui-view[11]/div/div[2]/div/div/ncp-editor-form/div[4]/div/a',
                          '/html/body/ui-view[1]/div[3]/div/div[3]/div/ui-view/div[2]/fieldset/form/ng-include/ui-view[11]/div/div[2]/div/div/ncp-editor-form/div[4]/div/a']
            smart_edit_element = self.driver_find_xpath_list(xpath_list, target_name="smart editor로 변환하기 버튼", depth=depth+1)
            if smart_edit_element:
                self.js_click(smart_edit_element)
                smart_complete_xpath=['/html/body/ui-view[1]/div[3]/div/div[3]/div/ui-view/div[2]/fieldset/form/ng-include/ui-view[11]/div/div[2]/div/div/ncp-editor-form/div[1]/div/p[4]/button',
                                      '//*[@id="productForm"]/ng-include/ui-view[11]/div/div[2]/div/div/ncp-editor-form/div[1]/div/p[4]/button']
                while not self.driver_find_xpath_list(smart_complete_xpath, target_name="smart editor로 수정 버튼(변환 완료)", depth=depth+1):
                    self.play_sound(r'C:\Users\한치\mnec\store\static\error_sound\상세페이지를작성해주세요.mp3')
                    time.sleep(5)
            else:
                item_dict['detail_page'] = 3

            if item_dict['price_state'] > 0:
                if naver_price - sale_price < float(item_dict['domeme_row_price']):
                    self.clear_and_send_element(self.driver_find_name("product.salePrice"), format(float(item_dict['domeme_row_price']), ".0f"), "정상가 입력창", depth=depth+1)
                    self.js_click(self.driver.find_element_by_id("r3_2_total"), "할인 설정 안함 버튼", depth=depth+1)
                    result_price = (float(item_dict['domeme_row_price']), 0)
                else:
                    self.clear_and_send_element(self.driver_find_name("product.salePrice"), format(naver_price, ".0f"), "정상가 입력창", depth=depth+1)
                    self.js_click(self.driver.find_element_by_id("r3_1_total"), "할인 설정 버튼", depth=depth+1)
                    self.clear_and_send_element(self.driver_find_name("product.customerBenefit.immediateDiscountPolicy.discountMethod.value"), format(sale_price, ".0f"), "할인가 입력창", depth=depth+1)
                    result_price = (naver_price, sale_price)
            else:
                result_price = (item_dict['naver_price'], item_dict['naver_sale'])
                
            self.save_item_page(depth=depth+1, try_count=5)
            return result_price
        else:
            self.save_item_page(depth=depth+1)
            return (None, None)


        # try:
        #     item = ItemData.objects.get(domeme_id=naver_info['domeme_id'])
        # except ItemData.DoesNotExist:
        #     item = ItemData.objects.create(user=None, item.title=domeme_info['name'], domeme_id=int(naver_info['domeme_id']), domeme_price=domeme_price,
        #                                     naver_id=int(naver_info['naver_id']), naver_price=naver_price, naver_sale=sale_price)
        #     item.save()
        # if item.domeme_price != domeme_price:
        # print("도매 가격이 바뀌었습니다. "+str(item.domeme_price)+" -> "+str(domeme_price))
    
    def save_item_page(self, depth=0, try_count=1):
        naver_depth_print("save_item_page 호출", depth=depth+1)
        self.js_click_with_xpath('//*[@id="seller-content"]/ui-view/div[3]/div[2]/div[1]/button[2]', target_name="저장하기 버튼", depth=depth+1)
        self.js_click(self.driver_find_xpath('/html/body/div[1]/div/div/div[3]/div[1]/button[1]', depth=depth+1, try_count=try_count), "상품속성 다음에 할래요 버튼", depth=depth+1)
        self.js_click_with_xpath('/html/body/div[1]/div/div/div[2]/div/button[2]', depth=depth+1, target_name="아이템 리스트 보기 버튼", try_count=try_count)
        child_warning = self.driver_find_xpath('//*[@id="error-certificationInfo_CHILD_CERTIFICATION0"]/p')
        # if child_warning:
        #     tts.execute('경고. 어린이 안전 관련 사항이 필요한 아이템')
            

    def set_new_title(self, item_info, depth=0):
        naver_depth_print("set_new_title 호출 ("+str(item_info)+")", depth+1)
        (result, item_info) = self.goto_item_page(item_info, depth=depth+1)
        if result and item_info:
            self.clear_and_send_element(self.driver_find_name("product.name"), item_info['title'], "상품명 입력창", depth=depth+1)
            self.save_item_page(depth=depth+1)
        else:
            naver_depth_print("페이지 이동 실패로 취소", depth+1)
        return (result, item_info)

    def delete_item_with_domeme_id(self, item_dict, depth=0):
        self.search_with_domeme_id(item_dict, depth=depth+1)
        self.js_click_with_xpath('//*[@id="seller-content"]/ui-view/div/ui-view[2]/div[1]/div[2]/div[3]/div/div/div/div/div[1]/div[1]/div/div[1]/div[2]/div/label/input', target_name="리스트 전체 선택 라디오", depth=depth+1)
        self.js_click_with_xpath('//*[@id="seller-content"]/ui-view/div/ui-view[2]/div[1]/div[2]/div[1]/div[1]/div/div[1]/button', target_name='선택 삭제', depth=depth+1)
        self.js_click_with_xpath('/html/body/div[1]/div/div/div[2]/div/span[2]/button', target_name='삭제 확인', depth=depth+1)
        self.js_click_with_xpath('/html/body/div[1]/div/div/div[1]/button', target_name='일괄변경 결과 닫기', depth=depth+1)

    def get_item_info(self, item_info, depth=0):
        self.search_item(item_info)
        (titles, domeme_ids, naver_ids, naver_prices, naver_sales) = self.get_origin_info_list()

        while len(titles) < 1 or len(domeme_ids) < 1 or len(naver_ids) < 1 or len(naver_prices) < 1 or len(naver_sales) < 1:
            self.search_item(item_info)
            (titles, domeme_ids, naver_ids, naver_prices, naver_sales) = self.get_origin_info_list()
            if self.driver_find_xpath('//*[@id="seller-content"]/ui-view/div/ui-view[2]/div[1]/div[2]/div[3]/div/div/div/div/div[6]/div/div/div/p', depth=depth+1).text == "데이터가 존재하지 않습니다.":
                break

        if len(titles) < 1 or len(domeme_ids) < 1 or len(naver_ids) < 1 or len(naver_prices) < 1 or len(naver_sales) < 1:
            item_info = None
        else:
            item_info = self.naver_info_list_to_dict(titles[0], domeme_ids[0], naver_ids[0], naver_prices[0], naver_sales[0])

        if self.js_click(self.driver_find_xpath(self.ORIGIN_ITEM_MODIFY_BUTTON_XPATH, try_count=10), "아이템 수정 버튼", depth=depth+1):
            time.sleep(2)
            self.js_click(self.driver_find_xpath('/html/body/div[1]/div/div/div[3]/div/button'), "KC인증 확인 버튼", depth=depth+1)
            time.sleep(1)
            try:
                item_info['naver_edit_id'] = int(self.driver.current_url.split('/')[-1])
            except:
                item_info['naver_edit_id'] = -1
            self.save_item_page(depth=depth+1)

        naver_depth_print("획득 item 정보: "+str(item_info), depth=depth+1)

        return item_info

    def cancel_item_page(self, depth=0):
        self.js_click(self.driver_find_xpath('//*[@id="seller-content"]/ui-view/div[3]/div[2]/div[2]/button[2]'), "취소 버튼", depth=depth+1)
        self.rand_sleep()
        try:
            self.check_alert_and_accept(depth=depth+1)
            naver_depth_print("페이지 종료시 알람 끄기", depth=depth+1)
        except:
            naver_depth_print("알람 안끔", depth=depth+1)
        self.set_url_state(self.STATE_NONE)

    def get_edit_id_from_url(self):
        # 숫자값이 안들어왔을때에 대한 대비가 필요함.
        edit_id = self.driver.current_url.split('/')[-1]
        if edit_id.isdigit():
            return int(edit_id)
        else:
            return -1

    def get_edit_id(self, item_info, depth=0, with_goto=True):
        if with_goto:
            (result, item_info) = self.goto_item_page(item_info, depth=depth+1)
        if int(item_info['naver_edit_id']) == -1:
            item_info['naver_edit_id'] = self.get_edit_id_from_url()
        if with_goto:
            self.save_item_page(depth=depth+1)
        return (result, item_info)

    def search_item(self, item_info, depth=0):
        naver_depth_print(str(item_info['naver_id'])+" 아이템 검색", depth=depth+1)
        self.goto_product_list(depth=depth+1)
        self.send_element(self.driver_find_xpath(self.ORIGIN_ITEM_ID_TEXTAREA_XPATH), str(item_info['naver_id']), "아이템 번호 "+str(item_info['naver_id']), depth=depth+1)
        self.js_click(self.driver_find_xpath(self.ORIGIN_ITEM_SEARCH_BUTTON_XPATH), "아이템 검색 버튼", depth=depth+1)

    def goto_item_page(self, item_info, with_search=True, depth=0):
        result = True

        if not item_info:
            return (False, None)

        naver_depth_print("goto_item_page 콜", depth+1)
        
        # 현재 페이지가 해당 페이지 일 경우에 이동하지 않음.
        if self.url_state != self.STATE_EDIT_PAGE or self.url_edit_id != int(item_info['naver_edit_id']):
            if item_info and 'naver_edit_id' in item_info and int(item_info['naver_edit_id']) != -1:
                naver_depth_print("naver_edit_id("+str(item_info['naver_edit_id'])+")가 존재해서 직접 이동", depth+1)

                page_check = False
                count = 3
                # 페이지가 정상적인지 혹은 페이지가 삭제되었는지 체크하기위해 사용
                while not page_check:
                    self.driver_get('https://sell.smartstore.naver.com/#/products/edit/'+str(item_info['naver_edit_id']), depth=depth+1, sleep_time=count)
                    if count > 5:
                        self.play_sound(r'C:\Users\한치\mnec\store\static\error_sound\아이템페이지획득실패.mp3')
                    deleted_alert_element = self.driver_find_xpath('/html/body/div[1]/div/div/div[1]/p[2]', '삭제된 아이템 알림창1', depth=depth+1)
                    if deleted_alert_element and deleted_alert_element.text == '삭제된 상품입니다.':
                        item_info = None
                        result = False
                        self.js_click(self.driver_find_xpath('/html/body/div[1]/div/div/div[2]/div/span/button', target_name="삭제된 상품 확인 버튼", depth=depth+1), "삭제된 상품 확인 버튼", depth=depth+1)
                        break
                    deleted_alert_element = self.driver_find_xpath('//*[@id="syno-nsc-ext-gen3"]/div[1]/div/div/div[1]/p[2]', '삭제된 아이템 알림창2', depth=depth+1)
                    if deleted_alert_element and deleted_alert_element.text == '삭제된 상품입니다.':
                        item_info = None
                        result = False
                        self.js_click(self.driver_find_xpath('//*[@id="syno-nsc-ext-gen3"]/div[1]/div/div/div[2]/div/span/button', target_name="삭제된 상품 확인 버튼2", depth=depth+1), "삭제된 상품 확인 버튼2", depth=depth+1)
                        break
                    kc_button = self.driver_find_xpath('/html/body/div[1]/div/div/div[3]/div/button', target_name="KC인증 확인 버튼", depth=depth+1)
                    if kc_button:
                        self.js_click(kc_button, "KC인증 확인 버튼", depth=depth+1)

                    # 정확한 페이지가 실행되었음을 체크하기위한 title 확인 (url을 통해서 확인할 수 없음)
                    item_name_element = self.driver_find_xpath('//*[@id="productForm"]/ng-include/ui-view[6]/div/div[2]/div[1]/div/div/div/div/div/input', target_name="제품명 입력", depth=depth+1)
                    if item_name_element:
                        naver_depth_print('제품명 입력 버튼 획득('+str(item_name_element.get_attribute("value"))+')', depth=depth+1)
                        naver_depth_print('정보의 타이틀 값('+str(item_info['title'])+")", depth=depth+1)
                        # if item_name_element.get_attribute("value") == item_info['title']:
                        page_check = True
                        break
                    count = count + 1
                time.sleep(1)
            else:
                naver_depth_print(str(item_info['naver_id'])+" 아이템 페이지로 이동", depth=depth+1)
                if with_search:
                    self.search_item(item_info, depth=depth+1)
                if self.js_click(self.driver_find_xpath(self.ORIGIN_ITEM_MODIFY_BUTTON_XPATH, try_count=10), "아이템 수정 버튼", depth=depth+1):
                    time.sleep(2)
                    self.js_click(self.driver_find_xpath('/html/body/div[1]/div/div/div[3]/div/button'), "KC인증 확인 버튼", depth=depth+1)
                    time.sleep(1)
                    result = True
                    if not 'naver_edit_id' in item_info or item_info['naver_edit_id'] == -1:
                        item_info['naver_edit_id'] = self.get_edit_id_from_url()
                else:
                    item_info = None
                    result = False

        if result:
            self.set_url_state(self.STATE_EDIT_PAGE, item_info['naver_edit_id'])
        return (result, item_info)

    def driver_find_name(self, target, try_count=1, depth=0):
        for i in range(try_count):
            try:
                element = self.driver.find_element_by_name(target)
                break
            except NoSuchElementException:
                element = None
        naver_depth_print("driver_find_name ["+target+"] result: "+str(element), depth=depth+1)
        return element

    ''' 같은 버튼에 대한 여러개의 path가 존재할 경우에 사용하는 함수
        상대 경로와 절대 경로에 있는 element를 모두 검색해서 존재하는 경우에만 반환함 '''
    def driver_find_xpath_list(self, target_list, target_name="", try_count=1, depth=0):
        element = None

        for t in target_list:
            element = self.driver_find_xpath(t, target_name=target_name, try_count=try_count, depth=depth+1)
            if element:
                break

        return element

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

    def js_click_with_xpath(self, xpath, target_name=None, depth=0, try_count=-1):
        naver_depth_print("js_click_with_xpath call", depth=depth+1)
        result = False
        count = 0
        warning = 0
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
            #if try_count > 50 and warning == 0:
                # tts.execute('요소가 검색되지않은지 50회가 지남. 확인 필요.')
                # warning = 1

    def js_click(self, element, target_name=None, depth=0):
        result = False
        if element:
            self.driver.execute_script("arguments[0].click();", element)
            self.rand_sleep()
            result = True
        if target_name:
            naver_depth_print(target_name+" 클릭 ("+str(result)+")", depth=depth+1)
        return result
        
    def clear_and_send_element(self, element, input_str, target_name=None, depth=0):
        if element:
            if target_name:
                naver_depth_print(target_name+" 비우고 내용 '"+input_str+"' 보냄", depth=depth+1)
            element.clear()
            self.rand_sleep()
            element.send_keys(str(input_str))
            self.rand_sleep()
    
    def send_element(self, element, input_str, target_name=None, depth=0):
        if element:
            if target_name:
                naver_depth_print(target_name+" 내용 '"+input_str+"' 보냄", depth=depth+1)
            element.send_keys(str(input_str))
            self.rand_sleep()
            
    def get_pagenation_element(self, page_no, depth=0):
        return self.driver_find_xpath(self.get_pagenation_xpath(page_no), depth=depth+1)

    def get_pagenation_xpath(self, page_no):
        return '//*[@id="seller-content"]/ui-view/div/ui-view[2]/div[1]/div[2]/div[3]/div/div/nav/div[2]/ul/li['+str(page_no)+']'


def naver_depth_print(input_str, depth=0):
    indent = ""
    for i in range(depth):
        indent += "  "
    print(indent + "[Naver] " + input_str)


def calc_price(price, depth=0):
    domeme_price = float(price)
    naver_depth_print("domeme price int:"+str(domeme_price), depth=depth+1)
    no_margin_price = domeme_price / ( 1 - 0.03 )
    naver_depth_print("노마진 가격: "+str(no_margin_price), depth=depth+1)
    margin_price = domeme_price * ( 1.15 + ( random.random() * 0.15 ) )
    margin_percent = (1 - (domeme_price / margin_price))*100
    naver_depth_print("마진 가격: "+str(margin_price) + " 마진율: "+ str(margin_percent)+"%", depth=depth+1)
    sale_price = round(margin_price * ( 0.5 * random.random() + 0.05 ), -1)
    naver_depth_print("세일 추가값: " + str(sale_price), depth=depth+1)
    naver_price = round(margin_price + sale_price, -1)
    naver_depth_print("네이버 판매가: "+str(naver_price), depth=depth+1)

if __name__ == "__main__":
    # naver = Naver()
    # domeme = Domeme()

    # i = 0
    # unset_list = naver.get_sale_unset_item_list()
    # for item in unset_list:
    #     naver_depth_print("아이템 "+str(i)+"/"+str(len(unset_list)))
    #     naver.set_price(item, domeme.get_item_info(item_dict['domeme_id']))
    #     i = i + 1
    calc_price(41100)

