import time
from appium import webdriver


'''

appium操作自动添加微信好友
本人注释一般写于代码右侧,除非该写法由于代码过长不利于阅读,才写在代码上方


'''

list_ = ['手机号','微信号']#手机号码或微信号,列表(可遍历的对象就行)
caps = {
"platformName": "Android", # 声明是ios还是Android系统
"platformVersion": "7.1.2", # Android内核版本号
"deviceName": "SM-G988N", # 连接的设备名称
"appPackage": "com.tencent.mm", # apk的包名
"appActivity": "ui.LauncherUI", # apk的launcherActivity
"noReset": True # 在开始会话之前不要重置应用程序状态
}
def swipe_up(distance):  # distance为滑动距离，time为滑动时间
    size = driver.get_window_size()
    # print(size)
    x1 = 0.5 * size['width']
    y1 = 0.8 * size['height']
    y2 = (0.8 - distance) * size['height']
    driver.swipe(x1, y1, x1, y2, duration=500)
driver = webdriver.Remote("http://localhost:4723/wd/hub", caps) # 启动app
time.sleep(10)
driver.find_element_by_id('com.tencent.mm:id/hy6').click()
time.sleep(3)
#未找到合适的id只能使用xpath更建议使用byid
driver.find_element_by_xpath('''/hierarchy/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.ListView/android.widget.LinearLayout[2]/android.widget.LinearLayout/android.widget.LinearLayout/android.widget.TextView''').click()
time.sleep(3)
driver.find_element_by_id('com.tencent.mm:id/jcd').click()

# 下面这段代码开始循环
for i in list_:
    time.sleep(3)
    driver.find_element_by_id('com.tencent.mm:id/cd7').clear()#清空
    time.sleep(3)
    driver.find_element_by_id('com.tencent.mm:id/cd7').send_keys(i)#输入
    time.sleep(3)
    driver.find_element_by_id('com.tencent.mm:id/j63').click()#点击搜索
    time.sleep(5)
    el = driver.find_element_by_id('com.tencent.mm:id/khj')
    if el.text == '添加到通讯录':#该id选择在不用结果下都对应一个节点,因此使用判断避免报错
        el.click()
        time.sleep(3)
    else:
        driver.find_element_by_id('com.tencent.mm:id/g0').click()#点击返回按钮
        continue

    swipe_up(0.2)
    driver.find_element_by_id('com.tencent.mm:id/e9q').click()#发送按钮
    time.sleep(10)
    driver.find_element_by_id('com.tencent.mm:id/g1').click()#返回按钮
