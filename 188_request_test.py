#!/usr/bin/env python
# coding: utf-8

# In[ ]:


#coding=utf-8
import requests,hashlib,types,json,threading,time,unittest,re,datetime,cx_Oracle,sys,redis,random,urllib3,os
import requests,twstock
from bs4 import BeautifulSoup
from time import sleep,ctime
from numba import jit
import pandas as pd
from json.decoder import JSONDecodeError
import MySQLdb as p
from interval import Interval
os.environ['NLS_LANG'] = 'SIMPLIFIED CHINESE_CHINA.UTF8'
import matplotlib.pyplot as plt
from io import StringIO
from fake_useragent  import UserAgent
from collections import defaultdict
from selenium import webdriver
from urllib.parse import urlsplit
from functools import wraps
from ddt import ddt,data,unpack
import HTMLTestRunner


# In[ ]:


from IPython.display import clear_output as clear


# In[ ]:


'ipykernal' in sys.modules


# In[ ]:


# 切割url 
url = "http://3eeb8f01ffe7.ngrok.io/domain_status"
a = urlsplit(url)
print(a)
print(a.scheme,a.netloc)
print(type(a.scheme))


# In[ ]:


#ipynb檔  轉成 python檔
def IpynbToPython(): 
    try:
        get_ipython().system('jupyter nbconvert --to python 188_request_test.ipynb   ')
    except:
        pass
IpynbToPython()


# In[ ]:


FF_().user_agent['Pc']


# In[ ]:


def test(lottery_id,bet_type_code):
    sql = f"select actual_bonus,lhc_theory_bonus from game_award "                   "where LOTTERYID = {lottery_id} "                   f"and bet_type_code like '%{bet_type_code}%'"
    return sql
test('123','456')


# In[ ]:


class FF_(): #4.0專案
    cookies = {}
    submit_inf = {}
    # 存訪 PC前台用戶登入後的 cookie
    def __init__(self):
        self.dev_url = ['dev02','dev03','fh82dev02','88hlqpdev02','teny2020dev02']
        self.uat_url = ['joy188','joy188.195353']
        self.app_url = {'dev':['http://10.13.22.152:8199/','2D424FA3-D7D9-4BB2-BFDA-4561F921B1D5',
                               'fa0c0fd599eaa397bd0daba5f47e7151',0],
                        '188':['http://iphong.joy188.com/','f009b92edc4333fd',
                               '3bf6add0828ee17c4603563954473c1e',1]
                       }
        
        self.user_agent ={
        'Pc':"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) \
        Chrome/68.0.3440.100 Safari/537.36",
        'Ios': "Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 \
        (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1",
        'Andorid': "Mozilla/5.0 (Linux; Android 5.0; SM-G900P Build/LRX21T) AppleWebKit/537.36 \
        (KHTML, like Gecko) Chrome/70.0.3538.110 Mobile Safari/537.36",
        'Fake':  UserAgent().random
        }
        self.param =  b'ba359dddc3c5dfd979169d056de72638',#固定寫死即可
        self.session = requests.Session()
        self.lottery_dict = {
        'cqssc':[u'重慶','99101'],'xjssc':[u'新彊時彩','99103'],'tjssc':[u'天津時彩','99104'],
        'hljssc':[u'黑龍江','99105'],'llssc':[u'樂利時彩','99106'],'shssl':[u'上海時彩','99107'],
        'jlffc':[u'吉利分彩','99111'],'slmmc':[u'順利秒彩','99112'],'txffc':[u'騰訊分彩','99114'],
        'btcffc':[u'比特幣分彩','99115'],'fhjlssc':[u'吉利時彩','99116'],
        'sd115':[u'山東11選5','99301'],'jx115':[u"江西11選5",'99302'],
        'gd115':[u'廣東11選5','99303'],'sl115':[u'順利11選5','99306'],'jsk3':[u'江蘇快3','99501'],
        'ahk3':[u'安徽快3','99502'],'jsdice':[u'江蘇骰寶','99601'],'jldice1':[u'吉利骰寶(娛樂)','99602'],
        'jldice2':[u'吉利骰寶(至尊)','99603'],'fc3d':[u'3D','99108'],'p5':[u'排列5','99109'],
        'ssq':[u'雙色球','99401'],'lhc':[u'六合彩','99701'],'btcctp':[u'快開','99901'],
        'bjkl8':[u'快樂8','99201'],'pk10':[u"pk10",'99202'],'v3d':[u'吉利3D','99801'],
        'xyft':[u'幸運飛艇','99203'] ,'fhxjc':[u'鳳凰新疆','99118'],'fhcqc':[u'鳳凰重慶','99117'],
         'hnffc':[u'河內分彩','99119'],'360ffc':[u'360紛紛採','99121'],'3605fc':[u'360五分彩','99122'],
        'hn5fc':[u'河內五分彩','99120'],'n3d':[u'越南3d','99124'],'np3':[u'越南福利彩','99123'],
        'pcdd':[u'PC蛋蛋','99204']
        }
    def md5(self,password,param):#4.0 登入密碼加規則
        m = hashlib.md5()
        m.update(password)
        sr = m.hexdigest()
        for i in range(3):
            sr= hashlib.md5(sr.encode()).hexdigest()
        #print(sr.encode(),param)
        rx = hashlib.md5(sr.encode()+param).hexdigest()
        return rx
    def session_post(self,request_url,request_func,postData,header):#共用 request.post方式 ,url 為動態 請求url ,source預設走PC
        global r # 會針對每個不同請求, 回覆內容作調整
        r = self.session.post(request_url+request_func,data = postData,headers=header,verify=False)
    def session_get(self,request_url,request_func,getData,header):
        global r # 會針對每個不同請求, 回覆內容作調整
        r = self.session.get(request_url+request_func,data = getData,headers=header,verify=False)
    def Thread_Func(fun_name,num,*argv):
        threads = []
        for i in range(num):
            t = threading.Thread(target=fun_name,args=(argv))
            threads.append(t)
        for i in threads:
            i.start()
        for i in threads:
            i.join()
    def web_issuecode(self,lottery,account):#頁面產生  獎期用法,  取代DB連線問題
        now_time = int(time.time())
        header = {
                'User-Agent':self.user_agent['Pc'],
                'Cookie': 'ANVOID='+FF_().cookies[account]
                }
        FF_().session_get(em_url,'/gameBet/%s/dynamicConfig?_=%s'%(lottery,now_time),'',header)
        issuecode = r.json()['data']['gamenumbers']
        return issuecode
        #session = requests.Session()
        #try:
        '''
        if lottery == 'lhc':
            FF_().session_get(em_url,'/gameBet/lhc/dynamicConfig?_=%s'%(now_time),'',header)
            issuecode = r.json()['data']['issueCode']
        else:
            FF_().session_get(em_url,'/gameBet/%s/lastNumber?_=%s'%(lottery,now_time),'',header)
            issuecode = r.json()['issueCode']
        '''
        #print(issuecode)
        #except :
            #print("%s採種沒抓到 獎號"%lottery)

    def get_conn(self,env):#連結數據庫 env 0: dev02 , 1:188 ,2: 生產
        if env == 2:
            username = 'rdquery'
            service_name = 'gamenxsXDB'
        else:
            username = 'firefog'
            service_name = ''
        oracle_ = {'password':['LF64qad32gfecxPOJ603','JKoijh785gfrqaX67854','eMxX8B#wktFZ8V'],
        'ip':['10.13.22.161','10.6.1.41','10.6.1.31'],
        'sid':['firefog','game','']}
        conn = cx_Oracle.connect(username,oracle_['password'][env],oracle_['ip'][env]+':1521/'+
        oracle_['sid'][env]+service_name)
        return conn
    def select_joint_venture(self,conn,account):#查詢用戶 的  joint_venture身分
        with conn.cursor() as cursor:
            sql = "select joint_venture from user_customer where account = '%s'"%account
            cursor.execute(sql)
            print(sql)
            rows = cursor.fetchall()
            cursor.close()
            for i in rows:
                return i[0]
        
    def select_lottery(self,conn):#從DB取得　彩種資料，避免每次都要　新增
        with conn.cursor() as cursor:
            sql = "select lottery_name,lotteryid from game_series where lottery_front_type != '非彩票'"
            cursor.execute(sql)
            print(conn)
            print(sql)
            rows = cursor.fetchall()
            lottery_dict = defaultdict(list)
            for index,con in enumerate(rows):
                lottery_dict[index].append(con[0])
                lottery_dict[index].append(con[0])
            return lottery_dict
        print('lottery_dict')
        
    def select_issue(self,conn,lottery,type_):#查詢正在銷售的 期號 ,lotttery參數,對應 lotteryid
        #today_time = '2019-06-10'#寫死 for預售中

        if type_ == 1:#一般投注
            sql = "select issue_code from game_issue where lotteryid = '%s'             and sysdate between sale_start_time and sale_end_time"%(self.lottery_dict[lottery][1])
        else:# 追號
            sql = "select issue_code from game_issue where lotteryid = '%s'             and sale_start_time > trunc(sysdate,'DD') and             status !=7 and period_status !=2"%(self.lottery_dict[lottery][1])
        with conn.cursor() as cursor:
            print(sql)
            cursor.execute(sql)
            rows = cursor.fetchall()
            issue_code = {}
            if lottery in ['slmmc','sl115']:#順利秒彩,順利11選5  不需 講期
                issue_code[lottery] = "1"# 獎棋給空 ,傳到 投注 
            else:
                if type_ == 1:
                    try:
                        issue_code[lottery] = rows[0][0]# rows 為一個 list 理包 一個tuple
                    except IndexError:
                        issue_code = issueCode
                        
                else:
                    issue_plan = []#追號 放期數
                    for i in rows:# i為 追號 期號 , 為一個tuple直
                        issue_plan.append(i[0])
                    issue_code[lottery] = issue_plan

            return issue_code

    def Pc_Login(self,url,user,source='Pc'):
        global post_url,em_url #後續   登入後,  各請求 需要用的
        global envs#DB 環境變數用
        global Pc_header,account
        account = user
        em_url =  'http://em.%s.com'%url
        #print(em_url)
        if url in self.dev_url:
            post_url = 'http://www.%s.com'%url
            password = b'123qwe'
            envs = 0
        elif url in self.uat_url:
            post_url = 'http://www2.%s.com'%url
            password = b'amberrd'
            envs = 1
        else:
            return('錯誤%s'%url)
        postData = {
        "username": account,
        "param" : self.param[0],#固定寫死即可
        "password": FF_().md5(password,self.param[0])# self.param 為一個 tuple (byte的關係)
        }
        Pc_header = {'User-Agent':self.user_agent[source]}
        FF_().session_post(post_url,'/login/login',postData,Pc_header)# 登入皆口
        print('登入帳號: %s'%account)
        try:
            if r.json()['isSuccess'] == 1:
                #cookies = r.cookies.get_dict()#獲得登入的cookies 字典
                if user in FF_().cookies:# 刪除原本已經存菜的key, 重新獲得
                    del FF_().cookies[user]
                FF_().cookies.setdefault(account,r.cookies.get_dict()['ANVOID'])#存放用戶cookie
                #user_.setdefault(account,userAgent)#存放用戶 useragent
                t = time.strftime('%Y%m%d %H:%M:%S')
                print('現在時間:'+time.strftime('%Y%m%d %H:%M:%S'))
                print('登入成功')
        except KeyError:
            print('登入失敗')
    
            #sleep(20)
    def plan_return(self,type_,issuelist):# 根據 type_ 判斷是不是追號, 生成動態的 動態order  
        plan_= []
        for i in range(type_):
            plan_.append({"number": 'test', "issueCode": issuelist[i], "multiple": 1})
        print(plan_)
        return plan_
    
    # 各採種 對應的 投注格式
    def submit_json(self,lottery,awardmode,isTrace,traceWinStop ,traceStopValue,type_,ball):
        if awardmode is None:
            if lottery in ['btcctp','btcffc']:
                awardmode = 2
            else:
                awardmode = 1
        if type_ != 1 :
            print(issueCode[:type_])
            order_plan = FF_().plan_return(type_,issueCode)# 生成oredr 的投注奖期 列表'
            len_order = len(order_plan)
            print(len_order)
        else:
            print(issueCode)
            order_plan = [{"number":'test',"issueCode":issueCode,"multiple":1}]# 一般投注
            len_order = 1
        if lottery == 'btcctp':
            data_ = {"gameType":lottery,"isTrace":isTrace,"traceWinStop":traceWinStop,"traceStopValue":traceStopValue,"balls":[{"id":1,"ball":ball,"type":"chungtienpao.chungtienpao.chungtienpao","moneyunit":"1","multiple":1,"awardMode":awardmode,"num":1}],"orders":order_plan ,"amount":100.00*len_order}
        elif lottery in ['cqssc','hljssc','xjssc','tjssc','fhjlssc','fhcqc','fhxjc']:
            '''
            if lottery == 'cqssc':
                data_ = {"gameType":"cqssc","isTrace":0,"traceWinStop":0,"traceStopValue":-1,
            "balls":[{"id":1,"ball":"-,-,5,0,5","type":"housan.zhixuan.fushi","moneyunit":"1",
            "multiple":1,"awardMode":awardmode,"num":1}],"orders":order_plan,"redDiscountAmount":0,
            "amount":2*len_order}
            else:
            '''
            data_={"gameType":lottery,"isTrace":isTrace,"traceWinStop":traceWinStop,"traceStopValue":traceStopValue,"balls":[{"id":107,"ball":"-,-,-,-,-,-,-,-,龙,-","type":"longhu.longhudou.fushi","moneyunit":"1","multiple":1,"awardMode":awardmode,"num":1},{"id":106,"ball":"双,大","type":"daxiaodanshuang.dxds.houer","moneyunit":"1","multiple":1,"awardMode":awardmode,"num":1},{"id":105,"ball":"小","type":"daxiaodanshuang.dxds.houyi","moneyunit":"1","multiple":1,"awardMode":awardmode,"num":1},{"id":104,"ball":"小,双","type":"daxiaodanshuang.dxds.qianer","moneyunit":"1","multiple":1,"awardMode":awardmode,"num":1},{"id":103,"ball":"小","type":"daxiaodanshuang.dxds.qianyi","moneyunit":"1","multiple":1,"awardMode":awardmode,"num":1},{"id":102,"ball":"小","type":"daxiaodanshuang.dxds.zonghe","moneyunit":"1","multiple":1,"awardMode":awardmode,"num":1},{"id":101,"ball":"-,3,-,-,-","type":"yixing_2000.dingweidan.fushi","moneyunit":"1","multiple":1,"awardMode":awardmode,"num":1},{"id":100,"ball":"8","type":"houer_2000.zuxuan.baodan","moneyunit":"1","multiple":1,"awardMode":awardmode,"num":9},{"id":99,"ball":"13","type":"houer_2000.zuxuan.hezhi","moneyunit":"1","multiple":1,"awardMode":awardmode,"num":3},{"id":98,"ball":"25","type":"houer_2000.zuxuan.danshi","moneyunit":"1","multiple":1,"awardMode":awardmode,"num":1},{"id":97,"ball":"1,8","type":"houer_2000.zuxuan.fushi","moneyunit":"1","multiple":1,"awardMode":awardmode,"num":1},{"id":96,"ball":"5","type":"houer_2000.zhixuan.kuadu","moneyunit":"1","multiple":1,"awardMode":awardmode,"num":10},{"id":95,"ball":"14","type":"houer_2000.zhixuan.hezhi","moneyunit":"1","multiple":1,"awardMode":awardmode,"num":5},{"id":94,"ball":"65","type":"houer_2000.zhixuan.danshi","moneyunit":"1","multiple":1,"awardMode":awardmode,"num":1},{"id":93,"ball":"-,-,-,5,9","type":"houer_2000.zhixuan.fushi","moneyunit":"1","multiple":1,"awardMode":awardmode,"num":1},{"id":92,"ball":"2,7","type":"housan_2000.budingwei.ermabudingwei","moneyunit":"1","multiple":1,"awardMode":awardmode,"num":1},{"id":91,"ball":"7","type":"housan_2000.budingwei.yimabudingwei","moneyunit":"1","multiple":1,"awardMode":awardmode,"num":1},{"id":90,"ball":"047","type":"housan_2000.zuxuan.zuliudanshi","moneyunit":"1","multiple":1,"awardMode":awardmode,"num":1},{"id":89,"ball":"336","type":"housan_2000.zuxuan.zusandanshi","moneyunit":"1","multiple":1,"awardMode":awardmode,"num":1},{"id":88,"ball":"6","type":"housan_2000.zuxuan.baodan","moneyunit":"1","multiple":1,"awardMode":awardmode,"num":54},{"id":87,"ball":"024","type":"housan_2000.zuxuan.hunhezuxuan","moneyunit":"1","multiple":1,"awardMode":awardmode,"num":1},{"id":86,"ball":"2,5,9","type":"housan_2000.zuxuan.zuliu","moneyunit":"1","multiple":1,"awardMode":awardmode,"num":1},{"id":85,"ball":"5,9","type":"housan_2000.zuxuan.zusan","moneyunit":"1","multiple":1,"awardMode":awardmode,"num":2},{"id":84,"ball":"11","type":"housan_2000.zuxuan.hezhi","moneyunit":"1","multiple":1,"awardMode":awardmode,"num":14},{"id":83,"ball":"0","type":"housan_2000.zhixuan.kuadu","moneyunit":"1","multiple":1,"awardMode":awardmode,"num":10},{"id":82,"ball":"1","type":"housan_2000.zhixuan.hezhi","moneyunit":"1","multiple":1,"awardMode":awardmode,"num":3},{"id":81,"ball":"904","type":"housan_2000.zhixuan.danshi","moneyunit":"1","multiple":1,"awardMode":awardmode,"num":1},{"id":80,"ball":"-,-,3,7,4","type":"housan_2000.zhixuan.fushi","moneyunit":"1","multiple":1,"awardMode":awardmode,"num":1},{"id":79,"ball":"-,0,-,-,-","type":"yixing.dingweidan.fushi","moneyunit":"1","multiple":1,"awardMode":awardmode,"num":1},{"id":78,"ball":"8","type":"houer.zuxuan.baodan","moneyunit":"1","multiple":1,"awardMode":awardmode,"num":9},{"id":77,"ball":"12","type":"houer.zuxuan.hezhi","moneyunit":"1","multiple":1,"awardMode":awardmode,"num":3},{"id":76,"ball":"48","type":"houer.zuxuan.danshi","moneyunit":"1","multiple":1,"awardMode":awardmode,"num":1},{"id":75,"ball":"4,6","type":"houer.zuxuan.fushi","moneyunit":"1","multiple":1,"awardMode":awardmode,"num":1},{"id":74,"ball":"8","type":"houer.zhixuan.kuadu","moneyunit":"1","multiple":1,"awardMode":awardmode,"num":4},{"id":73,"ball":"3","type":"houer.zhixuan.hezhi","moneyunit":"1","multiple":1,"awardMode":awardmode,"num":4},{"id":72,"ball":"12","type":"houer.zhixuan.danshi","moneyunit":"1","multiple":1,"awardMode":awardmode,"num":1},{"id":71,"ball":"-,-,-,7,9","type":"houer.zhixuan.fushi","moneyunit":"1","multiple":1,"awardMode":awardmode,"num":1},{"id":70,"ball":"8","type":"qianer.zuxuan.baodan","moneyunit":"1","multiple":1,"awardMode":awardmode,"num":9},{"id":69,"ball":"10","type":"qianer.zuxuan.hezhi","moneyunit":"1","multiple":1,"awardMode":awardmode,"num":4},{"id":68,"ball":"37","type":"qianer.zuxuan.danshi","moneyunit":"1","multiple":1,"awardMode":awardmode,"num":1},{"id":67,"ball":"6,8","type":"qianer.zuxuan.fushi","moneyunit":"1","multiple":1,"awardMode":awardmode,"num":1},{"id":66,"ball":"7","type":"qianer.zhixuan.kuadu","moneyunit":"1","multiple":1,"awardMode":awardmode,"num":6},{"id":65,"ball":"9","type":"qianer.zhixuan.hezhi","moneyunit":"1","multiple":1,"awardMode":awardmode,"num":10},{"id":64,"ball":"23","type":"qianer.zhixuan.danshi","moneyunit":"1","multiple":1,"awardMode":awardmode,"num":1},{"id":63,"ball":"6,7,-,-,-","type":"qianer.zhixuan.fushi","moneyunit":"1","multiple":1,"awardMode":awardmode,"num":1},{"id":62,"ball":"1,2","type":"housan.budingwei.ermabudingwei","moneyunit":"1","multiple":1,"awardMode":awardmode,"num":1},{"id":61,"ball":"5","type":"housan.budingwei.yimabudingwei","moneyunit":"1","multiple":1,"awardMode":awardmode,"num":1},{"id":60,"ball":"457","type":"housan.zuxuan.zuliudanshi","moneyunit":"1","multiple":1,"awardMode":awardmode,"num":1},{"id":59,"ball":"113","type":"housan.zuxuan.zusandanshi","moneyunit":"1","multiple":1,"awardMode":awardmode,"num":1},{"id":58,"ball":"1","type":"housan.zuxuan.baodan","moneyunit":"1","multiple":1,"awardMode":awardmode,"num":54},{"id":57,"ball":"236","type":"housan.zuxuan.hunhezuxuan","moneyunit":"1","multiple":1,"awardMode":awardmode,"num":1},{"id":56,"ball":"5,6,9","type":"housan.zuxuan.zuliu","moneyunit":"1","multiple":1,"awardMode":awardmode,"num":1},{"id":55,"ball":"6,8","type":"housan.zuxuan.zusan","moneyunit":"1","multiple":1,"awardMode":awardmode,"num":2},{"id":54,"ball":"16","type":"housan.zuxuan.hezhi","moneyunit":"1","multiple":1,"awardMode":awardmode,"num":14},{"id":53,"ball":"3","type":"housan.zhixuan.kuadu","moneyunit":"1","multiple":1,"awardMode":awardmode,"num":126},{"id":52,"ball":"9","type":"housan.zhixuan.hezhi","moneyunit":"1","multiple":1,"awardMode":awardmode,"num":55},{"id":51,"ball":"561","type":"housan.zhixuan.danshi","moneyunit":"1","multiple":1,"awardMode":awardmode,"num":1},{"id":50,"ball":"-,-,3,6,4","type":"housan.zhixuan.fushi","moneyunit":"1","multiple":1,"awardMode":awardmode,"num":1},{"id":49,"ball":"1,9","type":"zhongsan.budingwei.ermabudingwei","moneyunit":"1","multiple":1,"awardMode":awardmode,"num":1},{"id":48,"ball":"8","type":"zhongsan.budingwei.yimabudingwei","moneyunit":"1","multiple":1,"awardMode":awardmode,"num":1},{"id":47,"ball":"179","type":"zhongsan.zuxuan.zuliudanshi","moneyunit":"1","multiple":1,"awardMode":awardmode,"num":1},{"id":46,"ball":"002","type":"zhongsan.zuxuan.zusandanshi","moneyunit":"1","multiple":1,"awardMode":awardmode,"num":1},{"id":45,"ball":"2","type":"zhongsan.zuxuan.baodan","moneyunit":"1","multiple":1,"awardMode":awardmode,"num":54},{"id":44,"ball":"018","type":"zhongsan.zuxuan.hunhezuxuan","moneyunit":"1","multiple":1,"awardMode":awardmode,"num":1},{"id":43,"ball":"0,4,9","type":"zhongsan.zuxuan.zuliu","moneyunit":"1","multiple":1,"awardMode":awardmode,"num":1},{"id":42,"ball":"0,9","type":"zhongsan.zuxuan.zusan","moneyunit":"1","multiple":1,"awardMode":awardmode,"num":2},{"id":41,"ball":"20","type":"zhongsan.zuxuan.hezhi","moneyunit":"1","multiple":1,"awardMode":awardmode,"num":8},{"id":40,"ball":"7","type":"zhongsan.zhixuan.kuadu","moneyunit":"1","multiple":1,"awardMode":awardmode,"num":126},{"id":39,"ball":"042","type":"zhongsan.zhixuan.danshi","moneyunit":"1","multiple":1,"awardMode":awardmode,"num":1},{"id":38,"ball":"398","type":"zhongsan.zhixuan.danshi","moneyunit":"1","multiple":1,"awardMode":awardmode,"num":1},{"id":37,"ball":"-,7,8,2,-","type":"zhongsan.zhixuan.fushi","moneyunit":"1","multiple":1,"awardMode":awardmode,"num":1},{"id":36,"ball":"1,2","type":"qiansan.budingwei.ermabudingwei","moneyunit":"1","multiple":1,"awardMode":awardmode,"num":1},{"id":35,"ball":"5","type":"qiansan.budingwei.yimabudingwei","moneyunit":"1","multiple":1,"awardMode":awardmode,"num":1},{"id":34,"ball":"035","type":"qiansan.zuxuan.zuliudanshi","moneyunit":"1","multiple":1,"awardMode":awardmode,"num":1},{"id":33,"ball":"113","type":"qiansan.zuxuan.zusandanshi","moneyunit":"1","multiple":1,"awardMode":awardmode,"num":1},{"id":32,"ball":"9","type":"qiansan.zuxuan.baodan","moneyunit":"1","multiple":1,"awardMode":awardmode,"num":54},{"id":31,"ball":"277","type":"qiansan.zuxuan.hunhezuxuan","moneyunit":"1","multiple":1,"awardMode":awardmode,"num":1},{"id":30,"ball":"1,7,8","type":"qiansan.zuxuan.zuliu","moneyunit":"1","multiple":1,"awardMode":awardmode,"num":1},{"id":29,"ball":"1,8","type":"qiansan.zuxuan.zusan","moneyunit":"1","multiple":1,"awardMode":awardmode,"num":2},{"id":28,"ball":"9","type":"qiansan.zuxuan.hezhi","moneyunit":"1","multiple":1,"awardMode":awardmode,"num":11},{"id":27,"ball":"8","type":"qiansan.zhixuan.kuadu","moneyunit":"1","multiple":1,"awardMode":awardmode,"num":96},{"id":26,"ball":"0","type":"qiansan.zhixuan.hezhi","moneyunit":"1","multiple":1,"awardMode":awardmode,"num":1},{"id":25,"ball":"037","type":"qiansan.zhixuan.danshi","moneyunit":"1","multiple":1,"awardMode":awardmode,"num":1},{"id":24,"ball":"9,6,9,-,-","type":"qiansan.zhixuan.fushi","moneyunit":"1","multiple":1,"awardMode":awardmode,"num":1},{"id":23,"ball":"5,7","type":"sixing.budingwei.ermabudingwei","moneyunit":"1","multiple":1,"awardMode":awardmode,"num":1},{"id":22,"ball":"3","type":"sixing.budingwei.yimabudingwei","moneyunit":"1","multiple":1,"awardMode":awardmode,"num":1},{"id":21,"ball":"0,9","type":"sixing.zuxuan.zuxuan4","moneyunit":"1","multiple":1,"awardMode":awardmode,"num":1},{"id":20,"ball":"2,9","type":"sixing.zuxuan.zuxuan6","moneyunit":"1","multiple":1,"awardMode":awardmode,"num":1},{"id":19,"ball":"5,03","type":"sixing.zuxuan.zuxuan12","moneyunit":"1","multiple":1,"awardMode":awardmode,"num":1},{"id":18,"ball":"3,4,5,8","type":"sixing.zuxuan.zuxuan24","moneyunit":"1","multiple":1,"awardMode":awardmode,"num":1},{"id":17,"ball":"9545","type":"sixing.zhixuan.danshi","moneyunit":"1","multiple":1,"awardMode":awardmode,"num":1},{"id":16,"ball":"-,5,5,2,3","type":"sixing.zhixuan.fushi","moneyunit":"1",
            "multiple":1,"awardMode":awardmode,"num":1},{"id":15,"ball":"8",
                "type":"wuxing.quwei.sijifacai","moneyunit":"1","multiple":1,"awardMode":awardmode,"num":1},{"id":14,"ball":"8","type":"wuxing.quwei.sanxingbaoxi","moneyunit":"1","multiple":1,"awardMode":awardmode,"num":1},{"id":13,"ball":"7","type":"wuxing.quwei.haoshichengshuang","moneyunit":"1","multiple":1,"awardMode":awardmode,"num":1},{"id":12,"ball":"4","type":"wuxing.quwei.yifanfengshun","moneyunit":"1","multiple":1,"awardMode":awardmode,"num":1},{"id":11,"ball":"0,5,8","type":"wuxing.budingwei.sanmabudingwei","moneyunit":"1","multiple":1,"awardMode":awardmode,"num":1},{"id":10,"ball":"2,7","type":"wuxing.budingwei.ermabudingwei","moneyunit":"1","multiple":1,"awardMode":awardmode,"num":1},{"id":9,"ball":"5","type":"wuxing.budingwei.yimabudingwei","moneyunit":"1","multiple":1,"awardMode":awardmode,"num":1},{"id":8,"ball":"9,8","type":"wuxing.zuxuan.zuxuan5","moneyunit":"1","multiple":1,"awardMode":awardmode,"num":1},{"id":7,"ball":"5,1","type":"wuxing.zuxuan.zuxuan10","moneyunit":"1","multiple":1,"awardMode":awardmode,"num":1},{"id":6,"ball":"4,01","type":"wuxing.zuxuan.zuxuan20","moneyunit":"1","multiple":1,"awardMode":awardmode,"num":1},{"id":5,"ball":"57,4","type":"wuxing.zuxuan.zuxuan30","moneyunit":"1","multiple":1,"awardMode":awardmode,"num":1},{"id":4,"ball":"6,357","type":"wuxing.zuxuan.zuxuan60","moneyunit":"1","multiple":1,"awardMode":awardmode,"num":1},{"id":3,"ball":"0,1,5,6,7","type":"wuxing.zuxuan.zuxuan120","moneyunit":"1","multiple":1,"awardMode":awardmode,"num":1},{"id":2,"ball":"32077","type":"wuxing.zhixuan.danshi","moneyunit":"1","multiple":1,"awardMode":awardmode,"num":1},{"id":1,"ball":"1,7,1,0,6","type":"wuxing.zhixuan.fushi","moneyunit":"1","multiple":1,"awardMode":awardmode,"num":1}],"orders":order_plan ,"amount":1680*len_order}

        elif lottery in ['ahk3','jsk3']:
            data_ = {"gameType":lottery,"isTrace":isTrace,"traceWinStop":traceWinStop,"traceStopValue":traceStopValue,"balls":[{"id":9,"ball":"6","type":"yibutonghao.yibutonghao.yibutonghao","moneyunit":"1","multiple":1,"awardMode":awardmode,"num":1},{"id":8,"ball":"2,4","type":"erbutonghao.biaozhun.biaozhuntouzhu","moneyunit":"1","multiple":1,"awardMode":awardmode,"num":1},{"id":7,"ball":"11#3","type":"ertonghaodanxuan.ertonghaodanxuan.ertonghaodanxuan","moneyunit":"1","multiple":1,"awardMode":awardmode,"num":1},{"id":6,"ball":"55*","type":"ertonghaofuxuan.ertonghaofuxuan.ertonghaofuxuan","moneyunit":"1","multiple":1,"awardMode":awardmode,"num":1},{"id":5,"ball":"123 234 345 456","type":"sanlianhaotongxuan.sanlianhaotongxuan.sanlianhaotongxuan","moneyunit":"1","multiple":1,"awardMode":awardmode,"num":1},{"id":4,"ball":"1,2,6","type":"sanbutonghao.biaozhun.biaozhuntouzhu","moneyunit":"1","multiple":1,"awardMode":awardmode,"num":1},{"id":3,"ball":"111","type":"santonghaodanxuan.santonghaodanxuan.santonghaodanxuan","moneyunit":"1","multiple":1,"awardMode":awardmode,"num":1},{"id":2,"ball":"111 222 333 444 555 666","type":"santonghaotongxuan.santonghaotongxuan.santonghaotongxuan","moneyunit":"1","multiple":1,"awardMode":awardmode,"num":1},{"id":1,"ball":"14","type":"hezhi.hezhi.hezhi","moneyunit":"1","multiple":1,"awardMode":awardmode,"num":1}],"orders":order_plan ,"amount":18*len_order}
        elif lottery in ['sd115','jx115','gd115','sl115']:
            data_ = {"gameType":lottery,"isTrace":isTrace,"traceWinStop":traceWinStop,"traceStopValue":traceStopValue,"balls":[{"id":37,"ball":"03","type":"quwei.normal.caizhongwei","moneyunit":1,"multiple":1,"awardMode":awardmode,"num":1},{"id":36,"ball":"4单1双","type":"quwei.normal.dingdanshuang","moneyunit":1,"multiple":1,"awardMode":awardmode,"num":1},{"id":35,"ball":"[胆02]  01,05,06,08,09,10,11","type":"xuanba.renxuanbazhongwu.dantuo","moneyunit":1,"multiple":1,"awardMode":awardmode,"num":1},{"id":34,"ball":"01 03 05 06 08 09 10 11","type":"xuanba.renxuanbazhongwu.danshi","moneyunit":1,"multiple":1,"awardMode":awardmode,"num":1},{"id":33,"ball":"01,02,03,05,06,07,08,10","type":"xuanba.renxuanbazhongwu.fushi","moneyunit":1,"multiple":1,"awardMode":awardmode,"num":1},{"id":32,"ball":"[胆01]  04,05,08,09,10,11","type":"xuanqi.renxuanqizhongwu.dantuo","moneyunit":1,"multiple":1,"awardMode":awardmode,"num":1},{"id":31,"ball":"01 02 04 05 06 10 11","type":"xuanqi.renxuanqizhongwu.danshi","moneyunit":1,"multiple":1,"awardMode":awardmode,"num":1},{"id":30,"ball":"02,03,06,08,09,10,11","type":"xuanqi.renxuanqizhongwu.fushi","moneyunit":1,"multiple":1,"awardMode":awardmode,"num":1},{"id":29,"ball":"[胆10]  01,03,06,08,09","type":"xuanliu.renxuanliuzhongwu.dantuo","moneyunit":1,"multiple":1,"awardMode":awardmode,"num":1},{"id":28,"ball":"01 04 05 07 09 10","type":"xuanliu.renxuanliuzhongwu.danshi","moneyunit":1,"multiple":1,"awardMode":awardmode,"num":1},{"id":27,"ball":"01,03,05,06,09,10","type":"xuanliu.renxuanliuzhongwu.fushi","moneyunit":1,"multiple":1,"awardMode":awardmode,"num":1},{"id":26,"ball":"[胆10]  01,05,07,11","type":"xuanwu.renxuanwuzhongwu.dantuo","moneyunit":1,"multiple":1,"awardMode":awardmode,"num":1},{"id":25,"ball":"01 03 06 07 09","type":"xuanwu.renxuanwuzhongwu.danshi","moneyunit":1,"multiple":1,"awardMode":awardmode,"num":1},{"id":24,"ball":"03,04,06,09,11","type":"xuanwu.renxuanwuzhongwu.fushi","moneyunit":1,"multiple":1,"awardMode":awardmode,"num":1},{"id":23,"ball":"[胆10]  03,08,09","type":"xuansi.renxuansizhongsi.dantuo","moneyunit":1,"multiple":1,"awardMode":awardmode,"num":1},{"id":22,"ball":"03 07 08 10","type":"xuansi.renxuansizhongsi.danshi","moneyunit":1,"multiple":1,"awardMode":awardmode,"num":1},{"id":21,"ball":"02,03,04,06","type":"xuansi.renxuansizhongsi.fushi","moneyunit":1,"multiple":1,"awardMode":awardmode,"num":1},{"id":20,"ball":"[胆02]  01,11","type":"xuansan.renxuansanzhongsan.renxuandantuo","moneyunit":1,"multiple":1,"awardMode":awardmode,"num":1},{"id":19,"ball":"01 07 08","type":"xuansan.renxuansanzhongsan.renxuandanshi","moneyunit":1,"multiple":1,"awardMode":awardmode,"num":1},{"id":18,"ball":"02,05,10","type":"xuansan.renxuansanzhongsan.renxuanfushi","moneyunit":1,"multiple":1,"awardMode":awardmode,"num":1},{"id":17,"ball":"[胆02]  06,08","type":"xuansan.qiansanzuxuan.zuxuandantuo","moneyunit":1,"multiple":1,"awardMode":awardmode,"num":1},{"id":16,"ball":"01 04 09","type":"xuansan.qiansanzuxuan.zuxuandanshi","moneyunit":1,"multiple":1,"awardMode":awardmode,"num":1},{"id":15,"ball":"03,08,09","type":"xuansan.qiansanzuxuan.zuxuanfushi","moneyunit":1,"multiple":1,"awardMode":awardmode,"num":1},{"id":14,"ball":"08 09 06","type":"xuansan.qiansanzhixuan.zhixuandanshi","moneyunit":1,"multiple":1,"awardMode":awardmode,"num":1},{"id":13,"ball":"10,01,02,-,-","type":"xuansan.qiansanzhixuan.zhixuanfushi","moneyunit":1,"multiple":1,"awardMode":awardmode,"num":1},{"id":12,"ball":"[胆 10] 09","type":"xuaner.renxuanerzhonger.renxuandantuo","moneyunit":1,"multiple":1,"awardMode":awardmode,"num":1},{"id":11,"ball":"09 10","type":"xuaner.renxuanerzhonger.renxuandanshi","moneyunit":1,"multiple":1,"awardMode":awardmode,"num":1},{"id":10,"ball":"02,06","type":"xuaner.renxuanerzhonger.renxuanfushi","moneyunit":1,"multiple":1,"awardMode":awardmode,"num":1},{"id":9,"ball":"[胆 01] 08","type":"xuaner.qianerzuxuan.zuxuandantuo","moneyunit":1,"multiple":1,"awardMode":awardmode,"num":1},{"id":8,"ball":"06 07","type":"xuaner.qianerzuxuan.zuxuandanshi","moneyunit":1,"multiple":1,"awardMode":awardmode,"num":1},{"id":7,"ball":"02,03","type":"xuaner.qianerzuxuan.zuxuanfushi","moneyunit":1,"multiple":1,"awardMode":awardmode,"num":1},{"id":6,"ball":"02 04","type":"xuaner.qianerzhixuan.zhixuandanshi","moneyunit":1,"multiple":1,"awardMode":awardmode,"num":1},{"id":5,"ball":"07,02,-,-,-","type":"xuaner.qianerzhixuan.zhixuanfushi","moneyunit":1,"multiple":1,"awardMode":awardmode,"num":1},{"id":4,"ball":"05","type":"xuanyi.renxuanyizhongyi.danshi","moneyunit":"1","multiple":1,"awardMode":awardmode,"num":1},{"id":3,"ball":"05","type":"xuanyi.renxuanyizhongyi.fushi","moneyunit":"1","multiple":1,"awardMode":awardmode,"num":1},{"id":2,"ball":"04,-,-,-,-","type":"xuanyi.dingweidan.fushi","moneyunit":"1","multiple":1,"awardMode":awardmode,"num":1},{"id":1,"ball":"02","type":"xuanyi.qiansanyimabudingwei.fushi","moneyunit":"1","multiple":1,"awardMode":awardmode,"num":1}],"orders":order_plan ,"amount":74*len_order}          
        elif lottery in ['pk10','xyft']:   
            data_ = {"gameType": lottery, "isTrace": isTrace, "traceWinStop": traceWinStop, "traceStopValue": traceStopValue, "balls": [{"id": 22, "ball": "-,-,-,-,-,01 02 03 04 05,01 02 03 04 05,01 02 03 04 05,01 02 03 04 05,01 02 03 04 05", "type": "caipaiwei.dingweidan.houfushi", "moneyunit": 1, "multiple": 1, "awardMode": awardmode, "amount": 50, "num": 25}, {"id": 21, "ball": "06 07 08 09 10,06 07 08 09 10,06 07 08 09 10,06 07 08 09 10,06 07 08 09 10,-,-,-,-,-", "type": "caipaiwei.dingweidan.qianfushi", "moneyunit": 1, "multiple": 1, "awardMode": awardmode, "amount": 50, "num": 25}, {"id": 20, "ball": "02 06 07 08 09", "type": "qianwu.zuxuan.danshi", "moneyunit": 1, "multiple": 1, "awardMode": awardmode, "amount": 2, "num": 1}, {"id": 19, "ball": "06,07,08,09,10", "type": "qianwu.zuxuan.fushi", "moneyunit": 1, "multiple": 1, "awardMode": awardmode, "amount": 2, "num": 1}, {"id": 18, "ball": "01 04 05 06 07", "type": "qianwu.zhixuan.danshi", "moneyunit": 1, "multiple": 1, "awardMode": awardmode, "amount": 2, "num": 1}, {"id": 17, "ball": "02 04 06 08 10,02 04 06 08 10,02 04 06 08 10,02 04 06 08 10,02 04 06 08 10,-,-,-,-,-", "type": "qianwu.zhixuan.fushi", "moneyunit": 1, "multiple": 1, "awardMode": awardmode, "amount": 240, "num": 120}, {"id": 16, "ball": "06 07 08 09", "type": "qiansi.zuxuan.danshi", "moneyunit": 1, "multiple": 1, "awardMode": awardmode, "amount": 2, "num": 1}, {"id": 15, "ball": "02,04,06,08,10", "type": "qiansi.zuxuan.fushi", "moneyunit": 1, "multiple": 1, "awardMode": awardmode, "amount": 10, "num": 5}, {"id": 14, "ball": "06 07 08 09", "type": "qiansi.zhixuan.danshi", "moneyunit": 1, "multiple": 1, "awardMode": awardmode, "amount": 2, "num": 1}, {"id": 13, "ball": "02 04 06 08 10,02 04 06 08 10,02 04 06 08 10,02 04 06 08 10,-,-,-,-,-,-", "type": "qiansi.zhixuan.fushi", "moneyunit": 1, "multiple": 1, "awardMode": awardmode, "amount": 240, "num": 120}, {"id": 12, "ball": "05 06 07", "type": "guanyaji.caiguanyaji.danshi", "moneyunit": 1, "multiple": 1, "awardMode": awardmode, "amount": 2, "num": 1}, {"id": 11, "ball": "01 02 03 04 05,01 02 03 04 05,01 02 03 04 05,-,-,-,-,-,-,-", "type": "guanyaji.caiguanyaji.fushi", "moneyunit": 1, "multiple": 1, "awardMode": awardmode, "amount": 120, "num": 60}, {"id": 10, "ball": "05 06 07", "type": "guanyaji.zuxuan.danshi", "moneyunit": 1, "multiple": 1, "awardMode": awardmode, "amount": 2, "num": 1}, {"id": 9, "ball": "01,02,03,04,05", "type": "guanyaji.zuxuan.fushi", "moneyunit": 1, "multiple": 1, "awardMode": awardmode, "amount": 20, "num": 10}, {"id": 8, "ball": "05 06 07", "type": "guanyaji.zhixuan.danshi", "moneyunit": 1, "multiple": 1, "awardMode": awardmode, "amount": 2, "num": 1}, {"id": 7, "ball": "01 02 03 04 05,01 02 03 04 05,01 02 03 04 05,-,-,-,-,-,-,-", "type": "guanyaji.zhixuan.fushi", "moneyunit": 1, "multiple": 1, "awardMode": awardmode, "amount": 120, "num": 60}, {"id": 6, "ball": "01 02", "type": "guanya.caiguanya.danshi", "moneyunit": 1, "multiple": 1, "awardMode": awardmode, "amount": 2, "num": 1}, {"id": 5, "ball": "01 02 03 04 05,01 02 03 04 05,-,-,-,-,-,-,-,-", "type": "guanya.caiguanya.fushi", "moneyunit": 1, "multiple": 1, "awardMode": awardmode, "amount": 40, "num": 20}, {"id": 4, "ball": "3,4,5,6,7,8,9,10,11", "type": "guanya.hezhi.fushi", "moneyunit": 1, "multiple": 1, "awardMode": awardmode, "amount": 100, "num": 50}, {"id": 3, "ball": "01 02", "type": "guanya.zuxuan.danshi", "moneyunit": 1, "multiple": 1, "awardMode": awardmode, "amount": 2, "num": 1}, {"id": 2, "ball": "01,02,03,04,05", "type": "guanya.zuxuan.fushi", "moneyunit": 1, "multiple": 1, "awardMode": awardmode, "amount": 20, "num": 10}, {"id": 1, "ball": "01 02", "type": "guanya.zhixuan.danshi", "moneyunit": 1, "multiple": 1, "awardMode": awardmode, "amount": 2, "num": 1}], "orders": order_plan ,"amount":1032*len_order}
        elif lottery == 'slmmc':
            data_ = {"gameType":"slmmc","isTrace":0,"traceWinStop":0,"traceStopValue":-1,"balls":[{"id":1,"ball":"9,9,-,-,-","type":"qianer.zhixuan.fushi","moneyunit":1,"multiple":2222,"awardMode":2,"num":1}],"orders":[{"number":"/","issueCode":1,"multiple":1}],"amount":4444,"redDiscountAmount":0}
        elif lottery in ['llssc','jlffc','btcffc']:
            data_ = {"gameType":lottery,"isTrace":isTrace,"traceWinStop":traceWinStop,"traceStopValue":traceStopValue,"balls":[{"id":85,"ball":"-,和,-,-,-,-,-,-,-,-","type":"longhu.longhudou.fushi","moneyunit":1,"multiple":1,"awardMode":awardmode,"num":1},{"id":84,"ball":"双,大","type":"daxiaodanshuang.dxds.houer","moneyunit":1,"multiple":1,"awardMode":awardmode,"num":1},{"id":83,"ball":"小","type":"daxiaodanshuang.dxds.houyi","moneyunit":1,"multiple":1,"awardMode":awardmode,"num":1},{"id":82,"ball":"大,单","type":"daxiaodanshuang.dxds.qianer","moneyunit":1,"multiple":1,"awardMode":awardmode,"num":1},{"id":81,"ball":"大","type":"daxiaodanshuang.dxds.qianyi","moneyunit":1,"multiple":1,"awardMode":awardmode,"num":1},{"id":80,"ball":"双","type":"daxiaodanshuang.dxds.zonghe","moneyunit":1,"multiple":1,"awardMode":awardmode,"num":1},{"id":79,"ball":"-,-,-,5,-","type":"yixing.dingweidan.fushi","moneyunit":1,"multiple":1,"awardMode":awardmode,"num":1},{"id":78,"ball":"5","type":"houer.zuxuan.baodan","moneyunit":1,"multiple":1,"awardMode":awardmode,"num":9},{"id":77,"ball":"11","type":"houer.zuxuan.hezhi","moneyunit":1,"multiple":1,"awardMode":awardmode,"num":4},{"id":76,"ball":"46","type":"houer.zuxuan.danshi","moneyunit":1,"multiple":1,"awardMode":awardmode,"num":1},{"id":75,"ball":"2,4","type":"houer.zuxuan.fushi","moneyunit":1,"multiple":1,"awardMode":awardmode,"num":1},{"id":74,"ball":"3","type":"houer.zhixuan.kuadu","moneyunit":1,"multiple":1,"awardMode":awardmode,"num":14},{"id":73,"ball":"5","type":"houer.zhixuan.hezhi","moneyunit":1,"multiple":1,"awardMode":awardmode,"num":6},{"id":72,"ball":"49","type":"houer.zhixuan.danshi","moneyunit":1,"multiple":1,"awardMode":awardmode,"num":1},{"id":71,"ball":"-,-,-,3,6","type":"houer.zhixuan.fushi","moneyunit":1,"multiple":1,"awardMode":awardmode,"num":1},{"id":70,"ball":"7","type":"qianer.zuxuan.baodan","moneyunit":1,"multiple":1,"awardMode":awardmode,"num":9},{"id":69,"ball":"8","type":"qianer.zuxuan.hezhi","moneyunit":1,"multiple":1,"awardMode":awardmode,"num":4},{"id":68,"ball":"27","type":"qianer.zuxuan.danshi","moneyunit":1,"multiple":1,"awardMode":awardmode,"num":1},{"id":67,"ball":"1,6","type":"qianer.zuxuan.fushi","moneyunit":1,"multiple":1,"awardMode":awardmode,"num":1},{"id":66,"ball":"4","type":"qianer.zhixuan.kuadu","moneyunit":1,"multiple":1,"awardMode":awardmode,"num":12},{"id":65,"ball":"8","type":"qianer.zhixuan.hezhi","moneyunit":1,"multiple":1,"awardMode":awardmode,"num":9},{"id":64,"ball":"31","type":"qianer.zhixuan.danshi","moneyunit":1,"multiple":1,"awardMode":awardmode,"num":1},{"id":63,"ball":"3,5,-,-,-","type":"qianer.zhixuan.fushi","moneyunit":1,"multiple":1,"awardMode":awardmode,"num":1},{"id":62,"ball":"3,5","type":"housan.budingwei.ermabudingwei","moneyunit":1,"multiple":1,"awardMode":awardmode,"num":1},{"id":61,"ball":"7","type":"housan.budingwei.yimabudingwei","moneyunit":1,"multiple":1,"awardMode":awardmode,"num":1},{"id":60,"ball":"078","type":"housan.zuxuan.zuliudanshi","moneyunit":1,"multiple":1,"awardMode":awardmode,"num":1},{"id":59,"ball":"577","type":"housan.zuxuan.zusandanshi","moneyunit":1,"multiple":1,"awardMode":awardmode,"num":1},{"id":58,"ball":"9","type":"housan.zuxuan.baodan","moneyunit":1,"multiple":1,"awardMode":awardmode,"num":54},{"id":57,"ball":"125","type":"housan.zuxuan.hunhezuxuan","moneyunit":1,"multiple":1,"awardMode":awardmode,"num":1},{"id":56,"ball":"2,3,9","type":"housan.zuxuan.zuliu","moneyunit":1,"multiple":1,"awardMode":awardmode,"num":1},{"id":55,"ball":"1,2","type":"housan.zuxuan.zusan","moneyunit":1,"multiple":1,"awardMode":awardmode,"num":2},{"id":54,"ball":"26","type":"housan.zuxuan.hezhi","moneyunit":1,"multiple":1,"awardMode":awardmode,"num":1},{"id":53,"ball":"1","type":"housan.zhixuan.kuadu","moneyunit":1,"multiple":1,"awardMode":awardmode,"num":54},{"id":52,"ball":"6","type":"housan.zhixuan.hezhi","moneyunit":1,"multiple":1,"awardMode":awardmode,"num":28},{"id":51,"ball":"794","type":"housan.zhixuan.danshi","moneyunit":1,"multiple":1,"awardMode":awardmode,"num":1},{"id":50,"ball":"-,-,0,3,8","type":"housan.zhixuan.fushi","moneyunit":1,"multiple":1,"awardMode":awardmode,"num":1},{"id":49,"ball":"5,8","type":"zhongsan.budingwei.ermabudingwei","moneyunit":1,"multiple":1,"awardMode":awardmode,"num":1},{"id":48,"ball":"1","type":"zhongsan.budingwei.yimabudingwei","moneyunit":1,"multiple":1,"awardMode":awardmode,"num":1},{"id":47,"ball":"025","type":"zhongsan.zuxuan.zuliudanshi","moneyunit":1,"multiple":1,"awardMode":awardmode,"num":1},{"id":46,"ball":"338","type":"zhongsan.zuxuan.zusandanshi","moneyunit":1,"multiple":1,"awardMode":awardmode,"num":1},{"id":45,"ball":"5","type":"zhongsan.zuxuan.baodan","moneyunit":1,"multiple":1,"awardMode":awardmode,"num":54},{"id":44,"ball":"149","type":"zhongsan.zuxuan.hunhezuxuan","moneyunit":1,"multiple":1,"awardMode":awardmode,"num":1},{"id":43,"ball":"4,5,7","type":"zhongsan.zuxuan.zuliu","moneyunit":1,"multiple":1,"awardMode":awardmode,"num":1},{"id":42,"ball":"0,3","type":"zhongsan.zuxuan.zusan","moneyunit":1,"multiple":1,"awardMode":awardmode,"num":2},{"id":41,"ball":"14","type":"zhongsan.zuxuan.hezhi","moneyunit":1,"multiple":1,"awardMode":awardmode,"num":15},{"id":40,"ball":"5","type":"zhongsan.zhixuan.kuadu","moneyunit":1,"multiple":1,"awardMode":awardmode,"num":150},{"id":39,"ball":"15","type":"zhongsan.zhixuan.hezhi","moneyunit":1,"multiple":1,"awardMode":awardmode,"num":73},{"id":38,"ball":"669","type":"zhongsan.zhixuan.danshi","moneyunit":1,"multiple":1,"awardMode":awardmode,"num":1},{"id":37,"ball":"-,6,9,1,-","type":"zhongsan.zhixuan.fushi","moneyunit":1,"multiple":1,"awardMode":awardmode,"num":1},{"id":36,"ball":"0,9","type":"qiansan.budingwei.ermabudingwei","moneyunit":1,"multiple":1,"awardMode":awardmode,"num":1},{"id":35,"ball":"3","type":"qiansan.budingwei.yimabudingwei","moneyunit":1,"multiple":1,"awardMode":awardmode,"num":1},{"id":34,"ball":"147","type":"qiansan.zuxuan.zuliudanshi","moneyunit":1,"multiple":1,"awardMode":awardmode,"num":1},{"id":33,"ball":"599","type":"qiansan.zuxuan.zusandanshi","moneyunit":1,"multiple":1,"awardMode":awardmode,"num":1},{"id":32,"ball":"2","type":"qiansan.zuxuan.baodan","moneyunit":1,"multiple":1,"awardMode":awardmode,"num":54},{"id":31,"ball":"159","type":"qiansan.zuxuan.hunhezuxuan","moneyunit":1,"multiple":1,"awardMode":awardmode,"num":1},{"id":30,"ball":"0,5,7","type":"qiansan.zuxuan.zuliu","moneyunit":1,"multiple":1,"awardMode":awardmode,"num":1},{"id":29,"ball":"2,3","type":"qiansan.zuxuan.zusan","moneyunit":1,"multiple":1,"awardMode":awardmode,"num":2},{"id":28,"ball":"14","type":"qiansan.zuxuan.hezhi","moneyunit":1,"multiple":1,"awardMode":awardmode,"num":15},{"id":27,"ball":"4","type":"qiansan.zhixuan.kuadu","moneyunit":1,"multiple":1,"awardMode":awardmode,"num":144},{"id":26,"ball":"2","type":"qiansan.zhixuan.hezhi","moneyunit":1,"multiple":1,"awardMode":awardmode,"num":6},{"id":25,"ball":"582","type":"qiansan.zhixuan.danshi","moneyunit":1,"multiple":1,"awardMode":awardmode,"num":1},{"id":24,"ball":"0,5,8,-,-","type":"qiansan.zhixuan.fushi","moneyunit":1,"multiple":1,"awardMode":awardmode,"num":1},{"id":23,"ball":"1,9","type":"sixing.budingwei.ermabudingwei","moneyunit":1,"multiple":1,"awardMode":awardmode,"num":1},{"id":22,"ball":"8","type":"sixing.budingwei.yimabudingwei","moneyunit":1,"multiple":1,"awardMode":awardmode,"num":1},{"id":21,"ball":"4,0","type":"sixing.zuxuan.zuxuan4","moneyunit":1,"multiple":1,"awardMode":awardmode,"num":1},{"id":20,"ball":"4,5","type":"sixing.zuxuan.zuxuan6","moneyunit":1,"multiple":1,"awardMode":awardmode,"num":1},{"id":19,"ball":"7,28","type":"sixing.zuxuan.zuxuan12","moneyunit":1,"multiple":1,"awardMode":awardmode,"num":1},{"id":18,"ball":"1,2,5,9","type":"sixing.zuxuan.zuxuan24","moneyunit":1,"multiple":1,"awardMode":awardmode,"num":1},{"id":17,"ball":"6266","type":"sixing.zhixuan.danshi","moneyunit":1,"multiple":1,"awardMode":awardmode,"num":1},{"id":16,"ball":"-,9,4,6,4","type":"sixing.zhixuan.fushi","moneyunit":1,"multiple":1,"awardMode":awardmode,"num":1},{"id":15,"ball":"6","type":"wuxing.quwei.sijifacai","moneyunit":1,"multiple":1,"awardMode":awardmode,"num":1},{"id":14,"ball":"6","type":"wuxing.quwei.sanxingbaoxi","moneyunit":1,"multiple":1,"awardMode":awardmode,"num":1},{"id":13,"ball":"8","type":"wuxing.quwei.haoshichengshuang","moneyunit":1,"multiple":1,"awardMode":awardmode,"num":1},{"id":12,"ball":"4","type":"wuxing.quwei.yifanfengshun","moneyunit":1,"multiple":1,"awardMode":awardmode,"num":1},{"id":11,"ball":"0,3,7","type":"wuxing.budingwei.sanmabudingwei","moneyunit":1,"multiple":1,"awardMode":awardmode,"num":1},{"id":10,"ball":"5,8","type":"wuxing.budingwei.ermabudingwei","moneyunit":1,"multiple":1,"awardMode":awardmode,"num":1},{"id":9,"ball":"3","type":"wuxing.budingwei.yimabudingwei","moneyunit":1,"multiple":1,"awardMode":awardmode,"num":1},{"id":8,"ball":"2,7","type":"wuxing.zuxuan.zuxuan5","moneyunit":1,"multiple":1,"awardMode":awardmode,"num":1},{"id":7,"ball":"0,4","type":"wuxing.zuxuan.zuxuan10","moneyunit":1,"multiple":1,"awardMode":awardmode,"num":1},{"id":6,"ball":"4,79","type":"wuxing.zuxuan.zuxuan20","moneyunit":1,"multiple":1,"awardMode":awardmode,"num":1},{"id":5,"ball":"01,3","type":"wuxing.zuxuan.zuxuan30","moneyunit":1,"multiple":1,"awardMode":awardmode,"num":1},{"id":4,"ball":"4,078","type":"wuxing.zuxuan.zuxuan60","moneyunit":1,"multiple":1,"awardMode":awardmode,"num":1},{"id":3,"ball":"1,2,5,6,8","type":"wuxing.zuxuan.zuxuan120","moneyunit":1,"multiple":1,"awardMode":awardmode,"num":1},{"id":2,"ball":"74993","type":"wuxing.zhixuan.danshi","moneyunit":"1","multiple":1,"awardMode":awardmode,"num":1},{"id":1,"ball":"9,9,6,4,8","type":"wuxing.zhixuan.fushi","moneyunit":"1","multiple":1,"awardMode":awardmode,"num":1}],"orders":order_plan ,"redDiscountAmount":0,"amount":1566*len_order}
        elif lottery == 'txffc':
            data_ = {"gameType":lottery,"isTrace":isTrace,"traceWinStop":traceWinStop,"traceStopValue":traceStopValue,"balls":[{"id":85,"ball":"-,-,-,龙,-,-","type":"longhu.longhudou.fushi","moneyunit":"1","multiple":1,"awardMode":awardmode,"num":1},{"id":84,"ball":"大,双","type":"daxiaodanshuang.dxds.houer","moneyunit":"1","multiple":1,"awardMode":awardmode,"num":1},{"id":83,"ball":"单","type":"daxiaodanshuang.dxds.houyi","moneyunit":"1","multiple":1,"awardMode":awardmode,"num":1},{"id":82,"ball":"小","type":"daxiaodanshuang.dxds.houyi","moneyunit":"1","multiple":1,"awardMode":awardmode,"num":1},{"id":81,"ball":"双","type":"daxiaodanshuang.dxds.houyi","moneyunit":"1","multiple":1,"awardMode":awardmode,"num":1},{"id":80,"ball":"大","type":"daxiaodanshuang.dxds.houyi","moneyunit":"1","multiple":1,"awardMode":awardmode,"num":1},{"id":79,"ball":"-,-,-,-,1","type":"yixing.dingweidan.fushi","moneyunit":"1","multiple":1,"awardMode":awardmode,"num":1},{"id":78,"ball":"3","type":"houer.zuxuan.baodan","moneyunit":"1","multiple":1,"awardMode":awardmode,"num":9},{"id":77,"ball":"17","type":"houer.zuxuan.hezhi","moneyunit":"1","multiple":1,"awardMode":awardmode,"num":1},{"id":76,"ball":"57","type":"houer.zuxuan.danshi","moneyunit":"1","multiple":1,"awardMode":awardmode,"num":1},{"id":75,"ball":"6,9","type":"houer.zuxuan.fushi","moneyunit":"1","multiple":1,"awardMode":awardmode,"num":1},{"id":74,"ball":"4","type":"houer.zhixuan.kuadu","moneyunit":"1","multiple":1,"awardMode":awardmode,"num":12},{"id":73,"ball":"1","type":"houer.zhixuan.hezhi","moneyunit":"1","multiple":1,"awardMode":awardmode,"num":2},{"id":72,"ball":"04","type":"houer.zhixuan.danshi","moneyunit":"1","multiple":1,"awardMode":awardmode,"num":1},{"id":71,"ball":"-,-,-,2,2","type":"houer.zhixuan.fushi","moneyunit":"1","multiple":1,"awardMode":awardmode,"num":1},{"id":70,"ball":"7","type":"qianer.zuxuan.baodan","moneyunit":"1","multiple":1,"awardMode":awardmode,"num":9},{"id":69,"ball":"17","type":"qianer.zuxuan.hezhi","moneyunit":"1","multiple":1,"awardMode":awardmode,"num":1},{"id":68,"ball":"05","type":"qianer.zuxuan.danshi","moneyunit":"1","multiple":1,"awardMode":awardmode,"num":1},{"id":67,"ball":"5,7","type":"qianer.zuxuan.fushi","moneyunit":"1","multiple":1,"awardMode":awardmode,"num":1},{"id":66,"ball":"3","type":"qianer.zhixuan.kuadu","moneyunit":"1","multiple":1,"awardMode":awardmode,"num":14},{"id":65,"ball":"13","type":"qianer.zhixuan.hezhi","moneyunit":"1","multiple":1,"awardMode":awardmode,"num":6},{"id":64,"ball":"94","type":"qianer.zhixuan.danshi","moneyunit":"1","multiple":1,"awardMode":awardmode,"num":1},{"id":63,"ball":"2,9,-,-,-","type":"qianer.zhixuan.fushi","moneyunit":"1","multiple":1,"awardMode":awardmode,"num":1},{"id":62,"ball":"0,9","type":"housan.budingwei.ermabudingwei","moneyunit":"1","multiple":1,"awardMode":awardmode,"num":1},{"id":61,"ball":"5","type":"housan.budingwei.yimabudingwei","moneyunit":"1","multiple":1,"awardMode":awardmode,"num":1},{"id":60,"ball":"346","type":"housan.zuxuan.zuliudanshi","moneyunit":"1","multiple":1,"awardMode":awardmode,"num":1},{"id":59,"ball":"455","type":"housan.zuxuan.zusandanshi","moneyunit":"1","multiple":1,"awardMode":awardmode,"num":1},{"id":58,"ball":"2","type":"housan.zuxuan.baodan","moneyunit":"1","multiple":1,"awardMode":awardmode,"num":54},{"id":57,"ball":"346","type":"housan.zuxuan.hunhezuxuan","moneyunit":"1","multiple":1,"awardMode":awardmode,"num":1},{"id":56,"ball":"1,4,7","type":"housan.zuxuan.zuliu","moneyunit":"1","multiple":1,"awardMode":awardmode,"num":1},{"id":55,"ball":"4,9","type":"housan.zuxuan.zusan","moneyunit":"1","multiple":1,"awardMode":awardmode,"num":2},{"id":54,"ball":"2","type":"housan.zuxuan.hezhi","moneyunit":"1","multiple":1,"awardMode":awardmode,"num":2},{"id":53,"ball":"2","type":"housan.zhixuan.kuadu","moneyunit":"1","multiple":1,"awardMode":awardmode,"num":96},{"id":52,"ball":"1","type":"housan.zhixuan.hezhi","moneyunit":"1","multiple":1,"awardMode":awardmode,"num":3},{"id":51,"ball":"207","type":"housan.zhixuan.danshi","moneyunit":"1","multiple":1,"awardMode":awardmode,"num":1},{"id":50,"ball":"-,-,2,5,3","type":"housan.zhixuan.fushi","moneyunit":"1","multiple":1,"awardMode":awardmode,"num":1},{"id":49,"ball":"2,4","type":"zhongsan.budingwei.ermabudingwei","moneyunit":"1","multiple":1,"awardMode":awardmode,"num":1},{"id":48,"ball":"6","type":"zhongsan.budingwei.yimabudingwei","moneyunit":"1","multiple":1,"awardMode":awardmode,"num":1},{"id":47,"ball":"017","type":"zhongsan.zuxuan.zuliudanshi","moneyunit":"1","multiple":1,"awardMode":awardmode,"num":1},{"id":46,"ball":"779","type":"zhongsan.zuxuan.zusandanshi","moneyunit":"1","multiple":1,"awardMode":awardmode,"num":1},{"id":45,"ball":"9","type":"zhongsan.zuxuan.baodan","moneyunit":"1","multiple":1,"awardMode":awardmode,"num":54},{"id":44,"ball":"156","type":"zhongsan.zuxuan.hunhezuxuan","moneyunit":"1","multiple":1,"awardMode":awardmode,"num":1},{"id":43,"ball":"1,4,9","type":"zhongsan.zuxuan.zuliu","moneyunit":"1","multiple":1,"awardMode":awardmode,"num":1},{"id":42,"ball":"1,6","type":"zhongsan.zuxuan.zusan","moneyunit":"1","multiple":1,"awardMode":awardmode,"num":2},{"id":41,"ball":"20","type":"zhongsan.zuxuan.hezhi","moneyunit":"1","multiple":1,"awardMode":awardmode,"num":8},{"id":40,"ball":"7","type":"zhongsan.zhixuan.kuadu","moneyunit":"1","multiple":1,"awardMode":awardmode,"num":126},{"id":39,"ball":"17","type":"zhongsan.zhixuan.hezhi","moneyunit":"1","multiple":1,"awardMode":awardmode,"num":63},{"id":38,"ball":"402","type":"zhongsan.zhixuan.danshi","moneyunit":"1","multiple":1,"awardMode":awardmode,"num":1},{"id":37,"ball":"-,5,2,4,-","type":"zhongsan.zhixuan.fushi","moneyunit":"1","multiple":1,"awardMode":awardmode,"num":1},{"id":36,"ball":"2,3","type":"qiansan.budingwei.ermabudingwei","moneyunit":"1","multiple":1,"awardMode":awardmode,"num":1},{"id":35,"ball":"3","type":"qiansan.budingwei.yimabudingwei","moneyunit":"1","multiple":1,"awardMode":awardmode,"num":1},{"id":34,"ball":"179","type":"qiansan.zuxuan.zuliudanshi","moneyunit":"1","multiple":1,"awardMode":awardmode,"num":1},{"id":33,"ball":"007","type":"qiansan.zuxuan.zusandanshi","moneyunit":"1","multiple":1,"awardMode":awardmode,"num":1},{"id":32,"ball":"3","type":"qiansan.zuxuan.baodan","moneyunit":"1","multiple":1,"awardMode":awardmode,"num":54},{"id":31,"ball":"034","type":"qiansan.zuxuan.hunhezuxuan","moneyunit":"1","multiple":1,"awardMode":awardmode,"num":1},{"id":30,"ball":"3,4,5","type":"qiansan.zuxuan.zuliu","moneyunit":"1","multiple":1,"awardMode":awardmode,"num":1},{"id":29,"ball":"0,1","type":"qiansan.zuxuan.zusan","moneyunit":"1","multiple":1,"awardMode":awardmode,"num":2},{"id":28,"ball":"3","type":"qiansan.zuxuan.hezhi","moneyunit":"1","multiple":1,"awardMode":awardmode,"num":2},{"id":27,"ball":"6","type":"qiansan.zhixuan.kuadu","moneyunit":"1","multiple":1,"awardMode":awardmode,"num":144},{"id":26,"ball":"16","type":"qiansan.zhixuan.hezhi","moneyunit":"1","multiple":1,"awardMode":awardmode,"num":69},{"id":25,"ball":"338","type":"qiansan.zhixuan.danshi","moneyunit":"1","multiple":1,"awardMode":awardmode,"num":1},{"id":24,"ball":"8,8,2,-,-","type":"qiansan.zhixuan.fushi","moneyunit":"1","multiple":1,"awardMode":awardmode,"num":1},{"id":23,"ball":"4,6","type":"sixing.budingwei.ermabudingwei","moneyunit":"1","multiple":1,"awardMode":awardmode,"num":1},{"id":22,"ball":"2","type":"sixing.budingwei.yimabudingwei","moneyunit":"1","multiple":1,"awardMode":awardmode,"num":1},{"id":21,"ball":"5,0","type":"sixing.zuxuan.zuxuan4","moneyunit":"1","multiple":1,"awardMode":awardmode,"num":1},{"id":20,"ball":"6,7","type":"sixing.zuxuan.zuxuan6","moneyunit":"1","multiple":1,"awardMode":awardmode,"num":1},{"id":19,"ball":"9,04","type":"sixing.zuxuan.zuxuan12","moneyunit":"1","multiple":1,"awardMode":awardmode,"num":1},{"id":18,"ball":"3,4,5,8","type":"sixing.zuxuan.zuxuan24","moneyunit":"1","multiple":1,"awardMode":awardmode,"num":1},{"id":17,"ball":"8360","type":"sixing.zhixuan.danshi","moneyunit":"1","multiple":1,"awardMode":awardmode,"num":1},{"id":16,"ball":"-,8,8,3,4","type":"sixing.zhixuan.fushi","moneyunit":"1","multiple":1,"awardMode":awardmode,"num":1},{"id":15,"ball":"6","type":"wuxing.quwei.sijifacai","moneyunit":"1","multiple":1,"awardMode":awardmode,"num":1},{"id":14,"ball":"6","type":"wuxing.quwei.sanxingbaoxi","moneyunit":"1","multiple":1,"awardMode":awardmode,"num":1},{"id":13,"ball":"8","type":"wuxing.quwei.haoshichengshuang","moneyunit":"1","multiple":1,"awardMode":awardmode,"num":1},{"id":12,"ball":"6","type":"wuxing.quwei.yifanfengshun","moneyunit":"1","multiple":1,"awardMode":awardmode,"num":1},{"id":11,"ball":"3,4,8","type":"wuxing.budingwei.sanmabudingwei","moneyunit":"1","multiple":1,"awardMode":awardmode,"num":1},{"id":10,"ball":"3,7","type":"wuxing.budingwei.ermabudingwei","moneyunit":"1","multiple":1,"awardMode":awardmode,"num":1},{"id":9,"ball":"6","type":"wuxing.budingwei.yimabudingwei","moneyunit":"1","multiple":1,"awardMode":awardmode,"num":1},{"id":8,"ball":"3","type":"wuxing.budingwei.yimabudingwei","moneyunit":"1","multiple":1,"awardMode":awardmode,"num":1},{"id":7,"ball":"4","type":"wuxing.budingwei.yimabudingwei","moneyunit":"1","multiple":1,"awardMode":awardmode,"num":1},{"id":6,"ball":"2","type":"wuxing.budingwei.yimabudingwei","moneyunit":"1","multiple":1,"awardMode":awardmode,"num":1},{"id":5,"ball":"6","type":"wuxing.budingwei.yimabudingwei","moneyunit":"1","multiple":1,"awardMode":awardmode,"num":1},{"id":4,"ball":"1","type":"wuxing.budingwei.yimabudingwei","moneyunit":"1","multiple":1,"awardMode":awardmode,"num":1},{"id":3,"ball":"5","type":"wuxing.budingwei.yimabudingwei","moneyunit":"1","multiple":1,"awardMode":awardmode,"num":1},{"id":2,"ball":"0","type":"wuxing.budingwei.yimabudingwei","moneyunit":"1","multiple":1,"awardMode":awardmode,"num":1},{"id":1,"ball":"8","type":"wuxing.budingwei.yimabudingwei","moneyunit":"1","multiple":1,"awardMode":awardmode,"num":1}],"orders":order_plan ,"amount":1594*len_order}
        elif lottery == 'bjkl8':
            data_ = {"gameType":lottery,"isTrace":isTrace,"traceWinStop":traceWinStop,"traceStopValue":traceStopValue,"balls":[{"id":8,"ball":"05,25,42,43,51,67,80","type":"renxuan.putongwanfa.renxuan7","moneyunit":"1","multiple":1,"awardMode":awardmode,"num":1},{"id":7,"ball":"12,28,54,64,69,80","type":"renxuan.putongwanfa.renxuan6","moneyunit":"1","multiple":1,"awardMode":awardmode,"num":1},{"id":6,"ball":"24,29,39,50,71","type":"renxuan.putongwanfa.renxuan5","moneyunit":"1","multiple":1,"awardMode":awardmode,"num":1},{"id":5,"ball":"03,14,51,57","type":"renxuan.putongwanfa.renxuan4","moneyunit":"1","multiple":1,"awardMode":awardmode,"num":1},{"id":4,"ball":"16,52,79","type":"renxuan.putongwanfa.renxuan3","moneyunit":"1","multiple":1,"awardMode":awardmode,"num":1},{"id":3,"ball":"48,74","type":"renxuan.putongwanfa.renxuan2","moneyunit":"1","multiple":1,"awardMode":awardmode,"num":1},{"id":2,"ball":"25","type":"renxuan.putongwanfa.renxuan1","moneyunit":"1","multiple":1,"awardMode":awardmode,"num":1},{"id":1,"ball":"中","type":"quwei.panmian.quweib","moneyunit":"1","multiple":1,"awardMode":awardmode,"num":1}],"orders":order_plan ,"amount":16*len_order}
        elif lottery in ['v3d','fc3d']:
            data_ = {"gameType":lottery,"isTrace":isTrace,"traceWinStop":traceWinStop,"traceStopValue":traceStopValue,"balls":[{"id":30,"ball":"-,1,-","type":"yixing.dingweidan.fushi","moneyunit":1,"multiple":1,"awardMode":awardmode,"num":1},{"id":29,"ball":"6","type":"houer.zuxuan.zuxuanbaodan","moneyunit":1,"multiple":1,"awardMode":awardmode,"num":9},{"id":28,"ball":"12","type":"houer.zuxuan.zuxuanhezhi","moneyunit":1,"multiple":1,"awardMode":awardmode,"num":3},{"id":27,"ball":"28","type":"houer.zuxuan.zuxuandanshi","moneyunit":1,"multiple":1,"awardMode":awardmode,"num":1},{"id":26,"ball":"6,8","type":"houer.zuxuan.zuxuanfushi","moneyunit":1,"multiple":1,"awardMode":awardmode,"num":1},{"id":25,"ball":"1","type":"houer.zhixuan.zhixuankuadu","moneyunit":1,"multiple":1,"awardMode":awardmode,"num":18},{"id":24,"ball":"6","type":"houer.zhixuan.zhixuanhezhi","moneyunit":1,"multiple":1,"awardMode":awardmode,"num":7},{"id":23,"ball":"58","type":"houer.zhixuan.zhixuandanshi","moneyunit":1,"multiple":1,"awardMode":awardmode,"num":1},{"id":22,"ball":"-,4,3","type":"houer.zhixuan.zhixuanfushi","moneyunit":1,"multiple":1,"awardMode":awardmode,"num":1},{"id":21,"ball":"3","type":"qianer.zuxuan.zuxuanbaodan","moneyunit":1,"multiple":1,"awardMode":awardmode,"num":9},{"id":20,"ball":"11","type":"qianer.zuxuan.zuxuanhezhi","moneyunit":1,"multiple":1,"awardMode":awardmode,"num":4},{"id":19,"ball":"05","type":"qianer.zuxuan.zuxuandanshi","moneyunit":1,"multiple":1,"awardMode":awardmode,"num":1},{"id":18,"ball":"1,7","type":"qianer.zuxuan.zuxuanfushi","moneyunit":1,"multiple":1,"awardMode":awardmode,"num":1},{"id":17,"ball":"1","type":"qianer.zhixuan.zhixuankuadu","moneyunit":1,"multiple":1,"awardMode":awardmode,"num":18},{"id":16,"ball":"11","type":"qianer.zhixuan.zhixuanhezhi","moneyunit":1,"multiple":1,"awardMode":awardmode,"num":8},{"id":15,"ball":"23","type":"qianer.zhixuan.zhixuandanshi","moneyunit":1,"multiple":1,"awardMode":awardmode,"num":1},{"id":14,"ball":"1,0,-","type":"qianer.zhixuan.zhixuanfushi","moneyunit":1,"multiple":1,"awardMode":awardmode,"num":1},{"id":13,"ball":"4,7","type":"sanxing.budingwei.ermabudingwei","moneyunit":1,"multiple":1,"awardMode":awardmode,"num":1},{"id":12,"ball":"3","type":"sanxing.budingwei.yimabudingwei","moneyunit":1,"multiple":1,"awardMode":awardmode,"num":1},{"id":11,"ball":"235","type":"sanxing.zuxuan.zuliudanshi","moneyunit":1,"multiple":1,"awardMode":awardmode,"num":1},{"id":10,"ball":"388","type":"sanxing.zuxuan.zusandanshi","moneyunit":1,"multiple":1,"awardMode":awardmode,"num":1},{"id":9,"ball":"1","type":"sanxing.zuxuan.zuxuanbaodan","moneyunit":1,"multiple":1,"awardMode":awardmode,"num":54},{"id":8,"ball":"248","type":"sanxing.zuxuan.hunhezuxuan","moneyunit":1,"multiple":1,"awardMode":awardmode,"num":1},{"id":7,"ball":"3,7,8","type":"sanxing.zuxuan.zuliu","moneyunit":1,"multiple":1,"awardMode":awardmode,"num":1},{"id":6,"ball":"5,7","type":"sanxing.zuxuan.zusan","moneyunit":1,"multiple":1,"awardMode":awardmode,"num":2},{"id":5,"ball":"6","type":"sanxing.zuxuan.zuxuanhezhi","moneyunit":1,"multiple":1,"awardMode":awardmode,"num":6},{"id":4,"ball":"6","type":"sanxing.zhixuan.kuadu","moneyunit":1,"multiple":1,"awardMode":awardmode,"num":144},{"id":3,"ball":"25","type":"sanxing.zhixuan.hezhi","moneyunit":1,"multiple":1,"awardMode":awardmode,"num":6},{"id":2,"ball":"126","type":"sanxing.zhixuan.danshi","moneyunit":"1","multiple":1,"awardMode":awardmode,"num":1},{"id":1,"ball":"4,4,3","type":"sanxing.zhixuan.fushi","moneyunit":"1","multiple":1,"awardMode":awardmode,"num":1}],"orders":order_plan ,"amount":610*len_order}
        elif lottery in ['jsdice','jldice1','jldice2']:
            data_ = {"gameType":lottery,"isTrace":isTrace,"multiple":1,"trace":1,"amount":"520.00","balls":[{"ball":"大","id":0,"moneyunit":1,"multiple":1,"amount":10,"num":5,"type":"daxiao.daxiao"},{"ball":"单","id":1,"moneyunit":1,"multiple":1,"amount":10,"num":5,"type":"danshuang.danshuang"},{"ball":"66*","id":2,"moneyunit":1,"multiple":1,"amount":10,"num":5,"type":"ertonghaofuxuan.ertonghaofuxuan"},{"ball":"55*","id":3,"moneyunit":1,"multiple":1,"amount":10,"num":5,"type":"ertonghaofuxuan.ertonghaofuxuan"},{"ball":"44*","id":4,"moneyunit":1,"multiple":1,"amount":10,"num":5,"type":"ertonghaofuxuan.ertonghaofuxuan"},{"ball":"666","id":5,"moneyunit":1,"multiple":1,"amount":10,"num":5,"type":"santonghaodanxuan.santonghaodanxuan"},{"ball":"555","id":6,"moneyunit":1,"multiple":1,"amount":10,"num":5,"type":"santonghaodanxuan.santonghaodanxuan"},{"ball":"444","id":7,"moneyunit":1,"multiple":1,"amount":10,"num":5,"type":"santonghaodanxuan.santonghaodanxuan"},{"ball":"333","id":8,"moneyunit":1,"multiple":1,"amount":10,"num":5,"type":"santonghaodanxuan.santonghaodanxuan"},{"ball":"222","id":9,"moneyunit":1,"multiple":1,"amount":10,"num":5,"type":"santonghaodanxuan.santonghaodanxuan"},{"ball":"111","id":10,"moneyunit":1,"multiple":1,"amount":10,"num":5,"type":"santonghaodanxuan.santonghaodanxuan"},{"ball":"111 222 333 444 555 666","id":11,"moneyunit":1,"multiple":1,"amount":10,"num":5,"type":"santonghaotongxuan.santonghaotongxuan"},{"ball":"33*","id":12,"moneyunit":1,"multiple":1,"amount":10,"num":5,"type":"ertonghaofuxuan.ertonghaofuxuan"},{"ball":"22*","id":13,"moneyunit":1,"multiple":1,"amount":10,"num":5,"type":"ertonghaofuxuan.ertonghaofuxuan"},{"ball":"11*","id":14,"moneyunit":1,"multiple":1,"amount":10,"num":5,"type":"ertonghaofuxuan.ertonghaofuxuan"},{"ball":"小","id":15,"moneyunit":1,"multiple":1,"amount":10,"num":5,"type":"daxiao.daxiao"},{"ball":"双","id":16,"moneyunit":1,"multiple":1,"amount":10,"num":5,"type":"danshuang.danshuang"},{"ball":"17","id":17,"moneyunit":1,"multiple":1,"amount":10,"num":5,"type":"hezhi.hezhi"},{"ball":"16","id":18,"moneyunit":1,"multiple":1,"amount":10,"num":5,"type":"hezhi.hezhi"},{"ball":"15","id":19,"moneyunit":1,"multiple":1,"amount":10,"num":5,"type":"hezhi.hezhi"},{"ball":"14","id":20,"moneyunit":1,"multiple":1,"amount":10,"num":5,"type":"hezhi.hezhi"},{"ball":"13","id":21,"moneyunit":1,"multiple":1,"amount":10,"num":5,"type":"hezhi.hezhi"},{"ball":"12","id":22,"moneyunit":1,"multiple":1,"amount":10,"num":5,"type":"hezhi.hezhi"},{"ball":"11","id":23,"moneyunit":1,"multiple":1,"amount":10,"num":5,"type":"hezhi.hezhi"},{"ball":"10","id":24,"moneyunit":1,"multiple":1,"amount":10,"num":5,"type":"hezhi.hezhi"},{"ball":"9","id":25,"moneyunit":1,"multiple":1,"amount":10,"num":5,"type":"hezhi.hezhi"},{"ball":"8","id":26,"moneyunit":1,"multiple":1,"amount":10,"num":5,"type":"hezhi.hezhi"},{"ball":"7","id":27,"moneyunit":1,"multiple":1,"amount":10,"num":5,"type":"hezhi.hezhi"},{"ball":"6","id":28,"moneyunit":1,"multiple":1,"amount":10,"num":5,"type":"hezhi.hezhi"},{"ball":"5","id":29,"moneyunit":1,"multiple":1,"amount":10,"num":5,"type":"hezhi.hezhi"},{"ball":"4","id":30,"moneyunit":1,"multiple":1,"amount":10,"num":5,"type":"hezhi.hezhi"},{"ball":"5,6","id":31,"moneyunit":1,"multiple":1,"amount":10,"num":5,"type":"erbutonghao.erbutonghao"},{"ball":"4,6","id":32,"moneyunit":1,"multiple":1,"amount":10,"num":5,"type":"erbutonghao.erbutonghao"},{"ball":"4,5","id":33,"moneyunit":1,"multiple":1,"amount":10,"num":5,"type":"erbutonghao.erbutonghao"},{"ball":"3,6","id":34,"moneyunit":1,"multiple":1,"amount":10,"num":5,"type":"erbutonghao.erbutonghao"},{"ball":"3,5","id":35,"moneyunit":1,"multiple":1,"amount":10,"num":5,"type":"erbutonghao.erbutonghao"},{"ball":"3,4","id":36,"moneyunit":1,"multiple":1,"amount":10,"num":5,"type":"erbutonghao.erbutonghao"},{"ball":"2,6","id":37,"moneyunit":1,"multiple":1,"amount":10,"num":5,"type":"erbutonghao.erbutonghao"},{"ball":"2,5","id":38,"moneyunit":1,"multiple":1,"amount":10,"num":5,"type":"erbutonghao.erbutonghao"},{"ball":"2,4","id":39,"moneyunit":1,"multiple":1,"amount":10,"num":5,"type":"erbutonghao.erbutonghao"},{"ball":"2,3","id":40,"moneyunit":1,"multiple":1,"amount":10,"num":5,"type":"erbutonghao.erbutonghao"},{"ball":"1,6","id":41,"moneyunit":1,"multiple":1,"amount":10,"num":5,"type":"erbutonghao.erbutonghao"},{"ball":"1,5","id":42,"moneyunit":1,"multiple":1,"amount":10,"num":5,"type":"erbutonghao.erbutonghao"},{"ball":"1,4","id":43,"moneyunit":1,"multiple":1,"amount":10,"num":5,"type":"erbutonghao.erbutonghao"},{"ball":"1,3","id":44,"moneyunit":1,"multiple":1,"amount":10,"num":5,"type":"erbutonghao.erbutonghao"},{"ball":"1,2","id":45,"moneyunit":1,"multiple":1,"amount":10,"num":5,"type":"erbutonghao.erbutonghao"},{"ball":"6","id":46,"moneyunit":1,"multiple":1,"amount":10,"num":5,"type":"yibutonghao.yibutonghao"},{"ball":"5","id":47,"moneyunit":1,"multiple":1,"amount":10,"num":5,"type":"yibutonghao.yibutonghao"},{"ball":"4","id":48,"moneyunit":1,"multiple":1,"amount":10,"num":5,"type":"yibutonghao.yibutonghao"},{"ball":"3","id":49,"moneyunit":1,"multiple":1,"amount":10,"num":5,"type":"yibutonghao.yibutonghao"},{"ball":"2","id":50,"moneyunit":1,"multiple":1,"amount":10,"num":5,"type":"yibutonghao.yibutonghao"},{"ball":"1","id":51,"moneyunit":1,"multiple":1,"amount":10,"num":5,"type":"yibutonghao.yibutonghao"}],"orders":order_plan }
        elif lottery == 'p5':
            data_ = {"gameType":lottery,"isTrace":isTrace,"traceWinStop":traceWinStop,"traceStopValue":traceStopValue,"balls":[{"id":38,"ball":"2","type":"p3houer.zuxuan.zuxuanp3houerbaodan","moneyunit":1,"multiple":1,"awardMode":awardmode,"num":9},{"id":37,"ball":"6","type":"p3houer.zuxuan.zuxuanp3houerhezhi","moneyunit":1,"multiple":1,"awardMode":awardmode,"num":3},{"id":36,"ball":"38","type":"p3houer.zuxuan.zuxuanp3houerdanshi","moneyunit":1,"multiple":1,"awardMode":awardmode,"num":1},{"id":35,"ball":"0,7","type":"p3houer.zuxuan.zuxuanp3houerfushi","moneyunit":1,"multiple":1,"awardMode":awardmode,"num":1},{"id":34,"ball":"9","type":"p3houer.zhixuan.zhixuanp3houerkuadu","moneyunit":1,"multiple":1,"awardMode":awardmode,"num":2},{"id":33,"ball":"5","type":"p3houer.zhixuan.zhixuanp3houerhezhi","moneyunit":1,"multiple":1,"awardMode":awardmode,"num":6},{"id":32,"ball":"02","type":"p3houer.zhixuan.zhixuanp3houerdanshi","moneyunit":1,"multiple":1,"awardMode":awardmode,"num":1},{"id":31,"ball":"-,2,7","type":"p3houer.zhixuan.zhixuanp3houerfushi","moneyunit":1,"multiple":1,"awardMode":awardmode,"num":1},{"id":30,"ball":"2","type":"p3qianer.zuxuan.zuxuanp3qianerbaodan","moneyunit":1,"multiple":1,"awardMode":awardmode,"num":9},{"id":29,"ball":"7","type":"p3qianer.zuxuan.zuxuanp3qianerhezhi","moneyunit":1,"multiple":1,"awardMode":awardmode,"num":4},{"id":28,"ball":"67","type":"p3qianer.zuxuan.zuxuanp3qianerdanshi","moneyunit":1,"multiple":1,"awardMode":awardmode,"num":1},{"id":27,"ball":"2,5","type":"p3qianer.zuxuan.zuxuanp3qianerfushi","moneyunit":1,"multiple":1,"awardMode":awardmode,"num":1},{"id":26,"ball":"3","type":"p3qianer.zhixuan.zhixuanp3qianerkuadu","moneyunit":1,"multiple":1,"awardMode":awardmode,"num":14},{"id":25,"ball":"18","type":"p3qianer.zhixuan.zhixuanp3qianerhezhi","moneyunit":1,"multiple":1,"awardMode":awardmode,"num":1},{"id":24,"ball":"48","type":"p3qianer.zhixuan.zhixuanp3qianerdanshi","moneyunit":1,"multiple":1,"awardMode":awardmode,"num":1},{"id":23,"ball":"7,2,-","type":"p3qianer.zhixuan.zhixuanp3qianerfushi","moneyunit":1,"multiple":1,"awardMode":awardmode,"num":1},{"id":22,"ball":"3,8","type":"p3sanxing.budingwei.ermabudingwei","moneyunit":1,"multiple":1,"awardMode":awardmode,"num":1},{"id":21,"ball":"1","type":"p3sanxing.budingwei.yimabudingwei","moneyunit":1,"multiple":1,"awardMode":awardmode,"num":1},{"id":20,"ball":"279","type":"p3sanxing.zuxuan.p3zuliudanshi","moneyunit":1,"multiple":1,"awardMode":awardmode,"num":1},{"id":19,"ball":"229","type":"p3sanxing.zuxuan.p3zusandanshi","moneyunit":1,"multiple":1,"awardMode":awardmode,"num":1},{"id":18,"ball":"6","type":"p3sanxing.zuxuan.p3zuxuanbaodan","moneyunit":1,"multiple":1,"awardMode":awardmode,"num":54},{"id":17,"ball":"179","type":"p3sanxing.zuxuan.p3hunhezuxuan","moneyunit":1,"multiple":1,"awardMode":awardmode,"num":1},{"id":16,"ball":"1,3,9","type":"p3sanxing.zuxuan.p3zuliu","moneyunit":1,"multiple":1,"awardMode":awardmode,"num":1},{"id":15,"ball":"7,8","type":"p3sanxing.zuxuan.p3zusan","moneyunit":1,"multiple":1,"awardMode":awardmode,"num":2},{"id":14,"ball":"23","type":"p3sanxing.zuxuan.p3zuxuanhezhi","moneyunit":1,"multiple":1,"awardMode":awardmode,"num":4},{"id":13,"ball":"0","type":"p3sanxing.zhixuan.p3kuadu","moneyunit":1,"multiple":1,"awardMode":awardmode,"num":10},{"id":12,"ball":"27","type":"p3sanxing.zhixuan.p3hezhi","moneyunit":1,"multiple":1,"awardMode":awardmode,"num":1},{"id":11,"ball":"249","type":"p3sanxing.zhixuan.p3danshi","moneyunit":1,"multiple":1,"awardMode":awardmode,"num":1},{"id":10,"ball":"7,1,9","type":"p3sanxing.zhixuan.p3fushi","moneyunit":1,"multiple":1,"awardMode":awardmode,"num":1},{"id":9,"ball":"-,-,2,-,-","type":"p5yixing.dingweidan.fushi","moneyunit":1,"multiple":1,"awardMode":awardmode,"num":1},{"id":8,"ball":"7","type":"p5houer.zuxuan.zuxuanp5houerbaodan","moneyunit":1,"multiple":1,"awardMode":awardmode,"num":9},{"id":7,"ball":"9","type":"p5houer.zuxuan.zuxuanp5houerhezhi","moneyunit":1,"multiple":1,"awardMode":awardmode,"num":5},{"id":6,"ball":"03","type":"p5houer.zuxuan.zuxuanp5houerdanshi","moneyunit":1,"multiple":1,"awardMode":awardmode,"num":1},{"id":5,"ball":"3,4","type":"p5houer.zuxuan.zuxuanp5houerfushi","moneyunit":1,"multiple":1,"awardMode":awardmode,"num":1},{"id":4,"ball":"4","type":"p5houer.zhixuan.zhixuanp5houerkuadu","moneyunit":1,"multiple":1,"awardMode":awardmode,"num":12},{"id":3,"ball":"14","type":"p5houer.zhixuan.zhixuanp5houerhezhi","moneyunit":1,"multiple":1,"awardMode":awardmode,"num":5},{"id":2,"ball":"64","type":"p5houer.zhixuan.zhixuanp5houerdanshi","moneyunit":"1","multiple":1,"awardMode":awardmode,"num":1},{"id":1,"ball":"-,-,-,7,4","type":"p5houer.zhixuan.zhixuanp5houerfushi","moneyunit":"1","multiple":1,"awardMode":awardmode,"num":1}],"orders":order_plan ,"amount":342*len_order}
        elif lottery == 'ssq':
            data_ = {"gameType":lottery,"isTrace":isTrace,"traceWinStop":traceWinStop,"traceStopValue":traceStopValue,"balls":[{"id":3,"ball":"D:18_T:01,03,06,26,33+13","type":"biaozhuntouzhu.biaozhun.dantuo","moneyunit":1,"multiple":1,"awardMode":awardmode,"num":1},{"id":2,"ball":"08,17,19,22,24,33+07","type":"biaozhuntouzhu.biaozhun.danshi","moneyunit":"1","multiple":1,"awardMode":awardmode,"num":1},{"id":1,"ball":"10,15,18,23,24,31+05","type":"biaozhuntouzhu.biaozhun.fushi","moneyunit":"1","multiple":1,"awardMode":awardmode,"num":1}],"orders":order_plan ,"amount":6*len_order}  
        elif lottery == "shssl":
            data_ = {"gameType":lottery,"isTrace":isTrace,"traceWinStop":traceWinStop,"traceStopValue":traceStopValue,"balls":[{"id":81,"ball":"-,-,和","type":"longhu.longhudou.fushi","moneyunit":1,"multiple":1,"awardMode":awardmode,"num":1},{"id":80,"ball":"大,大","type":"daxiaodanshuang.dxds.houer","moneyunit":1,"multiple":1,"awardMode":awardmode,"num":1},{"id":79,"ball":"小","type":"daxiaodanshuang.dxds.houyi","moneyunit":1,"multiple":1,"awardMode":awardmode,"num":1},{"id":78,"ball":"双","type":"daxiaodanshuang.dxds.houyi","moneyunit":1,"multiple":1,"awardMode":awardmode,"num":1},{"id":77,"ball":"单","type":"daxiaodanshuang.dxds.houyi","moneyunit":1,"multiple":1,"awardMode":awardmode,"num":1},{"id":76,"ball":"大","type":"daxiaodanshuang.dxds.houyi","moneyunit":1,"multiple":1,"awardMode":awardmode,"num":1},{"id":75,"ball":"-,0,-","type":"yixing.dingweidan.fushi","moneyunit":1,"multiple":1,"awardMode":awardmode,"num":1},{"id":74,"ball":"3,5","type":"housan.budingwei.ermabudingwei","moneyunit":1,"multiple":1,"awardMode":awardmode,"num":1},{"id":73,"ball":"3,8","type":"housan.budingwei.ermabudingwei","moneyunit":1,"multiple":1,"awardMode":awardmode,"num":1},{"id":72,"ball":"0,7","type":"housan.budingwei.ermabudingwei","moneyunit":1,"multiple":1,"awardMode":awardmode,"num":1},{"id":71,"ball":"1,2","type":"housan.budingwei.ermabudingwei","moneyunit":1,"multiple":1,"awardMode":awardmode,"num":1},{"id":70,"ball":"1,7","type":"housan.budingwei.ermabudingwei","moneyunit":1,"multiple":1,"awardMode":awardmode,"num":1},{"id":69,"ball":"4,5","type":"housan.budingwei.ermabudingwei","moneyunit":1,"multiple":1,"awardMode":awardmode,"num":1},{"id":68,"ball":"3,9","type":"housan.budingwei.ermabudingwei","moneyunit":1,"multiple":1,"awardMode":awardmode,"num":1},{"id":67,"ball":"0,2","type":"housan.budingwei.ermabudingwei","moneyunit":1,"multiple":1,"awardMode":awardmode,"num":1},{"id":66,"ball":"0,2","type":"housan.budingwei.ermabudingwei","moneyunit":1,"multiple":1,"awardMode":awardmode,"num":1},{"id":65,"ball":"0,4","type":"housan.budingwei.ermabudingwei","moneyunit":1,"multiple":1,"awardMode":awardmode,"num":1},{"id":64,"ball":"0,9","type":"housan.budingwei.ermabudingwei","moneyunit":1,"multiple":1,"awardMode":awardmode,"num":1},{"id":63,"ball":"4,7","type":"housan.budingwei.ermabudingwei","moneyunit":1,"multiple":1,"awardMode":awardmode,"num":1},{"id":62,"ball":"4,6","type":"housan.budingwei.ermabudingwei","moneyunit":1,"multiple":1,"awardMode":awardmode,"num":1},{"id":61,"ball":"3,4","type":"housan.budingwei.ermabudingwei","moneyunit":1,"multiple":1,"awardMode":awardmode,"num":1},{"id":60,"ball":"0,2","type":"housan.budingwei.ermabudingwei","moneyunit":1,"multiple":1,"awardMode":awardmode,"num":1},{"id":59,"ball":"3,5","type":"housan.budingwei.ermabudingwei","moneyunit":1,"multiple":1,"awardMode":awardmode,"num":1},{"id":58,"ball":"7,9","type":"housan.budingwei.ermabudingwei","moneyunit":1,"multiple":1,"awardMode":awardmode,"num":1},{"id":57,"ball":"4","type":"housan.budingwei.yimabudingwei","moneyunit":1,"multiple":1,"awardMode":awardmode,"num":1},{"id":56,"ball":"028","type":"housan.zuxuan.zuliudanshi","moneyunit":1,"multiple":1,"awardMode":awardmode,"num":1},{"id":55,"ball":"6","type":"housan.zuxuan.baodan","moneyunit":1,"multiple":1,"awardMode":awardmode,"num":54},{"id":54,"ball":"058","type":"housan.zuxuan.hunhezuxuan","moneyunit":1,"multiple":1,"awardMode":awardmode,"num":1},{"id":53,"ball":"2,5,7","type":"housan.zuxuan.zuliu","moneyunit":1,"multiple":1,"awardMode":awardmode,"num":1},{"id":52,"ball":"2,4","type":"housan.zuxuan.zusan","moneyunit":1,"multiple":1,"awardMode":awardmode,"num":2},{"id":51,"ball":"4","type":"housan.zuxuan.hezhi","moneyunit":1,"multiple":1,"awardMode":awardmode,"num":4},{"id":50,"ball":"3","type":"housan.zhixuan.kuadu","moneyunit":1,"multiple":1,"awardMode":awardmode,"num":126},{"id":49,"ball":"2","type":"housan.zhixuan.hezhi","moneyunit":1,"multiple":1,"awardMode":awardmode,"num":6},{"id":48,"ball":"168","type":"housan.zuxuan.zuliudanshi","moneyunit":1,"multiple":1,"awardMode":awardmode,"num":1},{"id":47,"ball":"124","type":"housan.zuxuan.zuliudanshi","moneyunit":1,"multiple":1,"awardMode":awardmode,"num":1},{"id":46,"ball":"568","type":"housan.zuxuan.zuliudanshi","moneyunit":1,"multiple":1,"awardMode":awardmode,"num":1},{"id":45,"ball":"579","type":"housan.zuxuan.zuliudanshi","moneyunit":1,"multiple":1,"awardMode":awardmode,"num":1},{"id":44,"ball":"256","type":"housan.zuxuan.zuliudanshi","moneyunit":1,"multiple":1,"awardMode":awardmode,"num":1},{"id":43,"ball":"236","type":"housan.zuxuan.zuliudanshi","moneyunit":1,"multiple":1,"awardMode":awardmode,"num":1},{"id":42,"ball":"349","type":"housan.zuxuan.zuliudanshi","moneyunit":1,"multiple":1,"awardMode":awardmode,"num":1},{"id":41,"ball":"067","type":"housan.zuxuan.zuliudanshi","moneyunit":1,"multiple":1,"awardMode":awardmode,"num":1},{"id":40,"ball":"046","type":"housan.zuxuan.zuliudanshi","moneyunit":1,"multiple":1,"awardMode":awardmode,"num":1},{"id":39,"ball":"236","type":"housan.zuxuan.zuliudanshi","moneyunit":1,"multiple":1,"awardMode":awardmode,"num":1},{"id":38,"ball":"169","type":"housan.zuxuan.zuliudanshi","moneyunit":1,"multiple":1,"awardMode":awardmode,"num":1},{"id":37,"ball":"256","type":"housan.zuxuan.zuliudanshi","moneyunit":1,"multiple":1,"awardMode":awardmode,"num":1},{"id":36,"ball":"368","type":"housan.zuxuan.zuliudanshi","moneyunit":1,"multiple":1,"awardMode":awardmode,"num":1},{"id":35,"ball":"679","type":"housan.zuxuan.zuliudanshi","moneyunit":1,"multiple":1,"awardMode":awardmode,"num":1},{"id":34,"ball":"138","type":"housan.zuxuan.zuliudanshi","moneyunit":1,"multiple":1,"awardMode":awardmode,"num":1},{"id":33,"ball":"056","type":"housan.zuxuan.zuliudanshi","moneyunit":1,"multiple":1,"awardMode":awardmode,"num":1},{"id":32,"ball":"159","type":"housan.zuxuan.zuliudanshi","moneyunit":1,"multiple":1,"awardMode":awardmode,"num":1},{"id":31,"ball":"1","type":"housan.zuxuan.baodan","moneyunit":1,"multiple":1,"awardMode":awardmode,"num":54},{"id":30,"ball":"567","type":"housan.zuxuan.hunhezuxuan","moneyunit":1,"multiple":1,"awardMode":awardmode,"num":1},{"id":29,"ball":"024","type":"housan.zuxuan.hunhezuxuan","moneyunit":1,"multiple":1,"awardMode":awardmode,"num":1},{"id":28,"ball":"0,4","type":"housan.zuxuan.zusan","moneyunit":1,"multiple":1,"awardMode":awardmode,"num":2},{"id":27,"ball":"16","type":"housan.zuxuan.hezhi","moneyunit":1,"multiple":1,"awardMode":awardmode,"num":14},{"id":26,"ball":"0","type":"housan.zhixuan.kuadu","moneyunit":1,"multiple":1,"awardMode":awardmode,"num":10},{"id":25,"ball":"17","type":"housan.zhixuan.hezhi","moneyunit":1,"multiple":1,"awardMode":awardmode,"num":63},{"id":24,"ball":"4,9","type":"housan.budingwei.ermabudingwei","moneyunit":1,"multiple":1,"awardMode":awardmode,"num":1},{"id":23,"ball":"0,1","type":"housan.budingwei.ermabudingwei","moneyunit":1,"multiple":1,"awardMode":awardmode,"num":1},{"id":22,"ball":"1,8","type":"housan.budingwei.ermabudingwei","moneyunit":1,"multiple":1,"awardMode":awardmode,"num":1},{"id":21,"ball":"4,7","type":"housan.budingwei.ermabudingwei","moneyunit":1,"multiple":1,"awardMode":awardmode,"num":1},{"id":20,"ball":"2,9","type":"housan.budingwei.ermabudingwei","moneyunit":1,"multiple":1,"awardMode":awardmode,"num":1},{"id":19,"ball":"2,3","type":"housan.budingwei.ermabudingwei","moneyunit":1,"multiple":1,"awardMode":awardmode,"num":1},{"id":18,"ball":"2,5","type":"housan.budingwei.ermabudingwei","moneyunit":1,"multiple":1,"awardMode":awardmode,"num":1},{"id":17,"ball":"2,5","type":"housan.budingwei.ermabudingwei","moneyunit":1,"multiple":1,"awardMode":awardmode,"num":1},{"id":16,"ball":"3,5","type":"housan.budingwei.ermabudingwei","moneyunit":1,"multiple":1,"awardMode":awardmode,"num":1},{"id":15,"ball":"2,5","type":"housan.budingwei.ermabudingwei","moneyunit":1,"multiple":1,"awardMode":awardmode,"num":1},{"id":14,"ball":"4,6","type":"housan.budingwei.ermabudingwei","moneyunit":1,"multiple":1,"awardMode":awardmode,"num":1},{"id":13,"ball":"5,9","type":"housan.budingwei.ermabudingwei","moneyunit":1,"multiple":1,"awardMode":awardmode,"num":1},{"id":12,"ball":"4,8","type":"housan.budingwei.ermabudingwei","moneyunit":1,"multiple":1,"awardMode":awardmode,"num":1},{"id":11,"ball":"2,8","type":"housan.budingwei.ermabudingwei","moneyunit":1,"multiple":1,"awardMode":awardmode,"num":1},{"id":10,"ball":"3,6","type":"housan.budingwei.ermabudingwei","moneyunit":1,"multiple":1,"awardMode":awardmode,"num":1},{"id":9,"ball":"9","type":"housan.budingwei.yimabudingwei","moneyunit":1,"multiple":1,"awardMode":awardmode,"num":1},{"id":8,"ball":"405","type":"housan.zhixuan.danshi","moneyunit":1,"multiple":1,"awardMode":awardmode,"num":1},{"id":7,"ball":"593","type":"housan.zhixuan.danshi","moneyunit":1,"multiple":1,"awardMode":awardmode,"num":1},{"id":6,"ball":"430","type":"housan.zhixuan.danshi","moneyunit":1,"multiple":1,"awardMode":awardmode,"num":1},{"id":5,"ball":"596","type":"housan.zhixuan.danshi","moneyunit":1,"multiple":1,"awardMode":awardmode,"num":1},{"id":4,"ball":"143","type":"housan.zhixuan.danshi","moneyunit":1,"multiple":1,"awardMode":awardmode,"num":1},{"id":3,"ball":"275","type":"housan.zhixuan.danshi","moneyunit":1,"multiple":1,"awardMode":awardmode,"num":1},{"id":2,"ball":"416","type":"housan.zhixuan.danshi","moneyunit":"1","multiple":1,"awardMode":awardmode,"num":1},{"id":1,"ball":"3,7,0","type":"housan.zhixuan.fushi","moneyunit":"1","multiple":1,"awardMode":awardmode,"num":1}],"orders":order_plan,"redDiscountAmount":0,"amount":812*len_order}
        elif lottery == 'pcdd':
            data_ = {"balls":[{"id":1,"moneyunit":1,"multiple":1,"num":1,"type":"zhenghe.hezhi.hezhi",
            "amount":50,
            "ball":"11","odds":13.04,"awardMode":1}],"orders":order_plan,"redDiscountAmount":0,
            "amount":str(50*len_order),"isTrace":isTrace,"traceWinStop":traceWinStop,
            "traceStopValue":traceStopValue}
        elif lottery == 'test':#測試用
            data_ = {"gameType":"cqssc","isTrace":0,"traceWinStop":0,"traceStopValue":-1,
            "balls":[{"id":1,"ball":"-,-,5,0,5","type":"housan.zhixuan.fushi","moneyunit":"1",
            "multiple":1,"awardMode":awardmode,"num":1}],"orders":order_plan,"redDiscountAmount":0,
            "amount":2*len_order}
            
        return data_
    def Account_Cookie(self,user):# 用戶登入 的cookie 值
        account_cookie  = FF_().cookies[user]#用戶登入的cookie
        Pc_header['Cookie'] =  'ANVOID='+ account_cookie# 在header增加用戶登入cookie
        return Pc_header
        
    def Pc_Submit(self,user,lottery,awardmode,type_,stop="",ball=""):#PC投注
        
        Pc_header =FF_().Account_Cookie(user)# 用戶 header 增加登入 
        global issueCode# PC 和APP 投注共用 旗號參數
        #print(FF_().submit_inf)
        if type_ == 1:# 一般投注
            isTrace =  0 
            traceWinStop = 0
            traceStopValue = -1
        else:#追號
            if stop == "":# 預設追種即停
                traceWinStop=1
                traceStopValue=1
                print ('追中即停')
            else:
                traceWinStop=0
                traceStopValue=-1
                print('追中不停')
            isTrace=1
        if FF_().submit_inf == {}:# 初始化投注. 一定會呼叫奖期, 不燃會報錯
            print('要獎其')
            issueCode = FF_().select_issue(FF_().get_conn(envs),lottery,type_)[lottery]# 奖期api , 為一個dict ,key為採種
            print(issueCode )
            #issueCode = FF_().submit_inf[lottery]# 這段 紀錄上個有抓到奖期的資訊
        elif lottery not in FF_().submit_inf: # 裡面沒有  該彩種 ,救要一次
            issueCode = FF_().select_issue(FF_().get_conn(envs),lottery,type_)[lottery]
        else:# 
            issueCode = FF_().submit_inf[lottery]
        postData = FF_().submit_json(lottery,awardmode,isTrace,traceWinStop ,traceStopValue,type_,ball)
        FF_().session_post(em_url,'/gameBet/%s/submit'%lottery,json.dumps(postData),Pc_header)
        print('%s投注,彩種: %s'%(user,self.lottery_dict[lottery][0]))
        try:
            print( r.json()['isSuccess'])
        except:
            return 'wrong'
        #try: # 投注成功才會有  r.json()
        if r.json()['isSuccess'] == 1:# 頭住成功
            FF_().submit_inf[lottery] = issueCode # 投注成功  ,紀錄 彩種: 奖期,避免一直要DB 奖期
            print( FF_().submit_inf)
            print('投注成功 ,訂單id: %s'%(r.json()['data']['projectId']))
        else:#w投注失敗
            if "您本期已进行投注" in  r.json()['msg']:# 快開慘種 回復訊息(一期一筆).其他彩種 正常不會走這段
                sleep(30)
            elif "已截止销售" in r.json()['msg']:
                for i in range(1,9):
                    print('已截止销售,第%s次 要獎期'%i)
                    issueCode = FF_().select_issue(FF_().get_conn(envs),lottery,type_)[lottery]
                    sleep(3)
                    postData = FF_().submit_json(lottery,awardmode,isTrace,traceWinStop ,traceStopValue,type_,ball)
                    print(issueCode)
                    FF_().session_post(em_url,'/gameBet/%s/submit'%lottery,json.dumps(postData),Pc_header)
                    if r.json()['isSuccess'] == 1:
                        FF_().submit_inf[lottery] = issueCode
                        return('投注成功')
            elif '超出倍数限制' in r.json()['msg']:
                return '超出倍数限制'

    def Third_Home(self):# 第三方連線
        Pc_header =FF_().Account_Cookie()
        getData = ""
        FF_().session_get(post_url,'/lc/home',getData,header)
        soup = BeautifulSoup(r.text,'lxml')
        print(soup.find_all('strong',{'id_':'_userName'}))
class App(FF_):
    token = defaultdict(list)
    #token = {}# APP 登入後, 各鳩口 會需要用到 , 列表分表包  token和userid
    def App_LotteryData(self,App_account,lottery):#APP投注會呼叫此皆口
        now = int(time.time()*1000)#現再投注時間戳
        token = App().token[App_account][0]
        userid = App().token[App_account][1]
        data={"head":{"sessionId":token},
        "body":{"param":{"CGISESSID":token,
        "lotteryId":self.lottery_dict[lottery][1],"chan_id":1,"userid":userid,"money": 1,
        "redDiscountTotal":0,"issue":issueCode,"issueName":"2020077","isFirstSubmit":0,
        "list":[{"methodid":"65_72_105","codes":"1.01","nums":1,"fileMode":0,"mode":1,"times":1,
        "money":1,"awardMode":2}],"traceIssues":"","traceTimes":"","traceIstrace":0,
        "channelVersion":"1.0.23.0013","saleTime":now,"userIp":168627224,"channelId":202,"traceStop":0,
        "app_id":9,"come_from":"3","appname":"1"}}}        
        return data 
    def App_Login(self,env,App_account,joint_=0):# 預設走  一般 joint_venture 0
        global envs
        envs = self.app_url[env][3]# 環境DB 參數
        #joint_venture = FF_().select_joint_venture(FF_().get_conn(envs),account)
        #print(joint_venture)
        postdata ={"head": {"sessionId": ''},
        "body": {"param": {
        "username":  App_account+"|"+ self.app_url[env][1],"loginpassSource":self.app_url[env][2],
        "appCode": 1,"uuid": self.app_url[env][1],
        "loginIp": 2130706433,"device": 2,"app_id": 9,"come_from": "3","appname": "1","jointVenture": joint_
        }}}
        global App_header# 後續 APP 接口使用
        App_header = {'User-Agent':self.user_agent['Pc']}
        App_header['Content-Type'] = 'application/json'
        App().session_post(self.app_url[env][0],'front/login',json.dumps(postdata),App_header)# 登入皆口
        status = r.json()['head']['status']
        token = r.json()['body']['result']['token']
        userid = r.json()['body']['result']['userid']
        if App_account in App().token:
            pass
        else:
            App.token.setdefault(App_account,[]).append(token)
            App.token.setdefault(App_account,[]).append(userid)
        if status == 0:
            print ('登入成功')
        else:
            print(r.json())
            print('登入失敗')    
    
    def App_Submit(self,lottery,App_account,type_=1):# APP投注 不先要奖期. 用投注結果 來確認(避免多投注,會一直要DB資料)
        global issueCode#PC和APP共用
        if FF_().submit_inf == {}:# 初始化投注. 一定會呼叫奖期, 不燃會報錯
            issueCode = FF_().select_issue(FF_().get_conn(envs),lottery,type_)[lottery]# 奖期api , 為一個dict ,key為採種
        else:
            issueCode = FF_().submit_inf[lottery]# 這段 紀錄上個有抓到奖期的資訊
        postdata = App().App_LotteryData(App_account,lottery)
        App().session_post(self.app_url[env_][0],'game/buy',json.dumps(postdata),App_header)# 投注皆口
        status = r.json()['head']['status']# 投注回復狀態 判斷
        print (status)
        if status == 0:
            orderid = r.json()['body']['result']['orderId']
            print (orderid)
            print('投注成功')
            FF_().submit_inf[lottery] = issueCode# 投注成功  ,紀錄 彩種: 奖期,避免一直要DB 奖期
        elif status == 201004:
            issueCode = FF_().select_issue(FF_().get_conn(envs),lottery,1)[lottery]#type 目前寫死 1 , 一般投注
            print (issueCode)
            print('期號需確認,重新要一次奖期: %s'%issueCode)
            issueCode = FF_().submit_inf[lottery]
            #sleep(10)
        else:
            print('投注失敗,待確認')


# In[ ]:


FF_().select_lottery(FF_().get_conn(0))


# In[ ]:


FF_().lottery_dict


# In[ ]:


FF_().web_issuecode(lottery='cqssc',account='kerr001')


# In[ ]:


FF_().cookies


# In[ ]:


print(test_user)


# In[ ]:


#for user in test_user:
FF_().Pc_Login(url='joy188',user='kerr000')#登入接口, url: 環境 , user: 用戶, source: 登入莊置(不帶: 預設PC)


# In[ ]:


FF_().submit_inf


# In[ ]:


FF_().lottery_dict


# In[ ]:


#for user in FF_().cookies.keys():
for i in range(30):
    FF_().Pc_Submit(lottery = 'slmmc',awardmode=None,type_=1,user='kerr000')


# In[ ]:





# In[ ]:


for lottery_name in FF_().lottery_dict:
    FF_().Pc_Submit(lottery = lottery_name,awardmode=None,type_=1,user='kerr001')


# In[ ]:


# 一般投注 ,stop預設為""(一般投注),ball 預設為""(寫死投注內容,後續彩種補上) 

for i in range(100):
    for user_ in FF_.cookies.keys():
        FF_().Pc_Submit(lottery='cqssc',awardmode=1,type_=1,user=user_)


# In[ ]:


threads = []

for user in range(50):
    t = threading.Thread(target=FF_().Pc_Submit,args=('kerr{:03d}'.format(user),'txffc',1,1,                                           ))
    threads.append(t)
for i in threads:
    i.start()
for i in threads:
    i.join()


# In[ ]:


class DG(FF_):
    def __init__(self,username):
        self.data_type ={
        'login':
        ['玩家登陆',{"token": "402a5c318a105c2b47368c6726b74869","random": "123456","lang": "cn",
        "member": {"username": username,"password": "123456"}}],
        'signup':
        ['注册新玩家',{"token":"402a5c318a105c2b47368c6726b74869","random":123456,"data":"A",
        "member":{"username":"TEST10000","password":"e10adc3949ba59abbe56e057f20f883e", 
        "currencyName":"CNY","winLimit":1000 }}],
        'free':
        ['玩家登陆试玩',{"token":"402a5c318a105c2b47368c6726b74869","random":"123456", "lang":"en"}],
        'update':
        ['修改玩家信息',{"token":"402a5c318a105c2b47368c6726b74869", "random":"123456", 
        "member":{"username":"TEST10000","password":"e10adc3949ba59abbe56e057f20f883e",
        "winLimit":0.0,"status":1}}],
        'getBalance':
        ['获取玩家余额',{"token":"402a5c318a105c2b47368c6726b74869","random":"123456","member":
        {"username":"TEST10000"}}],
        'transfer':
        ['玩家存取款',{"token":"402a5c318a105c2b47368c6726b74869","random":"123456",  "data":"202007231356256", 
        "member":{"username":"TEST10000","amount":100}}],
        'checkTransfer':
        ['检查存取款操作是否成功',{ "token":"402a5c318a105c2b47368c6726b74869","random":"123456", 
        "data":"202007230956256"}],
        'updateLimit':
        ['修改玩家限红组',{ "token":"402a5c318a105c2b47368c6726b74869", "random":"123456","data":"B", 
        "member":{"username":"TEST10000"}}],
        'getReport': 
        ['抓取注单报表',{"token":"59c78f14ae96a00bc907c2adaffc7938","random":"5bb96d22327eba3609438c955a903b4d"}],
        'onlineReport':
        ['获取在线玩家',{"token":"402a5c318a105c2b47368c6726b74869","random":"123456"}],
        'offline':
        ['踢人下线',{"token":"402a5c318a105c2b47368c6726b74869","random":"123456",  "list":[] }],
        }
    def DG_Test(username,type_):# DG 皆口  
    #key為各街口參數 ,  value 為各皆口 data參數
        urllib3.disable_warnings()#解決 會跳出 request InsecureRequestWarning問題
        test_header = { 
            "Content-Type": "application/json",
            'User-Agent':FF_().user_agent['Pc']
        }
        test_data = DG(username).data_type[type_][1]
        if type_ in ['transfer','checkTransfer']:
            url = 'account'
        elif type_ in ['updateLimit','getReport']:
            url = 'game'
        else:
            url = 'user'
        url = '/%s/%s/DGTE01011T'%(url,type_)
        print(url)
        FF_().session_post('https://api.dg99web.com',url,json.dumps(test_data),test_header)#https://api.dg99web.com
        print('連線狀態: %s '%r.status_code)
        print('回覆內容: %s'%r.json())

for item in DG(username='hsieh001').data_type.keys():
    print(item+DG(username='hsieh001').data_type[item][0])
    DG.DG_Test(username='hsieh001',type_=item)

#DG.DG_Test(username='hsieh001',type_='login')


# In[ ]:


from collections import defaultdict
d = defaultdict(list)
d['a'].append(1)
d['a'].append(1)
d['b'].append(2)
print(d)


# In[ ]:


os.getcwd()# 當前路徑


# In[ ]:


from functools import reduce
def list_cal(list_):#列表直計算
    #return list_[0] - list_[1]
    return reduce(lambda x,y: x-y, list_)
list_cal(Turnover)


# In[ ]:


Turnover = [540, 1220,300]


# In[ ]:


test = {'Turnover': [None, None], 'Activities': [None, None], 'Rebates': [None, None], 'NewVipReward': [None, None], 'Red': [None, None], 'Depoist': [None, None], 'Withdraw': [None, None], 'DailyWage': [None, None], 'MonthWage': [None, None], 
'ThirdRebates': [None, None], 'ThirdShares': [None, None]}
test1 = {'tsr': [1]}
test+test1


# In[ ]:



now = datetime.datetime(2020, 12, 15, 12, 58, 37)
s = datetime.datetime.strftime(now,'%Y-%m-%d %H:%M:%S')
print(s)


# In[ ]:


time_ = 1609227686
appId = "1pj0ylXd"
#test_header['appKey'] = "316489e115371ed23808a9ce2ee094a38ca4411a"
m = hashlib.md5()
appKey = '24b1cd59ed928b03ceed3ac72a5dbd7497bf0246'
str_ = "appId=%s&nonce-str=ibuaiVcKdpRxkhJA&timestamp=%s&appKey=%s"%(appId,str(time_),appKey)
print(str_)
m.update(str_.encode())
str_md = m.hexdigest().upper()

print(str_md)


# In[ ]:


timestap =int(time.time())
token_time = time.localtime(int(timestap))
                    
print(timestap,token_time)


# In[ ]:


from requests_toolbelt import MultipartEncoder
class GameBox(FF_):
    #appId = "HvMOR9fH"
    def __init__(self,clientId='',username='',app_Id='',member_Id='',password='',amount=1.5,bill_No=''):
        self.data_type = {
        "token":['管理/獲取令牌',
        "/oauth/token?client_id=admin&client_secret=gameBox-2020-08-11*admin&username=admin&password=gameBox-2020-08-11*admin&grant_type=password&scope=all"
        
                 ,""],
        "createApp":["管理/創建APP帳號",
        "/admin/client/createApp",{
        "clientId": supplier_user,"clientSecret": "string","dec": "string","email": "%s@gmail.com"%supplier_user,
        "ipWhitelist": "61.220.138.45","supplierAccountDTOList": [
        {"apiKey": api_key,"apiUrl": api_url,"password": password,
        "supplierType": supplier_type,"username":supplier_user }]
        }],
        "getClientInfo":["获取client信息",
        "/admin/client/getClientInfo?appId=%s&"%app_Id,""],
        "updateIpWhitelist":["管理/修改客户的ip白名单",
        "/admin/client/updateIpWhitelist?appId=%s&ipWhitelist=61.220.138.45"%app_Id,""],
        "updateSupplierAccount":["管理/修改三方账号信息",
        "/admin/client/updateSupplierAccount?appId=%s&type=%s"%(app_Id,update_type),{
        "apiKey": api_key,"apiUrl": api_url,"password": password,
        "username": supplier_user,"supplierType": supplier_type}],
        "signUp":["客戶/註冊",
        "/api/member/signUp?agent_name=%s"%clientId,[
        {"0":{"member": {"currencyName": "CNY", "password": password, "username": username, "winLimit": 0 },"oddType": "A" }},
        {"1":{"member": {"currencyName": "UUS", "maxtransfer": 1000,"mintransfer": 1,"payRadioType": "2","username": "%s_test"%username}}},
        {"2":{"member": {"currencyName": "CNY", "username": username },"oddType": "260301,260302" }},
        {"3":{"member": {"password": password,"username": username}}},
        {"4":{"member": {"password": 'q'+password.upper(),"username": username}}},
        {"5":{"lang": "cs","member": {"password": password, "username": username},"oddType":"4440"}},
        {"6":{"member": {"currencyName": "CNY", "username": username }}},
        {"7":{"agentLogin": "amberdev","member": {"username": username}}},
        {"8":{"member": {"username": username}}},
        {"9":{"member": { "currencyName": "CNY","password": password, "username": username }}},
        {"10":{"member": {"password": password,"username": username}}},
        {"11":{"agentLogin": "xosouat","member": {"username": username}}},
        {"12":{"member": {"username": username}}},
        {"13":{"member": {"username": username}}},
        {"14":{"ipAddress": "61.220.138.45","member": {"amount": amount,"username": username }}}]
        ],
        "login":["客戶/登入",
        "/api/member/login?agent_name=%s"%clientId,[
        {"0":{"lang": "CNY","member": {"password": password, "username": username}}},
        {"1":{"member": {"username":"%s_test"%username}}},
        {"2":{"member": {"username":username}}},
        {"3":{"lang": "cs","member": {"password": password, "username": username}}},
        {"4":{"lang": "cs","type":"LC","member": {"password": 'q'+password.upper(), "username": username}}},
        {"5":{"deviceId": "1","lang": "cs","member": {"password": password,"username": username},
        "oddType": "4445","backUrl":"https://www.baidu.com"}},
        {"6":{"lang":"cs","member": {"username": username}}},
        {"7":{"deviceId": "1","lang":"cs","backUrl":"http:///www.baidu.com","agentLogin": "amberdev","member": {"username": username}}},
        {"8":{"member": {"username": username}}},
        {"9":{"ipAddress":"192.168.1.1","lang":"cs","deviceId":"1","member": {"password": password,"username": username}}},
        {"10":{"member": {"password": password,"username": username}}},
        {"11":{"lang":"cs","member": {"username": username}}},
        {"12":{"lang":"cs","member": {"username": username}}},
        {"13":{"member": {"username": username}}},
        {"14":{"ipAddress": "61.220.138.45","member": {"amount": amount,"username": username }}}]
        ],
        "freeLogin":["客戶/試玩登入",
        "/api/member/freeLogin?agent_name=%s"%clientId,[
        {"0":{"lang": "cs"}},{"1":{}},{"2":{}},{"3":{}},{"4":{}},
        {"5":{"backUrl": "https://www.baidu.com","deviceId": "1","lang": "cs"}},
        {"6":{"lang": "cs"}},
        {"7":{"deviceId": "4","lang":"cs","backUrl":"http:///www.baidu.com"}},
        {"8":{}},{"9":{}},{"10":{}},
        {"11":{"lang": "cs"}},
        {"12":{}},{"13":{}},{"14":{}}]
        ],
        "update":["客戶/修改会员信息","/api/member/update?agent_name=%s"%clientId,[
        {"0":{"member": {"status": 1, "winLimit": 0,"password": password, "username":username }}}, 
        {"1":{"member":{"maxtransfer": 1000,"mintransfer": 1,"payRadioType": "2","username": "%s_test"%username}}},
        {"2":{}},
        {"3":{"member": {"password": password,"username": username}}},
        {"4":{"member": {"password": 'q'+password.upper(),"oldPw": 'q'+password.upper(),"username": username}}},
        {"5":{"member": {"password": password,"username": username}}},
        {"6":{}},{"7":{}},{"8":{}},
        {"9":{"member": {"password": password,"username": username}}},
        {"10":{}},
        {"11":{}},
        {"12":{}},
        {"13":{}},
        {"14":{}}]
        ],
        "balance":['客戶/获取会员余额接口',
        "/api/member/balance?agent_name=%s"%clientId,[
        {"0":{"member": {"username": username,}}},
        {"1":{"member": {"username": "%s_test"%username}}},
        {"2":{"member": {"username": username,}}},
        {"3":{"member": {"username": username,}}},
        {"4":{"member": {"username": username,"password": 'q'+password.upper()}}},
        {"5":{"member": {"username": username,}}},
        {"6":{"member": {"username": username,}}},
        {"7":{"agentLogin": "amberdev","member": {"username": username}}},
        {"8":{"member": {"username": username}}},
        {"9":{"member": {"username": username}}},
        {"10":{"member": {"username": username}}},
        {"11":{"agentLogin": "xosouat","member": {"username": username}}},
        {"12":{"member": {"username": username}}},
        {"13":{"member": {"username": username,}}},
        {"14":{"member": {"username": username,}}}]
        ],
        "transfer":["客戶/会员存取款接口",
        "/api/member/transfer?agent_name=%s"%clientId,[
        {"0":{"billNo": '%s'%random.randint(1,1000000000),"member": {"amount":amount ,"username": username,}}},
        {"1":{"billNo": '%s'%random.randint(1,1000000000),"member": {"amount":amount ,"currencyName": "UUS","username": "%s_test"%username}}},
        {"2":{"billNo": '%s'%random.randint(1,1000000000),"member": {"amount":amount,"username": username,}}},
        {"3":{"billNo": '%s'%random.randint(1,1000000000),"member": {"amount":amount ,"username": username,}}},
        {"4":{"billNo": '%s'%random.randint(1,1000000000),"member": {"amount":amount ,"password": 'q'+password.upper(),"username": username,}}},
        {"5":{"billNo": '%s'%random.randint(1,1000000000),"member": {"amount":amount ,"username": username,}}},
        {"6":{"billNo": '%s'%random.randint(1,1000000000),"member": {"amount":amount ,"username": username,}}},
        {"7":{"billNo": '%s'%random.randint(1,1000000000),"agentLogin": "amberdev","member": {"amount":amount,"username": username}}},
        {"8":{"billNo": '%s'%random.randint(1,1000000000),"member": {"amount":amount ,"username": username,}}},
        {"9":{"billNo": '%s'%random.randint(1,1000000000),"member": {"amount":amount ,"username": username,}}},
        {"10":{"billNo": '%s'%random.randint(1,1000000000),"member": {"amount":amount ,"username": username,}}},
        {"11":{"billNo": '%s'%random.randint(1,1000000000),"agentLogin": "xosouat","member": {"amount":amount,"username": username}}},
        {"12":{"billNo": '%s'%random.randint(1,1000000000),"member": {"amount":amount ,"username": username,}}},
        {"13":{"billNo": '%s'%random.randint(1,1000000000),"member": {"amount":amount ,"username": username,}}},
        {"14":{"billNo": '%s'%random.randint(1,1000000000),"member": {"amount":amount ,"username": username,}}}]
        ],
        "checkTransfer":["客戶/检查存取款操作是否成功",
        "/api/member/checkTransfer?agent_name=%s"%clientId,[
        {"0":{"billNo": bill_No}},{"1":{"billNo": bill_No}},
        {"2":{"billNo": bill_No}},{"3":{"billNo": bill_No}},
        {"4":{}},
        {"5":{"billNo": bill_No,"member": {"username": username}}},
        {"6":{"billNo": bill_No,"member": {"username": username}}},
        {"7":{"billNo": bill_No,"member": {"username": username}}},
        {"8":{"billNo": bill_No,"member": {"username": username}}},
        {"9":{"billNo": bill_No,"member": {"username": username}}},
        {"10":{"billNo": bill_No,"member": {"username": username}}},
        {"11":{"billNo":bill_No,"agentLogin":"xosouat"}},
        {"12":{"billNo": bill_No}},
        {"13":{}},
        {"14":{"billNo": bill_No,"member": {"username": username}}}]
        ],
        "updateLimit":['客戶/修改会员限红组',
        "/api/member/updateLimit?agent_name=%s"%clientId,[
        {"0":{"member": {"username": username},"oddType": "A"}},
        {"1":{}},
        {"2":{"member": {"username": "testsz8"},"oddType": "260301"}},
        {"3":{}},{"4":{}},{"5":{}},{"6":{}},{"7":{}},{"8":{}},{"9":{}},{"10":{}},{"11":{}},{"12":{}},{"13":{}},{"14":{}}]
        ],
        "checkOnline":["客戶/查询玩家在线状态",
        "/api/member/checkOnline?agent_name=%s"%clientId,[
        {"0":{"member": {"username": username.upper()}}},
        {"1":{"member": {"username": "%s_test"%username.upper()}}},
        {"2":{}},
        {"3":{"member": {"username": username}}},
        {"4":{}},{"5":{}},{"6":{}},{"7":{}},{"8":{}},{"9":{}},{"10":{}},{"11":{}},{"12":{}},{"13":{}},
        {"14":{"member": {"username": username}}}]
        ],
        "onlineCount":['客戶/查询在线玩家数量','/api/member/onlineCount?agent_name=%s'%clientId,[
        {"0":{}},{"1":{}},{"2":{}},{"3":{}},{"4":{}},{"5":{}},{"6":{}},{"7":{}},{"8":{}},{"9":{}},{"10":{}},{"11":{}},{"12":{}},{"13":{}},{"14":{}}]
        ],
        "offline":['客戶/踢人','/api/member/offline?agent_name=%s'%clientId,[
        {"0":{"member": {"memberId":member_Id}}},
        {"1":{"member": {"username": "%s_test"%username}}},
        {"2":{"member": {"username": username}}},
        {"3":{"member": {"username": username}}},
        {"4":{}},{"5":{}},{"6":{}},
        {"7":{"agentLogin": "amberdev","member": {"username": username}}},
        {"8":{"member": {"username": username}}},
        {"9":{}},
        {"10":{"member": {"username": username}}},
        {"11":{"agentLogin": "xosouat","member": {"username": username}}},
        {"12":{}},
        {"13":{}},
        {"14":{"member": {"username": username}}}]
        ],
        "lockMember":['客戶/封鎖會員','/api/member/lockMember?agent_name=%s'%clientId,[
        {"0":{"member": {"password":password,"username": username}}},
        {"1":{"member": {"username": "%s_test"%username}}},
        {"2":{}},{"3":{}},{"4":{}},
        {"5":{"member": {"username": username}}},
        {"6":{}},
        {"7":{"agentLogin": "amberdev","member": {"username": username}}},
        {"8":{"member": {"username": username}}},
        {"9":{}},{"10":{}},{"11":{}},{"12":{}},{"13":{}},{"14":{}}]
        ],
        "unlockMember":['客戶/解封鎖會員','/api/member/unlockMember?agent_name=%s'%clientId,[
        {"0":{"member": {"password":password,"username": username}}},
        {"1":{"member": {"username": "%s_test"%username}}},
        {"2":{}},{"3":{}},{"4":{}},
        {"5":{"member": {"username": username}}},
        {"6":{}},
        {"7":{"agentLogin": "amberdev","member": {"username": username}}},
        {"8":{"member": {"username": username}}},
        {"9":{}},{"10":{}},{"11":{}},{"12":{}},{"13":{}},{"14":{}}]
        ],
        "onlineMember":['客戶/查询在线玩家','/api/member/onlineMember?agent_name=%s&page=1&size=100'%clientId,
        [{"0":{}},{"1":{}},{"2":{}},{"3":{}},{"4":{}},{"5":{}},{"6":{}},{"7":{}},{"8":{}},{"9":{}},{"10":{}},{"11":{}},{"12":{}},{"13":{}},{"14":{}}]
        ],  
        "supplierGameFile":['上传三方游戏列表','/admin/config/supplierGameFile']
        }
    def GameBox_Con(client_id,env):# 連線 mysql
        env_dict = {0:['103.242.101.102',21330,'amberrd','Gvmz8DErUcHgMgQh','test.t_client'],
                    1:['54.248.18.149',3306,'gamebox','sgkdjsdf^mdsD1538','game_box_api.t_client']}
        db = p.connect(
        host = env_dict[env][0],
        port = env_dict[env][1],
        user = env_dict[env][2],
        passwd = env_dict[env][3],
        )
        table_name = env_dict[env][4]
        cur = db.cursor()
        sql = "SELECT app_id,app_key FROM %s where client_id = '%s'"%(table_name,client_id)# clien_id 找出 id,key
        #print(sql)
        cur.execute(sql)
        client_detail = {}
        rows = cur.fetchall()
        for i in rows:
            client_detail[client_id] = i
        #print(client_detail)
        return client_detail
        cur.close()
    
    # type_: 是用function 名, clientId = client帳號
    def GameBox_test(type_,clientId,username,client_detail,password,url,amount,filename,supplier_index):
        try:
            global access_token,token_type,pc_url,dr,memberId,appId,billNo,client_env
            #client_detail = GameBox.GameBox_Con(clientId)
            #username = 'kerr%s'%random.randint(1,1000)
            data_ =  GameBox(clientId=clientId,username=username,password=password).data_type[type_]
            print(type_,data_[0])
            #url_content = data_[1]
            test_header = { 
                "Content-Type": "application/json",
                'User-Agent':FF_().user_agent['Pc']
            }
         # 有可能DB 沒有該 clinet_id
            #if type_ != 'token':
            appId = client_detail[clientId][0]
            appKey = client_detail[clientId][1]
            #print(appId,appKey)
            if type_ in ['createApp','updateIpWhitelist','updateSupplierAccount','token','getClientInfo']:
                test_header['Authorization'] = token_type + " %s"%access_token
                if type_!= 'createApp':#另外兩個  需 在產 global appId
                    data_ =  GameBox(clientId,username,password=password,app_Id=appId).data_type[type_]
                data = data_[2]
                url_content = data_[1]
            #elif type_ in ['signUp','login','freeLogin','checkOnline','balance','transfer','updateLimit']:
            elif type_ == 'supplierGameFile':# 上传三方游戏列表 系統管理
                data_ =  GameBox(clientId,username,password=password,app_Id=appId).data_type[type_]
                data = MultipartEncoder(
                fields={'filename': '%s'%filename,
                    'version': '10001',
                    'file': ('%s.xlsx'%filename, #PG游戏名称列表 , test
                            open('C:\python3\Scripts\\FF_Script\\%s.xlsx'%filename, 
                            'rb'),
                     'application/octet-stream')})
                url_content = data_[1]
                test_header = { 
                "Content-Type": data.content_type,#"multipart/form-data",
                'User-Agent':FF_().user_agent['Pc'],
                }
                test_header['Authorization'] = token_type + " %s"%access_token
                #test_header['multipart/form-data'] = 'test'
            else:#客戶端
                if type_ == 'checkOnline':
                    if client_env not in [0,1,3]:# sexy ,gpi,YB, PG沒有 查詢再線玩家功能
                        #print("%s沒有查询玩家在线状态"%supplier_type)
                        pass
                        #return "%s沒有查询玩家在线状态"%supplier_type
                    else:
                        dr = webdriver.Chrome(executable_path=r'C:\python3\Scripts\FF_Script\chromedriver.exe')
                        print('需先瀏覽器登入PC login_url: %s'%pc_url)
                        dr.get(pc_url)# 用 瀏覽器登入, 才能 獲得 memberid(DG踢人才需要 memberid)
                        #sleep(20)
                        #dr.quit()
                elif type_ == 'offline':# 踢人 ,在把 global memberid 傳還init  
                    data_ =  GameBox(clientId,username,member_Id=memberId).data_type[type_]
                elif type_ == 'checkTransfer':# 檢查 轉帳轉太, 需把 transfer的 bill_no 傳回來
                    data_ =  GameBox(clientId,username,bill_No=billNo).data_type[type_]
                elif type_ == 'transfer':# 轉帳  ,把 amount 加進
                    data_ =  GameBox(clientId,username,password=password,amount=amount).data_type[type_]
                else:
                    pass
                time_ = int(time.time())
                test_header['appId'] = appId #appId#"930ea5d5a258f4f"#appId
                test_header['nonce-str'] = "ibuaiVcKdpRxkhJA"
                #test_header['appKey'] = "316489e115371ed23808a9ce2ee094a38ca4411a"
                test_header['timestamp'] = str(time_)#"1597729724"#str(time_)
                m = hashlib.md5()
                str_ = "appId=%s&nonce-str=ibuaiVcKdpRxkhJA&timestamp=%s&appKey=%s"%(appId,str(time_),
                                                                                     appKey)
                #print(str_)
                #print(str_,type(str_))
                m.update(str_.encode())
                str_md = m.hexdigest()
                test_header['signature'] = str_md.upper()#'9A0A8659F005D6984697E2CA0A9CF3B7'#str_md.upper()
                
                # data 內容 是大list 的第二元, 小list先帶出第幾個dict,載用str(數直取出)
                data = data_[2][client_env][str(client_env)]
                #print(supplier_type)
                supplier_ = supplier_type[bg_type] if client_env == 7 else supplier_type             
                if supplier_index == 1:# 需帶  suppliet_type 數
                    url_content = data_[1]+"&supplierType=%s"%supplier_ 
                else:
                    url_content = data_[1]
                if client_env == 3:# cq_9 url 後面參數  需用寫死  cq_9Key  
                    url_content = url_content.replace(clientId,cq_9Key)
                elif client_env == 2:# sexy的 agent_name 用 ambertest .不是client_id 
                    url_content = url_content.replace(clientId,"ambertest")
                else:
                    pass
            #print(type(data))    
            print('data:%s'%data)
            print('url: %s'%url_dict[env]+url_content)
            print(test_header)
            if type_ == 'supplierGameFile':# 上傳excel 需額外.json()
                FF_().session_post(url,url_content,data,test_header)
            else:
                #print(url_content)
                FF_().session_post(url,url_content,json.dumps(data),test_header)
            r_json = r.json()
            global status_code # 到時用來  驗證 請求狀態用
            status_code = r.status_code 
            #print('連線狀態: %s'%status_code)
            print('response: %s'%r.text)
            if type_ == 'token':
                access_token = r_json['access_token']
                token_type = r_json['token_type']
            elif type_ == 'checkOnline': #玩家在线状态
                if client_env == 0:# 沙巴 ,不需要 memeberID
                    memberId = r_json['data']['member']['memberId']
                else:
                    memberId = ''# 其它 硬給 .offline 踢人接口 會硬塞一個值
            elif type_ == 'login':
                pc_url = r_json['data']['pc']# 拿來 checkOnline  要先登入,才能  獲得memberId   
            elif type_ == 'transfer':
                if client_env in [3,4,5,7,8,9,10,11,12]:# cq_9,gpi,YB,pg response不會回傳  billNo , 需自己帶
                    billNo = data["billNo"]
                else:
                    billNo = r_json['data']['billNo']
        except KeyError as e:
            error_msg = 'KeyError : %s'%e
            print(error_msg)
            if 'memberId' in error_msg:
                for i in range(5):
                    try:
                        sleep(10)
                        FF_().session_post(url,url_content,json.dumps(data),test_header)
                        memberId = (r.json()['data']['member']['memberId'])
                        print(memberId)
                        return memberId
                    except:
                        print('繼續等候登入要memeberId')
            elif clientId in error_msg:# 創紀 createAPP 走這段, 因為 client_detail 為空 ,
                if type_ == 'createApp':
                    test_header['Authorization'] = token_type + " %s"%access_token
                url_content = data_[1]
                data = data_[2]
                FF_().session_post(url,url_content,json.dumps(data),test_header)
                r_json = r.json()
                print('連線狀態: %s'%status_code)
                print(r_json)
                if type_ == 'token':
                    access_token = r_json['access_token']
                    token_type = r_json['token_type']
        except NameError as e:
            error_msg  = "NameError : %s"%e
            print(error_msg)
            if 'token_type' in error_msg:# 需要從新獲取令牌
                print('需從新獲取令牌 token')
                url_content="/oauth/token?client_id=admin&client_secret=gameBox-2020-08-11*admin&username=admin&password=gameBox-2020-08-11*admin&grant_type=password&scope=all"
                test_header = { 
                "Content-Type": "application/json",
                'User-Agent':FF_().user_agent['Pc']
                }
                FF_().session_post(url,url_content,'',test_header) 
                access_token = r.json()['access_token']
                token_type = r.json()['token_type']



update_type  = 0# 0 : 刪除 . 1: 修改 ,updateSupplierAccount  更改管理端 client_id 用
url_dict = {0:'http://103.242.101.102:21080',1:'http://54.248.18.149:8203'}# 測試 / 灰度
#cq_9 的  key叫特別
cq_9Key="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyaWQiOiI1ZjU5OWU3NTc4MDdhYTAwMDFlYTFjMjYiLCJhY2NvdW50IjoiYW1iZXJ1YXQiLCJvd25lciI6IjVkYzExN2JjM2ViM2IzMDAwMTA4ZTQ4NyIsInBhcmVudCI6IjVkYzExN2JjM2ViM2IzMDAwMTA4ZTQ4NyIsImN1cnJlbmN5IjoiVk5EIiwianRpIjoiNzkyMjU1MDIzIiwiaWF0IjoxNTk5NzA4Nzg5LCJpc3MiOiJDeXByZXNzIiwic3ViIjoiU1NUb2tlbiJ9.cyvPJaWFGwhX4dZV7fwcwgUhGM9d5dVv8sgyctlRijc"

client_type = {
"api_key":
    {0: "1566e8efbdb444dfb670cd515ab99fda",1: "XT",2: "9RJ0PYLC5Ko4O4vGsqd",3:"",
4:"a93f661cb1fcc76f87cfe9bd96a3623f",5:"BgRWofgSb0CsXgyY",6:"b86fc6b051f63d73de262d4c34e3a0a9",
7:"8153503006031672EF300005E5EF6AEF",8:"000268d7cf113cb434e80f2de71188ddc3f45a0c8643c9fadf7d639\
2ec4dd42b3f2b82687999588fab2722814c62f650f98a588e8f372cb377b4e62302dc4addfdaa3e95cc48cfa9\
e308e3285e0eb54781b0ab29c2a95d544c64847c216c2f2b10a9e083de4506b0a901dac71651be86e680f5\
f61c4a2fb1fbccaa56ce9d88715a8c",9:"",10:"DF0FAEB6171BDEF9",11:"fe9b68fca25f2fe2",12:"dbettest",
13: "89CA25C2BA65AC9DD12E04BD66B6B467",14: "FB9EFF5983F0683F"},
"api_url":
    {0: "https://api.dg99web.com",1:"http://tsa.l0044.xtu168.com",
2:"https://testapi.onlinegames22.com",3:"http://api.cqgame.games",4:"http://gsmd.336699bet.com",
5:"https://api.ybzr.online/",6:"http://ab.test.gf-gaming.com",
7:'http://am.bgvip55.com/open-cloud/api/',8:"https://spi-test.r4espt.com",
9:"http://operatorapi.staging.imaegisapi.com",10:'https://api.cp888.cloud',11:"http://api.jygrq.com",
12:"https://linkapi.bbinauth.net/app/WebService/JSON/display.php",13:"https://api.0x666666.com",
14: "https://wc-api.hddv1.com/channelHandle"},
"supplier_type":
    {0:"dream_game",1:"sa_ba_sports",2: "ae_sexy",3:"cq_9",4:"gpi",5:"ya_bo_live",6:"pg_game",
7:{"game":"bg_game","fish":'bg_fishing','chess':'bg_chess','lottery':'bg_lottery'},
8:"tf_gaming",9:"im_sb",10: "ya_bo_lottery",11: "jdb_electronic",
12: "bb_in",13:"yx_game",14: "ky_chess"},
"supplier_user":
{0: "DGTE01011T",1: "6yayl95mkn",2: "fhlmag",3: "cq9_test",4: "xo8v",5: "ZSCH5",
 6: "aba4d198602ba6f2a3a604edcebd08f1",7:"am00",8:"711",9:"OPRikJXEbbH36LAphfbD5RXcum6qifl8",
 10:"fhagen",11:"XT",12: "test",13: "FH",14: "72298"}# DB 裡 client_id
}

env = 0# 環境變數  0 測試區 或1 灰度
# 0 : DG , 1: 沙巴 ,2: sexy, 3 : cq9 , 4: gpi,5: YB,6: PG, 7:bg ,8: tfGaming,9: imSb ,10: ya_bo_lottery
#11: JDB , 12: bbin 13: yx_game ,14: ky
client_env = 11

clientId = client_type["supplier_user"][client_env]# agent_name 商戶 ,gamebox預設 : DGTE01011T , 沙巴: 
client_detail = GameBox.GameBox_Con(clientId,env)# 登入DB , 是 寫死 cq9_test ,
api_key = client_type["api_key"][client_env]
api_url = client_type["api_url"][client_env]
supplier_type = client_type["supplier_type"][client_env]
supplier_user = client_type["supplier_user"][client_env]
#for i in range(1):# http://43.240.38.15:21080  , http://54.248.18.149:82030
bg_type = 'fish' #['game','fish','chess','lottery']

GameBox.GameBox_test(type_= 'login',clientId=clientId,username='kerr483ss2',
client_detail=client_detail,password='123qwe',url=url_dict[env],amount="100",
                     filename='gameList',supplier_index=1)


#(['token', 'createApp', 'updateIpWhitelist', 'updateSupplierAccount', getClientInfo
#'signUp', 'login', 'freeLogin', 'update', 'balance', 'transfer', lockMember, unlockMember
#'checkTransfer', 'updateLimit', 'checkOnline', 'onlineCount', 'offline','onlineMember', 
#supplierGameFile]):ii


# In[ ]:


threads = []
for i in range(2):
    t = threading.Thread(target=GameBox.GameBox_test,args=('transfer',clientId,'hsieh0sdsdsd01',
     client_detail,'123qwe',url_dict[env],'-10'))

    threads.append(t)

for i in threads:
    i.start()
for i in threads:
    i.join()


# In[ ]:



class GameBoxTest_Admin(unittest.TestCase):
    '''GameBox管理端'''
    def assert_(self):
        return self.assertEqual(200,status_code,msg='請求狀態有誤')
    def func(func_='client'):# 共用 的方法, 差別再type_ ,需宿改 各參數 再這邊加
        if func_ == 'client':
            for supplier_ in supplier_list:
                #print(supplier_)
                print("query不帶supplierType參數") if supplier_ == 0 else print("query帶supplierType參數")
                GameBox.GameBox_test(type_= type_,clientId=clientId,username=username,
                    client_detail=client_detail,password='123qwe',url=url_dict[env][0],amount="10",
                    filename='gray',supplier_index=supplier_ ),
                GameBoxTest_Admin().assert_()
    def func_wrap(func):# 獲取當前 測試案例的 名稱 ,扣除 test
        @wraps(func)
        def tmp(*args, **kwargs):
            global type_
            type_ = (func.__name__).split('_')[1]#切割 名稱 , unittest 統一案例,都已 test_ 為開頭
            return func(*args, **kwargs)
        return tmp
    @func_wrap
    def test_token(self):
        '''管理端-獲取token'''
        GameBoxTest_Admin.func(func_='admin')
    @func_wrap
    def test_createApp(self):
        '''管理端-獲取client帳號'''
        GameBoxTest_Admin.func(func_='admin')
    @func_wrap
    def test_updateIpWhitelist(self):
        '''管理端-修改ip白名單'''
        GameBoxTest_Admin.func(func_='admin')
    @func_wrap
    def test_updateSupplierAccount(self):
        '''管理端-修改client信息'''
        GameBoxTest_Admin.func(func_='admin')
    @func_wrap
    def test_getClientInfo(self):
        '''管理端-获取client信息'''
        GameBoxTest_Admin.func(func_='admin')
class GameBoxTest_User(GameBoxTest_Admin):
    '''GameBox客戶端'''
    @GameBoxTest_Admin.func_wrap
    def test_signUp(self):
        '''用戶端-註冊'''
        GameBoxTest_Admin.func()
    @GameBoxTest_Admin.func_wrap
    def test_login(self):
        '''用戶端-登入'''
        GameBoxTest_Admin.func()
    @GameBoxTest_Admin.func_wrap
    def test_freeLogin(self):
        '''用戶端-試玩帳號'''
        GameBoxTest_Admin.func()
    @GameBoxTest_Admin.func_wrap
    def test_update(self):
        '''用戶端-修改用戶信息'''
        GameBoxTest_Admin.func()
    @GameBoxTest_Admin.func_wrap
    def test_balance(self):
        '''用戶端-查詢餘額'''
        GameBoxTest_Admin.func()
    @GameBoxTest_Admin.func_wrap
    def test_transfer(self):
        '''用戶端-加幣額度'''
        GameBoxTest_Admin.func()
    @GameBoxTest_Admin.func_wrap
    def test_checkTransfer(self):
        '''用戶端-檢查轉帳狀態'''
        GameBoxTest_Admin.func()
    @GameBoxTest_Admin.func_wrap
    def test_updateLimit(self):
        '''用戶端-更新用戶限紅組'''
        GameBoxTest_Admin.func()
    @GameBoxTest_Admin.func_wrap
    def test_checkOnline(self):
        '''用戶端-在線狀態'''
        GameBoxTest_Admin.func()
    @GameBoxTest_Admin.func_wrap
    def test_onlineCount(self):
        '''用戶端-在線人數'''
        GameBoxTest_Admin.func()
    @GameBoxTest_Admin.func_wrap
    def test_offline(self):
        '''用戶端-踢人'''
        GameBoxTest_Admin.func()
    @GameBoxTest_Admin.func_wrap
    def test_lockMember(self):
        '''用戶端-封鎖會員'''
        GameBoxTest_Admin.func()
    @GameBoxTest_Admin.func_wrap
    def test_unlockMember(self):
        '''用戶端-解封鎖會員'''
        GameBoxTest_Admin.func()
    @GameBoxTest_Admin.func_wrap
    def test_onlineMember(self):
        '''用戶端-查询在线玩家'''
        GameBoxTest_Admin.func()

# 0 : gamebox , 1: 沙巴 ,2: sexy, 3 : cq9 , 4: gpi,5: YB,6: PG, 7:bg ,8: tfGaming,9: imSb ,10: ya_bo_lottery
#11: JDB  12: bbin 13: yx_game
client_env = 7
env = 0# 0為 43 測試 , 1 為 54 灰度   
supplier_list = [1]
bg_type = 'lottery' #['game','fish','chess','lottery']
url_dict = {0:['http://103.242.101.102:21080','測試區'],1:['http://54.248.18.149:8203','灰度']}# 測試 / 灰度

api_key = client_type["api_key"][client_env]
api_url = client_type["api_url"][client_env]
supplier_type = client_type["supplier_type"][client_env]
supplier_user = client_type["supplier_user"][client_env]
clientId = supplier_user# agent_name 商戶
client_detail = GameBox.GameBox_Con(clientId,env)# 登入DB

# 生產 帶 gray ,測試不帶
username = 'kerrgray%s'%random.randint(1,10000) if env ==1 else 'kerr%s'%random.randint(1,100000)
#bg supplier_type需處理  
supplier_ =  supplier_type[bg_type] if client_env == 7 else supplier_type 

suite = unittest.TestSuite()
#管理端 測試項目
admin_test = [GameBoxTest_Admin('test_token'),GameBoxTest_Admin('test_getClientInfo')]
#用戶端 測試項目 0 : gamebox .1 : 沙巴 .  沙巴不需要  試玩freeLogin ,  updateLimit 会员限红组


user_test = [GameBoxTest_User('test_signUp'),GameBoxTest_User('test_login'),
GameBoxTest_User('test_freeLogin'),GameBoxTest_User('test_update'),
GameBoxTest_User('test_lockMember'),GameBoxTest_User('test_unlockMember')
,GameBoxTest_User('test_transfer'),
GameBoxTest_User('test_checkTransfer'),
GameBoxTest_User('test_balance'),GameBoxTest_User('test_updateLimit'),
GameBoxTest_User('test_checkOnline'),GameBoxTest_User('test_onlineCount'),
GameBoxTest_User('test_offline'),GameBoxTest_User('test_onlineMember')]

ID_test = [GameBoxTest_User('test_balance'),GameBoxTest_User('test_transfer')]#克制  餘額和轉帳

#test = [GameBoxTest_User('test_login')]


#suite.addTests(admin_test)
suite.addTests(user_test)

#suite.addTests(ID_test)


now = time.strftime('%Y_%m_%d^%H-%M-%S')
filename = now + supplier_  + '.html'
fp = open(filename, 'wb')
runner = HTMLTestRunner.HTMLTestRunner(
        stream=fp,
        title=u'測試報告',
        description='環境: %s, client商戶: %s, supplierType: %s, 用戶名: %s '
    %(url_dict[env][1]+url_dict[env][0]
         ,clientId,supplier_,username)
        )
runner.run(suite)
fp.close()

#sleep(10)
#dr.quit()
'''
runner = unittest.TextTestRunner(verbosity=2)
runner.run(suite)
'''


# In[ ]:


bet_type


# In[ ]:



class YFT(GameBoxTest_Admin):
    def title(self,type_,env_type): # type_ : 雨淋, 菲奧 , 天雅  ,env_type :  測試 ,  生產
        header = FF_().user_agent['Pc']
        Pc_header = {'User-Agent': FF_().user_agent['Pc']}
        if env_type == "test":#測試
            print('測試環境')
            url = "http://www.%s.qa.space/"%type_
        else: # 生產
            if type_ == "yulin":
                url_con = "260"
            elif type_ == "feiao":
                url_con = "222"
            elif type_ == "tianya":
                url_con = "07"
            url = "https://www.%s%s.com"%(type_,url_con)
        FF_().session_get(url,'','',Pc_header)
        html = BeautifulSoup(r.text,'lxml')
        global title
        title = str(html.title) 
        print (title)
        #print(type(title))
    def assert_title(self,title_name):
        title_names = "<title>%s</title>"%title_name
        return self.assertEqual(title_names,title,msg='title有誤')
    @GameBoxTest_Admin.func_wrap
    def test_feiao(self):
        '''菲奧測試'''
        print(type_)
        YFT().title(type_,env_type)
        YFT().assert_title("菲澳娱乐")
        print('ok')
    @GameBoxTest_Admin.func_wrap
    def test_tianya(self):
        '''天亞測試'''
        print(type_)
        YFT().title(type_,env_type)
        YFT().assert_title("天亚娱乐")
    @GameBoxTest_Admin.func_wrap
    def test_yulin(self):
        '''雨林測試'''
        YFT().title(type_,env_type)
        YFT().assert_title("羽林娱乐")

env_type = "test1"# test測試 , 非 test: 生產
suite = unittest.TestSuite()
admin_test = [YFT('test_feiao'),YFT('test_tianya'),YFT('test_yulin')]
suite.addTests(admin_test)
runner = unittest.TextTestRunner(verbosity=2)
runner.run(suite)


# In[ ]:


dr.quit()# 瀏覽器關閉


# In[ ]:


# 執行續 併發
threads = []
user = 'kerr'
func_name = 'signUp'
for i in range(21,40,1):
    t = threading.Thread(target=GameBox.GameBox_test,args=(func_name,clientId,'kerr{:03d}'.format(i),
    client_detail,'123qwe'))
    threads.append(t)
for i in threads:
    i.start()
for i in threads:
    i.join()


# In[ ]:


client_list =[ 'signUp', 'login', 'freeLogin', 'update', 'balance', 'transfer', #客戶端 function name
'checkTransfer', 'updateLimit', 'checkOnline', 'onlineCount', 'offline']
username = 'kerr%s'%random.randint(1,1000)# 建立一個 隨機用戶名
print(username)
clientId = 'DGTE01011T'# agent_name 商戶
env = 1# 環境變數 , 0: 測試 , 1: 灰度
client_detail = GameBox.GameBox_Con(clientId,env)# 登入DB
url_dict = {0:'http://43.240.38.15:21080',1:'http://54.248.18.149:8203'}# 測試 / 灰度
#for i in range(1):# http://43.240.38.15:21080  , http://54.248.18.149:8203
for func_name in client_list:
    GameBox.GameBox_test(type_= func_name,clientId=clientId,username=username,
    client_detail=client_detail,password='123qwe',url=url_dict[env])
dr.quit()


# In[ ]:


GameBox().data_type.keys()
#GameBox(clientId).data_type[type_][1]


# In[ ]:


DG(username='hsieh001').data_type.keys()


# In[ ]:



print(App.token,FF_().cookies,FF_().submit_inf)


# In[ ]:


account_list = ['kerr000','kerr003','kerr001','kerr00','kerr0','kerr002','kerr004','kerr005','kerr006','kerr007']
for i in account_list:
    FF_().Pc_Login('joy188',i)


# In[ ]:


App().App_Login('dev','hsiehwin001',1)# 1 為joint_venture參數


# In[ ]:


# 一般投注 ,stop預設為""(一般投注),ball 預設為""(寫死投注內容,後續彩種補上) 
FF_().Pc_Submit(lottery='cqssc',awardmode=2,type_=1,user='kerr000')


# In[ ]:


#多彩種投注
for lottery in FF_().lottery_dict.keys():
    print(lottery)
    if lottery in ['cqssc','xjssc','tjssc','hljssc','llssc','slmmc','txffc',
                   'fhjlssc','fhcqc','fhxjc','ssq']:
        awardmode_ = 1
    else:
        awardmode_ = 2
    try:
        FF_().Pc_Submit(lottery=lottery,awardmode=awardmode_,type_=2)
    except UnboundLocalError as e:
        print(e)
    except JSONDecodeError as e:
        print(e)


# In[ ]:


def sum_three(number):#三位數相加
    result = number % 10 # 取各位數
    result += number // 10 % 10#十位數 : 先除10 ,除整數, 再 取10的魚數
    result += number //100
    return result
sum_three(123)


# In[ ]:


pcdd_paly = {}
def three_tool(index):#index 參數 為  三個數值總合  ,ＰＣＤＤ　
    all_three = []# 所有足合地方
    for num in range(1000):#0-999 三位數
        three_num = '{:03d}'.format(num)# 000格式
        #print(three_num)
        three_sum = (sum_three(int(three_num)))
        if three_sum == index:
            all_three.append(three_sum)
    return(len(all_three))
gray_num = 0
green_num = 0
blue_num = 0
red_num = 0
for i in range(28):
    if i in [0,13,14,27]:
        number_color = '灰'
        gray_num = gray_num + three_tool(i)
    elif i in [1,4,7,10,16,19,22,25]:
        number_color = '綠'
        green_num = green_num + three_tool(i)
    elif i in [2,5,8,1,11,17,20,23,26]:
        number_color = '藍'
        blue_num = blue_num + three_tool(i)
    else:
        number_color = '紅'
        red_num = red_num + three_tool(i)
    dict_num = {}#個數
    dict_color ={}#顏色 分步
    dict_list = []# value 一個list
    dict_num['個數'] = three_tool(i)
    dict_color['顏色'] = number_color
    dict_list.append(dict_num)
    dict_list.append(dict_color)
    pcdd_paly[i] = dict_list
    
    #print('%s: %s'%(i,three_tool(i)))
pcdd_paly  


# In[ ]:


#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#繪圖用
    
###############################################################################
#                              股票機器人 籌碼面分析                            #
###############################################################################

# 畫出籌碼面圖

urllib3.disable_warnings()#解決 會跳出 request InsecureRequestWarning問題
'''
for i in range(3,0,-1):
    date = datetime.datetime.strftime(datetime.datetime.now() - datetime.timedelta(days=i),'%Y%m%d') #先設定要爬的時間
    print(date)
'''
def fake_user():
    ua = UserAgent()
    global user_agent
    user_agent = ua.random
tst  = []# 存放 各  股號: 法人買賣 的list
sumstock=[]
stockdate=[]
stock_test = {}# key為 時尖
def test_gov(stocknumber):
    global sumstock,stockdate,stock_test,stock_test2,tst
    stock_test2 = []# key微鼓號,  value 為 法人買賣
    date = datetime.datetime.strftime(datetime.datetime.now() ,'%Y%m%d')#給 證交往頁請求用
    date_sql = datetime.datetime.strftime(datetime.datetime.now(),'%Y-%m-%d' )#給sql 用
    #print(date)
    session = requests.Session()
    fake_user()
    header = {
         'User-Agent':user_agent,
        'Content-Type': 'application/json; charset=UTF-8',
        'Accept': 'application/json, text/javascript, */*; q=0.01'
    }
    #date = '20200727'# 測試用
    print(date)
    r = session.get('https://www.twse.com.tw/fund/T86?response=csv&date='+date+'&selectType=ALLBUT0999',
    verify=False,timeout=10) #要爬的網站
    #print(twstock.codes[stocknumber][2]) 名曾
    if r.text != '\r\n': #有可能會沒有爬到東西，有可能是六日
        get = pd.read_csv(StringIO(r.text), header=1).dropna(how='all', axis=1).dropna(how='any') # 把交易所的csv資料載下來
        get=get[get['證券代號']==stocknumber] # 找到我們要搜尋的股票
        if len(get) >0:
            get['三大法人買賣超股數'] = get['三大法人買賣超股數'].str.replace(',','').astype(float) # 去掉','這個符號把它轉成數字

            stock_test2.append(stocknumber)
            stock_test2.append(get['三大法人買賣超股數'].values[0])
            stock_test2.append(date_sql)
            tst.append(tuple(stock_test2))
            #print(tst)
            stock_test[date] = tst

            stockdate.append(date)
            sumstock.append(get['三大法人買賣超股數'].values[0])
''' 圖生成
if len(stockdate) >0:
    ### 開始畫圖 ###
    plt.bar(stockdate, sumstock) 
    plt.xticks(fontsize=10,rotation=90)
    plt.axhline(0, color='c', linewidth=1) # 繪製0的那條線
    plt.title('Institutional Investors', fontsize=20)
    plt.xlabel("Day", fontsize=15)
    plt.ylabel("Quantity", fontsize=15)
    plt.show()
    plt.savefig('showII.png') #存檔
    plt. close() # 殺掉記憶體中的圖片
'''


# In[ ]:


stock_test


# In[ ]:


stock_num


# In[ ]:


tst  = []#
stock_test = {}# key為 時尖
stock_test2 = []
while True:
    for i in stock_num:#  stock_num  是從DB抓取股票號碼
        sleep(random.uniform(1,3.5))
        try:
            test_gov(str(i))
            print('%s成功'%i)
        except:
            print('%s失敗'%i)
            break
    break
print(stock_test)
    


# In[ ]:



start = datetime.datetime(2020,1,1)
df_2330 = pdr.DataReader('2330.TW', 'yahoo', start=start)
df_2330.index = df_2330.index.format(formatter=lambda x: x.strftime('%Y-%m-%d')) 
#plt.style.use('ggplot')
fig = plt.figure(figsize=(24, 15))

#ax = fig.add_subplot(1, 1, 1)
ax = fig.add_axes([0,0.2,1,0.5])
ax2 = fig.add_axes([0,0,1,0.2])
ax.set_xticks(range(0, len(df_2330.index), 100))
ax.set_xticklabels(df_2330.index[::100])#10唯一循環
mpf.candlestick2_ochl(ax, df_2330['Open'], df_2330['Close'], df_2330['High'],
df_2330['Low'], width=0.6, colorup='r', colordown='g', alpha=0.75); 

sma_10 = talib.SMA(np.array(df_2330['Close']), 10)
sma_30 = talib.SMA(np.array(df_2330['Close']), 30)

plt.rcParams['font.sans-serif']=['Microsoft JhengHei'] 
ax.plot(sma_10, label='10日均線')
ax.plot(sma_30, label='30日均線')

mpf.volume_overlay(ax2, df_2330['Open'], df_2330['Close'], df_2330['Volume'], colorup='r', colordown='g', width=0.5, alpha=0.8)
ax2.set_xticks(range(0, len(df_2330.index), 10))
ax2.set_xticklabels(df_2330.index[::10])
ax.legend();


# In[ ]:


import pandas_datareader as pdr
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties




import twstock
def df_test(number):
    plt.rcParams['font.sans-serif']=['Microsoft JhengHei'] #用来正常显示中文标签
    plt.rcParams['axes.unicode_minus']=False #用来正常显示负号
    plt.style.use('ggplot')
    start = datetime.datetime(2018,1,1)
    global df_#回傳給test_forecast 預測方法用
    try:
        df_ = pdr.DataReader(number+'.TW','yahoo',start=start)
    except:
        return('NO')
    print(df_)
    plt.title(twstock.codes[number][2])
    #plt.style.use('ggplot')
    test = df_['Adj Close']
    #print(list(test))#該股  列表歷史收盤
    #test_vol = df_['Volume']

    #plt.title('我')
    plt.ylabel(u"股價")


    test.plot(figsize=(12,8))
    #test_vol.plot(figsize=(12,8))
    #print(test)
df_test('2409')


# In[ ]:


now = datetime.datetime.now()
now_date = datetime.datetime(now.year,now.month,now.day)
print(now_date)
try:
    df = pdr.DataReader('1234'+'.TW','yahoo',start=now_date)
    print(df)
except KeyError:
    pass
a =df['Close']
print(a)
print(list(a))
test = round(a[0],2)
print(type(test))


# In[ ]:


def admin_Login(url):
    global admin_cookie
    global admin_url
    global envs
    global userAgent
    global session
    global header
    admin_cookie = {} 
    session = requests.Session()
    userAgent = UserAgent().random
    header = {
        'User-Agent': userAgent,
        'Content-Type':'application/x-www-form-urlencoded; charset=UTF-8'
    }

    admin_url = 'http://admin.%s.com'%url
    username = 'cancus'
    bindpwd = 123456
    if url in ['dev02','dev03']:
        password = '123qwe'
        envs = 0
    elif url == 'joy188':
        password = 'amberrd'
        envs = 1
    else:#生產  phl58'
        username = 'tprd'
        password = 'amberrd'
        r = session.get('http://admin.dev03.com'+'/admin/login/bindpwd',headers=header)
        bindpwd = (r.text.split('<br>')[2])
        envs = 2

    data_ = {
        'username':username,
        'password':password,
        'bindpwd':bindpwd 
    }
    
    # 'username=cancus&password=123qwe&bindpwd=123456'
    r = session.post(admin_url+'/admin/login/login',data = data_, headers = header)
    global cookies
    cookies = r.cookies.get_dict()#獲得登入的cookies 字典
    
    admin_cookie['admin_cookie'] =  cookies['ANVOAID']
    t = time.strftime('%Y%m%d %H:%M:%S')
    print('登錄環境%s,'%url+'現在時間:'+t)
    print(r.text)
    
    
admin_Login('dev02')


# In[ ]:


select_fundID(get_conn(envs),'hsieh001')
fund_id


# In[ ]:


select_userid(get_conn(1),'kerr001')


# In[ ]:



def add_activity(user,depoist,value):# 增加後台禮金 ,value 是人工資項金的類型  總共有  1-60 項
    header={
            'User-Agent': userAgent,
            'Cookie': 'ANVOAID='+cookies['ANVOAID'],
             'Accept':'application/json, text/javascript, */*; q=0.01',
            'Content-Type':'application/x-www-form-urlencoded; charset=UTF-8'
         }
    user_id = select_userid(get_conn(envs),user)[0]
    data = "rcvAct=%s&depositAmt=%s&memo=test&id=&userId=%s&sSelectValue=%s&note=test&     chargeSn="%(user,depoist,user_id,value)

    r = session.post(admin_url+'/admin/Opterators/index?parma=opter1',headers=header,data=data)
    if (r.json()['status']) == 'ok':
        print('%s後台建立成功'%user)
    else:
        print('建立失敗')   
def activity_confirm(user):# 審核,需透過DB查id
    select_fundID(get_conn(envs),user)# 從DB 抓豬 typeid和 id
    for key in fund_id.keys():
        id_ = fund_id[key][0]# id值  ,審核需要用
        type_id = fund_id[key][1]# typeid 為人工類型
        data = 'id=%s&status=1&typeId=%s'%(id_,type_id)
        r =session.post(admin_url+'/admin/Opterators/index?parma=sv2',headers=header,data=data)
        if r.json()['status'] == 'ok':
            print('成功')
        else:
            print('失敗')
def admin_benefit(id_,sum_):
    header['Cookie'] = 'ANVOAID='+cookies['ANVOAID']
    data = "id=%s&realDailyWageAmt=%s&note=test"%(id_,sum_)
    r =session.post(admin_url+'/benefitAdmin/reviewOneDailyWage',headers=header,data=data)
    print(r.text)


# In[ ]:


admin_benefit(5441,153318000)


# In[ ]:


FF_().Pc_Submit(lottery = 'slmmc',awardmode=None,type_=1,user='kerr000')


# In[ ]:


for user in ['hsieh000']:
    for i in range(1,61):
        add_activity(user,i,str(i)) #後台創建 人工資金名細
    activity_confirm(user)


# In[ ]:


activity_confirm('hsieh001')


# In[ ]:


r =session.get(admin_url+'/admin/Opterators/index?parma=opter1',headers=header)
soup =  BeautifulSoup(r.text,'lxml')
#print(soup)
a = soup.find_all('select',{'id':'bankName'})
for i in a:
    print(i)['5']


# In[ ]:


def tran_user(move_type): # 代理線轉移
    header['ANVOAID'] = cookies['ANVOAID']
    if move_type ==0:#提升總代
        move_type = 'ga'
        target = ''# 提升總代 無需目標
        select_tranUser(get_conn(1),'%kerr%',1)#抓出一代用戶
        user = tran_user[0]
        print('用戶: %s轉移至總代'%user)
    elif move_type ==1:#跨代理轉一代
        move_type = 'loa'
        select_tranUser(get_conn(1),'%kerr%',2)#抓出二代用戶,目標需為不同上級
        random_user = random.randint(1,len(tran_user))# 隨機取出用戶,避免容易失敗,
        user = tran_user[random_user]#要做的用戶
        #print(user)
        target = user_chain[0].split('/')[1]# 此為  抓出來的總帶,  需找出  不是這個總帶的一帶
        #print(target)
        select_tranChainUser(get_conn(1),target,'%kerr%')# 抓出 不同的總帶
        random_user = random.randint(1,len(tran_user))# 隨機取出總代,避免容易失敗,
        target = tran_user[random_user]#此用戶 即為  目標
        #print(target)
        print('二代: %s用戶,轉移至一代,新總代為: %s'%(user,target))
    elif move_type == 2:#相同代理,跨上去一層
        move_type = 'lua'
        select_tranUser(get_conn(1),'%kerr%',3)#抓出三代用戶,目標需為相同上級
        user = tran_user[0]#要做的用戶
        target = user_chain[0].split('/')[1]# 此為  抓出來的總帶,  需找出  是這個用戶的總代
        print('三代: %s用戶,轉移至二代,相同總代為: %s'%(user,target))
        
    data = 'moveAccount=%s&targetAccount=%s&moveType=%s'%(user,target,move_type)# 要做轉移的用戶,目標用戶 ,類型 
    r= session.post(admin_url+'/admin/user/userchaincreate',headers=header,data=data)
    #print(r.json())
    if 'true' in r.text:
        print('成功')
    else:
        print(r.json()['errorMsg'])
    
    
#tran_user(move_type=2)


# In[ ]:


import time
import datetime
 
# 先获得时间数组格式的日期
threeDayAgo = (datetime.datetime.now() - datetime.timedelta(days = 31))
print(threeDayAgo)


# In[ ]:


any(s in domain for s in ['joy188','dev'])


# In[ ]:


def kerr_conn():
    db = p.connect(
    host="127.0.0.1",
    user="root",
    passwd="123qwe",
    database="kerr_test",
    use_unicode=True,
    charset="utf8"
    )
    return db
def kerr_insert(db,list_name,type_): # list_name  為一個列表裡面  ,是tuple 的值
    cur = db.cursor()
    if type_ ==1 : #每月營收
    # insert  所有表
        sql = "INSERT INTO STOCK_REV          (ID ,STOCK_NUM ,STOCK_NAME ,STOCK_CUR_MONREV ,STOCK_LAST_MONREV ,        STOCK_LAST_YEARMONREV,STOCK_LAST_MONRATE ,STOCK_LAST_YEARMONRATE,STOCK_CUR_YEARREV ,        STOCK_LAST_YEARREV ,STOCK_YEARRATE  ,STOCK_MEMO) Values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s, %s,%s)"
    elif type_ ==2:
        sql = "INSERT INTO STOCK_GOV         (STOCK_NUM,GOV_SELL,CUR_DATE) Values (%s,%s,%s)"
    elif type_ == 3 : # 給別的想inset處理的條件
        sql = "INSERT INTO STOCK_GOV (CUR_DATE) Values(%s)" 
    else:# 塞第三方投注紀錄
        if type_ == 'ag':
            sql = "INSERT INTO AG_BET_RECORD              (ID ,AG_ACCOUNT ,PLAT_SN ,PLATFORM_TYPE ,GAME_TYPE ,            COST,PRIZE ,PROFIT,VALID_BET ,STATUS,CURRENCY,CREATE_TIME,UPDATE_TIME,CALCU_TIME,COLLECT_CREATE_TIME,             COLLECT_UPDATE_TIME ,JSON_RESULT  ,CALCU_LOCAL_TIME)             Values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s, %s,%s,%s,%s,%s,%s,%s,%s)"
        elif type_ == 'bbin':
            sql = "INSERT INTO THIRDLY_BET_RECORD              (SEQ_ID ,THIRDLY_USER_ID,THIRDLY_ACCOUNT ,WAGERS_ID ,WAGERS_DATE ,            MODIFIED_DATE, SERIAL_ID ,ROUND_NO, GAME_TYPE ,WAGER_DETAIL, GAME_CODE, RESULT, RESULT_TYPE, CARD,            BET_AMOUNT, PAY_OFF,CURRENCY, EXCHANGE_RATE, COMMISSIONABLE, ORIGIN, CREATE_DATE,UPDATE_DATE,            JSON_RESULT,USER_MSG_FLAG ,USER_MSG_DATE  ,GAME_KIND)             Values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s, %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        elif type_ == 'bc':
            sql = "INSERT INTO THIRDLY_BET_RECORD              (ID ,THIRDLY_ACCOUNT ,SN  ,            GAME_TYPE ,COST,PRIZE ,PROFIT,VALID_BET ,STATUS,CURRENCY,            BET_TIME, CREATE_TIME,UPDATE_TIME,            JSON_RESULT,CALC_DATE ,DEDUCTION_STATUS  )             Values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s, %s,%s,%s,%s,%s,%s)"
        elif type_ == 'im':
            sql = "INSERT INTO THIRDLY_BET_RECORD              (ID ,THIRDLY_ACCOUNT ,SN  ,            GAME_TYPE ,COST,PRIZE ,PROFIT,VALID_BET ,STATUS,CURRENCY,            BET_TIME, CREATE_TIME,UPDATE_TIME,            JSON_RESULT  )             Values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s, %s,%s,%s,%s)"
            
    cur.executemany(sql,list_name)
    db.commit()
    print("insert成功")
    cur.close()
def kerr_update2(db):# 找出對應號碼, update 營收
    cur = db.cursor()
    for num in range(len(stock_Name)):
        
        sql = "UPDATE STOCK_REV SET STOCK_CUR_MONREV = %s,STOCK_LAST_MONREV=%s,STOCK_LAST_YEARMONREV=%s,         STOCK_LAST_MONRATE=%s ,STOCK_LAST_YEARMONRATE=%s,STOCK_CUR_YEARREV=%s ,STOCK_LAST_YEARREV=%s ,        STOCK_YEARRATE=%s  ,STOCK_MEMO ='%s'          WHERE STOCK_NUM = %s"%(stock_Name[num][3],stock_Name[num][4],stock_Name[num][5],stock_Name[num][6],
        stock_Name[num][7],stock_Name[num][8],stock_Name[num][9],stock_Name[num][10],stock_Name[num][11],
        stock_Name[num][1])
        print('%s update營收完成'%num)
        cur.execute(sql)
        
    db.commit()
    print("update完成")
    cur.close()
def kerr_select(db):#找出股號, 然後傳到 twstock, 找出股價
    cur = db.cursor()
    #預設股市
    sql = "SELECT STOCK_NUM from STOCK_REV"
    cur.execute(sql)
    global stock_num
    stock_num = []
    rows = cur.fetchall()
    for i in rows:
        stock_num.append(i[0])# i為一個tuple
    cur.close()

def select_config(db):# config定
    cur = db.cursor()
    #預設股市
    sql = "SELECT *  from Config"
    cur.execute(sql)
    global config_con
    config_con = {}
    config_list = []
    rows = cur.fetchall()
    print(rows)
    for index,content in enumerate(rows):
        config_con[index] = content
    cur.close()
    


# In[ ]:


kerr_insert(my_con(1,'im'),record_list,'im')


# In[ ]:


kerr_select(kerr_conn())# 股票 所以 名稱
print(len(stock_num))
stock_num


# In[ ]:


kerr_update2(kerr_conn())#塞每月營收資料 進表


# In[ ]:


select_config(kerr_conn())
config_con


# In[ ]:


kerr_insert(kerr_conn(),stock_test[list(stock_test.keys())[0]],2)#更新每日法人買


# In[ ]:


kerr_update2(kerr_conn())


# In[ ]:


now = datetime.datetime.now()
print(type(now.day))


# In[ ]:


def soup_stock():# 抓取數據 , len_index  為抓到的東西 , date 為時間 ,格式 109_3 ,每月營收數據
    userAgent ="Mozilla/5.0 (Windows NT 10.0; Win64; x64)    AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.122 Safari/537.36"
    urllib3.disable_warnings()#解決 會跳出 request InsecureRequestWarning問題
    header = {
            'User-Agent': userAgent,
            'Content-Type':'application/x-www-form-urlencoded; charset=UTF-8'
        }
    session = requests.Session()
    now = datetime.datetime.now()#年找出今年.  月和日做參數化.因為可能會找先前日棋
    year = now.year -1911# 換算民國
    month = now.month -1#抓上個月
    print("抓取%s月"%month)# 當月
    r = session.get('https://mops.twse.com.tw'+'/nas/t21/sii/t21sc03_%s_%s_0.html'
    %(year,month),headers=header,verify=False)
    r.encoding = 'Big5' #繁體編碼
    soup = BeautifulSoup(r.text,'lxml')
    #soup.encode('gb18030')
    #global len_index
    len_index = [i for i in soup.find_all('tr',{'align':'right'})]
    #print(len(len_index))
    global stock_Name
    stock_Name = [] #存放所有抓到的資訊
    stock_list =[]
    for number in range(len(len_index)-1):#先取出多少長度, -1 用意, 最後一行不是抓股資訊
        stock_list.append(number)# mysql 的 ID 欄位
        for text in len_index[number]:#再從len_index陣列,取出 每個index的資訊
            stock_list.append('0' if text.text.strip() in ['','合計']#strip()把空白部分去除
            else text.text.strip().replace(',',''))
        if stock_list[-1] == '0':#過濾 不是股票名稱的 
            pass
        else:
            for num,text in enumerate(stock_list):# 需判斷 各 欄位 型態, 因為要Inser進去 Mysql, 型態需和mysql 欄位一致
                if num in [0,1]:
                    text = int(text)
                elif num in [2,11]:
                    text = str(text)
                elif num in [6,7,10]:
                    text = float(text)
                else:
                    text = int(text)
                stock_list[num] = text
        if len(stock_list) != 12:# 這邊代表 抓到的 不是股名 那行,可能是 合計
            pass
        else:
            stock_Name.append(tuple(stock_list))# 轉成tuple用意 ,好insert資料進mysql
        stock_list= []
    print(len(stock_Name))


# In[ ]:


soup_stock()
stock_Name


# In[ ]:




def my_con(evn,third):
    third_dict = {'lc':['lcadmin',['cA28yF#K=yx*RPHC','XyH]#xk76xY6e+bV'],'ff_lc'],
        'ky':['kyadmin',['ALtfN#F7Zj%AxXgs=dT9','kdT4W3#dEug3$pMM#z7q'],'ff_ky'],
        'city':['761cityadmin',['KDpTqUeRH7s-s#D*7]mY','bE%ytPX$5nU3c9#d'],'ff_761city'],
        'im':['imadmin',['D97W#$gdh=b39jZ7Px','nxDe2yt7XyuZ@CcNSE'],'ff_im'],
        'sb':['sbadmin',['UHRkbvu[2%N=5U*#P3JR','aR8(W294XV5KQ!Zf#"v9'],'ff_sb'],
        'bbin':['bbinadmin',['Csyh*P#jB3y}EyLxtg','t7H4h*wQfKgCk#Uu2}95'],'ff_bbin'],
        'gns':['gnsadmin','Gryd#aCPWCkT$F4pmn','ff_gns'],
        'ag': ['agadmin2',['qt5qGq9R3%yxn#8P3JR','RjZY2#aCPWCk%3dBvh'],'ff_ag2'],# 測是   
        'bc':['bcadmin',['u8u#4Q=xB$3xePHE$hF','6eUA2HgczV#ZYbG$hF'],'ff_bc']
         }
    third_dict2 = {'ag':['agrd2','QsKN2mdXsH6pK$*#M2d','ff_ag2'],'bbin':['bbinrd','de*USFzkDb#q4k37VSN','ff_bbin'],
                   'im':['imrd','F9Tv#KN4GX%Kxr#f6pf3kB','ff_im'],
                   'bc':['bcrd','AWnF#ThF8W*wB*9VH','ff_bc']
                 }
    if evn == 0:#dev
        ip = '10.13.22.151'
    elif evn == 1:#188
        ip = '10.6.32.147'
    elif evn == 2: # 生產
        ip = '10.6.31.145'
    else:
        print('evn 錯誤')
    if evn !=2: #測是
        user_ =  third_dict[third][0]
        db_ = third_dict[third][2]
        if third == 'gns':#gns只有一個 測試環境
            passwd_ = third_dict[third][1]
        else:
            passwd_ = third_dict[third][1][evn]
    else:#生產
        user_ =  third_dict2[third][0]
        db_ = third_dict2[third][2]
        passwd_ = third_dict2[third][1]
        
    
    db = p.connect(
    host = ip,
    user = user_,
    passwd = passwd_,
    db = db_,
    charset = 'utf8')
    return db
def mysql_avail(db,user):#第三方餘額

    cur = db.cursor()
    cur.execute("select avail_bal from THIRDLY_USER_CUSTOMER where ff_account = '%s'"%user)
    for row in cur.fetchall():
        return (row[0])
    cur.close()
    
def thirdly_tran(db,tran_type,third):#查詢第三方 單號 狀態
    cur = db.cursor()
    if third in ['lc','ky','city','im','sb']:
        table_name = 'THIRDLY_TRANSCATION_LOG'
        if tran_type == 0:
            trans_name = 'FIREFROG_TO_THIRDLY'
        else:
            trans_name = 'THIRDLY_TO_FIREFROG'
    elif third  == 'gns':
        table_name = 'GNS_TRANSCATION_LOG'
        if tran_type == 0:
            trans_name = 'FIREFROG_TO_GNS'
        else:
            trans_name = 'GNS_TO_FIREFROG'
    else:
        print('第三方 名稱錯誤')

    sql ="SELECT SN,STATUS FROM %s WHERE FF_ACCOUNT = 'kerr001'    AND CREATE_DATE >  DATE(NOW()) AND TRANS_NAME= '%s'"%(table_name,trans_name)

    global thirdly_sn,statu
    thirdly_sn = []#轉帳帳變
    statu = []#轉帳狀態  
    cur.execute(sql)
    for row in cur.fetchall():
        thirdly_sn.append(row[0])
        statu.append(row[1])
    cur.close()
def thrid_affUser(db,account):#查詢 是否為有效用戶 第三方帳號
    cur = db.cursor()
    sql ="SELECT THIRDLY_ACCOUNT,ACTIVE_DATE     FROM THIRDLY_ACTIVE_USER_LOG WHERE  thirdly_account = '%s'"%account
    global user_active
    user_active = {}#key 為 有效用戶 ,value 為 有效用戶的時間
    cur.execute(sql)
    for row in cur.fetchall():
        user_active[row[0]] = row[1]
    cur.close()
def thrid_affbet(db,account):#抓出有效用戶 投注的有效消亮
    cur = db.cursor()
    sql = "SELECT sum(cell_score) FROM THIRDLY_BET_RECORD WHERE thirdly_account = '%s'     AND game_end_time < '%s'"%(account,user_active[account])
    global sum_
    sum_ = []
    cur.execute(sql)
    for row in cur.fetchall():
        sum_.append(row)
    cur.close()
def thrid_submit(db,type_):#抓出注單
    cur = db.cursor()
    if type_ == 'ag':
        sql = "SELECT ID,AG_ACCOUNT,PLAT_SN,PLATFORM_TYPE,GROUP_CONCAT(DISTINCT game_type), COST,PRIZE,        PROFIT,VALID_BET ,STATUS,CURRENCY,CREATE_TIME,UPDATE_TIME,CALCU_TIME,COLLECT_CREATE_TIME,         COLLECT_UPDATE_TIME ,JSON_RESULT  ,CALCU_LOCAL_TIME         FROM AG_BET_RECORD         WHERE create_time BETWEEN  '2020-11-01 18:00:00' AND '2020-11-02 18:30:00' GROUP BY game_type"
    elif type_ == 'bbin':
        sql = "SELECT SEQ_ID ,THIRDLY_USER_ID,THIRDLY_ACCOUNT ,WAGERS_ID ,WAGERS_DATE ,            MODIFIED_DATE, SERIAL_ID ,ROUND_NO, GROUP_CONCAT(DISTINCT game_type) ,WAGER_DETAIL, GAME_CODE,             RESULT, RESULT_TYPE, CARD,            BET_AMOUNT, PAY_OFF,CURRENCY, EXCHANGE_RATE, COMMISSIONABLE, ORIGIN, CREATE_DATE,UPDATE_DATE,            JSON_RESULT,USER_MSG_FLAG ,USER_MSG_DATE  ,GAME_KIND         FROM THIRDLY_BET_RECORD WHERE create_date BETWEEN  '2020-11-02 00:00:00' AND '2020-11-02 23:30:00'         GROUP BY game_type"# 抓出不同的game_type
    elif type_ == 'bbin_1':# 抓出不同的 status
        sql = "SELECT SEQ_ID ,THIRDLY_USER_ID,THIRDLY_ACCOUNT ,WAGERS_ID ,WAGERS_DATE ,            MODIFIED_DATE, SERIAL_ID ,ROUND_NO, game_type ,WAGER_DETAIL, GAME_CODE,             RESULT,  GROUP_CONCAT(DISTINCT RESULT_TYPE), CARD,            BET_AMOUNT, PAY_OFF,CURRENCY, EXCHANGE_RATE, COMMISSIONABLE, ORIGIN, CREATE_DATE,UPDATE_DATE,            JSON_RESULT,USER_MSG_FLAG ,USER_MSG_DATE  ,GAME_KIND             FROM THIRDLY_BET_RECORD WHERE create_date BETWEEN  '2020-10-31 00:00:00' AND '2020-10-31 18:30:00'             GROUP BY RESULT_TYPE"
    elif type_ == 'bc':
        sql = "SELECT * FROM THIRDLY_BET_RECORD WHERE create_time  > '2020-11-03 00:00:00'"
    elif type_  == 'im':
        sql = "SELECT * FROM THIRDLY_BET_RECORD WHERE create_time  >  '2020-11-03 00:00:00'"
    print(sql)
    global record
    record = {}
    try:
        cur.execute(sql)
    except UnicodeDecodeError as e:
        print(e)
    for index,con in enumerate(cur.fetchall()):
        record[index] = con
    cur.close()


# In[ ]:


thrid_submit(my_con(2,'im'),'im')


# In[ ]:


print(len(record))
record_list = []
for i in record.keys():
    record_list.append(record[i])
print(record_list)


# In[ ]:



def date_time():#給查詢 獎期to_date時間用, 今天時間
    global today_time

    now = datetime.datetime.now()
    year = now.year
    month = now.month
    day = now.day-1
    format_day = '{:02d}'.format(day)
    today_time = '%s-%s-%s'%(year,month,format_day)
def get_conn(env):#連結數據庫 env 0: dev02 , 1:188 ,2: 生產
    if env == 2:
        username = 'rdquery'
        service_name = 'gamenxsXDB'
    else:
        username = 'firefog'
        service_name = ''
    oracle_ = {'password':['LF64qad32gfecxPOJ603','JKoijh785gfrqaX67854','eMxX8B#wktFZ8V'],
    'ip':['10.13.22.161','10.6.1.41','10.6.1.31'],
    'sid':['firefog','game','']}
    conn = cx_Oracle.connect(username,oracle_['password'][env],oracle_['ip'][env]+':1521/'+
    oracle_['sid'][env]+service_name)
    return conn
def select_fundID(conn,user):# 後台活動禮今障變id  用來審核用 ,value 為 人工件單類型, 
    with conn.cursor() as cursor:
        sql = "SELECT id,type_id FROM FUND_MANUAL_DEPOSIT where approve_time is null and         rcv_account = '%s' and apply_time > trunc(sysdate,'mm')         ORDER BY APPLY_TIME DESC"%user
        print(sql)
        cursor.execute(sql)
        rows = cursor.fetchall()
        global fund_id
        fund_id = {}
        for index,cont in enumerate(rows):
            fund_id[index] = cont
    conn.close()
def select_fundCharge(conn,user):# 充值訂單,和狀態
    with conn.cursor() as cursor:
        sql = "select user_customer.account,user_customer.id,fund_charge.SN,fund_charge.DEPOSIT_MODE,         fund_charge.status from fund_charge inner join user_customer on         fund_charge.user_id = user_customer.id where user_customer.account = '%s'         and fund_charge.apply_time > sysdate- 10 and fund_charge.status != 2            order by fund_charge.apply_time desc"%user
        
        cursor.execute(sql)
        rows = cursor.fetchall()
        global fund_charge
        fund_charge = {}
        for index,content in enumerate(rows):
            fund_charge[index] = content
    conn.close()
    
    
def select_tranUser(conn,account,usr_lvl):#查詢轉移用戶 , usr_lvl : 代理等級
    with conn.cursor() as cursor:
        sql = "select account,user_chain from user_customer where account like  '%s' and user_lvl = %s         and joint_venture = 0"%(account,usr_lvl)
        cursor.execute(sql)
        rows = cursor.fetchall()
        global tran_user,user_chain
        tran_user = []
        user_chain = []
        
        for i in rows:
            tran_user.append(i[0])
            user_chain.append(i[1])
    conn.close()
def select_tranChainUser(conn,account,account2):#找尋上級相關用戶 , for代理線轉一代用,不同總代
    with conn.cursor() as cursor:
        sql ="select account from user_customer where user_lvl = 0 and account != '%s'        and account like '%s'"%(account,account2)
        cursor.execute(sql)
        rows = cursor.fetchall()
        global tran_user
        tran_user = []
        
        for i in rows:
            tran_user.append(i[0])
    conn.close()
def select_awardGroupid(conn,lotteryid):#APP開戶連結, 抓出lotteryid 對應出的 award_grop_id
    with conn.cursor() as cursor:
        sql ="select SYS_AWARD_GROUP_ID from GAME_AWARD_USER_GROUP where LOTTERYID = %s         group by SYS_AWARD_GROUP_ID order by sys_award_group_id desc"%lotteryid
        cursor.execute(sql)
        rows = cursor.fetchall()
        global group_id
        group_id = []
        
        for i in rows:
            group_id.append(i[0])
    conn.close()
def select_tranUserStaut(conn,account):#找尋上級相關用戶 , for代理線轉一代用,不同總代
    with conn.cursor() as cursor:
        sql ="select id,ff_flag from user_chain_transfer_log  where account like '%s' order by id desc"%(account)
        cursor.execute(sql)
        rows = cursor.fetchall()
        global ff_flage
        ff_flage = {}
        #print(rows[0])
        ff_flage[rows[0][0]] = rows[0][1]
    conn.close()
    
def select_userid(conn,account_):
    with conn.cursor() as cursor:
        sql = "select id from user_customer where account = '%s'"%account_
        cursor.execute(sql)
        rows = cursor.fetchall()
        userid = []
        for i in rows:
            userid.append(i[0])
        return userid
def select_registerDate(conn,date,account_):
    with conn.cursor() as cursor:
        account_ = account_
        
        sql = "select  trunc(to_date('%s','YYYY-MM-DD')+1) - trunc(register_date) as bron_day from        user_customer where account = '%s'"%(date,account_)# date參數 為  指定選擇日棋
        cursor.execute(sql)
        rows = cursor.fetchall()
        global bron_day
        bron_day = []

        for i in rows:
            bron_day.append(i[0])
    conn.close()
def select_bal(conn,lotteryid):#開獎號
    with conn.cursor() as cursor:
        sql = "select number_record from game_issue where lotteryid = '%s'         and create_time > to_date('2019-01-01','YYYY-MM-DD')"%lotteryid  
        cursor.execute(sql)
        rows = cursor.fetchall()
        global number_record
        number_record = []
        
        for i in rows:
            number_record.append(i[0])
    conn.close()
    
def select_numberRecord(conn,lottery,num):#開獎號
    with conn.cursor() as cursor:
        sql =  "select * from (select number_record,web_issue_code, rank() over         (partition by lotteryid order by sale_start_time desc) as rank_num from game_issue         where lotteryid = %s and number_record is not NULL and  sale_start_time <         sysdate and  sale_start_time >  sysdate - 5) a where rank_num <=  %s"%(FF_().lottery_dict[lottery][1],num)
        print(sql)
        cursor.execute(sql)
        rows = cursor.fetchall()
        global number_record
        number_record = {}
        #print(rows)
        for tuple_ in (rows):
            number_record[tuple_[1]] = tuple_[0]
    conn.close()
def select_test_user(conn,lottery,account=''):# 找出相關用戶
    date_time()
    with conn.cursor() as cursor:
        if lottery =='':# 測試  活動裡今 
            sql_hsieh = "select account from user_customer where parent_id in             ( select id from user_customer where account = '%s') and user_lvl = 1 "%account
        elif lottery == 'benefit':
            query = 'min":1,"max":10'
            sql_hsieh = "select * from agent_contract_setting inner join user_customer on             agent_contract_setting.user_id = user_customer.id ,            (select * from user_customer where account = account) user_agent             where (user_customer.parent_id = user_agent.id or user_customer.id =user_agent.id )"             f"and agent_contract_setting.daily_wage_dynamic_rate like '%{query}%'" 
            #"select account from user_customer where account like '%hsieh%'"
        else:
        #sql_ ="select account from user_customer where register_date > to_date('2015-01-01','YYYY-MM-DD') and is_freeze =0 and user_lvl != 0 and id in (select userid from game_award_user_group where lotteryid = %s and bet_type = 1and userid in (select user_id from fund where bal> 100000000 ))"%(lottery_dict[lottery][1])
            sql_hsieh = "select account from user_customer where  is_freeze =0 and joint_venture=0              and register_date >to_date('2013-01-01','YYYY-MM-DD')             and id in (select userid from game_award_user_group where lotteryid = %s and             bet_type = 1 and userid in             (select user_id from fund where bal> 100000))"%FF_().lottery_dict[lottery][1]
        
        cursor.execute(sql_hsieh)
        rows = cursor.fetchall()
        test_user = []

        for i in rows:
            test_user.append(i[0])
        return test_user
    conn.close()
def update_user(conn):
    with conn.cursor() as cursor:
        for i in test_user:
            sql = "update user_customer set freeze_method = 0 where account = '%s'"%i
            cursor.execute(sql)
            print('%s值行'%i)
        
        conn.commit()
        print('update done')
    conn.close()
    
    
def select_issue(conn,lotteryid):#查詢正在銷售的 期號
    #date_time()
    #today_time = '2019-06-10'#寫死 for預售中
    with conn.cursor() as cursor:
        sql = "select web_issue_code,issue_code from game_issue where lotteryid = '%s'         and sysdate between sale_start_time and sale_end_time"%(lotteryid)
        
        cursor.execute(sql)
        rows = cursor.fetchall()

        global issueName
        global issue
        issueName = []
        issue = []
        if lotteryid in ['99112','99306']:#順利秒彩,順利11選5  不需 講期
            issueName.append('1')
            issue.append('1')
        else:
            for i in rows:# i 生成tuple
                #print(rows)
                issueName.append(i[0])
                issue.append(i[1])

    conn.close()
def select_HistoryIssue(conn,lottery,num):#查詢歷史開獎號碼
    with conn.cursor() as cursor:
        sql = "select web_issue_code,number_record from (select * from game_issue where         lotteryid = %s and sysdate > sale_end_time order by id desc ) where rownum <=%s"%(FF_().lottery_dict[lottery][1],num)
        
        cursor.execute(sql)
        rows = cursor.fetchall()

        global issue_dict
        issue_dict ={}
        if lottery in ['slmmc','sl115']:#順利秒彩,順利11選5  不需 講期
            pass
        else:
            #print(rows)
            for i in rows:# i 生成tuple
                #print(rows)
                issue_dict[i[0]] = i[1]# 旗號: 開講號
                
    conn.close()

def select_userUrl(conn,userid):
    with conn.cursor() as cursor:
        sql = "select url from user_url where url like '%"+ '%s'%(userid) +"%'"
        print(sql)
        cursor.execute(sql)
        rows = cursor.fetchall()
        global user_url
        user_url = []

        for i in rows:
            user_url.append(i[0])
    conn.close()


# In[ ]:



select_test_user(get_conn(1),lottery='',account='kerr000')


# In[ ]:


FF_().Pc_Login(url='dev02',user='hsieh000')


# In[ ]:


FF_().Account_Cookie('kerrwin000')


# In[ ]:


test_user = select_test_user(get_conn(0),lottery='',account='hsieh000')[0:100]
print(len(test_user))


# In[ ]:


test_user


# In[ ]:


def test_benfit(login_user,account):
    Pc_header = FF_().Account_Cookie(login_user)
    Pc_header['Content-Type'] = "application/json; charset=UTF-8"
    print(Pc_header)
    data = {"account":account,"dividendDynamicRate":[{"rate":"10000","max":"300000","activeNumber":"0"},
                {"rate":"20000","min":"300001","max":"600001","activeNumber":"0"}],"dividendStatus":"1"}
    
    FF_().session_post("http://www.dev02.com","/benefit/user/agentContractUpdate",
                      json.dumps(data),Pc_header )
    print(r.text)
for user in test_user:
    print(user)
    test_benfit('hsieh000',user)


# In[ ]:


def bjkl8_Tran_pcdd(issue):# 北京快樂8 轉 PC蛋蛋 號碼
    sum_1 = 0
    sum_2 = 0
    sum_3 = 0
    for index,num in enumerate(issue.split(',')):
        if index in Interval(0,5):
            sum_1 = int(num)+sum_1
        elif index in Interval(6,11):
            sum_2 = int(num)+sum_2
        elif index in Interval(12,17):
            sum_3 = int(num)+sum_3
    return sum_1,sum_2,sum_3
bjkl8_Tran_pcdd('01,02,03,04,05,06,07,08,09,10,11,12,13,14,15,16,17,18,19,20')


# In[ ]:


test_ = {}
for i in range(27):# PC蛋蛋個號碼mapping 顏色 
    if i in [0,13,14,27]:
        number_color = '灰'
    elif i in [1,4,7,10,16,19,22,25]:
        number_color = '綠'
    elif i in [2,5,8,1,11,17,20,23,26]:
        number_color = '藍'
    else:
        number_color = '紅'
    test_[i] = number_color
test_


# In[ ]:


select_numberRecord(get_conn(0),'bjkl8',10)
print(number_record)
for issue  in number_record.keys():
    print(issue)
    print(bjkl8_Tran_pcdd(number_record[issue]))


# In[ ]:


class RedisConnection:
    def __init__(self):
        self.env_connect = {'ip': ['10.13.22.152', '10.6.1.82','127.0.0.1']}  # 0:dev,1:188 ,2: 本地
    def get_rediskey(self,envs):  # env參數 決定是哪個環境
        #redis_dict = {'ip': ['10.13.22.152', '10.6.1.82','127.0.0.1']}  # 0:dev,1:188 ,2: 本地
        pool = redis.ConnectionPool(host=self.env_connect['ip'][envs], port=6379)
        r = redis.Redis(connection_pool=pool)
        return r
    @staticmethod
    def set_key(envs,key_name,key_value):
        r = RedisConnection().get_rediskey(envs)
        json_str = json.dumps(key_value)# 轉成str 存入redis 
        r.set(key_name,json_str)
    @staticmethod
    def get_key(envs,key_name):
        r = RedisConnection().get_rediskey(envs)
        key_ = r.get(key_name)
        if key_ is None:
            return 'not exist'
        else:
            return json.loads(key_)#取出來 byte 轉成 dict
    @staticmethod
    def get_token(envs, user):#查詢用戶 APP token 時間
        r = RedisConnection().get_rediskey(envs)
        r_keys = (r.keys('USER_TOKEN_%s*' % re.findall(r'[0-9]+|[a-z]+', user)[0]))
        for i in r_keys:
            if user in str(i):
                user_keys = (str(i).replace("'", '')[1:])
        print(user_keys)
        user_dict = r.get(user_keys)
        timestap = str(user_dict).split('timeOut')[1].split('"token"')[0][2:-4]  #時間戳
        token_time = time.localtime(int(timestap))#到期時間
        print('token到期時間: %s-%s-%s %s:%s:%s' % (token_time.tm_year, token_time.tm_mon, token_time.tm_mday,
                                                token_time.tm_hour, token_time.tm_min, token_time.tm_sec))
RedisConnection.get_key(envs=2,key_name="1/1:2020/9")


# In[ ]:




def em_post(account,lottery,post_data):#共用 彩種 em開頭  session post方式
    global r
    header={
        'User-Agent': userAgent,
        'Cookie': 'ANVOID='+cookies_[account], 
        #+';ActivitySSID=o4dd8gr758r68q1jqr6vc5bma5'()  活動系統
        #'Content-Type': 'application/json; charset=UTF-8', 
        'Accept':  'application/json, text/javascript, */*; q=0.01',
            }

     # em_url : em開頭網域, post_url : www2開頭或www
    try:
        r = session.post(em_url+'/gameBet/%s/submit'%lottery,headers=header,data=json.dumps(post_data))
        
        print(r.json()['msg'])
        print(r.json()['data']['projectId'])
        global orderid
            
        orderid = (r.json()['data']['orderId'])
        print('result: '+str(r.status_code)+"\n"+'---------------------')

    except requests.exceptions.ConnectionError:
        print('連線有問題,請稍等')
    

#共用 session post方式, data參數可帶可不帶, 為post提交出去的data內容 
#data_type 可帶可不帶, 帶了在用是 dump或者load,或者不用
def session_post(account,url,data_type='',*data):
    header={
        'User-Agent': userAgent,
        'Cookie': 'ANVOID='+cookies_[account],
        #'Content-Type':'application/json; charset=UTF-8'
     } 
    #+';ActivitySSID=o4dd8gr758r68q1jqr6vc5bma5'()  活動系統
    #Content-Type': 'application/json; charset=UTF-8',#第三方轉入 需帶 
    #Accept':  'application/json, text/javascript, */*; q=0.01',
    #header 改為各街口去呼叫
    
    global r
    if data == (): #帶入空的的data
        datas = ''
    else:        
        if data_type  == '':
            datas = data[0]
            print(datas)
        elif data_type == 'loads':
            datas = json.loads(data[0])
        elif data_type  == 'dumps':
                datas = json.dumps(data[0])#因為參數為不限置數量的*data, 所以會產生tuple,在用[0]來取出
    
 # em_url : em開頭網域, post_url : www2開頭或www

    try:
        header['Content-Type'] = 'application/json; charset=UTF-8'
        r = session.post(post_url+url,headers=header,data=datas)
        #balance = r.json()['balance']
        if r.status_code  ==  200:
            html = BeautifulSoup(r.text,'lxml')
            #title = html.title

            #print(title)
            print(r.json())
            print('result: '+str(r.status_code)+"\n"+'---------------------')
        else:  #針對 status_code 去判斷 .第三方多增加content_type 來寫, 活動抽獎 不需此conten-type
            #header['Content-Type'] = 'application/json; charset=UTF-8'
            r = session.post(post_url+url,headers=header,data=datas)

            #print(r.json())
            print('result: '+str(r.status_code)+"\n"+'---------------------')
    except requests.exceptions.ConnectionError:
        print('連線有問題,請稍等')
def session_get(account,url):#共用 session get方式
    
    header={
    'User-Agent': userAgent,
    'Cookie': 'ANVOID='+cookies_[account],
        #活動系統  +';ANVOAID=j9mh8f60fttqc86ck80k2lb6j3'
   # 'Content-Type': 'application/json; charset=UTF-8', 
    'Accept':  'application/json, text/javascript, */*; q=0.01',
    'X-Requested-With': 'XMLHttpRequest',
    #'Referer' : 'http://www.dev02.com/transfer/thirdlytransfer'
    
        }

    try:
        r = session.get(post_url+url,headers=header)
        html = BeautifulSoup(r.text,'lxml')
        #third_balance = r.json()['balance']
        print(r.status_code)
        #print('餘額為: %s'%third_balance)# third_balance 餘額查詢 用
        #print('result: '+str(r.status_code)+"\n"+'---------------------')
        
    except requests.exceptions.ConnectionError:
        print('連線有問題,請稍等')



# In[ ]:


def get_userbal(account):#查詢第三方餘額皆口
    header={
    'User-Agent': userAgent,
    'Cookie': 'ANVOID='+cookies_[account], 
    #+';ActivitySSID=o4dd8gr758r68q1jqr6vc5bma5'()  活動系統
    #'Content-Type': 'application/json; charset=UTF-8', 
    'Accept':  'application/json, text/javascript, */*; q=0.01'
    }

 # em_url : em開頭網域, post_url : www2開頭或www
    try:
        r = session.post(post_url+'/index/getuserbal',headers=header)
        print(r.text)

    except requests.exceptions.ConnectionError:
        print('連線有問題,請稍等')
for i in cookies_.keys():
    get_userbal(i)


# In[ ]:



def cancel_submit(account,lottery):#投注在撤銷
    #select_issue(get_conn(envs),lottery_dict[lottery][1])
    ball = [str(random.randint(0,9)) for i in range(3)]
    #print(ball)
    ball_submit = ",".join(ball)
    print("投注內容: %s"%ball_submit)
    post_data ={"gameType":"n3d","isTrace":1,"traceWinStop":1,"traceStopValue":1,"balls":[{"id":1,"ball":"0,2,0","type":"sanxing.zhixuan.fushi","moneyunit":"0.1","multiple":1,"awardMode":1,"num":1}],"orders":[{"number":"2020132","issueCode":20200511124001,"multiple":11111}],"amount":"2222.20"}
    em_post(account,lottery,post_data)
    header={
        'User-Agent': userAgent,
        'Cookie': 'ANVOID='+cookies_[account], 
        #+';ActivitySSID=o4dd8gr758r68q1jqr6vc5bma5'()  活動系統
        #'Content-Type': 'application/json; charset=UTF-8', 
        'Accept':  'application/json, text/javascript, */*; q=0.01',
            }
    r = session.post(em_url+'/gameUserCenter/cancelOrder?orderId=%s'%orderid,headers=header)#撤銷皆口
    
for i in range(1):
    cancel_submit(user,'n3d')


# In[ ]:


def cancel_order(account,orderid):#撤銷皆口

    header={
    'User-Agent': userAgent,
    'Cookie': 'ANVOID='+cookies_[account], 
    #+';ActivitySSID=o4dd8gr758r68q1jqr6vc5bma5'()  活動系統
    #'Content-Type': 'application/json; charset=UTF-8', 
    'Accept':  'application/json, text/javascript, */*; q=0.01',
        }

    r = session.post(em_url+'/gameUserCenter/cancelOrder?orderId=%s'%orderid,headers=header)
    print(r.text)


# In[ ]:



def game_get(account,lottery):
    header  = {
        'User-Agent': userAgent,
        'Cookie': 'ANVOID='+cookies_[account]
    }
    r = session.get(em_url+'/gameBet/%s'%lottery,headers=header)
    html = BeautifulSoup(r.text,'lxml')
    print(r.status_code)
    print(html.title)

def third_home(account,third):
    #登入第三方頁面,創立帳號

    if third == 'sb':#沙巴特立
        url = '/shaba/home?act=esports'
    else:
        url = '/%s/home'%third
    session_get(account,url)

def third_transferin(account,url,amount,data_type='dumps'):#第三方轉入
    
    post_data = {"amount":amount}
    url = '/%s/transferToThirdly'%url
    session_post(account,url,data_type,post_data)


def third_transferout(account,url,amount,data_type='dumps'):#第三方喘出
    post_data = {"amount":amount}
    url = '/%s/transferToFF'%url#轉到4.0 url 規則 是一致, 可以不用和轉入寫if else
    session_post(account,url,data_type,post_data)

    
    
def third_balance(account,third):#第三方餘額
    #session_get(user,'/transfer/thirdlytransfer')
    header  = {
        'User-Agent': userAgent,
        'Cookie': 'ANVOID='+cookies_[account]
    }
    if third == 'gns':
        third_url = '/gns/gnsBalance'
    else:
        third_url = '/%s/thirdlyBalance'%third 
    r = session.post(post_url+third_url,headers=header)
    print('%s 餘額: %s'%(third,r.json()['balance']))
def ff_balance(account):
    header  = {
        'User-Agent': userAgent,
        'Cookie': 'ANVOID='+cookies_[account]
    }
    r = session.post(post_url+'/index/getuserbal',headers=header)
    print(r.json()['data'])
    
    
    
    
def third_Autoff(account):# 一鍵轉回 4.0
    session_post(account,'/thirdlyAutoTrans/transferAllToFF')# 一鍵轉回
def third_Autothird(account,third):#免轉第三方
    session_post(account,'/%s/user/checkThirdlyPlatStatus'%third)
def transfer_auto(account,type_):# 免轉開關
    header  = {
        'User-Agent': userAgent,
        'Cookie': 'ANVOID='+cookies_[account]
    }
    if type_ == 'on':
        num = '1'
    elif type_ == 'off':
        num  = '0'
    else:
        num = '1'
    datas = {
        'autoTransFlag':num
    }
    r = session.post(post_url+'/transfer/autotransflag',headers=header,data=datas)
    print(r.json())

#充值
def fund(user):
    Pc_header =FF_().Account_Cookie(user)
    FF_().session_get(post_url,'/fund','',Pc_header)

def fund_type(user,type_):
    Pc_header =FF_().Account_Cookie(user)
    url = '/fund/index?type='+  str(type_)
    FF_().session_get(post_url,url ,'',Pc_header)


def fund_confirm(user,type_,amount):#充值卻任
    if type_ == 12:# usdt
        payload_dict = {'currency':'USDT','type':'12','status':'USDT','chargeamount':'31.00',
                        'exchangeRate':'6.67','originalCurrencyAmount': '4.64'}
    else:
        payload_dict = {'type':type_,'status':'UPYQR','chargeamount':'%s.00'%amount}#UPYQR: 銀聯掃碼. type:8
    Pc_header =FF_().Account_Cookie(user) 
    FF_().session_post(post_url,'/fund/confirm' ,payload_dict,Pc_header)
    html = BeautifulSoup(r.text,'lxml')
    print(html.title)


            


# In[ ]:


for i in range(10):
    FF_().Pc_Login(url='joy188',user='kerr0%s'%i)


# In[ ]:


account


# In[ ]:


FF_.cookies


# In[ ]:


for i in range(3):
    print(i)
    for user in FF_.cookies.keys():
        print(user)
        fund(user)
        fund_type(user,type_=12)
        fund_confirm(user,type_=12,amount=31)
        print('ok')


# In[ ]:


user = 'kerr02'
fund(user)
fund_type(user,type_=12)
fund_confirm(user,type_=12,amount=31)


# In[ ]:


for i in test_user[72:]:
    print(i)
    Login('joy188.195353',i,'Pc')
    fund(i)
    fund_type(i,8)#8銀聯掃馬
    fund_confirm(i)


# In[ ]:


timestap = '1607322014000'
(time.localtime(int(timestap)/1000))


# In[ ]:


def get_rediskey(envs):#env參數 決定是哪個環境
    redis_dict = {'ip':['10.13.22.152','10.6.1.82','127.0.0.1']}#0:dev,1:188 ,2 本基
    global r
    pool = redis.ConnectionPool(host = redis_dict['ip'][envs],port = 6379)
    r = redis.Redis(connection_pool=pool)

def get_token(envs,user):
    get_rediskey(envs)
    global redis_
    redis_ = r_keys = (r.keys('USER_TOKEN_%s*'%re.findall(r'[0-9]+|[a-z]+',user)[0]))
    for i in r_keys:
        if user in str(i):
            user_keys = (str(i).replace("'",'')[1:])

    user_dict = (r.get(user_keys))
    timestap = (str(user_dict).split('timeOut')[1].split('"token"')[0][2:-4])#
    token_time = (time.localtime(int(timestap)))#時間戳 換成  日期顯示用法
    print(token_time)
    print('token到期時間: %s-%s-%s %s:%s:%s'%(token_time.tm_year,token_time.tm_mon,token_time.tm_mday,
                                         token_time.tm_hour,token_time.tm_min,token_time.tm_sec))
    #print(timestap)
#get_rediskey(0)
def user_ChargeLimit(env,user): # 查詢用戶充值限制次數
    get_rediskey(env)
    select_userid(get_conn(env),user)
                  
    r_keys = 'userChargeList%s'%userid[0]
    print(r_keys)
    try:
        user_fund = r.get(r_keys).decode() #bytes 轉str
        #print(user_fund)
    except:
        return"充值次數0" 
    r_list  = json.loads(user_fund)# 變成一個List
    #print(r_list)
    len_r = len(r_list)# redis 用戶充值次數, 用來判斷 目前 是被鎖在哪個位置        
    select_fundCharge(get_conn(env),user)# 充值明細表查詢
    #print(fund_charge)# DB 
    chargeway_list = []#紀錄用戶充值平台
    for fund,index in zip(r_list,sorted(fund_charge.keys())):
        chargeway_list.append([fund['chargeWaySet'],fund_charge[index][2]])
    print(chargeway_list)
    mul_times = cal_three([i[0] for i in chargeway_list][0:4])# 判斷連續次數[a[0][0] for i in a][0:4]
    print(mul_times)
    if mul_times[0] == 3:# [0,0,0] ,前面三次重複, 第四次開始被鎖 ,所以開始鎖定次數 都需  -2
        del_time = 2
        print("第1,2,3 同充值方式,第四次開始鎖定倒數")
    elif mul_times[1] == 3:# [1,0,0,0],第5 次開始被鎖, 所有次數 -1
        del_time = 1
        print("第2,3,4 同充值方式第五次開始鎖定倒數")
    else:# 正常流程 沒有重複
        print('前面無相同充值方式,走正常流程')
        del_time = 0
    len_r = len_r + del_time # 實際總長度
    if len_r == 13:
        msg = '目前被鎖1天'
    elif len_r == 11:
        msg = '目前鎖定1小'
    elif len_r == 9:
        msg = '目前鎖定五分鐘'
    elif len_r == 6:
        msg = '目前鎖定1分鐘'
    elif len_r in [12,10,8,7]:
        if len_r == 7:
             msg = "還能在發起2次"
        else:
            msg = "還能在發起1次"
    else:
        msg = "還未被鎖定"
    print("充值次數: %s, %s"%(len_r,msg))
#user_ChargeLimit(1,'kerr001')    





# In[ ]:


get_rediskey(2)


# In[ ]:



test_dict = {'1':2}
json_str = json.dumps(test_dict)
r.set('test',json_str)


# In[ ]:


redis_val = r.get('test')
print(type(redis_val),redis_val)
a = json.loads(redis_val)
print(type(a))


# In[ ]:



def cal_three(a):# 長度4個列表裡, 連續三的 組合,# 只有兩種  重複三次組合 ,前三重複, 後三重複
    if len(a) < 4: #最短第四次才會開始鎖定
        return "pass"# 不用駔下面邏輯
    last_word = None
    word_list = []
    for word in a:
        if word!= last_word:
            word_list.append([word,1])
            last_word = word
        else:
            word_list[-1][1] +=1
    #print(word_list)
    three_1 = word_list[0][1]
    if three_1 == 4:# 前面四個長度一樣, three_2 就沒有這組和ㄌ
        return (three_1-1,0)# 也當作前面三次重複
    three_2 = word_list[1][1]
    #print(three_1,three_2)
    return three_1,three_2

cal_three([0,0,0,0])


# In[ ]:


a = 14.749516
int(a *100)/100


# In[ ]:


timeStamp = 1606721539000/1000
timeArray = time.localtime(timeStamp)
otherStyleTime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
print(otherStyleTime)


# In[ ]:



#測試走勢圖 
def test_chart(account):
    header['Cookie'] = 'ANVOID='+cookies_[account]
    my_params =  {"periodsType":'periods',"gameType":'v3d',"gameMethod":'Qiansan',
                 "periodsNum":'50'
                 }
    
    #'/game/chart/v3d/Qiansan/data?periodsType=periods\&gameType=v3d&gameMethod=Qiansan&periodsNum=50'
    
    r = session.get(em_url+'/game/chart/v3d/Qiansan/data?' ,
    headers=header,params =my_params)
    
    print(r.json()['isSuccess'])
test_chart(user)

