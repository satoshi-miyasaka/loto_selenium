#!/bin/python3

import os
import sys
import argparse
import configparser
import re
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

class Mizuho:

    def __init__(self):
        self.driver = webdriver.Firefox()
        self.wait = WebDriverWait(self.driver, 20)

    def __del__(self):
        pass
        # self.driver.close()

    def logoin(self, id, pw):
        try:
            self.driver.get("https://web.ib.mizuhobank.co.jp/servlet/LOGBNK0000000B.do")
            self.driver.find_element(By.ID, "txbCustNo").send_keys(id)
            self.driver.find_element(By.NAME, "N00000-next").click()
            self.driver.find_element(By.ID, "PASSWD_LoginPwdInput").send_keys(pw)
            self.driver.find_element(By.ID, "btn_login").click()
        except Exception as e:
            raise MizuhoException(e, self.driver.page_source)

    def lotoMain(self):
        try:
            # 次へリンク
            self.driver.find_element(By.XPATH, "//*[@id='button-section']").click()

            # 一回メニューをオープンしてから宝くじリンクをクリック
            self.driver.find_element(By.XPATH, '//span[text()="宝くじ"]').click()
            self.driver.find_element(By.ID, "MB_R018N01").click()
        except Exception as e:
            raise MizuhoException(e, self.driver.page_source)

    def lotoSixBuy(self, numbers):
        try:
            self.driver.find_element(By.XPATH, "//*[contains(@value, '別の宝くじを追加')]").click()
        except:
            print("element nothing")

        try:
            # 数字を選択するの2個目がLOTO6 1個目はLOTO7
            self.driver.find_elements(By.XPATH, "//*[contains(text(), '数字を選択する')]")[1].click()

            for var in numbers:
                self.driver.find_element(By.XPATH, '//input[contains(@class, "loto-in-item2__key") and contains(@value, "' + str(var) + '")]').click()

            self.driver.find_element(By.ID, "okBtn").click()
            self.driver.find_element(By.XPATH, '//input[contains(@value, "カートに入れる")]').click()
        except Exception as e:
            raise MizuhoException(e, self.driver.page_source)

    def lotoSevenBuy(self, numbers):
        try:
            self.driver.find_element(By.XPATH, "//*[contains(@value, '別の宝くじを追加')]").click()
        except:
            print("element nothing")

        try:
            # 数字を選択するの2個目がLOTO6 1個目はLOTO7
            self.driver.find_elements(By.XPATH, "//*[contains(text(), '数字を選択する')]")[0].click()

            for var in numbers:
                self.driver.find_element(By.XPATH, '//input[contains(@class, "loto-in-item2__key") and contains(@value, "' + str(var) + '")]').click()

            self.driver.find_element(By.ID, "okBtn").click()
            self.driver.find_element(By.XPATH, '//input[contains(@value, "カートに入れる")]').click()
        except Exception as e:
            raise MizuhoException(e, self.driver.page_source)

    def finish(self):
        try:
            self.driver.find_element(By.ID, "confirmAmt_box").click()
            self.driver.find_element(By.ID, "approvel_box").click()
            self.driver.find_element(By.XPATH, "//*[contains(@value, '購入を確定する')]").click()

            # コンファームボックスのOKを押す
            self.wait.until(EC.alert_is_present())
            alert = self.driver.switch_to.alert
            alert.accept()
        except Exception as e:
            raise MizuhoException(e, self.driver.page_source)

class MizuhoException(Exception):
    def __init__(self, e, source):
        pageSource = re.sub(r'[\r\n]{1,2}', '', source)
        pageSource = re.sub(r'\t', '', pageSource)
        self.pageSource = re.sub(r'>\s*<', '><', pageSource)
        self.e = e

if __name__ == '__main__':
    parse = argparse.ArgumentParser(description='みずほ銀行のインターネットバンキングにログインし、LOTO6、LOTO7を購入します')
    parse.add_argument('-i', '--id',    help='LOTO6を購入します')
    parse.add_argument('-p', '--pw',    help='LOTO6を購入します')
    parse.add_argument('-6', '--six',   action='store_true', help='LOTO6を購入します')
    parse.add_argument('-7', '--seven', action='store_true', help='LOTO7を購入します')
    args = parse.parse_args()

    loto = Mizuho(iniFile)

    loto.logoin(arg.id, arg.pw)
    loto.lotoMain()
    if args.six: callLoto6Set()
    if args.seven: callLoto7Set()
    loto.finish()

