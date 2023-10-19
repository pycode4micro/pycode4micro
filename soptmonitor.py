import pandas as pd
import time
import datetime
import os
import shutil #引入库
import getpass #隐藏输入

from selenium import webdriver
from selenium.webdriver.common.by import By
from danmuyj import *


'''


确保自己的电脑有E盘
确保desktop上级是管理员,如果不是管理员需要修改路径

'''

def CleanDir( Dir ): #声明一个叫cleandir的函数，函数的参数是dir
    if os.path.isdir( Dir ): #os.path.isdir()函数判断dir是否是一个目录，同理os.path.isfile()函数判断是否是一个文件。
        paths = os.listdir( Dir )#os.listdir() 方法用于返回指定的文件夹包含的文件或文件夹的名字的列表。
        for path in paths:
            filePath = os.path.join( Dir, path )#os.path.join()方法是，拼接参数里的路径，
            if os.path.isfile( filePath ):#见第8行
                try:
                    os.remove( filePath )#删除
                except os.error:#后边这些都看不懂喽
                    autoRun.exception( "remove %s error." %filePath )#引入logging
            elif os.path.isdir( filePath ):
                if filePath[-4:].lower() == ".svn".lower():
                    continue
                shutil.rmtree(filePath,True)
    return True


def login(username,password):
    web.find_element(By.XPATH,'/html/body/div[1]/div/div[2]/form/div[2]/div[1]/input').send_keys(username)
    time.sleep(0.5)
    web.find_element(By.XPATH,'/html/body/div[1]/div/div[2]/form/div[2]/div[3]/input').send_keys(password)
    time.sleep(0.5)
    web.find_element(By.XPATH,'//*[@id="agreementCheck"]').click()
    time.sleep(0.5)
    web.find_element(By.XPATH,'//*[@id="login-sub"]').click()


def find_order_page():
    web.find_element(By.XPATH,'//*[@id="menuItemWrap-13"]/a/p').click()
    time.sleep(0.5)
    web.find_element(By.XPATH,'//*[@id="panel-13"]/div[4]/div/div[1]/div/div[1]/div[3]').click()
    time.sleep(3)
    
    #用xpath找到iframe
    iframe = web.find_element(By.XPATH,'//*[@id="iframe-聚水潭欢迎您"]')
    web.switch_to.frame(iframe)
    try:
        iframe = web.find_element(By.XPATH,'//*[@id="frame_list"]/iframe[2]')
        #进入iframe
        web.switch_to.frame(iframe)
        
        web.find_element(By.XPATH,'//*[@id="pop_close"]').click()
        #退出当前iframe
        web.switch_to.parent_frame()
    except:
        print('没有恶心人的拦截页面,继续Run.....')
def order_set():#订单模块内动作选择筛选条件
    try:
        iframe = web.find_element(By.XPATH,'//*[@id="frame_list"]/iframe[2]')#2这里有个问题等会改
        web.switch_to.frame(iframe)
    except:
        pass
    
    iframe = web.find_element(By.XPATH,'//*[@id="s_filter_frame"]')#3
    web.switch_to.frame(iframe)
    web.find_element(By.XPATH,'//*[@id="reload_rpt"]/span[2]').click()
    time.sleep(1)
    web.find_element(By.XPATH,'//*[@id="statuss"]/div[5]/div/div/div[1]/label').click()
    time.sleep(0.5)
    web.find_element(By.XPATH,'//*[@id="st_"]').click()
    time.sleep(0.5)
    # web.find_element(By.XPATH,'//*[@id="shop_site"]/div[3]/label').click()#头条放心购
    # time.sleep(0.5)
    web.find_element(By.XPATH,'//*[@id="reload_rpt"]/span[1]').click()
    time.sleep(4)
    web.switch_to.parent_frame()#2
    # iframe = web.find_element(By.XPATH,'//*[@id="frame_list"]/iframe[2]')
    # web.switch_to.frame(iframe)
    
    
def order_out():#订单导出动作并确认
    web.find_element(By.XPATH,'//*[@id="Tool_New_Btn"]/span[1]').click()
    web.switch_to.parent_frame()
    time.sleep(4)
    web.find_element(By.XPATH,'//*[@id="confirm_confirm"]').click()
    iframe = web.find_element(By.XPATH,'//*[@id="frame_list"]/iframe[2]')
    web.switch_to.frame(iframe)
    time.sleep(60)
    web.refresh()
    
def get_order(username,password):
    
    url = 'https://www.erp321.com/login.aspx'
    chrome_options = webdriver.ChromeOptions()
    tmp_path = "E:\\jushuitan"
    try:
        os.mkdir(tmp_path)
    except:
        pass
    prefs = {'profile.default_content_settings.popups': 0, #防止保存弹窗
    'download.default_directory':tmp_path,#设置默认下载路径
    "profile.default_content_setting_values.automatic_downloads":1#允许多文件下载
    }
    chrome_options.add_experimental_option('prefs', prefs)
    chrome_options.add_argument('--headless')#无头

    # 修改windows.navigator.webdriver，防机器人识别机制，selenium自动登陆判别机制
    chrome_options.add_experimental_option('excludeSwitches', ['enable-automation']) 
    global web
    web = webdriver.Chrome(chrome_options=chrome_options)
    web.get(url=url)
    # input()#阻塞函数
    CleanDir(tmp_path)
    login(username,password)
    time.sleep(2)
    # out_activity()
    find_order_page()
    order_set()
    order_out()
    time.sleep(60)
def out_activity():#退出仓库活动页面
    iframe = web.find_element(By.XPATH,'//*[@id="iframe-聚水潭欢迎您"]')
    web.switch_to.frame(iframe)
    web.find_element(By.XPATH,'/html/body/div[1]/div[2]/img').click()#仓库上线功能的提示页面
    time.sleep(1)
    web.switch_to.parent_frame()#退出iframe
    # except:
        
    #     iframe = web.find_element(By.XPATH,'//*[@id="frame_list"]/iframe[2]')
    #     #进入iframe
    #     web.switch_to.frame(iframe)
    #     web.find_element(By.XPATH,'//*[@id="pop_close"]').click()
    #     #退出当前iframe
    #     web.switch_to.parent_frame()
    #     order_out()

# def find_warning_order(date_pay,date_planned_goods):
#     if (date_planned_goods-date_pay).hours:
#         pass
    

#     return df_finally
def main(username,password,start_key,duration:int):
    if start_key != 'qianxi2023':
        print('请联系管理员获取密钥,程序将在3秒后退出')
        exit(3)
    else:
        get_order(username,password)
        print('第一次导出成功',datetime.datetime.now())
        yujing()
        time.sleep(60*duration)
        n = 1
        while True:
            if datetime.datetime.now().hour == 18:
                break
            n += 1
            tmp_path = 'E:\\jushuitan'
            CleanDir(tmp_path)
            find_order_page()
            order_set()
            order_out()
            time.sleep(60)
            print(f'第{n}次导出成功......\n','数据已经更新',datetime.datetime.now())
            yujing()#预警,检查表内是否存在现货预警
            # file_name = os.listdir("E:\\jushuitan")[0]
            # path = tmp_path+'\\'+file_name
            time.sleep(60*duration)
            
         
if __name__ == '__main__':
    username = input('请输入用户名(手机号):')
    password = getpass.getpass('请输入密码:')
    start_key = getpass.getpass('请输入密钥:')
    duration = int(input('请输入需要监测的时间间隔(目前只支持10分钟以上):'))
    main(username=username,password=password,start_key=start_key,duration=duration)
    
    

