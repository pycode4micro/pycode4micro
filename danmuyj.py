import pandas as pd
import os
import numpy as np
import datetime
import win32api,win32con
import openpyxl
import warnings




warnings.filterwarnings('ignore')#忽略警告级别的提示
def get_sheet(df:pd.DataFrame):
    '''
    返回现货表
    
    '''
    df.付款日期 = pd.to_datetime(df.付款日期)
    df.计划发货日期 = pd.to_datetime(df.计划发货日期)
    df['时效'] = (df.计划发货日期-df.付款日期)/np.timedelta64(1,'h')
    df['售卖类型'] = df.apply(lambda x :aging(x.时效),axis=1)
    
    return df[(df['售卖类型']!='其他')&(df['确认收货时间'].isna())]
def out_time(df:pd.DataFrame):
    '''
    返回预警表
    
    '''
    try:
        df['2小时预警'] = df.apply(lambda x : countdown_24_hour(x.付款日期,x.售卖类型,x.计划发货日期),axis=1)
    except ValueError as e:
        print(e)
        return '无预警表','不存在预警'
    df = df[(df['2小时预警']=='超时')|(df['2小时预警']=='急需发货')][['线上订单号','商品编码','付款日期','计划发货日期','2小时预警','售卖类型']]
    try:
        df.iloc[0,1]
        return df,'存在预警'
    except:
        return '异常中无预警','不存在预警'
    
    # df['是否预警'] = 
def countdown_24_hour(pay_time,x_type,x_plan_deliver):
    '''
    支揽率规则
    
    '''
    now = datetime.datetime.now()
    if x_type == '现货':
        countdown = (24-((now-pay_time)/np.timedelta64(1,'h')))
        if countdown <0:
            return '超时'
        elif countdown <2:
            return '急需发货'
        else:
            return '等待'
    elif x_type == '预售':
        countdown = (x_plan_deliver-now)/np.timedelta64(1,'h')
        if countdown <0:
            return '超时'
        elif countdown <2:
            return '急需发货'
        else:
            return '等待'

def aging(aging_time):
    '''
    售卖类型规则
    
    '''
    if 0<aging_time <49:
        return '现货'
    elif aging_time >49:
        return '预售'
    else:
        '其他'
def yujing(*args):
    try:
        if args:
            file_name = ''
        else:
            file_name = os.listdir('E:\\jushuitan')[0]
        
            
    except Exception as e:
        print(e)
    else:
        path = 'E:\\jushuitan\\'+file_name
        if args:
            path = args
            df = pd.read_excel(path[0])
        df = pd.read_excel(path)
        df_get = get_sheet(df)
        df_out_time,b = out_time(df_get)

        if b == '存在预警':
            out_yujing(df_out_time)
        else:
            print(df_out_time,b)
def out_yujing(df_out_time):
        df_out_time.线上订单号 = df_out_time.线上订单号.astype(str)
        try:
            os.mkdir('C:\\Users\\Administrator\\Desktop\\预警文件夹')
        except:
            pass
        df_out_time.to_excel("C:\\Users\\Administrator\\Desktop\\预警文件夹\\预警表.xlsx")
        record = '|'+str(datetime.datetime.now()).split('.')[0].ljust(5)+'|'.rjust(0)+'('+'有预警产生'+')'+'\n'
        with open(r"C:\Users\Administrator\Desktop\日志.txt",mode='a',encoding='utf-8') as f:
            f.write(record)
        win32api.MessageBox(0, "发现有需要预警,表格已经更新在桌面预警文件夹", "存在现货预警",win32con.MB_OK)
        
            
if __name__ == '__main__':
    path = r"E:\jushuitan\订单_2023-10-10_13-22-40.10611839.16671116_1.xlsx"
    yujing()