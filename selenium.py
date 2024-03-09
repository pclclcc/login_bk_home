from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.action_chains import ActionChains
from pathlib import Path
import datetime
import time


root_path = 'c:/test_cathay'
login_chrome_screenshot_path = Path('c:/test_cathay/cathaybk_login_chrome.png')
products_intro_path = Path('c:/test_cathay/products_intro.png')
more_functions_path = Path('c:/test_cathay/more_functions.png')
card_sub_list_path = Path('c:/test_cathay/card_sub_list.png')
supply_card_path = Path('c:/test_cathay/supply_card.png')

class CathayAuto(object):
    def __init__(self):
        self.options = webdriver.ChromeOptions()
        self.options.add_experimental_option("mobileEmulation", {"deviceName": "Pixel 7"})
        self.driver = webdriver.Chrome(service=Service(), options=self.options)
        self.wait = WebDriverWait(self.driver, 20)

    def takeScreenshot(self, filename: Path):
        self.driver.get_screenshot_as_file(filename)
    
    # Step 1.
    def test_launchtHomePage(self):
        """使用 Chrome app 到國泰世華銀行官網

        https://www.cathaybk.com.tw/cathaybk/
        並截圖。
        """
        self.driver.get("https://www.cathaybk.com.tw/cathaybk/")
        # 確認是否成功開啟首頁
        self.loginBtn_xpath='//p[@id="lblLoginText"]'
        try:
          WebDriverWait(self.driver, 15).until(EC.visibility_of_element_located((By.XPATH, self.loginBtn_xpath)))
        except TimeoutException:
          print('Fail to launch homepage!')
        # 截圖
        self.takeScreenshot(login_chrome_screenshot_path)

    # Step 2.
    def test_checkCardSubFunction(self):
        """點依照以下流程測試：

        1. 點擊左上角更多功能後，截圖
        2. 預設在"個人金融"分頁，點擊"產品介紹"後，截圖
        3. 點擊"信用卡"後截圖並將選單下所有子功能項目的文字儲存於log當中
        4. 點擊"申請信用卡"後，截圖"""
        # 點選更多功能
        more_function_xpath = '//div[@class="cubre-o-header__burger"]//a[@class="cubre-a-burger"]'
        WebDriverWait(self.driver, 15).until(EC.visibility_of_element_located((By.XPATH, more_function_xpath))).click()
        # 截圖
        self.takeScreenshot(more_functions_path)
        # 點選"產品介紹"
        WebDriverWait(self.driver, 15).until(EC.visibility_of_element_located((By.XPATH, '//div[.="產品介紹"]'))).click()
        time.sleep(1)
        # 截圖
        self.takeScreenshot(products_intro_path)
        card_xpath_l1 = '//div[@class="cubre-a-menuSortBtn" and text()="信用卡"]'
        WebDriverWait(self.driver, 15).until(EC.visibility_of_element_located((By.XPATH, card_xpath_l1))).click()
        # 確認出現信用卡子功能列表
        card_sub_xpath = '//div[@class="cubre-a-menuSortBtn" and text()="信用卡"]/../following-sibling::div'
        card_sub_list = WebDriverWait(self.driver, 15).until(EC.visibility_of_element_located((By.XPATH, card_sub_xpath)))
        try:
          card_sub_list
        except TimeoutException:
          print('Card subfunction list not found!')
        # 截圖
        time.sleep(1)
        self.takeScreenshot(card_sub_list_path)
        card_sub_list_a = card_sub_list.find_elements(By.XPATH,'a')
        card_sub_text_list = []
        for element in card_sub_list_a:
          text = element.text
          card_sub_text_list.append(text)
        print("子功能列表：", card_sub_text_list)
        # Save to log
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d-%H_%M_%S")
        with open(f"c:\\test_cathay\\logfile_{timestamp}.txt", "w") as file:
          file.write(str(card_sub_text_list))
        # 點選申請信用卡
        supply_card = '//a[text() = "申請信用卡" and @class="cubre-a-menuLink"]'
        WebDriverWait(self.driver, 15).until(EC.visibility_of_element_located((By.XPATH, supply_card))).click()
        self.takeScreenshot(supply_card_path)
    
    # Step 3.
    def test_scrollCardList(self):
        """
        測試信用卡列表滑動功能

        需求：
        1. "請選擇卡片"可左右滑動，每次往左或往右滑動一個項目，每滑動一個項目就截圖，直到所有項目都有滑動到。
        2. 滑動到"全部"項目，將底下介紹的卡片"每一張"都要截到圖，並且目標卡片垂直位置要在截圖畫面"正中心"。(目標卡片上下方都可能有其他卡片，須確保目標卡片在截圖的正中心)
        """
        # 點擊下一頁並截圖
        next_btn_xpath = '//a[@class="bx-next"][text()="Next"]'
        card_category = 7
        for i in range(card_category):  # TODO: 7可改善為找查對應元素的數量
          self.takeScreenshot(f'{root_path}/card_category_{i}.png')
          WebDriverWait(self.driver, 15).until(EC.visibility_of_element_located((By.XPATH, next_btn_xpath))).click()
          time.sleep(1)
        # 點選全部
        all_xpath = '//a[@href="javascript:void(0)"][@id="layout_0_content_0_rptSlider_hlkSliderItem_1"][text()="全部"]'
        WebDriverWait(self.driver, 15).until(EC.visibility_of_element_located((By.XPATH, all_xpath))).click()
        time.sleep(3)
        scroll_list_xpath = '//div[@class="wrap"]//ul[@class="gridHalf" and @data-id="list"]//li'
        scroll_list = WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.XPATH, scroll_list_xpath)))

        # 查找所有卡片照片的元素
        elements = self.driver.find_elements(By.CSS_SELECTOR, "div.wrap .scCardImage")
        # 循環遍歷元素並將它們滑動到中心, 除了最後一張會有誤差
        i = 1
        for element in elements:
            # 滑到指定信用卡圖
            actions = ActionChains(self.driver)
            actions.move_to_element(element).perform()
            time.sleep(1)
            # 將卡片移到中心點, 借助tag html來完成
            # TODO: 釐清為何用by offset 會 move out of bounds
            html = self.driver.find_element(By.TAG_NAME, "html")
            actions.drag_and_drop(element,html).perform()
            self.takeScreenshot(f'{root_path}/all_card_photo_{i}.png')
            i += 1


if __name__ == "__main__":
    automation = CathayAuto()
    # Testcase to perform
    automation.test_launchtHomePage()
    automation.test_checkCardSubFunction()
    automation.test_scrollCardList()
    automation.driver.quit()
