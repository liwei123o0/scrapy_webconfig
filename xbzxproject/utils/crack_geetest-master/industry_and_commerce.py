#!/usr/bin/env python
# -*- coding: utf-8 -*-

from geetest import BaseGeetestCrack
from selenium import webdriver


class IndustryAndCommerceGeetestCrack(BaseGeetestCrack):
    """工商滑动验证码破解类"""

    def __init__(self, driver):
        super(IndustryAndCommerceGeetestCrack, self).__init__(driver)

    def crack(self):
        """执行破解程序

        """
        self.input_by_id()
        self.click_by_id()
        x_offset = self.calculate_slider_offset()
        self.drag_and_drop(x_offset=x_offset)


def main():
    driver = webdriver.Firefox()
    driver.get("http://www.gsxt.gov.cn/index.html")
    cracker = IndustryAndCommerceGeetestCrack(driver)
    cracker.crack()
    # 打印浏览器宽高
    # print(driver.get_window_size())
    # time.sleep(10)
    # driver.save_screenshot("screen.png")
    driver.close()


if __name__ == "__main__":
    while 1:
        try:
            main()
        except:
            pass
