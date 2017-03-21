# -*- coding: utf-8 -*-
# ! /usr/bin/env python

"""
@author:LiWei
@license:LiWei
@contact:877129310@qq.com
@version:V1.0
@var:新浪股票行业连接地址
@note:获取新浪行业股票的连接

"""

from selenium import webdriver
import time
import re, json, os, logging
import MySQLdb


# 获取行业URL列表连接
def urllist():
    driver = webdriver.Firefox()
    key = {}
    driver.get("http://finance.sina.com.cn/stock/sl/#sinaindustry_1")
    time.sleep(3)

    urls = driver.find_elements_by_xpath("//table[@id='datatbl']//tbody//tr/td[1]")

    for url in urls:
        uri = url.find_element_by_xpath(".//a").get_attribute("href")
        name = url.find_element_by_xpath(".//a").text
        key[name] = uri
    key = json.dumps(key)
    with open("test.json", "a")as w:
        w.write("{}".format(key))

    driver.quit()


# 加载行业列表地址
def loadtxt():
    with open('test.json', 'rb')as f:
        txt = f.read()
    return json.loads(txt)


def mysqlnews():
    conn = MySQLdb.connect(host=u"127.0.0.1", port=3306, user=u"root", passwd=u"root", charset=u"utf8")
    cur = conn.cursor()
    cur.execute("SELECT URL,k FROM chenlong.urllist WHERE enble=0 limit 1")
    keyword = cur.fetchall()[0]
    cur.execute(u"update chenlong.urllist set enble=1 where url = '{}'".format(keyword[0]))
    conn.commit()
    cur.close()
    conn.close()
    return keyword


def mysqlnewes():
    conn = MySQLdb.connect(host=u"127.0.0.1", port=3306, user=u"root", passwd=u"root", charset=u"utf8")
    cur = conn.cursor()
    cur.execute("SELECT URL,k FROM chenlong.urllist WHERE enbles=0 limit 1")
    keyword = cur.fetchall()[0]
    cur.execute(u"update chenlong.urllist set enbles=1 where url = '{}'".format(keyword[0]))
    conn.commit()
    cur.close()
    conn.close()
    return keyword


# 获取企业基本信息
def parsef():
    conn = MySQLdb.connect(host=u"127.0.0.1", port=3306, user=u"root", passwd=u"root", charset=u"utf8")
    cur = conn.cursor()

    driver = webdriver.Firefox()

    keyword = mysqlnews()

    if not os.path.exists("E:\\chenlong\\{}".format(keyword[1].encode("gb2312"))):
        os.makedirs("E:\\chenlong\\{}".format(keyword[1].encode("gb2312")))
    print u"行业:{}".format(keyword[0])
    driver.get(keyword[0])
    hyurls = []
    while 1:
        cout = 1
        time.sleep(2)
        urls = driver.find_elements_by_xpath("//div[@id='tbl_wrap']//tr[@style='']//th[@class='sort_down']/a")
        for u in urls:
            try:
                url = u.find_element_by_xpath(".").get_attribute("href")
            except:
                continue
            hyurls.append(url)
        try:
            driver.find_element_by_xpath("//div[@id='list_page_btn2_2']/a[1]")
            driver.find_element_by_xpath("//div[@id='list_page_btn2_2']/a[1]").click()
            time.sleep(2.5)
        except:
            break
    for uri in hyurls:
        print u"##########当前:{}/{}##########".format(cout, len(hyurls))
        driver.get(uri)
        time.sleep(2)
        # 财务连接
        # cwurl = driver.find_element_by_xpath("(//h3/a[@class='a_blue_d_s'])[last()-1]").get_attribute("href")
        # 公司资料
        try:
            zlurl = driver.find_element_by_xpath("(//div[@class='sec_cont'])[2]//li[1]/a").get_attribute("href")
        except:
            continue
        driver.get(zlurl)
        time.sleep(2)
        try:
            gpdm = driver.find_element_by_xpath("//div[@class='r-title']/a").text
        except:
            cout += 1
            continue
        gsmc = driver.find_element_by_xpath("(//td[@class='ccl'])[1]").text
        zjjcgmls = driver.find_element_by_xpath("(//td[@class='ccl'])[3]").text
        zcdz = driver.find_element_by_xpath("(//td[@class='ccl'])[4]").text
        bgdz = driver.find_element_by_xpath("(//td[@class='ccl'])[5]").text
        gsjj = driver.find_element_by_xpath("(//td[@class='ccl'])[6]").text
        jyfw = driver.find_element_by_xpath("(//td[@class='ccl'])[7]").text
        sssc = driver.find_element_by_xpath("(//table[@id='comInfo1']//tr/td[2])[3]").text
        fxjg = driver.find_element_by_xpath("(//table[@id='comInfo1']//tr/td[2])[4]").text
        clrq = driver.find_element_by_xpath("(//table[@id='comInfo1']//tr/td[2])[5]").text
        jglx = driver.find_element_by_xpath("(//table[@id='comInfo1']//tr/td[2])[6]").text
        dshms = driver.find_element_by_xpath("(//table[@id='comInfo1']//tr/td[2])[7]").text
        dsdh = driver.find_element_by_xpath("(//table[@id='comInfo1']//tr/td[2])[8]").text
        dscz = driver.find_element_by_xpath("(//table[@id='comInfo1']//tr/td[2])[9]").text
        dsemail = driver.find_element_by_xpath("(//table[@id='comInfo1']//tr/td[2])[10]").text
        yzbm = driver.find_element_by_xpath("(//table[@id='comInfo1']//tr/td[2])[11]").text
        ssrq = driver.find_element_by_xpath("(//table[@id='comInfo1']//tr/td[4])[1]").text
        zcxs = driver.find_element_by_xpath("(//table[@id='comInfo1']//tr/td[4])[2]").text
        zczb = driver.find_element_by_xpath("(//table[@id='comInfo1']//tr/td[4])[3]").text
        zzxs = driver.find_element_by_xpath("(//table[@id='comInfo1']//tr/td[4])[4]").text
        gsdh = driver.find_element_by_xpath("(//table[@id='comInfo1']//tr/td[4])[5]").text
        gscz = driver.find_element_by_xpath("(//table[@id='comInfo1']//tr/td[4])[6]").text
        gsemail = driver.find_element_by_xpath("(//table[@id='comInfo1']//tr/td[4])[7]").text
        gswz = driver.find_element_by_xpath("(//table[@id='comInfo1']//tr/td[4])[8]").text
        xxplwz = driver.find_element_by_xpath("(//table[@id='comInfo1']//tr/td[4])[9]").text
        print zlurl
        print gsmc

        try:
            cur.execute(
                u"INSERT INTO chenlong.sina(zlurl,k,gpdm,gsmc,zjjcgmls,zcdz,bgdz,gsjj,jyfw,sssc,fxjg,clrq,jglx,dshms,dsdh,dscz,dsemail,yzbm,ssrq,zcxs,zczb,zzxs,gsdh,gscz,gsemail,gswz,xxplwz) VALUES('{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}');".format(
                    zlurl, keyword[1], gpdm, gsmc, zjjcgmls, zcdz, bgdz, gsjj, jyfw, sssc, fxjg, clrq, jglx, dshms,
                    dsdh,
                    dscz,
                    dsemail, yzbm, ssrq, zcxs, zczb, zzxs, gsdh, gscz, gsemail, gswz, xxplwz))
            conn.commit()
            logging.info(u"数据插入成功!")
        except MySQLdb.Error, e:
            logging.error(u"数据插入失败,失败原因:")
            try:
                logging.error(u"Mysql Error %d: %s" % (e.args[0], e.args[1]))
            except:
                cout += 1
                continue
        cout += 1

    cur.close()
    conn.close()
    driver.quit()


def filed():
    keyword = mysqlnewes()
    profile = webdriver.FirefoxProfile()
    profile.set_preference('browser.download.dir', u'E:\\chenlong\\{}'.format(keyword[1]))
    profile.set_preference('browser.download.folderList', 2)
    profile.set_preference('browser.download.manager.showWhenStarting', False)
    profile.set_preference('browser.helperApps.neverAsk.saveToDisk', 'application/vnd.ms-excel')
    driver = webdriver.Firefox(firefox_profile=profile)
    print u"行业:{}".format(keyword[0])
    driver.get(keyword[0])
    hyurls = []
    while 1:
        cout = 1
        time.sleep(2)
        urls = driver.find_elements_by_xpath("//div[@id='tbl_wrap']//tr[@style='']//th[@class='sort_down']/a")
        for u in urls:
            try:
                url = u.find_element_by_xpath(".").get_attribute("href")
            except:
                continue
            hyurls.append(url)
        try:
            driver.find_element_by_xpath("//div[@id='list_page_btn2_2']/a[1]")
            driver.find_element_by_xpath("//div[@id='list_page_btn2_2']/a[1]").clic()
            time.sleep(2.5)
        except:
            break
    for uri in hyurls:
        print u"##########当前:{}/{}##########".format(cout, len(hyurls))
        driver.get(uri)
        time.sleep(2)
        # 财务连接
        cwurl = driver.find_element_by_xpath("(//h3/a[@class='a_blue_d_s'])[last()-1]").get_attribute("href")
        driver.get(cwurl)
        time.sleep(2)
        driver.find_element_by_xpath("//li[@id='m02-1']/a").click()
        time.sleep(2)
        driver.find_element_by_xpath("//table[@class='table2']//td[1]/a").click()
        time.sleep(2)
        driver.find_element_by_xpath("//li[@id='m02-3']/a").click()
        time.sleep(2)
        driver.find_element_by_xpath("//table[@class='table2']//td[1]/a").click()
        time.sleep(2)
        driver.find_element_by_xpath("//li[@id='m02-5']/a").click()
        time.sleep(2)
        driver.find_element_by_xpath("//table[@class='table2']//td[1]/a").click()
        time.sleep(2)
        cout += 1

    driver.quit()


def filederror(url, index, key):
    profile = webdriver.FirefoxProfile()
    profile.set_preference('browser.download.dir', u'E:\\chenlong\\{}'.format(key))
    profile.set_preference('browser.download.folderList', 2)
    profile.set_preference('browser.download.manager.showWhenStarting', False)
    profile.set_preference('browser.helperApps.neverAsk.saveToDisk', 'application/vnd.ms-excel')
    driver = webdriver.Firefox(firefox_profile=profile)
    driver.get(url)
    hyurls = []
    print u"行业:{}".format(url)
    while 1:
        # for i in range(1, 3, 1):
        cout = 1
        time.sleep(2)
        urls = driver.find_elements_by_xpath("//div[@id='tbl_wrap']//tr[@style='']//th[@class='sort_down']/a")
        for u in urls:
            try:
                url = u.find_element_by_xpath(".").get_attribute("href")
            except:
                continue
            hyurls.append(url)
        try:
            driver.find_element_by_xpath("//div[@id='list_page_btn2_2']/a[1]").click()
            # driver.find_element_by_xpath("(//div[@class='pages'])[3]/a[last()]").click()
            time.sleep(2.5)
        except:
            break
    for uri in hyurls[index:]:
        print u"##########当前:{}/{}##########".format(cout + index - 1, len(hyurls))
        driver.get(uri)
        time.sleep(2)
        # 财务连接
        cwurl = driver.find_element_by_xpath("(//h3/a[@class='a_blue_d_s'])[last()-1]").get_attribute("href")
        driver.get(cwurl)
        time.sleep(2)
        driver.find_element_by_xpath("//li[@id='m02-1']/a").click()
        time.sleep(2)
        driver.find_element_by_xpath("//table[@class='table2']//td[1]/a").click()
        time.sleep(2)
        driver.find_element_by_xpath("//li[@id='m02-3']/a").click()
        time.sleep(2)
        driver.find_element_by_xpath("//table[@class='table2']//td[1]/a").click()
        time.sleep(2)
        driver.find_element_by_xpath("//li[@id='m02-5']/a").click()
        time.sleep(2)
        driver.find_element_by_xpath("//table[@class='table2']//td[1]/a").click()
        time.sleep(2)
        cout += 1

    driver.quit()


def parseferror(url, index, key):
    conn = MySQLdb.connect(host=u"127.0.0.1", port=3306, user=u"root", passwd=u"root", charset=u"utf8")
    cur = conn.cursor()

    driver = webdriver.Firefox()

    print u"行业:{}".format(url)
    driver.get(url)
    hyurls = []
    # for i in range(1, 3, 1):
    while 1:
        cout = 1
        time.sleep(2)
        urls = driver.find_elements_by_xpath("//div[@id='tbl_wrap']//tr[@style='']//th[@class='sort_down']/a")
        for u in urls:
            try:
                url = u.find_element_by_xpath(".").get_attribute("href")
            except:
                continue
            hyurls.append(url)
        try:
            # driver.find_element_by_xpath("(//div[@class='pages'])[3]/a[last()]").click()
            driver.find_element_by_xpath("//div[@id='list_page_btn2_2']/a[1]").click()
            time.sleep(2.5)
        except:
            break
    for uri in hyurls[index:]:
        print u"##########当前:{}/{}##########".format(cout + index - 1, len(hyurls))
        driver.get(uri)
        time.sleep(2)
        try:
            zlurl = driver.find_element_by_xpath("(//div[@class='sec_cont'])[2]//li[1]/a").get_attribute("href")
        except:
            continue
        driver.get(zlurl)
        time.sleep(2)
        try:
            gpdm = driver.find_element_by_xpath("//div[@class='r-title']/a").text
        except:
            cout += 1
            continue
        gsmc = driver.find_element_by_xpath("(//td[@class='ccl'])[1]").text
        zjjcgmls = driver.find_element_by_xpath("(//td[@class='ccl'])[3]").text
        zcdz = driver.find_element_by_xpath("(//td[@class='ccl'])[4]").text
        bgdz = driver.find_element_by_xpath("(//td[@class='ccl'])[5]").text
        gsjj = driver.find_element_by_xpath("(//td[@class='ccl'])[6]").text
        jyfw = driver.find_element_by_xpath("(//td[@class='ccl'])[7]").text
        sssc = driver.find_element_by_xpath("(//table[@id='comInfo1']//tr/td[2])[3]").text
        fxjg = driver.find_element_by_xpath("(//table[@id='comInfo1']//tr/td[2])[4]").text
        clrq = driver.find_element_by_xpath("(//table[@id='comInfo1']//tr/td[2])[5]").text
        jglx = driver.find_element_by_xpath("(//table[@id='comInfo1']//tr/td[2])[6]").text
        dshms = driver.find_element_by_xpath("(//table[@id='comInfo1']//tr/td[2])[7]").text
        dsdh = driver.find_element_by_xpath("(//table[@id='comInfo1']//tr/td[2])[8]").text
        dscz = driver.find_element_by_xpath("(//table[@id='comInfo1']//tr/td[2])[9]").text
        dsemail = driver.find_element_by_xpath("(//table[@id='comInfo1']//tr/td[2])[10]").text
        yzbm = driver.find_element_by_xpath("(//table[@id='comInfo1']//tr/td[2])[11]").text
        ssrq = driver.find_element_by_xpath("(//table[@id='comInfo1']//tr/td[4])[1]").text
        zcxs = driver.find_element_by_xpath("(//table[@id='comInfo1']//tr/td[4])[2]").text
        zczb = driver.find_element_by_xpath("(//table[@id='comInfo1']//tr/td[4])[3]").text
        zzxs = driver.find_element_by_xpath("(//table[@id='comInfo1']//tr/td[4])[4]").text
        gsdh = driver.find_element_by_xpath("(//table[@id='comInfo1']//tr/td[4])[5]").text
        gscz = driver.find_element_by_xpath("(//table[@id='comInfo1']//tr/td[4])[6]").text
        gsemail = driver.find_element_by_xpath("(//table[@id='comInfo1']//tr/td[4])[7]").text
        gswz = driver.find_element_by_xpath("(//table[@id='comInfo1']//tr/td[4])[8]").text
        xxplwz = driver.find_element_by_xpath("(//table[@id='comInfo1']//tr/td[4])[9]").text
        print zlurl
        print gsmc

        try:
            cur.execute(
                u"INSERT INTO chenlong.sina(zlurl,k,gpdm,gsmc,zjjcgmls,zcdz,bgdz,gsjj,jyfw,sssc,fxjg,clrq,jglx,dshms,dsdh,dscz,dsemail,yzbm,ssrq,zcxs,zczb,zzxs,gsdh,gscz,gsemail,gswz,xxplwz) VALUES('{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}');".format(
                    zlurl, key, gpdm, gsmc, zjjcgmls, zcdz, bgdz, gsjj, jyfw, sssc, fxjg, clrq, jglx, dshms,
                    dsdh,
                    dscz,
                    dsemail, yzbm, ssrq, zcxs, zczb, zzxs, gsdh, gscz, gsemail, gswz, xxplwz))
            conn.commit()
            logging.info(u"数据插入成功!")
        except MySQLdb.Error, e:
            logging.error(u"数据插入失败,失败原因:")
            try:
                logging.error(u"Mysql Error %d: %s" % (e.args[0], e.args[1]))
            except:
                cout += 1
                continue
        cout += 1

    cur.close()
    conn.close()
    driver.quit()


# 遗漏股票 基本信息采集
def parsefkeyword(dm):
    conn = MySQLdb.connect(host=u"127.0.0.1", port=3306, user=u"root", passwd=u"root", charset=u"utf8")
    cur = conn.cursor()

    driver = webdriver.Firefox()

    print u"搜索股票代码:{}".format(dm)
    driver.get("http://vip.stock.finance.sina.com.cn/mkt/")
    time.sleep(2)
    driver.find_element_by_xpath("//input[@id='inputSuggest']").send_keys(dm)
    driver.find_element_by_xpath("//form[@id='SSForm']/input[last()]").click()
    windows = driver.window_handles
    driver.switch_to_window(windows[1])
    time.sleep(10)
    key = driver.find_element_by_xpath("//div[@id='abhbk']/span/a").text
    url = driver.find_element_by_xpath("(//div[@class='sec_title']//a[@class='a_blue_d_s'])[1]").get_attribute("href")
    driver.get(url)
    time.sleep(2)
    zlurl = driver.current_url
    gpdm = driver.find_element_by_xpath("//div[@class='r-title']/a").text
    gsmc = driver.find_element_by_xpath("(//td[@class='ccl'])[1]").text
    zjjcgmls = driver.find_element_by_xpath("(//td[@class='ccl'])[3]").text
    zcdz = driver.find_element_by_xpath("(//td[@class='ccl'])[4]").text
    bgdz = driver.find_element_by_xpath("(//td[@class='ccl'])[5]").text
    gsjj = driver.find_element_by_xpath("(//td[@class='ccl'])[6]").text
    jyfw = driver.find_element_by_xpath("(//td[@class='ccl'])[7]").text
    sssc = driver.find_element_by_xpath("(//table[@id='comInfo1']//tr/td[2])[3]").text
    fxjg = driver.find_element_by_xpath("(//table[@id='comInfo1']//tr/td[2])[4]").text
    clrq = driver.find_element_by_xpath("(//table[@id='comInfo1']//tr/td[2])[5]").text
    jglx = driver.find_element_by_xpath("(//table[@id='comInfo1']//tr/td[2])[6]").text
    dshms = driver.find_element_by_xpath("(//table[@id='comInfo1']//tr/td[2])[7]").text
    dsdh = driver.find_element_by_xpath("(//table[@id='comInfo1']//tr/td[2])[8]").text
    dscz = driver.find_element_by_xpath("(//table[@id='comInfo1']//tr/td[2])[9]").text
    dsemail = driver.find_element_by_xpath("(//table[@id='comInfo1']//tr/td[2])[10]").text
    yzbm = driver.find_element_by_xpath("(//table[@id='comInfo1']//tr/td[2])[11]").text
    ssrq = driver.find_element_by_xpath("(//table[@id='comInfo1']//tr/td[4])[1]").text
    zcxs = driver.find_element_by_xpath("(//table[@id='comInfo1']//tr/td[4])[2]").text
    zczb = driver.find_element_by_xpath("(//table[@id='comInfo1']//tr/td[4])[3]").text
    zzxs = driver.find_element_by_xpath("(//table[@id='comInfo1']//tr/td[4])[4]").text
    gsdh = driver.find_element_by_xpath("(//table[@id='comInfo1']//tr/td[4])[5]").text
    gscz = driver.find_element_by_xpath("(//table[@id='comInfo1']//tr/td[4])[6]").text
    gsemail = driver.find_element_by_xpath("(//table[@id='comInfo1']//tr/td[4])[7]").text
    gswz = driver.find_element_by_xpath("(//table[@id='comInfo1']//tr/td[4])[8]").text
    xxplwz = driver.find_element_by_xpath("(//table[@id='comInfo1']//tr/td[4])[9]").text
    print gsmc
    gsjj = gsjj.replace('"', "'")

    try:
        cur.execute(
        # print(
            u'INSERT INTO chenlong.sina(zlurl,k,gpdm,gsmc,zjjcgmls,zcdz,bgdz,gsjj,jyfw,sssc,fxjg,clrq,jglx,dshms,dsdh,dscz,dsemail,yzbm,ssrq,zcxs,zczb,zzxs,gsdh,gscz,gsemail,gswz,xxplwz) VALUES("%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s");' % (
                zlurl, key, gpdm, gsmc, zjjcgmls, zcdz, bgdz, gsjj, jyfw, sssc, fxjg, clrq, jglx, dshms, dsdh, dscz,
                dsemail, yzbm, ssrq, zcxs, zczb, zzxs, gsdh, gscz, gsemail, gswz, xxplwz))
        conn.commit()
        logging.info(u"数据插入成功!")
    except MySQLdb.Error, e:
        logging.error(u"数据插入失败,失败原因:%s" % e)
        print u"插入失败,股票代码 gsjj:%s" % dm

    cur.close()
    conn.close()
    driver.quit()


# urllist()
# loadtxt()
# dms = ["600005"]
# 600005
# for dm in dms:
#     parsefkeyword(dm)
# filederror("http://vip.stock.finance.sina.com.cn/mkt/#new_qczz", 81, u'汽车制造')
# parseferror("http://vip.stock.finance.sina.com.cn/mkt/#new_zhhy", 12, u"综合行业")
# while 1:
#     filed()
# conn = MySQLdb.connect(host=u"127.0.0.1", port=3306, user=u"root", passwd=u"root", charset=u"utf8")
# cur = conn.cursor()
#
# urllisttest = loadtxt()
#
# for k, url in urllisttest.iteritems():
#     try:
#         cur.execute(
#             u"INSERT INTO chenlong.urllist(url,k) VALUES('{}','{}');".format(
#                 url, k, ))
#         conn.commit()
#         logging.info(u"数据插入成功!")
#     except MySQLdb.Error, e:
#         logging.error(u"数据插入失败,失败原因:")
#         logging.error(u"Mysql Error %d: %s" % (e.args[0], e.args[1]))
# cur.close()
# conn.close()
