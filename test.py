from mobly import base_test
from mobly import test_runner
from mobly.controllers import android_device
from snippet_uiautomator import uiautomator
import datetime
import time


_NEW_TAB_TEXT = '新增分頁'
_DIGI_SERVICE_TEXT = '數位服務'
_PRODUCT_INTRO_TEXT = '產品介紹'
_CREDITCARD_TEXT = '信用卡'
_SUPPLY_CARD_TEXT = '申請信用卡'
_SELECT_CARD_TEXT = '請選擇卡片'
_ALL_TEXT = '全部'
_CARD_LIST = ['CUBE卡', '亞洲萬里通聯名卡', '蝦皮購物聯名卡', '長榮航空聯名卡', '台塑聯名卡', '現金回饋玉璽卡', '世界卡', '雙幣卡', 'eTag聯名卡']


class FindError(Exception):
    """Exception raised for errors in the input.

    Attributes:
        expression -- input expression in which the error occurred
        message -- explanation of the error
    """
    def __init__(self, value):
        self.value = value
    
    def __str__(self):
      return(f'{self.value} not found!')

class MoblyTest(base_test.BaseTestClass):


  def setup_class(self):
    # Registering android_device controller module declares the test's
    # dependency on Android device hardware. By default, we expect at least one
    # object is created from this.
    self.ads = self.register_controller(android_device)
    self.dut = self.ads[0]
    self.dut.services.register(
    uiautomator.ANDROID_SERVICE_NAME,
    uiautomator.UiAutomatorService,)
    # # Start Mobly Bundled Snippets (MBS).
    # self.dut.load_snippet('mbs', android_device.MBS_PACKAGE)

  # Step 1.
  def test_login_homepage(self):
    directory = self.user_params.get('root_directory')
    self.dut.ui.press.home()
    # 開啟"Chrome"瀏覽器
    self.dut.ui(text='Chrome', desc='Chrome').click.wait()
    new_tab_button = self.dut.ui(text=_NEW_TAB_TEXT)
    # 如果沒有分頁,開啟新的分頁
    if new_tab_button.wait.exists(datetime.timedelta(seconds=3)):
      new_tab_button.click.wait()
    chrome_url_bar = self.dut.ui(res='com.android.chrome:id/url_bar')
    if not chrome_url_bar.wait.exists(datetime.timedelta(seconds=3)):
      chrome_search_box = self.dut.ui(res='com.android.chrome:id/search_box')
      chrome_search_box.wait.click()
    # 輸入'https://www.cathaybk.com.tw/cathaybk/'
    time.sleep(2)
    chrome_url_bar.click.wait()
    chrome_url_bar.set_text('https://www.cathaybk.com.tw/cathaybk/')
    self.dut.ui.press.enter()
    target_element = self.dut.ui(desc='cathaybk')
    if not target_element.wait.exists():
      self.dut.take_screenshot(directory,'cathaybk_login_chrome')
      raise FindError('cathaybk')
    # 截圖
    self.dut.take_screenshot(directory,'cathaybk_login_chrome')

  # Step 2.
  def test_product_intro_subfunction(self):
    directory = self.user_params.get('root_directory')
    # 點選"更多功能圖示"
    self.dut.ui(desc='cathaybk').left(clazz='android.view.View').wait.click()  # Work-around for unable to click "更多功能圖示"
    self.dut.take_screenshot(directory,'more_functions')
    # Work-around for unable to click "信用卡"
    credit_card_x = self.dut.ui(text=_DIGI_SERVICE_TEXT).info['visibleCenter']['x']
    credit_card_y = self.dut.ui(text=_DIGI_SERVICE_TEXT).info['visibleCenter']['y']
    # 點選"產品介紹"
    self.dut.ui(text=_PRODUCT_INTRO_TEXT).wait.click()
    # 截圖
    self.dut.take_screenshot(directory,'products_intro')
    time.sleep(3)
    # 點選"信用卡"
    self.dut.ui.click(x=credit_card_x, y=credit_card_y)
    # TODO: 用 xml.etree.ElementTree to get 來取得"信用卡" 座標來點擊 or Selenium

    
    ### Due to the webview compatibility of uiautomator, the following code is not workable or unstable. ###
    credit_card_sublist = self.dut.ui(text=_CREDITCARD_TEXT).find(clazz='android.widget.TextView')

    # Save to log
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d-%H_%M_%S")
    with open(f"{directory}\\logfile_{timestamp}.txt", "w") as file:

      file.write("\n".join(credit_card_sublist))
    # 點選"申請信用卡"
    self.dut.ui(text=_SUPPLY_CARD_TEXT).wait.click()
    self.dut.take_screenshot(directory,'apply_card')

  # Step 3.
  def test_card_list(self):
    directory = self.user_params.get('root_directory')
    card_selection_list = self.dut.ui(text=_SELECT_CARD_TEXT).bottom(clazz='android.view.View')
    #  請選擇卡片"可左右滑動，每次往左或往右滑動一個項目，每滑動一個項目就截圖，直到所有項目都有滑動到
    i = 0
    for i in range(7):
        i += 1
        self.dut.take_screenshot(directory,f'apply_card_category{i}')
        card_selection_list.click.bottomright()
    # 點選全部
    self.dut.ui(text=_ALL_TEXT).wait.click()
    # 滑動每張卡片到正中心截圖
    center_height = self.dut.ui.height / 2

    # Only Drag support to the specific point, Swipe need to work-around 
    for card_name in _CARD_LIST:
        self.dut.ui(scrollable=True).scroll.down(text=card_name)
        card_position_y = self.dut.ui(text=card_name).bottom(clazz='android.widget.Image').info['visibleBounds']['top']
        count = 0
        while card_position_y > center_height:
            self.dut.ui(text=card_name).swipe.up(percent=100, speed=200)
            # Update card image position
            card_position_y = self.dut.ui(text=card_name).bottom(clazz='android.widget.Image').info['visibleBounds']['top']
            if card_position_y <= center_height:
                self.dut.take_screenshot(directory)
                count += 1
                if count > 20:
                    break


if __name__ == '__main__':
  test_runner.main()