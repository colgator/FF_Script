#!/usr/bin/env python
# coding: utf-8

# In[1]:


#-*- coding: utf-8 -*-
import HTMLTestRunner,unittest,requests,hashlib,time,random,cx_Oracle,json
from bs4 import BeautifulSoup
import unittest
import datetime
from time import sleep
from selenium import webdriver
from faker import Factory
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import WebDriverException 
import os 
import MySQLdb
import threading
from collections import defaultdict


# In[184]:


fake = Factory.create()

card = (fake.credit_card_number(card_type='visa16'))#產生一個16位的假卡號
print(card)


# In[151]:



lottery_dict = {
'cqssc':[u'重慶','99101'],'xjssc':[u'新彊時彩','99103'],'tjssc':[u'天津時彩','99104'],
'hljssc':[u'黑龍江','99105'],'llssc':[u'樂利時彩','99106'],'shssl':[u'上海時彩','99107'],
'jlffc':[u'吉利分彩','99111'],'slmmc':[u'順利秒彩','99112'],'txffc':[u'騰訊分彩','99114'],
'btcffc':[u'比特幣分彩','99115'],'fhjlssc':[u'吉利時彩','99116'],
'sd115':[u'山東11選5','99301'],'jx115':[u"江西11選5",'99302'],
'gd115':[u'廣東11選5','99303'],'sl115':[u'順利11選5','99306'],'jsk3':[u'江蘇快3','99501'],
'ahk3':[u'安徽快3','99502'],'jsdice':[u'江蘇骰寶','99601'],'jldice1':[u'吉利骰寶(娛樂)','99602'],
'jldice2':[u'吉利骰寶(至尊)','99603'],'fc3d':[u'3D','99108'],'p5':[u'排列5','99109'],
'lhc':[u'六合彩','99701'],'btcctp':[u'快開','99901'],'pk10':[u"pk10",'99202'],'v3d':[u'吉利3D','99801'],
'xyft':[u'幸運飛艇','99203'],'fhxjc':[u'鳳凰新疆','99118'],'fhcqc':[u'鳳凰重慶','99117'],
'n3d':[u'越南3d','99124'],'np3':[u'越南福利彩','99123'],'pcdd':[u'PC蛋蛋','99204'],
    'xyft168':[u'幸運飛艇168','99205'], 'fckl8':[u'福彩快樂8','99206'],'ptxffc':[u'奇趣腾讯分分彩','99125']
            ,'hn60':[u'多彩河内分分彩','99126'],'hnffc':[u'河内分分彩','99119'],'hn5fc':[u'河内五分彩'
            ,'99120']}
lottery_sh = ['cqssc','xjssc','tjssc','hljssc','llssc','jlffc','slmmc','txffc',
            'fhjlssc','btcffc','fhcqc','fhxjc','hnffc','hn5fc','hn60','ptxffc']
lottery_3d = ['v3d']
lottery_115 = ['sd115','jx115','gd115','sl115']
lottery_k3 = ['ahk3','jsk3']
lottery_sb = ['jsdice',"jldice1",'jldice2']
lottery_fun = ['pk10','xyft','xyft168']
lottery_noRed = ['fc3d','n3d','np3','p5']#沒有紅包
third_list = ['gns','shaba','im','ky','lc','city','bg','yb','pg']
cancel_lottery_list = ['cqssc','xjssc','tjssc','hljssc','fhjlssc','xyft','pk10','fc3d',
                 'p5','n3d','np3']# 撤消彩種
env_dict = {
    '測試總代': ['hsieh00','kerr00'] ,'一般帳號': ['hsieh001','kerr001'],
    '合營1940': ['hsiehwin1940test','kerrwin1940test'],
    '轉入/轉出':['hsiehthird001','kerrthird001'],
    'APP帳號': ['hsiehapp001','kerrapp001'],
    '玩家':['hsieh0620','kerr010']
}

class Joy188Test(unittest.TestCase):
    u"trunk接口測試"

    @staticmethod
    def md(password,param):
        m = hashlib.md5()
        m.update(password)
        sr = m.hexdigest()
        for i in range(3):
            sr= hashlib.md5(sr.encode()).hexdigest()
        rx = hashlib.md5(sr.encode()+param).hexdigest()
        return rx
    @staticmethod
    def admin_login():
        global admin_cookie,admin_url,admin_header,admin_session
        admin_cookie = {}
        admin_dict = {0:'http://admin.dev02.com',1:'http://admin.joy188.com'}
        admin_url = admin_dict[envs] 
        admin_session = requests.Session()
        admin_header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.100 Safari/537.36',
                  'Content-Type': 'application/x-www-form-urlencoded'}
        admin_data = {'username':'cancus','password':  pass_list[envs],'bindpwd':123456}
        r = admin_session.post(admin_url+'/admin/login/login',data=admin_data,headers=admin_header)
        if r.json()['isSuccess'] ==1:# 這邊如果登入失敗, 正常會爆錯 ,因為沒有 r.json()
            print('後台登入成功')
        else:
            print('後台登入失敗')
        global cookies
        cookies = r.cookies.get_dict()#獲得登入的cookies 字典
        admin_header['ANVOAID'] =  cookies['ANVOAID'] 
    @staticmethod
    def test_Login():
        u"登入測試"
        global user#傳給webdriver方法 當登入用戶參數
        global  pass_list#傳入 werbdriver登入的密碼 
        global post_url#非em開頭
        global em_url#em開頭 
        global userAgent
        global Pc_header
        #global envs#回傳redis 或 sql 環境變數   ,dev :0, 188:1
        global cookies_
        cookies_ = {}
        url_dict = {0:['http://www.dev02.com','http://em.dev02.com'],
                    1:['http://www2.joy188.com','http://em.joy188.com']}
        post_url  = url_dict[envs][0]
        em_url = url_dict[envs][1]
        pass_list = {0: b'123qwe',1:b'amberrd'}


        account_ ={0: {
                'dev02': [{'hsieh000':u'總代','hsieh001':u'一代','hsiehthird001':'一代'},'一般4.0'],
                'fh82dev02': [{'hsiehwin000':u'總代','hsiehwin001':u'一代','hsiehwin1940test':'合營1940'
                              },'一般合營']
        } ,1:{
               'joy188.teny2020':[{'kerrwin000':u'總代','kerrwin001':u'一代'},'合營teny'],
               'joy188.195353':[{'kerrwin1940test':u'合營1940'},'一般合營'],
               'joy188.88hlqp':[{'hlqp001':u'總代','kerrlc001':u'玩家'},'歡樂棋牌'],
                'joy188':[{'kerr000':u'總代','kerr001':u'一代','kerr43453':u'玩家',
                'kerrthird001':'二代'},'一般4.0']}
                  }#各環境 的用戶 登入
        userAgent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.100 Safari/537.36"     
        
        Pc_header = {
            'User-Agent': userAgent 
        }
        global session
        while True:
            try:
                for e in account_[envs].keys():# e為環境
                    print(e,account_[envs][e][1])#環境和名稱 
                    for user,username in account_[envs][e][0].items():# account_[e] 為環境key 的values , 在loop 找出user名
                        postData = {
                            "username": user,
                            "password": Joy188Test.md(pass_list[envs],b'f4a30481422765de945833d10352ea18'),#密碼和param直
                            "param" :b'f4a30481422765de945833d10352ea18'
                        }
                        session = requests.Session()
                        if envs == 0:# dev 環境
                            login_url = "http://www.%s.com"%e
                        else:
                            login_url = 'http://www2.%s.com'%e
                        r = session.post(  login_url +'/login/login',data = postData,
                                headers = Pc_header )
                        cookies = r.cookies.get_dict()#獲得登入的cookies 字典
                        cookies_.setdefault(user,cookies['ANVOID'])
                        t = time.strftime('%Y%m%d %H:%M:%S')
                        print(u'登錄帳號: %s,登入身分: %s'%(user,username)+u',現在時間:'+t)
                        print(r.text)
                Joy188Test.admin_login()
                break
            except requests.exceptions.ConnectionError:
                print('please wait!')
                break

            except IOError:
                print('please wait!!!')
                break
    @staticmethod
    def web_issuecode(lottery):#頁面產生  獎期用法,  取代DB連線問題
        global issuecode
        now_time = int(time.time())
        Pc_header['Cookie']= 'ANVOID='+cookies_[env_dict['一般帳號'][envs]]
        try:
            if lottery == 'lhc':
                r = session.get(em_url+'/gameBet/lhc/dynamicConfig?_=%s'%(now_time),headers=Pc_header)
                issuecode = r.json()['data']['issueCode']
            else:
                r = session.get(em_url+'/gameBet/%s/lastNumber?_=%s'%(lottery,now_time),
                                headers=Pc_header)
                issuecode = r.json()['issueCode']
        except :
            print("%s採種沒抓到 獎號"%lottery)

        #print(issuecode)
    
    @staticmethod
    def date_time():#給查詢 獎期to_date時間用, 今天時間
        global today_time
        
        now = datetime.datetime.now()
        year = now.year
        month = now.month
        day = now.day
        format_day = '{:02d}'.format(day)
        today_time = '%s-%s-%s'%(year,month,format_day)
        

    @staticmethod
    def get_conn(env):#連結數據庫 env 0: dev02 , 1:188
        oracle_ = {'password':['LF64qad32gfecxPOJ603','JKoijh785gfrqaX67854'],
        'ip':['10.13.22.161','10.6.1.41'],'name':['firefog','game']}
        conn = cx_Oracle.connect('firefog',oracle_['password'][env],oracle_['ip'][env]+
        ':1521/'+oracle_['name'][env])
        return conn
    @staticmethod
    def select_issue(conn,lotteryid):#查詢正在銷售的 期號
        #Joy188Test.date_time()
        #today_time = '2019-06-10'#for 預售中 ,抓當天時間來比對,會沒獎期
        try:
            with conn.cursor() as cursor:
                #sql = "select web_issue_code,issue_code from game_issue where lotteryid = '%s' and sysdate between sale_start_time and sale_end_time"%(lotteryid)
                
                # 休市查詢槳期用
                sql = "select web_issue_code,issue_code from game_issue where lotteryid = '%s' and sysdate < sale_end_time"%lotteryid
                cursor.execute(sql)
                rows = cursor.fetchall()

                global issueName
                global issue
                issueName = []
                issue = []
                if lotteryid in ['99112','99306']:#順利秒彩,順利11選5  不需 講期. 隨便塞
                    issueName.append('1')
                    issue.append('1')
                else:
                    for i in rows:# i 生成tuple
                        issueName.append(i[0])
                        issue.append(i[1])
            conn.close()
        except:
            pass
    @staticmethod
    def select_FundSn(conn,userid):# 找充值單號
        with conn.cursor() as cursor:
            
            sql = "select sn from fund_charge where apply_time >= to_date(trunc(sysdate,'DD'))              and USER_ID = %s order by apply_time desc"%userid
            cursor.execute(sql)
            rows = cursor.fetchall()
            fund_sn = []
            for i in rows:
                fund_sn.append(i[0])
            return fund_sn[0]
    @staticmethod
    def select_WithDrawSn(conn,userid):# 找提現單號
        with conn.cursor() as cursor:
            sql = "select sn from FUND_WITHDRAW where apply_time >= to_date(trunc(sysdate,'DD'))              and USER_ID = %s order by apply_time desc"%userid
            cursor.execute(sql)
            rows = cursor.fetchall()
            withdraw_sn = []
            for i in rows:
                withdraw_sn.append(i[0])
            return withdraw_sn[0]
    @staticmethod
    def select_Lockid(conn,account):# 查詢綁卡鎖定id, 用來 鎖卡用
        with conn.cursor() as cursor:
            sql = "select ID from USER_BANK_LOCKED where user_id = (select id from user_customer             where account = '%s')"%account
            cursor.execute(sql)
            rows = cursor.fetchall()
            lockid = []
            for i in rows:
                lockid.append(i[0])
            return lockid
    
    
    @staticmethod
    def select_betTypeCode(conn,lotteryid,game_type):#從game_type 去對應玩法的數字,給app投注使用
        with conn.cursor() as cursor:
            sql = "select bet_type_code from game_bettype_status where lotteryid = '%s' and group_code_name||set_code_name||method_code_name = '%s'"%(lotteryid,game_type)
            
            cursor.execute(sql)
            rows = cursor.fetchall()

            global bet_type
            bet_type = []
            for i in rows:# i 生成tuple
                bet_type.append(i[0])
        conn.close()
    @staticmethod
    def select_orderCode(conn,orderid):# 從iapi投注的orderid對應出 order_code 方案編號
        with conn.cursor() as cursor:
            sql = "select order_code from game_order where id in (select orderid from game_slip where orderid = '%s')"%orderid
            
            cursor.execute(sql)
            rows = cursor.fetchall()

            global order_code 
            order_code = []
            for i in rows:# i 生成tuple
                order_code.append(i[0])
        conn.close()
    @staticmethod
    def select_PlanCode(conn,lotteryid,account):#找追號單號
        with conn.cursor() as cursor:
            sql = f"select game_plan.plan_code from game_package  inner join game_plan "            f"on game_package.id = game_plan.PACKAGE_ID "            f"where game_package.userid = (select id from user_customer "            f"where account = '{account}') and game_package.LOTTERYID = {lotteryid} "            f"and game_package.sale_time > to_date(trunc(sysdate,'DD')) "            f"order by game_package.sale_time desc "
            #print(sql)
            cursor.execute(sql)
            rows = cursor.fetchall()
            plan_code = []
            for i in rows:
                plan_code.append(i[0])
            #conn.close()
            return plan_code[0]
            
        
            
    @staticmethod
    def select_PcOredrCode(conn,user,lottery):#webdriver頁面投注產生定單
        Joy188Test.date_time()#先產生今天日期
        with conn.cursor() as cursor:
            sql = "select order_code from game_order where userid in (select id from user_customer where account = '%s' and order_time > to_date('%s','YYYY-MM-DD')and lotteryid = %s)"%(user,today_time,lottery_dict[lottery][1])
            cursor.execute(sql)
            rows = cursor.fetchall()

            global order_code 
            order_code = []
            for i in rows:# i 生成tuple
                order_code.append(i[0])
        conn.close()
    @staticmethod
    def select_RedBal(conn,user):
        with conn.cursor() as cursor:
            sql = "SELECT bal FROM RED_ENVELOPE WHERE             USER_ID = (SELECT id FROM USER_CUSTOMER WHERE account ='%s')"%user
            cursor.execute(sql)
            rows = cursor.fetchall()

            global red_bal
            red_bal = []
            for i in rows:# i 生成tuple
                red_bal.append(i[0])
        conn.close()
    @staticmethod
    def select_RedID(conn,user):#紅包加壁  的訂單號查詢 ,用來審核用
        with conn.cursor() as cursor:
            sql = "SELECT ID FROM RED_ENVELOPE_LIST WHERE status=1 and             USER_ID = (SELECT id FROM USER_CUSTOMER WHERE account ='%s')"%user
            cursor.execute(sql)
            rows = cursor.fetchall()

            global red_id
            red_id = []
            for i in rows:# i 生成tuple
                red_id.append(i[0])
        conn.close()
    @staticmethod
    #查詢轉移用戶 , usr_lvl : 代理等級 , top_account 總代
    def select_tranUser(conn,joint='0',type_=""):
        account_tran = {
            0:['%hsieh%','hsieh001','hsieh00'],
            1:['%kerr%','kerr000','kerr00']
        }
        with conn.cursor() as cursor:
            if type_ == "":# 預設 
                sql = "select account,user_chain from user_customer where account like  '%s'                 and joint_venture = %s and parent_id = (select id from user_customer where                 account='%s')                 order by register_date desc"%(account_tran[envs][0],joint,account_tran[envs][1])
            else:#  帶 type_ 不等於 "" . 用意 找出  指定一代 ,上級 為kerr00 
                sql = "select account,user_chain from user_customer where account like  '%s'                 and joint_venture = %s and parent_id = (select id from user_customer where                 account = '%s')                 order by register_date desc"%(account_tran[envs][0],joint,account_tran[envs][2])
            #print(sql)
            cursor.execute(sql)
            rows = cursor.fetchall()
            global tran_user,user_chain
            tran_user = []
            user_chain = []

            for i in rows:
                tran_user.append(i[0])
                user_chain.append(i[1])
        conn.close()
    @staticmethod
    def select_tranChainUser(conn,account,account2,joint=0,user_lvl=0):#找尋上級相關用戶 , for代理線轉一代用,不同總代
        with conn.cursor() as cursor:
            sql ="select account from user_customer where user_lvl = %s and account != '%s'            and joint_venture = %s and account like '%s'"%(user_lvl,account,joint,account2)
            #print(sql)
            cursor.execute(sql)
            rows = cursor.fetchall()
            global tran_user
            tran_user = []

            for i in rows:
                tran_user.append(i[0])
        conn.close()
    @staticmethod
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
    @staticmethod
    def select_userPass(conn,account):#找尋用戶密碼 ,給APP皆口用
        with conn.cursor() as cursor:
            sql ="select passwd from user_customer where account = '%s'"%account
            cursor.execute(sql)
            rows = cursor.fetchall()
            global password
            password = []
            #print(rows[0])
            for i in rows:
                password.append(i[0])
        conn.close()

    @staticmethod    
    def my_con(evn,third):#第三方  mysql連線
        third_dict = {'lc':['lcadmin',['cA28yF#K=yx*RPHC','XyH]#xk76xY6e+bV'],'ff_lc'],
            'ky':['kyadmin',['ALtfN#F7Zj%AxXgs=dT9','kdT4W3#dEug3$pMM#z7q'],'ff_ky'],
            'city':['761cityadmin',['KDpTqUeRH7s-s#D*7]mY','bE%ytPX$5nU3c9#d'],'ff_761city'],
            'im':['imadmin',['D97W#$gdh=b39jZ7Px','nxDe2yt7XyuZ@CcNSE'],'ff_im'],
            'shaba':['sbadmin',['UHRkbvu[2%N=5U*#P3JR','aR8(W294XV5KQ!Zf#"v9'],'ff_sb'],
            'bbin':['bbinadmin','Csyh*P#jB3y}EyLxtg','ff_bbin'],
            'gns':['gnsadmin','Gryd#aCPWCkT$F4pmn','ff_gns'],
            'yb':['ybadmin',['HseSdD2yf!^F32cR3f','aD5cWpMr%BdX#9t7mdBwr$tSjzvM'],'ff_yb'],
            'bg':['bgadmin',['fxWqpKnRm#ArxPhzm','vmFw8N!#hVkAHMdwZY'],'ff_bg'],
            'pg':['pgadmin',['pfW95$XvAYuS#dUntk','zWHvPpekr#rnbV#qwp'],'ff_pg']
             }  

        user_ =  third_dict[third][0]
        db_ = third_dict[third][2]

        if third == 'gns':#gns只有一個 測試環境
            passwd_ = third_dict[third][1]
            ip = '10.6.32.147'
        else:
            if evn == 0:#dev
                ip = '10.13.22.151'
            elif evn == 1:#188
                ip = '10.6.32.147'
            else:
                print('evn 錯誤')
            passwd_ = third_dict[third][1][evn] 
        
        db = MySQLdb.connect(
        host = ip,
        user = user_,
        passwd = passwd_,
        db = db_)
        return db

    @staticmethod
    def thirdly_tran(db,tran_type,third,user):
        cur = db.cursor()
        if  third  == 'gns':
            table_name = 'GNS_TRANSCATION_LOG'
            if tran_type == 0:
                trans_name = 'FIREFROG_TO_GNS'
            else:
                trans_name = 'GNS_TO_FIREFROG'
        else:
            table_name = 'THIRDLY_TRANSCATION_LOG'
            if tran_type == 0:#轉入
                trans_name = 'FIREFROG_TO_THIRDLY'
            else:#轉出
                trans_name = 'THIRDLY_TO_FIREFROG'
        sql ="SELECT SN,STATUS FROM %s WHERE FF_ACCOUNT = '%s'        AND CREATE_DATE > DATE(NOW()) AND TRANS_NAME= '%s'        order by CREATE_DATE desc"%(table_name,user,trans_name)
        #print(sql)
        thirdly_dict = {}#轉帳單號 key 和 狀態
        cur.execute(sql)
        for index,row in enumerate(cur.fetchall()):
            thirdly_dict[index] = list(row)
        cur.close()
        return thirdly_dict

    @staticmethod
    def random_mul(num):#生成random數, NUM參數為範圍
        return(random.randint(1,num))
    
    @staticmethod
    def plan_num(envs,lottery,plan_len):#追號生成
        plan_ = []#存放 多少 長度追號的 list
        Joy188Test.select_issue(Joy188Test.get_conn(envs),lottery_dict[lottery][1])
        for i in range(plan_len):
            plan_.append({"number":issueName[i],"issueCode":issue[i],"multiple":1})
        return plan_

    @staticmethod
    def play_type(type_=''):#隨機生成  group .  五星,四星.....
        game_group = {'wuxing':u'五星','sixing':u'四星','qiansan':u'前三','housan':u'後三',
        'zhongsan':u'中三','qianer':u'前二','houer':u'後二'}
        if type_== "ptxffc":# 奇趣 沒有五星
            del game_group['wuxing']
            num = 5
        elif type_ == 'btcctp':
            game_group = {'chungtienpao':'冲天炮'}
            num = 0
        elif type_ in lottery_fun:
            game_group = {'guanya':'冠亞','guanyaji': '冠亞季' , 'qiansi':'前四', 'qianwu':'前五'}
            num = 3
        else:
            num = 6
        return list(game_group.keys())[random.randint(0,num)]
    @staticmethod
    def ball_type(test):#對應完法,產生對應最大倍數和 投注完法
        range_ball = [i for i in range(1,11)]
        #  (Joy188Test.random_mul(9)) 隨機生成 9以內的數值
        global mul
        if test == 'wuxing':
            ball = [str(Joy188Test.random_mul(9)) for i in range(5)]#五星都是數值
            mul = Joy188Test.random_mul(2)
        elif test == 'sixing':
            ball = ['-' if i ==0  else str(Joy188Test.random_mul(9)) for i in range(5)]#第一個為-
            mul = Joy188Test.random_mul(22)
        elif test == 'housan':
            ball = ['-' if i in [0,1]  else str(Joy188Test.random_mul(9)) for i in range(5)]#第1和2為-
            mul = Joy188Test.random_mul(50)
        elif test == 'qiansan' :
            ball = ['-' if i in[3,4]  else str(Joy188Test.random_mul(9)) for i in range(5)]#第4和5為-
            mul = Joy188Test.random_mul(50)
        elif test == 'zhongsan':
            ball = ['-' if i in[0,4]  else str(Joy188Test.random_mul(9)) for i in range(5)]#第2,3,4為-
            mul = Joy188Test.random_mul(50)
        elif test == 'houer':
            ball = ['-' if i in [0,1,2]  else str(Joy188Test.random_mul(9)) for i in range(5)]#第1,2,3為-
            mul = Joy188Test.random_mul(50)
        elif test == 'qianer':
            ball = ['-' if i in [2,3,4]  else str(Joy188Test.random_mul(9)) for i in range(5)]#第3,4,5為-
            mul = Joy188Test.random_mul(50)
        elif test == 'yixing':# 五個號碼,只有一個隨機數值
            ran = Joy188Test.random_mul(4)
            ball = ['-' if i !=ran else str(Joy188Test.random_mul(9)) for i in range(5)]
            mul = Joy188Test.random_mul(50)
        elif test == 'chungtienpao':
            ball = [str(round(random.uniform(1,2),2))]
            mul = Joy188Test.random_mul(1)
        elif test == "guanya":
            ball = ['-' if i not in [0,1]  else '0%s'%range_ball[i] for i in range(10)]
            mul = Joy188Test.random_mul(10)
        elif test == 'guanyaji':
            ball = ['-' if i not in [0,1,2]  else '0%s'%range_ball[i]  for i in range(10)]
            mul = Joy188Test.random_mul(10)
        elif test == 'qiansi':
            ball = ["07 08 09 10,09 10,10,08 09 10,-,-,-,-,-,-"]
            mul = Joy188Test.random_mul(10)
        elif test == 'qianwu':
            ball = ["07 08 09 10,07 08 10,07 10,10,06 07 08 09 10,-,-,-,-,-"]
            mul = Joy188Test.random_mul(10)
        else:
             mul = Joy188Test.random_mul(1)
        a = (",".join(ball))
        return a
    @staticmethod
    def game_type(lottery):
        #test___ = play_type()
        game_group = {'wuxing':u'五星','sixing':u'四星','qiansan':u'前三','housan':u'後三',
        'zhongsan':u'中三','qianer':u'前二','houer':u'後二','xuanqi':u'選ㄧ','sanbutonghao':u'三不同號',
        'santonghaotongxuan':u'三同號通選','guanya':u'冠亞','biaozhuntouzhu':u'標準玩法','zhengma':u'正碼',
        'p3sanxing':u'P3三星','renxuan':u'任選','zhenghe':'整合','guanyaji':'冠亞季','qiansi':'前四',
                'qianwu':'前五'  }
        
        game_set = {
        'zhixuan': u'直選','renxuanqizhongwu': u'任選一中一','biaozhun':u'標準','zuxuan':u'組選'
        ,'pingma':u'平碼','putongwanfa':u'普通玩法','hezhi':'和值'}
        game_method = {
        'fushi': u'複式','zhixuanfushi':u'直選複式','zhixuanliuma':u'直選六碼',
        'renxuan7': u'任選7','hezhi':'和值'    
        }

        group_ = Joy188Test.play_type(lottery)#建立 個隨機的goup玩法 ex: wuxing,目前先給時彩系列使用
        global play_
        lottery_ball = Joy188Test.ball_type(group_)# 組出 動態的投注內容 , 目前只有num=0, lottery_sh


        test_dicts = {   
        0 : ["%s.zhixuan.fushi"%(group_,),lottery_ball] , 
        1 : ["qianer.zhixuan.zhixuanfushi",'3,6,-'],
        2 : ["xuanqi.renxuanqizhongwu.fushi","01,02,05,06,08,09,10"],
        3 : ["sanbutonghao.biaozhun.biaozhuntouzhu","1,2,6"],
        4 : ["santonghaotongxuan.santonghaotongxuan.santonghaotongxuan","111 222 333 444 555 666"],
        5 : ["%s.zhixuan.fushi"%(group_,),lottery_ball],
        6 : ['qianer.zuxuan.fushi','4,8'],
        7 : ["biaozhuntouzhu.biaozhun.fushi","04,08,13,19,24,27+09",],
        8 : ["zhengma.pingma.zhixuanliuma","04"],
        9 : ["p3sanxing.zhixuan.p3fushi","9,1,0",],
        10: ["renxuan.putongwanfa.renxuan7","09,13,16,30,57,59,71"],   
        11: ["%s.chungtienpao.chungtienpao"%(group_,),lottery_ball],#快開
        12: ["zhenghe.hezhi.hezhi","3"]#pc蛋蛋
        }

        if lottery in lottery_sh:
            num = 0
            play_ = u'玩法名稱: %s.%s.%s'%(game_group[group_],game_set['zhixuan'],
            game_method['fushi'])

        elif lottery in lottery_3d:
            num = 1
            play_ = u'玩法名稱: %s.%s.%s'%(game_group['qianer'],game_set['zhixuan'],
                    game_method['zhixuanfushi'])
        elif lottery in lottery_noRed:
            if lottery in ['p5','np3']:
                num = 9
                play_ = u'玩法名稱: %s.%s.%s'%(game_group['p3sanxing'],game_set['zhixuan'],
                    game_method['fushi'])
            else:
                num = 1
                play_ = u'玩法名稱: %s.%s.%s'%(game_group['qianer'],game_set['zhixuan'],
                        game_method['zhixuanfushi'])

        elif lottery in lottery_115:
            num = 2
            play_ = u'玩法名稱: %s.%s.%s'%(game_group['xuanqi'],game_set['renxuanqizhongwu'],
                    game_method['fushi'])
        elif lottery in lottery_k3:
            num = 3
            play_ = u'玩法名稱: %s.%s'%(game_group['sanbutonghao'],game_set['biaozhun'])
        elif lottery in lottery_sb:
            num = 4
            play_ = u'玩法名稱: %s'%(game_group['santonghaotongxuan'])
        elif lottery in lottery_fun:
            num = 5
            play_ = u'玩法名稱: %s.%s.%s'%(game_group[group_],game_set['zhixuan'],
                    game_method['fushi'])
        elif lottery == 'shssl':
            num = 6
            play_ = u'玩法名稱: %s.%s.%s'%(game_group['qianer'],game_set['zuxuan'],
                    game_method['fushi'])
        elif lottery ==  'ssq':
            num = 7
            play_ = u'玩法名稱: %s.%s.%s'%(game_group['biaozhuntouzhu'],game_set['biaozhun'],
                    game_method['fushi'])
        elif lottery == 'lhc':
            num = 8
            play_ = u'玩法名稱: %s.%s.%s'%(game_group['zhengma'],game_set['pingma'],
                    game_method['zhixuanliuma'])
        
        elif lottery in ['bjkl8','fckl8']:
            num = 10
            play_ = u'玩法名稱: %s.%s.%s'%(game_group['renxuan'],game_set['putongwanfa'],
                    game_method['renxuan7'])
        elif lottery == 'pcdd':
            num = 12
            play_ = u'玩法名稱: %s.%s.%s'%(game_group['zhenghe'],game_set['hezhi'],
            game_method['hezhi'])
        else:
            num = 11
            play_ = u'玩法名稱: 沖天炮'
        return test_dicts[num][0],test_dicts[num][1]
    @staticmethod
    def req_post_submit(account,lottery,data_,moneyunit,awardmode,plan):
        awardmode_dict = {0:u"非一般模式",1:u"非高獎金模式",2:u"高獎金"}
        money_dict = {1:u"元模式",0.1:u"分模式",0.01:u"角模式"}
        Pc_header['Cookie']= 'ANVOID='+ cookies_[account]
    

        r = session.post(em_url+'/gameBet/'+lottery+'/submit', 
        data = json.dumps(data_),headers=Pc_header)

        global content_,order_dict 
        lottery_name= u'投注彩種: %s'%lottery_dict[lottery][0]  
        try:
            msg = (r.json()['msg'])
            orderid = (r.json()['data']['orderId'])#用來 到時撤銷接口使用
            mode = money_dict[moneyunit]
            mode1 = awardmode_dict[awardmode]
            project_id = (r.json()['data']['projectId'])#訂單號
            submit_amount = (r.json()['data']['totalprice'])#投注金額
            #submit_mul = u"投注倍數: %s"%m#隨機倍數     
            #print(r.json()['isSuccess'])

            if r.json()['isSuccess'] == 0:#
                #select_issue(get_conn(envs),lottery_dict[lottery][1])#呼叫目前正在販售的獎期
                content_ = (lottery_name+"\n"+ mul_+ "\n"+play_ +"\n"+ msg+"\n")

                if r.json()['msg'] == u'存在封锁变价':#有可能封鎖變價,先跳過   ()
                    print(r.json()['msg'])
                elif r.json()['msg'] == u'您的投注内容 超出倍数限制，请调整！':
                    #print(u'倍數超出了唷,下次再來')
                    pass # 因為 超出被數 已經 在msg 裡.不用重複 顯示
                elif  r.json()['msg']==u'方案提交失败，请检查网络并重新提交！':
                    print(r.json()['msg'])

                else:#可能剛好 db抓到獎期剛好截止
                    #Joy188Test.select_issue(Joy188Test.get_conn(1),lottery_dict[lottery][1])
                    Joy188Test.web_issuecode(lottery)#抓獎其
                    plan_ = [{"number":"123","issueCode":issuecode,"multiple":1}]
                    data_['orders'] = plan_

                    r = session.post(em_url+'/gameBet/'+lottery+'/submit', 
                    data = json.dumps(data_),headers=Pc_header)
            else:#投注成功
                if plan > 1:# 追號

                    print(u'追號, 期數:%s'%plan)
                    plan_code = Joy188Test.select_PlanCode(Joy188Test.get_conn(envs),
                                lottery_dict[lottery][1],account)
                    content_ = (lottery_name+"\n"+u'追號單號: '+plan_code+"\n"
                                +mul_+ "\n" 
                                +play_+"\n"+u"投注金額: "+ str(float(submit_amount*0.0001*plan))+"\n"
                                +mode+"/"+mode1+"\n"+msg+"\n")
                else:
                    content_ = (lottery_name+"\n"+u'投注單號: '+project_id+"\n"
                                +mul_+ "\n" 
                                +play_+"\n"+u"投注金額: "+ str(float(submit_amount*0.0001))+"\n"
                                +mode+"/"+mode1+"\n"+msg+"\n")
                order_dict[lottery]  = {project_id: orderid}# 存放, 後續 掣單使用
        except:
            content_ = lottery_name + "失敗"
        print(content_)
    @staticmethod
    #@jit_func_time
    def test_Submit(account,moneyunit,plan):#彩種投注
        global order_dict
        order_dict = {}
        for i in lottery_dict.keys(): 
        #for i in lottery_sh:
            while True:
                try:
                    global mul_ #傳回 投注出去的組合訊息 req_post_submit 的 content裡
                    global mul
                    #ball_type_post = Joy188Test.game_type(i)# 找尋彩種後, 找到Mapping後的 玩法後內容
                    if i in ['btcctp','btcffc','xyft','xyft168']:# 只開放開獎金彩種
                        awardmode = 2
                        mul = Joy188Test.random_mul(10)
                        if i == 'btcctp':#快開
                            mul = Joy188Test.random_mul(1)#不支援倍數,所以random參數為1

                    else:
                        mul = Joy188Test.random_mul(5)
                        awardmode = 1
                    ball_type_post = Joy188Test.game_type(i)# 找尋彩種後, 找到Mapping後的 玩法後內容
                    mul_ = (u'選擇倍數: %s'%mul)
                    amount = 2*mul*moneyunit

                    if plan == 1   :# 一般投住
                        Joy188Test.web_issuecode(i)#抓獎其
                        plan_ = [{"number":'123',"issueCode":issuecode,"multiple":1}]
                        print(u'一般投住')
                        isTrace=0
                        traceWinStop=0
                        traceStopValue=-1
                    else: #追號
                        if i in ['slmmc','sl115','jsdice','jldice1','jldice2','btcctp','lhc']:
                            print("彩種: %s 沒開放追號"%lottery_dict[i][0]+"\n")
                            break
                        plan_ = Joy188Test.plan_num(envs,i,random.randint(2,plan))#隨機生成 50期內的比數
                        isTrace=1
                        traceWinStop=1
                        traceStopValue=1
                    len_ = len(plan_)# 一般投注, 長度為1, 追號長度為
                    post_data = {"gameType":i,"isTrace":isTrace,"traceWinStop":traceWinStop,
                    "traceStopValue":traceWinStop,
                    "balls":[{"id":1,"ball":ball_type_post[1],"type":ball_type_post[0],
                    "moneyunit":moneyunit,"multiple":mul,"awardMode":awardmode,
                    "num":1}],"orders": plan_,"redDiscountAmount": 0 ,"amount" : len_*amount}

                    global post_noRed
                    post_noRed = {"gameType":i,"isTrace":isTrace,"traceWinStop":traceWinStop,
                    "traceStopValue":traceWinStop,
                    "balls":[{"id":1,"ball":ball_type_post[1],"type":ball_type_post[0],
                    "moneyunit":moneyunit,"multiple":mul,"awardMode":awardmode,
                    "num":1}],"orders": plan_ ,"amount" : len_*amount}

                    post_data_lhc = {"balls":[{"id":1,"moneyunit":moneyunit,"multiple":1,"num":1,
                    "type":ball_type_post[0],"amount":amount,"lotterys":"13",
                    "ball":ball_type_post[1],"odds":"7.5"}],
                    "isTrace":0,"orders":plan_,
                    "amount":amount,"awardGroupId":202}

                    post_data_sb ={"gameType":i,"isTrace":0,"multiple":1,"trace":1,
                    "amount":amount,
                    "balls":[{"ball":ball_type_post[1],
                    "id":11,"moneyunit":moneyunit,"multiple":1,"amount":amount,"num":1,
                    "type":ball_type_post[0]}],
                    "orders":plan_}

                    post_data_pcdd = {"balls":[{"id":1,"moneyunit":1,"multiple":1,"num":1,
                    "type":"zhenghe.hezhi.hezhi","amount":50,"ball":"3","odds":90,"awardMode":1}],
                    "orders":plan_,
                    "redDiscountAmount":0,"amount":50*len_,"isTrace":isTrace,
                    "traceWinStop":traceWinStop,"traceStopValue":traceStopValue}
                    
                    
                    if i == 'lhc':
                        Joy188Test.req_post_submit(account,'lhc',post_data_lhc,moneyunit,awardmode,len_)
                    elif i == 'pcdd':
                        Joy188Test.req_post_submit(account,'pcdd',post_data_pcdd,moneyunit,awardmode,
                                                   len_)
                    elif i in lottery_sb:
                        Joy188Test.req_post_submit(account,i,post_data_sb,moneyunit,awardmode,len_) 
                    else:
                        Joy188Test.req_post_submit(account,i,post_noRed,moneyunit,awardmode,len_)
                    break
                except IndexError as e :
                    #print(e)
                    print("彩種: %s 投注失敗"%lottery_dict[i][0]+"\n")
                    break
    @staticmethod
    def test_LotterySubmit():
        u"投注測試"
        Joy188Test.test_Submit(account=env_dict['一般帳號'][envs],moneyunit=1,
            plan=1)#
    @staticmethod
    def test_LotteryPlanSubmit():
        u"追號測試"
        Joy188Test.test_Submit(account=env_dict['合營1940'][envs],moneyunit=1,
            plan=10)#
    @staticmethod
    def APP_SessionPost(third,url,post_data):#共用 session post方式 (Pc)
        header={
            'User-Agent': userAgent,
            'Content-Type': 'application/json; charset=UTF-8', 
        }
        try:
            session = requests.Session()
            #r = requests.post(env+'/%s/balance'%third,data=json.dumps(data_),headers=header)
            #print(env)
            r = session.post(env+'/%s/%s'%(third,url),headers=header,data=json.dumps(post_data))
            
            if 'balance' in url:
                balance = r.json()['body']['result']['balance']
                print('%s 的餘額為: %s'%(third,balance))
            elif 'getBalance' in url:
                balance = r.json()['body']['result']['balance']
                print('4.0餘額: %s'%balance)

        except requests.exceptions.ConnectionError:
            print(third)
            print(u'連線有問題,請稍等')
    @staticmethod
    def session_post(user,third,url,post_data):#共用 session post方式 (Pc)
        Pc_header['Cookie']= 'ANVOID='+cookies_[user]
        try:
            r = session.post(post_url+url,headers= Pc_header,data=json.dumps(post_data))

            if 'Balance' in url:
                print('%s, 餘額: %s'%(third,r.json()['balance']))
            elif 'transfer' in url:
                if r.json()['status'] == True:
                    print('帳號 %s 轉入 %s ,金額:1, 進行中'%(user,third))
                else:
                    print('%s 轉帳失敗'%third)
            elif 'getuserbal' in url:
                print('4.0 餘額: %s'%r.json()['data'])
            #print(title)#強制便 unicode, 不燃顯示在html報告  會有誤
            #print('result: '+statu_code+"\n"+'---------------------')

        except requests.exceptions.ConnectionError:
            print(third)
            print(u'連線有問題,請稍等')
    @staticmethod
    def session_get(url_,url):#共用 session get方式
        Pc_header['Cookie']= 'ANVOID='+cookies_[env_dict['一般帳號'][envs]]
        try:
            r = session.get(url_+url,headers=Pc_header)
            html = BeautifulSoup(r.text,'lxml')# type為 bs4類型
            title = str(html.title)
            statu_code = str(r.status_code)#int 轉  str
            
            print(title)#強制便 unicode, 不燃顯示在html報告  會有誤
            print(url)
            print('result: '+statu_code+"\n"+'---------------------')

        except requests.exceptions.ConnectionError:
            print(title)
            print(u'連線有問題,請稍等')
    
    @staticmethod
    def test_ThirdHome():#登入第三方頁面,創立帳號
        u"第三方頁面測試"
        threads = []
        for i in third_list:
            url = '/%s/home'%i
            if i == 'shaba':#沙巴特立
                url = url+'?act=esports'
            #print(url)
            t = threading.Thread(target=Joy188Test.session_get,args=(post_url,url))
            threads.append(t)
        for i in threads:
            i.start()
        for i in threads:
            i.join()
    @staticmethod
    def test_188():
        u"4.0頁面測試"
        threads = []
        url_188 = ['/fund','/bet/fuddetail','/withdraw','/transfer','/index/activityMall'
        ,'/ad/noticeList?noticeLevel=2','/frontCheckIn/checkInIndex','/frontScoreMall/pointsMall'
        ,'/proxy/index','/proxy/cusmag','/proxy/promotetpl']        
        em_188 = ['/gameUserCenter/queryOrdersEnter','/gameUserCenter/queryPlans'
                  ,'/gameUserCenter/queryCurrentUserReport']
        for i in url_188:
            t = threading.Thread(target=Joy188Test.session_get,args=(post_url,i))
            threads.append(t)
        for i in em_188:
            t = threading.Thread(target=Joy188Test.session_get,args=(em_url,i))
            threads.append(t)
        for i in threads:
            i.start()
        for i in threads:
            i.join()
    @staticmethod
    def test_chart():
        u"走勢圖測試"
        ssh_url = ['cqssc','hljssc','tjssc','xjssc','llssc','txffc','btcffc','fhjlssc',
                   'jlffc','slmmc','sd115','ll115','gd115','jx115']
        k3_url = ['jsk3','ahk3','jsdice','jldice1','jldice2']
        low_url = ['d3','v3d']
        fun_url = ['xyft','pk10']
        for i in ssh_url:
            Joy188Test.session_get(em_url,'/game/chart/%s/Wuxing'%i)
        for i in k3_url:
            Joy188Test.session_get(em_url,'/game/chart/%s/chart'%i)
        for i in low_url:
            Joy188Test.session_get(em_url,'/game/chart/%s/Qiansan'%i)
        for i in fun_url:
            Joy188Test.session_get(em_url,'/game/chart/%s/CaipaiweiQianfushi'%i)
        Joy188Test.session_get(em_url,'/game/chart/p5/p5chart')
        Joy188Test.session_get(em_url,'/game/chart/ssq/ssq_basic')
        Joy188Test.session_get(em_url,'/game/chart/kl8/Quwei')
    @staticmethod
    def test_thirdBalance():
        '''4.0/第三方餘額'''
        threads = []
        user = env_dict['轉入/轉出'][envs]
    
        print('帳號: %s'%user)
        for third in third_list:
            if third == 'gns':
                third_url = '/gns/gnsBalance'
            else:
                third_url = '/%s/thirdlyBalance'%third 
            #r = session.post(post_url+third_url,headers=header)
            #print('%s, 餘額: %s'%(third,r.json()['balance']))
            t = threading.Thread(target=Joy188Test.session_post,args=(user,third,third_url,''))
            threads.append(t)
        t = threading.Thread(target=Joy188Test.session_post,args=(user,'','/index/getuserbal',''))
        threads.append(t)
        for i in threads:
            i.start()
        for i in threads:
            i.join()
    @staticmethod
    def test_transferin():#第三方轉入
        '''第三方轉入'''
        user = env_dict['轉入/轉出'][envs]
        Pc_header['Cookie']= 'ANVOID='+cookies_[user]
        Pc_header['Content-Type'] = 'application/json; application/json; charset=UTF-8' 
        statu_list = []
        post_data = {"amount":1}
        for third in third_list:
            if third == 'gns':
                url = '/gns/transferToGns'

            else:
                url = '/%s/transferToThirdly'%third
            r = session.post(post_url+url,data=json.dumps(post_data),headers= Pc_header)
            if r.json()['status'] == True:
                print('帳號: %s 轉入 %s ,金額:1, 進行中'%(user,third))
                statu_list.append(third)
            else:
                print('%s轉帳接口失敗, api回復訊息: %s'%(third,r.json()['errorMsg']))
        print('--------------------------------------------')
        for third in statu_list:
            thirdly_status = Joy188Test.thirdly_tran(Joy188Test.my_con(evn=envs,third=third),tran_type=0,
            third=third,user=user)# 先確認資料轉帳傳泰
            staut_mapping = thirdly_status[0][1]
            msg = '%s 轉帳單號: %s . '%(third,thirdly_status[0][0])
            if staut_mapping == '2':
                msg = msg +" 狀態成功"
            else:
                msg = msg +" 狀態待確認"
            sleep(3)
            print(msg)
        Joy188Test.test_thirdBalance()
    @staticmethod
    def test_transferout():#第三方轉回
        '''第三方轉出'''
        statu_list = []
        user = env_dict['轉入/轉出'][envs]
        Pc_header['Cookie']= 'ANVOID='+cookies_[user]
        Pc_header['Content-Type'] = 'application/json; application/json; charset=UTF-8' 
        post_data = {"amount":1}
        for third in third_list:
            url = '/%s/transferToFF'%third
            r = session.post(post_url+url,data=json.dumps(post_data),headers= Pc_header)
            if r.json()['status'] == True:
                print('帳號: %s, %s轉回4.0 ,金額:1, 進行中'%(user,third))
                statu_list.append(third)
            else:
                print('%s轉帳接口失敗'%third)
        for third in statu_list:
            thirdly_status = Joy188Test.thirdly_tran(Joy188Test.my_con(evn=envs,third=third),tran_type=1,
                third=third,user=user)# 先確認資料轉帳傳泰
            staut_mapping = thirdly_status[0][1]
            msg = '%s 轉帳單號: %s . '%(third,thirdly_status[0][0])
            if staut_mapping == '2':
                msg = msg +" 狀態成功"
            else:
                msg = msg +" 狀態待確認"
            sleep(3)
            print(msg)
            
        Joy188Test.test_thirdBalance()
    @staticmethod
    def test_tranUser(): # 代理線轉移
        '''代理線轉移'''
        #Joy188Test.admin_login()
        for move_type in [3]: #擇一個做
            if move_type ==0:#提升總代
                move_type = 'ga'
                target = ''# 提升總代 無需目標
                Joy188Test.select_tranUser(Joy188Test.get_conn(envs),'%kerr%',1)#抓出一代用戶
                random_user = random.randint(1,len(tran_user))
                user = tran_user[random_user]# 隨機找出用戶
                print('一代用戶: %s轉移至總代'%user)
            elif move_type ==1:#跨代理轉一代
                move_type = 'loa'
                Joy188Test.select_tranUser(Joy188Test.get_conn(envs),'%kerr%',2)#抓出二代用戶,目標需為不同上級
                random_user = random.randint(1,len(tran_user))# 隨機取出用戶,避免容易失敗,
                user = tran_user[random_user]#要做的用戶
                target = user_chain[0].split('/')[1]# 此為  抓出來的總帶,  需找出  不是這個總帶的一帶
                Joy188Test.select_tranChainUser(Joy188Test.get_conn(envs),target,'%kerr%')# 抓出 不同的代理 預設總帶,
                random_user = random.randint(1,len(tran_user))# 隨機取出總代,避免容易失敗,
                target = tran_user[random_user]#此用戶 即為  目標
                #print(target)
                print('二代: %s用戶,轉移至一代,新總代為: %s'%(user,target))
            elif move_type == 2:#相同代理,跨上去一層
                move_type = 'lua'
                Joy188Test.select_tranUser(Joy188Test.get_conn(envs),'%kerr%',3)#抓出三代用戶,目標需為相同上級
                user = tran_user[0]#要做的用戶
                target = user_chain[0].split('/')[1]# 此為  抓出來的總帶,  需找出  是這個用戶的總代
                print('三代: %s用戶,轉移至一代,相同總代為: %s'%(user,target))
            elif move_type == 3:#代理線轉移, 隨意跨線 ,可以是 同條線 ,也可以是 別條線
                move_type = 'lca'
                random_lvl = random.randint(2,10) # 隨意等級 ,2 -6 
                Joy188Test.select_tranUser(conn=Joy188Test.get_conn(envs) )#抓一個
                user = tran_user[0]#要做的用戶
                Joy188Test.select_tranUser(conn=Joy188Test.get_conn(envs),type_='t')#

                target = tran_user[0]#要做的用戶
                print('%s用戶,做代理線移轉 ,新上級代理: %s, 新總代: %s'%(user, target,
                                                     env_dict['測試總代'][envs]))
            
            
            admin_header['Content-Type'] = "application/x-www-form-urlencoded; charset=UTF-8"
            data = 'moveAccount=%s&targetAccount=%s&moveType=%s'%(user,target,move_type)# 要做轉移的用戶,目標用戶 ,類型 
            r = admin_session.post(admin_url+'/admin/user/userchaincreate',headers=admin_header,
                                   data=data)

            #print(r.json())
            #print(r.json()['status'])
            if 'errorMsg' in r.text:
                print('代理線需確認')
            else:
                print('轉移成功')
            print('----------------')
    @staticmethod
    def test_redEnvelope():#紅包加壁,審核用
        '''紅包測試'''
        #user = 'kerr001'
        user = env_dict['一般帳號'][envs]
        print('用戶: %s'%user)
        red_list = [] #放交易訂單號id
        Joy188Test.select_RedBal(Joy188Test.get_conn(envs),user)
        print('紅包餘額: %s'%(int(red_bal[0])/10000))
        
        #Joy188Test.admin_login()#登入後台
        data = {"receives":user,"blockType":"2","lotteryType":"1","lotteryCodes":"",
        "amount":"100","note":"test"}
        #header['Cookie'] = 'ANVOAID='+ admin_cookie['admin_cookie']#存放後台cookie
        admin_header['Content-Type'] ='application/json'
        r = admin_session.post(admin_url+'/redAdmin/redEnvelopeApply',#後台加紅包街口 
        data = json.dumps(data),headers=admin_header)
        if r.json()['status'] ==0:
            print('紅包加幣100')
        else:
            print ('失敗')
        Joy188Test.select_RedID(Joy188Test.get_conn(envs),user)#查詢教地訂單號,回傳審核data
        #print(red_id)
        red_list.append('%s'%red_id[0])
        #print(red_list)
        data = {"ids":red_list ,"status":2}
        r = admin_session.post(admin_url+'/redAdmin/redEnvelopeConfirm',#後台審核街口 
        data = json.dumps(data),headers=admin_header)
        if r.json()['status'] ==0:
            print('審核通過')
        else:
            print('審核失敗')
        Joy188Test.select_RedBal(Joy188Test.get_conn(envs),user)
        print('紅包餘額: %s'%(int(red_bal[0])/10000))
    
    @staticmethod
    def test_CancelOrder():#撤銷皆口
        '''撤消測試'''
        #user =  env_dict['一般帳號'][envs]
        Pc_header['Cookie']= 'ANVOID='+cookies_[env_dict['一般帳號'][envs]]
        try:
            ran_  = random.randint(0,len(cancel_lottery_list))# 隨機長
            try:
                can_lottery = cancel_lottery_list[ran_]# 要被撤消的彩種
            except IndexError:
                ran_  = random.randint(0,3)# 隨機長/
                can_lottery = cancel_lottery_list[ran_]# 要被撤消的彩種
            orderid = list(order_dict[can_lottery].values())[0]
            r = session.post(em_url+'/gameUserCenter/cancelOrder?orderId=%s'%orderid,headers=Pc_header)
            print('撤消彩種: %s ,方案編號: %s '%(can_lottery ,list(order_dict[can_lottery].keys())[0]))
            if r.json()['status'] == 1:
                print('撤消成功')
            else:
                print('撤銷失敗')
        except:
            #print(can_lottery)
            print('撤消問題確認')
    @staticmethod
    def test_ChargeLimit():
        '''充值解限測試'''
        user =  env_dict['一般帳號'][envs]
        userid = {'hsieh001': '1341294', 'kerr001': '1373224'}
        #Joy188Test.admin_login()
        admin_data = 'userId=%s&unlimitType=1&userLvl=1&username=%s&note=sdsdsds'%(userid[user],
                                                                                        user)
        admin_header['Content-Type'] = "application/x-www-form-urlencoded; charset=UTF-8"
        r = admin_session.post(admin_url+'/admin/user/userchargelimit' ,data=admin_data,
                               headers=admin_header)
        if r.json()['isSuccess'] == "1":
            print('%s 後台充值解限次數, 成功'%user)
        else:
            print('%s 後台充值解限次數, 失敗'%user)


# In[ ]:





# In[3]:


class Joy188Test2(unittest.TestCase):
    u"trunk頁面測試"
    @classmethod
    def setUpClass(cls):
        global dr,user
        try:
            cls.dr = webdriver.Chrome(executable_path=r'C:\python3\Scripts\FF_Script\chromedriver.exe')
            dr = cls.dr
            if envs == 1: 
                cls.dr.get(post_url)
                user = 'kerr002'
                password = 'amberrd'
                env_info = '188'
            else:
                cls.dr.get(post_url)
                user = 'hsieh002'
                password = '123qwe'
                env_info = 'dev'
            print(u'登入環境: %s,登入帳號: %s'%(env_info ,user))
            cls.dr.find_element_by_id('J-user-name').send_keys(user)
            cls.dr.find_element_by_id('J-user-password').send_keys(password)
            cls.dr.find_element_by_id('J-form-submit').click()
            sleep(3)
            if dr.current_url == post_url+'/index':#判斷是否登入成功
                print(u'登入成功')
            else:
                print(u'登入失敗')
        except NoSuchElementException as e:
            print(e)
    @staticmethod
    def ID(element):
        return  dr.find_element_by_id(element)
    def CSS( element):
        return  dr.find_element_by_css_selector(element)
    def CLASS( element):
        return  dr.find_element_by_class_name(element)
    @staticmethod
    def XPATH( element):
        return  dr.find_element_by_xpath(element)
    @staticmethod
    def LINK( element):
        return  dr.find_element_by_link_text(element)
    @staticmethod	
    def id_element(element1):#抓取id元素,判斷提示窗
        
        try:
            element = Joy188Test2.CSS("a.btn.closeTip")
            if element.is_displayed():
                Joy188Test2.LINK("关 闭").click()
            else:
                Joy188Test2.ID(element1).click() 
        except WebDriverException as e:
            pass
        except NoSuchElementException as e:
            pass
    @staticmethod	
    def class_element(element1):#抓取id元素,判斷提示窗
        
        try:
            element = Joy188Test2.CSS("a.btn.closeTip")
            if element.is_displayed():
                Joy188Test2.LINK("关 闭").click()
            else:
                Joy188Test2.CLASS(element1).click() 
        except WebDriverException as e:
            print(e)
        except NoSuchElementException as e:
            print(e)
    @staticmethod	
    def css_element(element1):#抓取css元素,判斷提示窗
        try:
            element = Joy188Test2.CSS("a.btn.closeTip")
            if element.is_displayed():
                sleep(3)
                element.click()
                Joy188Test2.CSS(element1).click()
            else:
                Joy188Test2.CSS(element1).click() 
        except WebDriverException as e:
            pass
        except NoSuchElementException as e:
            pass
        except AttributeError:
            pass
    @staticmethod	
    def xpath_element(element1):#抓取xpath元素,判斷提示窗

        try:
            element = Joy188Test2.CSS("a.btn.closeTip")
            if element.is_displayed():
                element.click()
                Joy188Test2.XPATH(element1).click() 
            else:
                Joy188Test2.XPATH(element1).click() 
        except WebDriverException as e:
            pass
        except NoSuchElementException as e:
            pass
    @staticmethod	
    def link_element(element1):#抓取link_text元素,判斷提示窗
        try:
            element = Joy188Test2.CSS("a.btn.closeTip")
            if element.is_displayed():
                element.click()
                Joy188Test2.LINK(element1).click() 
            else:
                Joy188Test2.LINK(element1).click() 
        except WebDriverException as e:
            pass
        except NoSuchElementException as e:
            pass
    #change > ul.play-select-content.clearfix > li.sixing.normal.current > dl.zhixuan > dd.danshi
    @staticmethod
    def normal_type(game):#普通玩法元素
        global game_list,game_list2
        game_list = ['wuxing','sixing','qiansan','zhongsan','housan','qianer','houer','yixing',
                    'super2000','houer_2000.caojiduizhi','yixing_2000.caojiduizhi',
                     'special','longhu.special']
        game_list2 = ['wuxing','sixing','qiansan','zhongsan','housan','qianer','houer','yixing',
                    'special','longhu.special']
        
        '''五星'''
        wuxing_element = ['dd.danshi','dd.zuxuan120','dd.zuxuan60','dd.zuxuan30',"dd.zuxuan20","dd.zuxuan10",
        "dd.zuxuan5","dd.yimabudingwei","dd.ermabudingwei","dd.sanmabudingwei","dd.yifanfengshun",
        "dd.haoshichengshuang","dd.sanxingbaoxi","dd.sijifacai"]
        '''四星'''
        sixing_element=['li.sixing.current > dl.zhixuan > dd.danshi','dd.zuxuan24',
        'dd.zuxuan12','dd.zuxuan6',"dd.zuxuan4","li.sixing.current > dl.budingwei > dd.yimabudingwei"
        ,"li.sixing.current > dl.budingwei > dd.ermabudingwei"]
        '''前三'''
        qiansan_element = ['li.qiansan.current > dl.zhixuan > dd.danshi','dd.hezhi','dd.kuadu',
        'dl.zuxuan > dd.hezhi','dd.zusan','dd.zuliu','dd.hunhezuxuan',
        'dd.baodan','dd.zusandanshi','dd.zuliudanshi',
        'li.qiansan.current > dl.budingwei > dd.yimabudingwei',
        'li.qiansan.current > dl.budingwei > dd.ermabudingwei']
        '''中三'''
        zhongsan_element = ['li.zhongsan.current > dl.zhixuan > dd.danshi',
        'li.zhongsan.current > dl.zhixuan > dd.hezhi',
        'li.zhongsan.current>  dl.zhixuan > dd.kuadu',
        'li.zhongsan.current > dl.zuxuan > dd.hezhi',
        'li.zhongsan.current > dl.zuxuan > dd.zusan',
        'li.zhongsan.current > dl.zuxuan > dd.zuliu',
        'li.zhongsan.current > dl.zuxuan > dd.hunhezuxuan',
        'li.zhongsan.current > dl.zuxuan > dd.baodan',
        'li.zhongsan.current > dl.zuxuan > dd.zusandanshi',
        'li.zhongsan.current > dl.zuxuan > dd.zuliudanshi',
        'li.zhongsan.current > dl.budingwei > dd.yimabudingwei',
        'li.zhongsan.current > dl.budingwei > dd.ermabudingwei']

        '''後三'''
        housan_element = ['li.housan.current > dl.zhixuan > dd.danshi',
        'li.housan.current > dl.zhixuan > dd.hezhi',
        'li.housan.current > dl.zhixuan > dd.kuadu',
        'li.housan.current > dl.zuxuan > dd.hezhi',
        'li.housan.current > dl.zuxuan > dd.zusan',
        'li.housan.current > dl.zuxuan > dd.zuliu',
        'li.housan.current > dl.zuxuan > dd.hunhezuxuan',
        'li.housan.current > dl.zuxuan > dd.baodan',
        'li.housan.current > dl.zuxuan > dd.zusandanshi',
        'li.housan.current > dl.zuxuan > dd.zuliudanshi',
        'li.housan.current > dl.budingwei > dd.yimabudingwei',
        'li.housan.current > dl.budingwei > dd.ermabudingwei']

        '''前二'''
        qianer_element = ['li.qianer.current > dl.zhixuan > dd.danshi',
        'li.qianer.current > dl.zhixuan > dd.hezhi',
        'li.qianer.current > dl.zhixuan > dd.kuadu',
        'li.qianer.current > dl.zuxuan > dd.fushi',
        'li.qianer.current > dl.zuxuan > dd.danshi',
        'li.qianer.current > dl.zuxuan > dd.hezhi',
        'li.qianer.current > dl.zuxuan > dd.baodan']
        '''後二'''
        houer_element = ['li.houer.current > dl.zhixuan > dd.danshi',
        'li.houer.current > dl.zhixuan > dd.hezhi',
        'li.houer.current > dl.zhixuan > dd.kuadu',
        'li.houer.current > dl.zuxuan > dd.fushi',
        'li.houer.current > dl.zuxuan > dd.danshi',
        'li.houer.current > dl.zuxuan > dd.hezhi',
        'li.houer.current > dl.zuxuan > dd.baodan']
        '''後三2000'''
        housan_2000_element = ['li.housan_2000.current > dl.zhixuan > dd.danshi',
        'li.housan_2000.current > dl.zhixualink_elementan > dd.kuadu',
        'li.housan_2000.current > dl.zuxuan > dd.hezhi',
        'li.housan_2000.current > dl.zuxuan > dd.zusan',
        'li.housan_2000.current > dl.zuxuan > dd.zuliu',
        'li.housan_2000.current > dl.zuxuan > dd.hunhezuxuan',
        'li.housan_2000.current > dl.zuxuan > dd.baodan',
        'li.housan_2000.current > dl.zuxuan > dd.zusandanshi',
        'li.housan_2000.current > dl.zuxuan > dd.zuliudanshi',
        'li.housan_2000.current > dl.budingwei > dd.yimabudingwei',
        'li.housan_2000.current > dl.budingwei > dd.ermabudingwei']
        '''後二2000'''
        houer_2000_element = ['li.houer_2000.current > dl.zhixuan > dd.danshi',
        'li.houer_2000.current > dl.zhixuan > dd.hezhi',
        'li.houer_2000.current > dl.zhixuan > dd.kuadu',
        'li.houer_2000.current > dl.zuxuan > dd.fushi',
        'li.houer_2000.current > dl.zuxuan > dd.danshi',
        'li.houer_2000.current > dl.zuxuan > dd.hezhi',
        'li.houer_2000.current > dl.zuxuan > dd.baodan']
        '''趣味大小單雙'''
        special_big_element = ['dd.qianyi','dd.qianer','dd.houyi','dd.houer']
        
        if game == game_list[0]:
            return wuxing_element
        elif game == game_list[1]:
            return sixing_element
        elif game == game_list[2]:
            return qiansan_element
        elif game == game_list[3]:
            return zhongsan_element
        elif game == game_list[4]:
            return housan_element
        elif game == game_list[5]:
            return qianer_element
        elif game == game_list[6]:
            return houer_element
        elif game == game_list[8]:
            return housan_2000_element
        elif game == game_list[9]:
            return houer_2000_element
        elif game == game_list[11]:
            return special_big_element
        else: #一星只有一個玩法
            pass
    def game_ssh(type_='0'):#時彩系列  有含 普通玩法,超級2000,趣味玩法, 預設type_ 是有超級2000
        Joy188Test2.normal_type('wuxing')#先呼叫 normal_type方法, 產生game_list 列表
        if type_ == 'no':
            list_type = game_list2
        else:
            list_type = game_list
        for game in list_type:#產生 五星,四星,.....列表 
            if game == 'special':# 要到趣味玩法頁簽, 沒提供 css_element 的定位方法, 使用xpath
                Joy188Test2.xpath_element('//li[@game-mode="special"]')
            else:
                    
                Joy188Test2.css_element('li.%s'%game)
            sleep(2)
            Joy188Test2.id_element('randomone')#進入tab,複式玩法為預設,值接先隨機一住
            if game in ['yixing','yixing_2000.caojiduizhi','longhu.special']:
                pass
            else:
                element_list = Joy188Test2.normal_type(game)#return 元素列表
                for i in element_list: #普通,五星玩法 元素列表
                    Joy188Test2.css_element(i)
                    Joy188Test2.css_element('a#randomone.take-one')#隨機一住
    @staticmethod
    def result():#投注結果
        soup = BeautifulSoup(dr.page_source, 'lxml')
        a = soup.find_all('ul',{'class':'ui-form'})
        for i in range(5):
            for b in a:
                c = b.find_all('li')[i]
                print(c.text)
    @staticmethod
    def test_cqssc():
        u'重慶時彩投注'
        
        sleep(3)
        dr.get(em_url+'/gameBet/cqssc')
        print(dr.title)
        
        Joy188Test2.game_ssh()
                    
        Joy188Test2.id_element('J-submit-order')#馬上投注
        Joy188Test2.result()
        Joy188Test2.link_element("确 认")
        sleep(3)
        Joy188Test.select_PcOredrCode(Joy188Test.get_conn(envs),user,'cqssc')
        
        print("方案編號: %s"%order_code[0])
    @staticmethod
    def test_hljssc():#黑龍江
        
        sleep(3)
        dr.get(em_url+'/gameBet/hljssc')
        print(dr.title)
        
        Joy188Test2.game_ssh()
                    
        Joy188Test2.id_element('J-submit-order')#馬上投注
        Joy188Test2.result()
        Joy188Test2.link_element("确 认")
        sleep(3)
        Joy188Test.select_PcOredrCode(Joy188Test.get_conn(1),user,'hljssc')
        
        print("方案編號: %s"%order_code[0])
    @staticmethod
    def test_hn5fc():
        
        sleep(3)
        dr.get(em_url+'/gameBet/hn5fc')
        print(dr.title)
        
        Joy188Test2.game_ssh()
                    
        Joy188Test2.id_element('J-submit-order')#馬上投注
        Joy188Test2.result()
        Joy188Test2.link_element("确 认")
        sleep(3)
        Joy188Test.select_PcOredrCode(Joy188Test.get_conn(1),user,'hn5fc')
        
        print("方案編號: %s"%order_code[0])
    @staticmethod    
    def test_fhxjc():
        
        sleep(3)
        dr.get(em_url+'/gameBet/fhxjc')
        print(dr.title)
        
        Joy188Test2.game_ssh()
                    
        Joy188Test2.id_element('J-submit-order')#馬上投注
        Joy188Test2.result()
        Joy188Test2.link_element("确 认")
        sleep(3)
        
        Joy188Test.select_PcOredrCode(Joy188Test.get_conn(1),user,'fhxjc')
        
        print("方案編號: %s"%order_code[0])
    @staticmethod
    def test_fhcqc():
        
        sleep(3)
        dr.get(em_url+'/gameBet/fhcqc')
        print(dr.title)
        
        Joy188Test2.game_ssh()
                    
        Joy188Test2.id_element('J-submit-order')#馬上投注
        Joy188Test2.result()
        Joy188Test2.link_element("确 认")
        sleep(3)
        Joy188Test.select_PcOredrCode(Joy188Test.get_conn(1),user,'fhcqc')
        
        print("方案編號: %s"%order_code[0])
    @staticmethod
    def test_shssl():# 五星完髮不同
        sleep(3)
        dr.get(em_url+'/gameBet/shssl')
        print(dr.title)
        
        Joy188Test2.game_ssh('no')# 
                    
        Joy188Test2.id_element('J-submit-order')#馬上投注
        Joy188Test2.result()
        Joy188Test2.link_element("确 认")
        sleep(3)
        Joy188Test.select_PcOredrCode(Joy188Test.get_conn(1),user,'shssl')
        
        print("方案編號: %s"%order_code[0])
    @staticmethod
    def test_txffc():# 五星完髮不同
        sleep(3)
        dr.get(em_url+'/gameBet/txffc')
        print(dr.title)
        
        Joy188Test2.game_ssh('no')# 
                    
        Joy188Test2.id_element('J-submit-order')#馬上投注
        Joy188Test2.result()
        Joy188Test2.link_element("确 认")
        sleep(3)
        Joy188Test.select_PcOredrCode(Joy188Test.get_conn(1),user,'txffc')
        
        print("方案編號: %s"%order_code[0])
    @staticmethod
    def test_llssc():
        sleep(3)
        dr.get(em_url+'/gameBet/llssc')
        print(dr.title)
        
        Joy188Test2.game_ssh('no')# 
                    
        Joy188Test2.id_element('J-submit-order')#馬上投注
        Joy188Test2.result()
        Joy188Test2.link_element("确 认")
        sleep(3)
        Joy188Test.select_PcOredrCode(Joy188Test.get_conn(1),user,'llssc')
        print("方案編號: %s"%order_code[0])
    @staticmethod
    def test_btcffc():
        sleep(3)
        dr.get(em_url+'/gameBet/btcffc')
        print(dr.title)
        
        Joy188Test2.game_ssh('no')# 
                    
        Joy188Test2.id_element('J-submit-order')#馬上投注
        Joy188Test2.result()
        Joy188Test2.link_element("确 认")
        sleep(3)
        
        Joy188Test.select_PcOredrCode(Joy188Test.get_conn(1),user,'btcffc')
        
        print("方案編號: %s"%order_code[0])
    @staticmethod
    def test_ahk3():
        sleep(3)
        dr.get(em_url+'/gameBet/ahk3')
        print(dr.title)
        
        k3_element = ['li.hezhi.normal','li.santonghaotongxuan.normal','li.santonghaodanxuan.normal',
        'li.sanbutonghao.normal','li.sanlianhaotongxuan.normal','li.ertonghaofuxuan.normal',
        'li.ertonghaodanxuan.normal','li.erbutonghao.normal','li.yibutonghao.normal']
        for i in k3_element:            
            Joy188Test2.css_element(i)
            sleep(0.5)
            Joy188Test2.id_element('randomone')
        
        Joy188Test2.id_element('J-submit-order')#馬上投注
        Joy188Test2.result()
        Joy188Test2.link_element("确 认")
        sleep(3)
        Joy188Test.select_PcOredrCode(Joy188Test.get_conn(1),user,'ahk3')
        
        print("方案編號: %s"%order_code[0])
        
    @staticmethod
    def test_jsk3():
        sleep(3)
        dr.get(em_url+'/gameBet/jsk3')
        print(dr.title)
        
        k3_element = ['li.hezhi.normal','li.santonghaotongxuan.normal','li.santonghaodanxuan.normal',
        'li.sanbutonghao.normal','li.sanlianhaotongxuan.normal','li.ertonghaofuxuan.normal',
        'li.ertonghaodanxuan.normal','li.erbutonghao.normal','li.yibutonghao.normal']
        for i in k3_element:            
            Joy188Test2.css_element(i)
            sleep(0.5)
            Joy188Test2.id_element('randomone')
        
        Joy188Test2.id_element('J-submit-order')#馬上投注
        Joy188Test2.result()
        Joy188Test2.link_element("确 认")
        sleep(3)
        
        Joy188Test.select_PcOredrCode(Joy188Test.get_conn(1),user,'jsk3')
        
        print("方案編號: %s"%order_code[0])
    @staticmethod
    def test_jsdice():
        sleep(3)
        dr.get(em_url+'/gameBet/jsdice')
        print(dr.title)
        global sb_element
        # 江蘇骰寶 列表, div 1~ 52
        sb_element = ['//*[@id="J-dice-sheet"]/div[%s]/div'%i for i in range(1,53,1)]
        
        for i in sb_element:
            sleep(1)
            Joy188Test2.xpath_element(i)
        sleep(0.5)
        Joy188Test2.xpath_element('//*[@id="J-dice-bar"]/div[5]/button[1]')#下注
        Joy188Test2.result()
        Joy188Test2.CSS('a.btn.btn-important').click()#確認
        
        Joy188Test.select_PcOredrCode(Joy188Test.get_conn(1),user,'jsdice')
        
        print("方案編號: %s"%order_code[0])
    
    @staticmethod
    def test_jldice():
        sleep(3)
        for lottery in ['jldice1','jldice2']:
            dr.get(em_url+'/gameBet/%s'%lottery)
            print(dr.title)

            for i in sb_element:
                if Joy188Test2.ID('diceCup').is_displayed():#吉利骰寶 遇到中間開獎, 讓他休息,在繼續
                    sleep(15)
                else:
                    sleep(1)
                    Joy188Test2.xpath_element(i)
            sleep(0.5)

            if Joy188Test2.ID('diceCup').is_displayed():
                sleep(15)
            else:
                Joy188Test2.xpath_element('//*[@id="J-dice-bar"]/div[5]/a[1]')#下注
                Joy188Test2.result()
                Joy188Test2.XPATH('/html/body/div[14]/a[1]').click()#確認
            Joy188Test.select_PcOredrCode(Joy188Test.get_conn(1),user,lottery)
        
            print("方案編號: %s"%order_code[0])
                
    @staticmethod
    def test_bjkl8():
        sleep(3)
        dr.get(em_url+'/gameBet/bjkl8')
        print(dr.title)
        
        bjk_element = ['dd.renxuan%s'%i for i in range(1,8)]#任選1 到 任選7
        Joy188Test2.id_element('randomone')
        sleep(1)
        Joy188Test2.css_element('li.renxuan.normal')
        for element in bjk_element:
            Joy188Test2.css_element(element)
            sleep(0.5)
            Joy188Test2.id_element('randomone')
        
        Joy188Test2.id_element('J-submit-order')#馬上投注
        Joy188Test2.result()
        sleep(1)
        Joy188Test2.link_element("确 认")
        
        Joy188Test.select_PcOredrCode(Joy188Test.get_conn(1),user,'bjkl8')
        
        print("方案編號: %s"%order_code[0])
        
    @staticmethod
    def test_safepersonal():
        u"修改登入密碼"
        #print(post_url)
        dr.get(post_url+'/safepersonal/safecodeedit')
        print(dr.title)
        global passwd_dict
        passwd_dict = {# 環境 密碼先 開始
            0:['123qwe','amberrd'],1:['amberrd','123qwe']
        }
        password = ['amberrd','123qwe']
        Joy188Test2.ID( 'J-password').send_keys(passwd_dict[envs][0])
        print(u'當前登入密碼: %s'%passwd_dict[envs][0])
        Joy188Test2.ID( 'J-password-new').send_keys(passwd_dict[envs][1])
        Joy188Test2.ID( 'J-password-new2').send_keys(passwd_dict[envs][1])
        print(u'新登入密碼: %s,確認新密碼: %s'%(passwd_dict[envs][1],passwd_dict[envs][1]))
        Joy188Test2.ID( 'J-button-submit-text').click()
        sleep(2)
        if Joy188Test2.ID( 'Idivs').is_displayed():#成功修改密碼彈窗出現
            print(u'恭喜%s密码修改成功，请重新登录。'%user)
            Joy188Test2.ID( 'closeTip1').click()#關閉按紐,跳回登入頁
            sleep(1)
            Joy188Test2.ID( 'J-user-name').send_keys(user)
            Joy188Test2.ID( 'J-user-password').send_keys(passwd_dict[envs][1])
            Joy188Test2.ID( 'J-form-submit').click()
            sleep(4)
            print((dr.current_url))
            if dr.current_url == post_url+'/index':#判斷是否登入成功
                print(u'%s登入成功'%user)
                dr.get(post_url+'/safepersonal/safecodeedit')
                Joy188Test2.ID( 'J-password').send_keys(passwd_dict[envs][1])#在重新把密碼改回原本的amberrd
                Joy188Test2.ID( 'J-password-new').send_keys(passwd_dict[envs][0])
                Joy188Test2.ID( 'J-password-new2').send_keys(passwd_dict[envs][0])
                Joy188Test2.ID( 'J-button-submit-text').click()
                sleep(5)
            else:
                print(u'登入失敗')
                pass

        else:
            print(u'密碼輸入錯誤')
            pass
    @staticmethod
    def test_applycenter():
        u'開戶中心'
        sleep(2)
        OpenUrl_dict = {
            0: "/register?id=18417062&exp=1902283553071&pid=13412941&token=e618",
            1: "/register/?id=27402734&exp=1885877796573&pid=13732231&token=3738"
        }
        dr.get(post_url+OpenUrl_dict[envs])#kerr000的連結
        print(dr.title)
        global user_random
        user_random = user+'%s'%random.randint(1,1000000)#隨機生成 kerr下面用戶名
        print(u'註冊用戶名: %s'%user_random)
        Joy188Test2.ID('J-input-username').send_keys(user_random)#用戶名
        Joy188Test2.ID('J-input-password').send_keys(passwd_dict[envs][0])#第一次密碼
        Joy188Test2.ID('J-input-password2').send_keys(passwd_dict[envs][0])#在一次確認密碼
        Joy188Test2.ID('J-button-submit').click()#提交註冊        
        sleep(5)
        if dr.current_url == post_url + '/index':
            (u'kerr%s註冊成功'%user_random)
            print(post_url)
            print(u'%s登入成功'%user_random)
        else:
            print(u'登入失敗')
    @staticmethod
    def test_safecenter():
        u"安全中心"
        global safe_dict
        safe_dict = {0:['hsieh','hsieh123'],1: ['kerr','kerr123']}# 安全問題 .安全密碼
        sleep(3)
        dr.get(post_url+'/safepersonal/safecodeset')#安全密碼連結
        print(dr.title)
        Joy188Test2.ID('J-safePassword').send_keys(safe_dict[envs][1])
        Joy188Test2.ID('J-safePassword2').send_keys(safe_dict[envs][1])
        print(u'設置安全密碼/確認安全密碼: %s'%safe_dict[envs][1])
        Joy188Test2.ID('J-button-submit').click()
        if dr.current_url == post_url+ '/safepersonal/safecodeset?act=smt':#安全密碼成功Url
            print(u'恭喜%s安全密码设置成功！'%user_random)
        else:
            print(u'安全密碼設置失敗')
        dr.get(post_url+'/safepersonal/safequestset')#安全問題
        print(dr.title)
        for i in range(1,4,1):#J-answrer 1,2,3  
            Joy188Test2.ID('J-answer%s'%i).send_keys(safe_dict[envs][0])#問題答案
        for i in range(1,6,2):# i產生  1,3,5 li[i], 問題選擇
            Joy188Test2.XPATH('//*[@id="J-safe-question-select"]/li[%s]/select/option[2]'%i).click()
        Joy188Test2.ID('J-button-submit').click()#設置按鈕
        Joy188Test2.ID('J-safequestion-submit').click()#確認
        if dr.current_url == post_url +'/safepersonal/safequestset?act=smt':#安全問題成功url
            print(u'恭喜%s安全问题设置成功！'%user_random)
        else:
            print(u'安全問題設置失敗')
    @staticmethod
    def test_bindcard():
        u"銀行卡綁定"
        dr.get(post_url+ '/bindcard/bindcardsecurityinfo/')
        print(dr.title)
        fake = Factory.create()
        card = (fake.credit_card_number(card_type='visa16'))#產生一個16位的假卡號
        
        Joy188Test2.XPATH('//*[@id="bankid"]/option[2]').click()#開戶銀行選擇
        Joy188Test2.XPATH('//*[@id="province"]/option[2]').click()#所在城市  :北京
        Joy188Test2.ID('branchAddr').send_keys(u'內湖分行')#之行名稱
        Joy188Test2.ID('bankAccount').send_keys('kerr')#開戶人
        Joy188Test2.ID('bankNumber').send_keys(str(card))#銀行卡浩
        print(u'綁定銀行卡號: %s'%card)
        Joy188Test2.ID('bankNumber2').send_keys(str(card))#確認銀行卡浩
        Joy188Test2.ID('securityPassword').send_keys(safe_dict[envs][1])#安全密碼
        Joy188Test2.ID('J-Submit').click()#提交
        sleep(3)
        if Joy188Test2.ID('div_ok').is_displayed():
            print(u'%s银行卡绑定成功！'%user_random)
            Joy188Test2.ID('CloseDiv2').click()#關閉
        else:
            print(u'銀行卡綁定失敗')
    @staticmethod
    def test_bindcardUs():
        u"數字貨幣綁卡"
        dr.get(post_url+'/bindcard/bindcarddigitalwallet?bindcardType=2')
        print(dr.title)
        card = random.randint(1000,1000000000)#usdt數字綁卡,隨機生成
        Joy188Test2.ID('walletAddr').send_keys(str(card))
        print(u'提現錢包地址: %s'%card)
        Joy188Test2.ID('securityPassword').send_keys(safe_dict[envs][1])
        print(u'安全密碼:%s'%safe_dict[envs][1])
        Joy188Test2.ID('J-Submit').click()#提交
        sleep(3)
        if Joy188Test2.ID('div_ok').is_displayed():#彈窗出現
            print(u'%s数字货币钱包账户绑定成功！'%user_random)
            Joy188Test2.ID('CloseDiv2').click()
        else:
            print(u"數字貨幣綁定失敗")
        
    @classmethod
    def tearDownClass(cls):
        cls.dr.quit()


# In[168]:





# In[175]:


class Joy188Test3(unittest.TestCase):
    u'trunkAPP接口測試'
    def Iapi_LoginData(username,uuid_,passwd ):
        login_data = {
            "head": {
                "sessionId": ''
            },
            "body": {
                "param": {
                "username": username+"|"+ uuid_,
                "loginpassSource":passwd ,
                "appCode": 1,
                "uuid": uuid,
                "loginIp": 2130706433,
                "device": 2,
                "app_id": 9,
                "come_from": "3",
                "appname": "1"
            }
            }
            }
        return login_data
        
    @staticmethod
    def test_iapiLogin():
        '''APP登入測試'''
        account_ ={0: {'hsieh00':'總代','hsieh001':'一代','hsiehapp001':'一代','hsieh0620':'玩家'} 
                   ,1:{'kerr00':u'總代','kerr001':u'一代','kerrapp001':'二代','kerr010':'玩家'}
                  }
        global token_,userid_,loginpasssource,uuid
        token_  ={}
        userid_ ={}
        global App_header
        
        App_header = {
        'User-Agent': userAgent, 
        'Content-Type': 'application/json'
        }
        
        #判斷用戶是dev或188,  uuid和loginpasssource為固定值
        global env# ipai環境
        env_dict = {0:'dev',1:'188'}
        if envs == 0:
            env = 'http://10.13.22.152:8199/'
            uuid = "2D424FA3-D7D9-4BB2-BFDA-4561F921B1D5"
            loginpasssource = "fa0c0fd599eaa397bd0daba5f47e7151"# 123qwe 加密
        elif envs == 1:
            env = 'http://iphong.joy188.com/'
            uuid = 'f009b92edc4333fd'
            loginpasssource = "3bf6add0828ee17c4603563954473c1e"# amberrd加密
        else:
            pass
        #登入request的json
        for i in account_[envs].keys():
            if i in ['kerr010','hsieh0620']:# 玩家 會使用更換密碼街口
                Joy188Test.select_userPass(Joy188Test.get_conn(envs),i)#找出動態的密碼, 避免更換密碼被更動
                login_data = Joy188Test3.Iapi_LoginData(username=i,uuid_=uuid,passwd=password[0])
            else:
                login_data = Joy188Test3.Iapi_LoginData(username=i,uuid_=uuid,passwd=loginpasssource)
            try:
                #print(loginpasssource)
                r = requests.post(env+'front/login',data=json.dumps(login_data),headers= App_header)
                #print(r.json())
                token = r.json()['body']['result']['token']
                userid = r.json()['body']['result']['userid']
                token_.setdefault(i,token)
                userid_.setdefault(i,userid)
                print(u'APP登入成功,登入帳號: %s,登入身分: %s'%(i,account_[envs][i]))
                print("Token: %s"%token)
                print("Userid: %s"%userid)
            except ValueError as e:
                print(e)
                print(u"登入失敗")
                break
            #user_list.setdefault(userid,token) 
    def IapiData(user):
        data = {"head":{"sowner":"","rowner":"","msn":"","msnsn":"","userId":"","userAccount":"",
        "sessionId":token_[user]},"body":{"param":{"CGISESSID":token_[user],"app_id":"9",
        "come_from":"3","appname":"1"},"pager":{"startNo":"","endNo":""}}}
        return data
    @staticmethod
    def test_iapiCheckIn():
        '''APP簽到'''
        user = env_dict['APP帳號'][envs]
        data_ = Joy188Test3.IapiData(user)
        r = requests.post(env+'/exp/checkInByUserId',
                    data=json.dumps(data_),headers=App_header)
        if r.json()['head']['status'] == 0:
            print('%s 簽到成功'%user)
        else:
            print('%s 簽到確認')
    @staticmethod
    def test_iapiSubmit():
        '''APP投注'''
        #Joy188Test3.test_iapiLogin(user='kerr001',envir='188')# evir = 'dev','188'
        global user,order_dict
        user = env_dict['APP帳號'][envs]
        t = time.strftime('%Y%m%d %H:%M:%S')
        print(u'投注帳號: %s, 現在時間: %s'%(user,t))
        order_dict = {}# 存放  到時 要撤消單
        try:
            for i in lottery_dict.keys():
                while True:
            #for i in ['xyft','xyft168']:
                    now = int(time.time()*1000)#時間戳
                    lotteryid = lottery_dict[i][1]
                    if i in ['slmmc','sl115']:
                        break
                    elif i == 'pcdd': # 先寫死 固定完法 和投注內容, 因為動態完法 賠率會不同
                        Joy188Test.web_issuecode(i)
                        data_ = {"head":{"sowner":"","rowner":"","msn":"","msnsn":"","userId":"","userAccount":"",
                        "sessionId":token_[user]},"body":{"pager":{"startNo":"1","endNo":"99999"},"param":
                        {"saleTime":now,"userIp":"168627247","isFirstSubmit":0,"channelId":202,
                        "channelVersion":"2.0.21.0013","lotteryId":"99204","issue":issuecode,
                         "traceStop":0,"money":50,"redDiscountTotal":0,"awardGroupId":"263","list":
                         [{"methodid":"66_28_71","codes":"15","nums":1,"fileMode":0,"mode":1,
                           "odds":"12.32","times":1,"money":50,"awardMode":1}]}}}
                    else:
                        Joy188Test.web_issuecode(i)
                        ball_type_post = Joy188Test.game_type(i)#玩法和內容,0為玩法名稱, 1為投注內容
                        methodid = ball_type_post[0].replace('.','')#ex: housan.zhuiam.fushi , 把.去掉


                        #找出對應的玩法id , bet_type[0]
                        Joy188Test.select_betTypeCode(Joy188Test.get_conn(envs),lotteryid,methodid)
                        data_ = {"head":
                        {"sessionId":token_[user]},
                        "body":{"param":{"CGISESSID":token_[user],# 產生  kerr001的token
                        "lotteryId":str(lotteryid),"chan_id":1,"userid":1373224,
                        "money":2*mul,"issue":issuecode,"issueName":issuecode,"isFirstSubmit":0,
                        "list":[{"methodid":bet_type[0],"codes":ball_type_post[1],"nums":1,
                        "fileMode":0,"mode":1,"times":mul,"money":2*mul}],#times是倍數
                        "traceIssues":"","traceTimes":"","traceIstrace":0,
                        "saleTime":now,
                        "userIp":168627247,"channelId":402,"traceStop":0}}}
                        if i in ['btcffc','btcctp','xyft','xyft168']: #高獎金玩法 彩種
                            data_['body']['param']['list'][0]['awardMode'] = 2# 彼特幣分彩 需增加awarcmode

                    r = requests.post(env+'game/buy',data=json.dumps(data_),headers=App_header) 

                    if r.json()['head']['status'] == 0: #status0 為投注成功
                        print(u'%s投注成功'%lottery_dict[i][0])
                        print(play_)#投注完法 中文名稱
                        print(u"投注內容: %s"%ball_type_post[1])
                        print(u"投注金額: %s, 投注倍數: %s"%(2*mul,mul))#mul 為game_type方法對甕倍數
                        #print(r.json())
                        orderid = (r.json()['body']['result']['orderId'])
                        Joy188Test.select_orderCode(Joy188Test.get_conn(envs),orderid)#找出對應ordercode
                        #print('orderid: %s'%orderid)
                        print(u'投注單號: %s'%order_code[0])
                        print('------------------------------')
                        order_dict[i]  = {order_code[0]: orderid}# 存放, 後續 掣單使用
                        break
                    else:
                        pass
                        break

                        #pass
        except requests.exceptions.ConnectionError:
            print('please wait')
        except IndexError as e:
            print(e)
    @staticmethod
    def test_IapiTransfer():
        '''APP上下級轉帳'''
        user_dict = {
            0:['hsieh00','hsiehapp001'],
            1:['kerr00','kerrapp001']
        }
        user = user_dict[envs][0]# 上級用戶 
        user_ = user_dict[envs][1]#下級用戶
        while True:
            for i in user,user_:
                data = Joy188Test3.IapiData(i)
                r = requests.post(env+'/information/getBalance',
                    data=json.dumps(Joy188Test3.IapiData(i)),headers=App_header)
                balance =  r.json()['body']['result']['balance']
                print('%s用戶餘額: %s'%(i,balance))
            
            data = Joy188Test3.IapiData(user)#從新生成初始 data
            money = random.randint(1,100)#  隨機金額 格式 需成 10000
            transfer_data = {"applyTime": int(time.time()*1000), "direction":0,"isUpward":0,
            "rcvAccount":user_ ,"transferAmt":money*10000,"userId":userid_[user]}# 上下級轉帳data
            param_data = data["body"]["param"]
            param_data.update(transfer_data)
            data['body']['param'] = param_data
            r = requests.post(env+'fund/confirmFundTransfer',data=json.dumps(data),headers=App_header)
            if r.json()['head']['status'] !=0: # 發起提現
                print('發起上下級轉帳確認')
                break
            
            question_dict = {
                0: "\\u6211\\u6700\\u559c\\u6b22\\u7684\\u7403\\u661f\\uff1f",
                1: "\\u6211\\u6700\\u559c\\u6b22\\u7684\\u6f14\\u5458\\uff1f"
            }
            qid_dict = {0:4,1:3}
            #安全問題
            data = Joy188Test3.IapiData(user)#從新生成初始 data
            safeQuestVerify_data = {"quests":[{"qid":qid_dict[envs],
            "question":question_dict[envs],
            "qpwd":passwd_info[envs][1],"isUsed":1}]}
            param_data = data["body"]["param"]
            param_data.update(safeQuestVerify_data)
            data['body']['param'] = param_data
            r = requests.post(env+'security/safeQuestVerify',data=json.dumps(data),headers=App_header)
            if r.json()['head']['status'] !=0: 
                print('安全問題確認')
                break

            #安全密碼
            data = Joy188Test3.IapiData(user)#從新生成初始 data
            checkSecpass_data = {"secpass":passwd_info[envs][0],"isCheckLoginPassword":0}
            param_data = data["body"]["param"]
            param_data.update(checkSecpass_data)
            data['body']['param'] = param_data
            r = requests.post(env+'/security/checkSecpass',data=json.dumps(data)
                              ,headers=App_header)# 安全密碼確認
            if r.json()['head']['status'] !=0: 
                print('安全密碼確認')
                break
            #提現提交
            data = Joy188Test3.IapiData(user)#從新生成初始 data
            confirm_data = {"applyTime": int(time.time()*1000), "direction":0,"isUpward":0,
            "rcvAccount":user_ ,"transferAmt":money*10000,"userId":userid_[user]}
            param_data = data["body"]["param"]
            param_data.update(confirm_data)
            data['body']['param'] = param_data
            r = requests.post(env+'fund/fundTransfer',data=json.dumps(data),headers=App_header)
            if r.json()['head']['status'] !=0: 
                print('上下級轉帳提交確認')# 確認
                break
            print('上級: %s 轉帳給下級: %s .金額: %s 成功'%(user,user_,money))
            for i in user,user_:
                data = Joy188Test3.IapiData(i)
                r = requests.post(env+'/information/getBalance',
                    data=json.dumps(Joy188Test3.IapiData(i)),headers=App_header)
                balance =  r.json()['body']['result']['balance']
                print('%s用戶餘額: %s'%(i,balance))
            break
        
        
        
    
    @staticmethod
    def test_IapiRecharge():
        '''APP充值發起'''
        user = env_dict['一般帳號'][envs]

        admin_fund = {# 後台 充值相關配置 , dev: APP 三合 . 188: APP plg
            0: "userGroupSetting[4][]=247&singleLowlimit[4]=1&singleUplimit[4]=10&dailyUplimit[4]=1000&chargeWaySet[4]=11&platform[4]=1&id[4]=90&isOpen[4]=N&userGroupSetting[15][]=247&singleLowlimit[15]=1&singleUplimit[15]=1000&dailyUplimit[15]=1000&chargeWaySet[15]=11&platform[15]=1&id[15]=62&isOpen[15]=Y&userGroupSetting[29][]=247&singleLowlimit[29]=1&singleUplimit[29]=100&dailyUplimit[29]=10000&chargeWaySet[29]=11&platform[29]=1&id[29]=100&isOpen[29]=N&userGroupSetting[41][]=247&singleLowlimit[41]=103&singleUplimit[41]=103&dailyUplimit[41]=1000&chargeWaySet[41]=11&platform[41]=1&id[41]=122&isOpen[41]=N&userGroupSetting[56][]=247&singleLowlimit[56]=104&singleUplimit[56]=104&dailyUplimit[56]=1000&chargeWaySet[56]=11&platform[56]=1&id[56]=107&isOpen[56]=N&userGroupSetting[64][]=247&singleLowlimit[64]=105&singleUplimit[64]=105&dailyUplimit[64]=1000&chargeWaySet[64]=11&platform[64]=1&id[64]=124&isOpen[64]=N&userGroupSetting[89][]=247&singleLowlimit[89]=1&singleUplimit[89]=10000&dailyUplimit[89]=10000&chargeWaySet[89]=11&platform[89]=1&id[89]=180&isOpen[89]=N&userGroupSetting[105][]=247&userGroupSetting[105][]=704&singleLowlimit[105]=20&singleUplimit[105]=5000&dailyUplimit[105]=100000&chargeWaySet[105]=11&platform[105]=1&id[105]=172&isOpen[105]=N",
            1: "userGroupSetting[4][]=27&singleLowlimit[4]=1&singleUplimit[4]=200&dailyUplimit[4]=0&chargeWaySet[4]=11&platform[4]=1&id[4]=90&isOpen[4]=N&userGroupSetting[15][]=27&singleLowlimit[15]=1&singleUplimit[15]=100000&dailyUplimit[15]=4500000&chargeWaySet[15]=11&platform[15]=1&id[15]=62&isOpen[15]=N&userGroupSetting[29][]=27&singleLowlimit[29]=102&singleUplimit[29]=102&dailyUplimit[29]=10000&chargeWaySet[29]=11&platform[29]=1&id[29]=100&isOpen[29]=N&userGroupSetting[41][]=27&singleLowlimit[41]=103&singleUplimit[41]=103&dailyUplimit[41]=1000&chargeWaySet[41]=11&platform[41]=1&id[41]=122&isOpen[41]=N&userGroupSetting[59][]=27&singleLowlimit[59]=5000&singleUplimit[59]=80000&dailyUplimit[59]=1000&chargeWaySet[59]=11&platform[59]=1&id[59]=107&isOpen[59]=N&userGroupSetting[67][]=27&singleLowlimit[67]=105&singleUplimit[67]=105&dailyUplimit[67]=1000&chargeWaySet[67]=11&platform[67]=1&id[67]=124&isOpen[67]=N&userGroupSetting[84][]=27&singleLowlimit[84]=1&singleUplimit[84]=10000&dailyUplimit[84]=10000&chargeWaySet[84]=11&platform[84]=1&id[84]=148&isOpen[84]=Y&userGroupSetting[113][]=27&singleLowlimit[113]=1&singleUplimit[113]=5000&dailyUplimit[113]=100000&chargeWaySet[113]=11&platform[113]=1&id[113]=181&isOpen[113]=N"
        }
        recharge_data = admin_fund[envs]
        r = admin_session.post(admin_url+'/admin/Rechargemange/index?parma=saveBypassCfg',
        headers=admin_header,
        data=recharge_data)# 後台 將 APP 銀聯掃馬 後台 開啟三和一個渠道 ,避免 發起充值 時 ,渠道沒開

        data_ = Joy188Test3.IapiData(user)
        money = random.randint(10,20)#  隨機金額
        fund_data = {"bankId":37,"money":money,"bankAccount":"","exchangeRate":"6.37",
        "cashBackSetId":None,"cashBackSetType":None,"originalCurrencyAmount":0,"userId":userid_[user],
        "customerIp":"10.13.12.47","system":1}
        param_data = data_["body"]["param"]
        param_data.update(fund_data)
        data_['body']['param'] = param_data
        
        r = requests.post(env+'recharge/quickCommit',data=json.dumps(data_),headers=App_header) 
        if r.json()['head']['status'] in [901000,0]:
            sn = Joy188Test.select_FundSn(Joy188Test.get_conn(envs),userid_[user])
            print('%s 充值發起成功 金額: %s, 單號:%s'%(user,money,sn))
        else:
            print('%s 充值發起失敗'%user)
                
    @staticmethod
    def test_IapiCancelSubmit():
        '''APP撤消投注'''
        user = env_dict['APP帳號'][envs]
        ran_  = random.randint(0,len(cancel_lottery_list))# 隨機長
        try:
            can_lottery = cancel_lottery_list[ran_]# 要被撤消的彩種
        except IndexError:
            ran_  = random.randint(0,3)# 隨機長
            can_lottery = cancel_lottery_list[ran_]# 要被撤消的彩種
        orderid = list(order_dict[can_lottery].values())[0]
        
        data_ = {"head":{"sowner":"","rowner":"","msn":"","msnsn":"","userId":"","userAccount":"","sessionId":token_[user]},"body":{"pager":{"startNo":"1","endNo":"99999"},"param":{
            "CGISESSID":token_[user],"id": str(orderid),"app_id":"9","come_from":"3","appname":"1"}}}
        r = requests.post(env+'game/cancelGame',data=json.dumps(data_),headers=App_header)
        print('撤消彩種: %s ,方案編號: %s '%(lottery_dict[can_lottery][0] ,
                                     list(order_dict[can_lottery].keys())[0]))  
        if r.json()['head']['status'] == 0:
            print('撤消成功')
        else:
            print('撤銷失敗')
            
    @staticmethod
    def test_OpenLink():
        '''APP開戶中心'''
        user = env_dict['一般帳號'][envs]
        data_ = Joy188Test3.IapiData(user)
        param_data = data_["body"]["param"]
        #info_dict ,dev和 188會因為用戶反點不同而不同
        info_dict = {0: [{"lotteryId":"77101","lotteryName":"\\u4e50\\u5229\\u771f\\u4eba\\u5f69",
        "lotterySeriesCode":10,"lotterySeriesName":"\\u771f\\u4eba\\u5f69\\u7968","awardGroupId":77101,"awardName":"\\u5956\\u91d1\\u7ec41800","directRet":"290","directLimitRet":500},
        {"lotteryId":"99101","lotteryName":"\\u6b22\\u4e50\\u751f\\u8096","lotterySeriesCode":1,
         "lotterySeriesName":"\\u65f6\\u65f6\\u5f69\\u7cfb","awardGroupId":12,"awardName":"\\u5956\\u91d1\\u7ec41800","directRet":"290","threeoneRet":"290","directLimitRet":500,"threeLimitRet":500,"superLimitRet":100},{"lotteryId":"99103","lotteryName":"\\u65b0\\u7586\\u65f6\\u65f6\\u5f69","lotterySeriesCode":1,"lotterySeriesName":"\\u65f6\\u65f6\\u5f69\\u7cfb","awardGroupId":19,"awardName":"\\u5956\\u91d1\\u7ec41800","directRet":"290","threeoneRet":"290","directLimitRet":500,"threeLimitRet":500,"superLimitRet":100},{"lotteryId":"99104","lotteryName":"\\u5929\\u6d25\\u65f6\\u65f6\\u5f69","lotterySeriesCode":1,"lotterySeriesName":"\\u65f6\\u65f6\\u5f69\\u7cfb","awardGroupId":36,"awardName":"\\u5956\\u91d1\\u7ec41800","directRet":"290","threeoneRet":"290","directLimitRet":500,"threeLimitRet":500,"superLimitRet":100},{"lotteryId":"99105","lotteryName":"\\u9ed1\\u9f99\\u6c5f\\u65f6\\u65f6\\u5f69","lotterySeriesCode":1,"lotterySeriesName":"\\u65f6\\u65f6\\u5f69\\u7cfb","awardGroupId":13,"awardName":"\\u5956\\u91d1\\u7ec41800","directRet":"290","threeoneRet":"290","directLimitRet":500,"threeLimitRet":500,"superLimitRet":100},{"lotteryId":"99105","lotteryName":"\\u9ed1\\u9f99\\u6c5f\\u65f6\\u65f6\\u5f69","lotterySeriesCode":1,"lotterySeriesName":"\\u65f6\\u65f6\\u5f69\\u7cfb","awardGroupId":5,"awardName":"\\u5956\\u91d1\\u7ec41700","directRet":"790","threeoneRet":"290","directLimitRet":1000,"threeLimitRet":500,"superLimitRet":100},{"lotteryId":"99105","lotteryName":"\\u9ed1\\u9f99\\u6c5f\\u65f6\\u65f6\\u5f69","lotterySeriesCode":1,"lotterySeriesName":"\\u65f6\\u65f6\\u5f69\\u7cfb","awardGroupId":16,"awardName":"\\u5956\\u91d1\\u7ec41500","directRet":"1790","threeoneRet":"1090","directLimitRet":2000,"threeLimitRet":1300,"superLimitRet":100},{"lotteryId":"99106","lotteryName":"\\u51e4\\u51f0\\u4e50\\u5229\\u65f6\\u65f6\\u5f69","lotterySeriesCode":1,"lotterySeriesName":"\\u65f6\\u65f6\\u5f69\\u7cfb","awardGroupId":33,"awardName":"\\u5956\\u91d1\\u7ec41800","directRet":"290","threeoneRet":"290","directLimitRet":500,"threeLimitRet":500},{"lotteryId":"99107","lotteryName":"\\u4e0a\\u6d77\\u65f6\\u65f6\\u4e50","lotterySeriesCode":1,"lotterySeriesName":"\\u65f6\\u65f6\\u5f69\\u7cfb","awardGroupId":15,"awardName":"\\u5956\\u91d1\\u7ec41800","directRet":"290","threeoneRet":"290","directLimitRet":500,"threeLimitRet":500},{"lotteryId":"99108","lotteryName":"3D","lotterySeriesCode":2,"lotterySeriesName":"3D\\u7cfb","awardGroupId":101,"awardName":"\\u5956\\u91d1\\u7ec41700","directRet":"790","threeoneRet":"290","directLimitRet":1000,"threeLimitRet":500},{"lotteryId":"99109","lotteryName":"P5","lotterySeriesCode":2,"lotterySeriesName":"3D\\u7cfb","awardGroupId":102,"awardName":"\\u5956\\u91d1\\u7ec41700","directRet":"790","threeoneRet":"290","directLimitRet":1000,"threeLimitRet":500},{"lotteryId":"99111","lotteryName":"\\u51e4\\u51f0\\u5409\\u5229\\u5206\\u5206\\u5f69","lotterySeriesCode":1,"lotterySeriesName":"\\u65f6\\u65f6\\u5f69\\u7cfb","awardGroupId":41,"awardName":"\\u5956\\u91d1\\u7ec41800","directRet":"290","threeoneRet":"290","directLimitRet":500,"threeLimitRet":500},{"lotteryId":"99112","lotteryName":"\\u51e4\\u51f0\\u987a\\u5229\\u79d2\\u79d2\\u5f69","lotterySeriesCode":1,"lotterySeriesName":"\\u65f6\\u65f6\\u5f69\\u7cfb","awardGroupId":56,"awardName":"\\u5956\\u91d1\\u7ec41800","directRet":"290","threeoneRet":"290","directLimitRet":500,"threeLimitRet":500},{"lotteryId":"99113","lotteryName":"\\u8d85\\u7ea72000\\u79d2\\u79d2\\u5f69(APP\\u7248)","lotterySeriesCode":1,"lotterySeriesName":"\\u65f6\\u65f6\\u5f69\\u7cfb","awardGroupId":11416083,"awardName":"2000\\u5956\\u91d1\\u7ec4","superLimitRet":100},{"lotteryId":"99114","lotteryName":"\\u817e\\u8baf\\u5206\\u5206\\u5f69","lotterySeriesCode":1,"lotterySeriesName":"\\u65f6\\u65f6\\u5f69\\u7cfb","awardGroupId":208,"awardName":"\\u5956\\u91d1\\u7ec41800","directRet":"290","threeoneRet":"290","directLimitRet":500,"threeLimitRet":500},{"lotteryId":"99115","lotteryName":"\\u51e4\\u51f0\\u6bd4\\u7279\\u5e01\\u5206\\u5206\\u5f69","lotterySeriesCode":1,"lotterySeriesName":"\\u65f6\\u65f6\\u5f69\\u7cfb","awardGroupId":214,"awardName":"\\u5956\\u91d1\\u7ec41000","directRet":"4590","threeoneRet":"4590","directLimitRet":4800,"threeLimitRet":4800},{"lotteryId":"99116","lotteryName":"\\u51e4\\u51f0\\u5409\\u5229\\u65f6\\u65f6\\u5f69","lotterySeriesCode":1,"lotterySeriesName":"\\u65f6\\u65f6\\u5f69\\u7cfb","awardGroupId":228,"awardName":"\\u5956\\u91d1\\u7ec41800","directRet":"290","threeoneRet":"290","directLimitRet":500,"threeLimitRet":500,"superLimitRet":100},{"lotteryId":"99117","lotteryName":"\\u51e4\\u51f0\\u91cd\\u5e86\\u5168\\u7403\\u5f69","lotterySeriesCode":1,"lotterySeriesName":"\\u65f6\\u65f6\\u5f69\\u7cfb","awardGroupId":263,"awardName":"\\u5956\\u91d1\\u7ec41800","directRet":"290","threeoneRet":"290","directLimitRet":500,"threeLimitRet":500,"superLimitRet":100},{"lotteryId":"99118","lotteryName":"\\u51e4\\u51f0\\u65b0\\u7586\\u5168\\u7403\\u5f69","lotterySeriesCode":1,"lotterySeriesName":"\\u65f6\\u65f6\\u5f69\\u7cfb","awardGroupId":264,"awardName":"\\u5956\\u91d1\\u7ec41800","directRet":"290","threeoneRet":"290","directLimitRet":500,"threeLimitRet":500,"superLimitRet":100},{"lotteryId":"99119","lotteryName":"\\u6cb3\\u5185\\u5206\\u5206\\u5f69","lotterySeriesCode":1,"lotterySeriesName":"\\u65f6\\u65f6\\u5f69\\u7cfb","awardGroupId":268,"awardName":"\\u5956\\u91d1\\u7ec41800","directRet":"290","threeoneRet":"290","directLimitRet":500,"threeLimitRet":500},{"lotteryId":"99120","lotteryName":"\\u6cb3\\u5185\\u4e94\\u5206\\u5f69","lotterySeriesCode":1,"lotterySeriesName":"\\u65f6\\u65f6\\u5f69\\u7cfb","awardGroupId":273,"awardName":"\\u5956\\u91d1\\u7ec41800","directRet":"290","threeoneRet":"290","directLimitRet":500,"threeLimitRet":500,"superLimitRet":100},{"lotteryId":"99121","lotteryName":"360\\u5206\\u5206\\u5f69","lotterySeriesCode":1,"lotterySeriesName":"\\u65f6\\u65f6\\u5f69\\u7cfb","awardGroupId":274,"awardName":"\\u5956\\u91d1\\u7ec41800","directRet":"290","threeoneRet":"290","directLimitRet":500,"threeLimitRet":500},{"lotteryId":"99122","lotteryName":"360\\u4e94\\u5206\\u5f69","lotterySeriesCode":1,"lotterySeriesName":"\\u65f6\\u65f6\\u5f69\\u7cfb","awardGroupId":275,"awardName":"\\u5956\\u91d1\\u7ec41800","directRet":"290","threeoneRet":"290","directLimitRet":500,"threeLimitRet":500,"superLimitRet":100},{"lotteryId":"99123","lotteryName":"\\u8d8a\\u5357\\u798f\\u5f69","lotterySeriesCode":2,"lotterySeriesName":"3D\\u7cfb","awardGroupId":278,"awardName":"\\u5956\\u91d1\\u7ec41800","directRet":"290","threeoneRet":"290","directLimitRet":500,"threeLimitRet":500},{"lotteryId":"99124","lotteryName":"\\u8d8a\\u53573D\\u798f\\u5f69","lotterySeriesCode":2,"lotterySeriesName":"3D\\u7cfb","awardGroupId":279,"awardName":"\\u5956\\u91d1\\u7ec41800","directRet":"290","threeoneRet":"290","directLimitRet":500,"threeLimitRet":500},{"lotteryId":"99125","lotteryName":"\\u5947\\u8da3\\u817e\\u8baf\\u5206\\u5206\\u5f69","lotterySeriesCode":1,"lotterySeriesName":"\\u65f6\\u65f6\\u5f69\\u7cfb","awardGroupId":308,"awardName":"\\u5956\\u91d1\\u7ec41800","directRet":"290","threeoneRet":"290","directLimitRet":500,"threeLimitRet":500},{"lotteryId":"99126","lotteryName":"\\u591a\\u5f69\\u6cb3\\u5185\\u5206\\u5206\\u5f69","lotterySeriesCode":1,"lotterySeriesName":"\\u65f6\\u65f6\\u5f69\\u7cfb","awardGroupId":316,"awardName":"\\u5956\\u91d1\\u7ec41800","directRet":"290","threeoneRet":"290","directLimitRet":500,"threeLimitRet":500},{"lotteryId":"99201","lotteryName":"\\u5317\\u4eac\\u5feb\\u4e508","lotterySeriesCode":4,"lotterySeriesName":"\\u57fa\\u8bfa\\u7cfb","awardGroupId":32,"awardName":"\\u6df7\\u5408\\u5956\\u91d1\\u7ec4","directRet":"1290","threeoneRet":"790","directLimitRet":1500,"threeLimitRet":1000},{"lotteryId":"99202","lotteryName":"PK10","lotterySeriesCode":4,"lotterySeriesName":"\\u57fa\\u8bfa\\u7cfb","awardGroupId":206,"awardName":"\\u5956\\u91d1\\u7ec41800","directRet":"290","directLimitRet":500},{"lotteryId":"99203","lotteryName":"\\u98de\\u8247","lotterySeriesCode":4,"lotterySeriesName":"\\u57fa\\u8bfa\\u7cfb","awardGroupId":233,"awardName":"\\u5956\\u91d1\\u7ec41000","directRet":"4590","directLimitRet":4800},{"lotteryId":"99204","lotteryName":"PC\\u86cb\\u86cb","lotterySeriesCode":4,"lotterySeriesName":"\\u57fa\\u8bfa\\u7cfb","awardGroupId":283,"awardName":"\\u5956\\u91d1\\u7ec41800","directRet":"290","directLimitRet":500},{"lotteryId":"99205","lotteryName":"168\\u98de\\u8247","lotterySeriesCode":4,"lotterySeriesName":"\\u57fa\\u8bfa\\u7cfb","awardGroupId":293,"awardName":"\\u5956\\u91d1\\u7ec41000","directRet":"4590","directLimitRet":4800},{"lotteryId":"99206","lotteryName":"\\u798f\\u5f69\\u5feb\\u4e508","lotterySeriesCode":4,"lotterySeriesName":"\\u57fa\\u8bfa\\u7cfb","awardGroupId":298,"awardName":"\\u6df7\\u5408\\u5956\\u91d1\\u7ec4","directRet":"1290","threeoneRet":"790","directLimitRet":1500,"threeLimitRet":1000},{"lotteryId":"99207","lotteryName":"\\u5feb\\u4e508\\u5168\\u7403\\u5f69","lotterySeriesCode":4,"lotterySeriesName":"\\u57fa\\u8bfa\\u7cfb","awardGroupId":303,"awardName":"\\u6df7\\u5408\\u5956\\u91d1\\u7ec4","directRet":"1290","threeoneRet":"790","directLimitRet":1500,"threeLimitRet":1000},{"lotteryId":"99301","lotteryName":"\\u5c71\\u4e1c11\\u90095","lotterySeriesCode":3,"lotterySeriesName":"11\\u90095\\u7cfb","awardGroupId":24,"awardName":"\\u5956\\u91d1\\u7ec41782","directRet":"290","directLimitRet":500},{"lotteryId":"99302","lotteryName":"\\u6c5f\\u897f11\\u90095","lotterySeriesCode":3,"lotterySeriesName":"11\\u90095\\u7cfb","awardGroupId":27,"awardName":"\\u5956\\u91d1\\u7ec41782","directRet":"290","directLimitRet":500},{"lotteryId":"99303","lotteryName":"\\u5e7f\\u4e1c11\\u90095","lotterySeriesCode":3,"lotterySeriesName":"11\\u90095\\u7cfb","awardGroupId":29,"awardName":"\\u5956\\u91d1\\u7ec41782","directRet":"290","directLimitRet":500},{"lotteryId":"99306","lotteryName":"\\u51e4\\u51f0\\u987a\\u522911\\u90095","lotterySeriesCode":3,"lotterySeriesName":"11\\u90095\\u7cfb","awardGroupId":192,"awardName":"\\u5956\\u91d1\\u7ec41782","directRet":"290","directLimitRet":500},{"lotteryId":"99401","lotteryName":"\\u53cc\\u8272\\u7403","lotterySeriesCode":5,"lotterySeriesName":"\\u53cc\\u8272\\u7403\\u7cfb","awardGroupId":107,"awardName":"\\u53cc\\u8272\\u7403\\u5956\\u91d1\\u7ec4","directRet":"790","directLimitRet":1000},{"lotteryId":"99501","lotteryName":"\\u6c5f\\u82cf\\u5feb\\u4e09","lotterySeriesCode":6,"lotterySeriesName":"\\u5feb\\u4e50\\u5f69\\u7cfb","awardGroupId":188,"awardName":"\\u6df7\\u5408\\u5956\\u91d1\\u7ec4","directRet":"590","directLimitRet":800},{"lotteryId":"99502","lotteryName":"\\u5b89\\u5fbd\\u5feb\\u4e09","lotterySeriesCode":6,"lotterySeriesName":"\\u5feb\\u4e50\\u5f69\\u7cfb","awardGroupId":190,"awardName":"\\u6df7\\u5408\\u5956\\u91d1\\u7ec4","directRet":"590","directLimitRet":800},{"lotteryId":"99601","lotteryName":"\\u6c5f\\u82cf\\u9ab0\\u5b9d","lotterySeriesCode":7,"lotterySeriesName":"\\u5feb\\u4e50\\u5f69\\u7cfb","awardGroupId":189,"awardName":"\\u6df7\\u5408\\u5956\\u91d1\\u7ec4","directRet":"290","directLimitRet":500},{"lotteryId":"99602","lotteryName":"\\u51e4\\u51f0\\u5409\\u5229\\u9ab0\\u5b9d(\\u5a31\\u4e50\\u5385)","lotterySeriesCode":7,"lotterySeriesName":"\\u5feb\\u4e50\\u5f69\\u7cfb","awardGroupId":203,"awardName":"\\u6df7\\u5408\\u5956\\u91d1\\u7ec4","directRet":"290","directLimitRet":500},{"lotteryId":"99603","lotteryName":"\\u51e4\\u51f0\\u5409\\u5229\\u9ab0\\u5b9d(\\u81f3\\u5c0a\\u5385)","lotterySeriesCode":7,"lotterySeriesName":"\\u5feb\\u4e50\\u5f69\\u7cfb","awardGroupId":204,"awardName":"\\u6df7\\u5408\\u5956\\u91d1\\u7ec4","directRet":"290","directLimitRet":500},{"lotteryId":"99604","lotteryName":"\\u5b89\\u5fbd\\u9ab0\\u5b9d","lotterySeriesCode":7,"lotterySeriesName":"\\u5feb\\u4e50\\u5f69\\u7cfb","awardGroupId":11416087,"awardName":"\\u6df7\\u5408\\u5956\\u91d1\\u7ec4","directRet":"290","directLimitRet":500},{"lotteryId":"99605","lotteryName":"\\u51e4\\u51f0\\u987a\\u5229\\u9ab0\\u5b9d","lotterySeriesCode":7,"lotterySeriesName":"\\u5feb\\u4e50\\u5f69\\u7cfb","awardGroupId":207,"awardName":"\\u6df7\\u5408\\u5956\\u91d1\\u7ec4","directRet":"290","directLimitRet":500,"threeLimitRet":150},{"lotteryId":"99701","lotteryName":"\\u516d\\u5408\\u5f69","lotterySeriesCode":9,"lotterySeriesName":"\\u516d\\u5408\\u7cfb","awardGroupId":202,"awardName":"\\u516d\\u5408\\u5f69\\u5956\\u91d1\\u7ec4","directRet":"1190","lhcFlatcode":"190","lhcYear":"90","lhcColor":"90","lhcHalfwave":"90","lhcNotin":"90","lhcContinuein23":"90","lhcContinuein4":"290","lhcContinuein5":"290","lhcContinuenotin23":"90","lhcContinuenotin4":"290","lhcContinuenotin5":"290","lhcContinuecode":"290","directLimitRet":1400,"lhcYearLimit":300,"lhcColorLimit":300,"lhcFlatcodeLimit":400,"lhcHalfwaveLimit":300,"lhcOneyearLimit":200,"lhcNotinLimit":300,"lhcContinuein23Limit":300,"lhcContinuein4Limit":500,"lhcContinuein5Limit":500,"lhcContinuenotin23Limit":300,"lhcContinuenotin4Limit":500,"lhcContinuenotin5Limit":500,"lhcContinuecodeLimit":500},{"lotteryId":"99801","lotteryName":"\\u51e4\\u51f0\\u5409\\u52293D","lotterySeriesCode":2,"lotterySeriesName":"3D\\u7cfb","awardGroupId":223,"awardName":"\\u5956\\u91d1\\u7ec41800","directRet":"290","threeoneRet":"290","directLimitRet":500,"threeLimitRet":500},{"lotteryId":"99901","lotteryName":"\\u5feb\\u5f00","lotterySeriesCode":11,"lotterySeriesName":"\\u9ad8\\u9891\\u5f69\\u7cfb",
        "awardGroupId":238,"awardName":"\\u5956\\u91d1\\u7ec41800","directLimitRet":200}]
                , 1: [{"lotteryId": "77101", "lotterySeriesCode": 10, "lotterySeriesName": "\\\\u771f\\\\u4eba\\\\u5f69\\\\u7968", "awardGroupId": 77101, "awardName": "\\\\u5956\\\\u91d1\\\\u7ec41800", "directLimitRet": 450, "directRet": 0, "threeoneRet": 0, "superRet": 0}, {"lotteryId": "99101", "lotterySeriesCode": 1, "lotterySeriesName": "\\\\u65f6\\\\u65f6\\\\u5f69\\\\u7cfb", "awardGroupId": 12, "awardName": "\\\\u5956\\\\u91d1\\\\u7ec41800", "directLimitRet": 450, "threeLimitRet": 450, "directRet": 0, "threeoneRet": 0, "superRet": 0}, {"lotteryId": "99103", "lotterySeriesCode": 1, "lotterySeriesName": "\\\\u65f6\\\\u65f6\\\\u5f69\\\\u7cfb", "awardGroupId": 19, "awardName": "\\\\u5956\\\\u91d1\\\\u7ec41800", "directLimitRet": 450, "threeLimitRet": 450, "directRet": 0, "threeoneRet": 0, "superRet": 0}, {"lotteryId": "99104", "lotterySeriesCode": 1, "lotterySeriesName": "\\\\u65f6\\\\u65f6\\\\u5f69\\\\u7cfb", "awardGroupId": 36, "awardName": "\\\\u5956\\\\u91d1\\\\u7ec41800", "directLimitRet": 450, "threeLimitRet": 405, "directRet": 0, "threeoneRet": 0, "superRet": 0}, {"lotteryId": "99105", "lotterySeriesCode": 1, "lotterySeriesName": "\\\\u65f6\\\\u65f6\\\\u5f69\\\\u7cfb", "awardGroupId": 13, "awardName": "\\\\u5956\\\\u91d1\\\\u7ec41800", "directLimitRet": 450, "threeLimitRet": 450, "directRet": 0, "threeoneRet": 0, "superRet": 0}, {"lotteryId": "99106", "lotterySeriesCode": 1, "lotterySeriesName": "\\\\u65f6\\\\u65f6\\\\u5f69\\\\u7cfb", "awardGroupId": 33, "awardName": "\\\\u5956\\\\u91d1\\\\u7ec41800", "directLimitRet": 450, "threeLimitRet": 450, "directRet": 0, "threeoneRet": 0, "superRet": 0}, {"lotteryId": "99107", "lotterySeriesCode": 1, "lotterySeriesName": "\\\\u65f6\\\\u65f6\\\\u5f69\\\\u7cfb", "awardGroupId": 15, "awardName": "\\\\u5956\\\\u91d1\\\\u7ec41800", "directLimitRet": 450, "threeLimitRet": 450, "directRet": 0, "threeoneRet": 0, "superRet": 0}, {"lotteryId": "99108", "lotterySeriesCode": 2, "lotterySeriesName": "3D\\\\u7cfb", "awardGroupId": 101, "awardName": "\\\\u5956\\\\u91d1\\\\u7ec41700", "directLimitRet": 950, "threeLimitRet": 450, "directRet": 0, "threeoneRet": 0, "superRet": 0}, {"lotteryId": "99109", "lotterySeriesCode": 2, "lotterySeriesName": "3D\\\\u7cfb", "awardGroupId": 102, "awardName": "\\\\u5956\\\\u91d1\\\\u7ec41700", "directLimitRet": 950, "threeLimitRet": 450, "directRet": 0, "threeoneRet": 0, "superRet": 0}, {"lotteryId": "99111", "lotterySeriesCode": 1, "lotterySeriesName": "\\\\u65f6\\\\u65f6\\\\u5f69\\\\u7cfb", "awardGroupId": 41, "awardName": "\\\\u5956\\\\u91d1\\\\u7ec41800", "directLimitRet": 450, "threeLimitRet": 450, "directRet": 0, "threeoneRet": 0, "superRet": 0}, {"lotteryId": "99112", "lotterySeriesCode": 1, "lotterySeriesName": "\\\\u65f6\\\\u65f6\\\\u5f69\\\\u7cfb", "awardGroupId": 56, "awardName": "\\\\u5956\\\\u91d1\\\\u7ec41800", "directLimitRet": 450, "threeLimitRet": 450, "directRet": 0, "threeoneRet": 0, "superRet": 0}, {"lotteryId": "99113", "lotterySeriesCode": 1, "lotterySeriesName": "\\\\u65f6\\\\u65f6\\\\u5f69\\\\u7cfb", "awardGroupId": 205, "awardName": "2000\\\\u5956\\\\u91d1\\\\u7ec4", "superLimitRet": 90, "directRet": 0, "threeoneRet": 0, "superRet": 0}, {"lotteryId": "99114", "lotterySeriesCode": 1, "lotterySeriesName": "\\\\u65f6\\\\u65f6\\\\u5f69\\\\u7cfb", "awardGroupId": 208, "awardName": "\\\\u5956\\\\u91d1\\\\u7ec41800", "directLimitRet": 450, "threeLimitRet": 450, "directRet": 0, "threeoneRet": 0, "superRet": 0}, {"lotteryId": "99115", "lotterySeriesCode": 1, "lotterySeriesName": "\\\\u65f6\\\\u65f6\\\\u5f69\\\\u7cfb", "awardGroupId": 219, "awardName": "\\\\u5956\\\\u91d1\\\\u7ec41000", "directLimitRet": 4300, "threeLimitRet": 4300, "directRet": 0, "threeoneRet": 0, "superRet": 0}, {"lotteryId": "99116", "lotterySeriesCode": 1, "lotterySeriesName": "\\\\u65f6\\\\u65f6\\\\u5f69\\\\u7cfb", "awardGroupId": 231, "awardName": "\\\\u5956\\\\u91d1\\\\u7ec41800", "directLimitRet": 450, "threeLimitRet": 450, "directRet": 0, "threeoneRet": 0, "superRet": 0}, {"lotteryId": "99117", "lotterySeriesCode": 1, "lotterySeriesName": "\\\\u65f6\\\\u65f6\\\\u5f69\\\\u7cfb", "awardGroupId": 248, "awardName": "\\\\u5956\\\\u91d1\\\\u7ec41800", "directLimitRet": 450, "threeLimitRet": 450, "directRet": 0, "threeoneRet": 0, "superRet": 0}, {"lotteryId": "99118", "lotterySeriesCode": 1, "lotterySeriesName": "\\\\u65f6\\\\u65f6\\\\u5f69\\\\u7cfb", "awardGroupId": 249, "awardName": "\\\\u5956\\\\u91d1\\\\u7ec41800", "directLimitRet": 450, "threeLimitRet": 450, "directRet": 0, "threeoneRet": 0, "superRet": 0}, {"lotteryId": "99201", "lotterySeriesCode": 4, "lotterySeriesName": "\\\\u57fa\\\\u8bfa\\\\u7cfb", "awardGroupId": 32, "awardName": "\\\\u6df7\\\\u5408\\\\u5956\\\\u91d1\\\\u7ec4", "directRet": 0, "threeoneRet": 0, "superRet": 0}, {"lotteryId": "99202", "lotterySeriesCode": 4, "lotterySeriesName": "\\\\u57fa\\\\u8bfa\\\\u7cfb", "awardGroupId": 206, "awardName": "\\\\u5956\\\\u91d1\\\\u7ec41800", "directRet": 0, "threeoneRet": 0, "superRet": 0}, {"lotteryId": "99203", "lotterySeriesCode": 4, "lotterySeriesName": "\\\\u57fa\\\\u8bfa\\\\u7cfb", "awardGroupId": 238, "awardName": "\\\\u5956\\\\u91d1\\\\u7ec41000", "directLimitRet": 4300, "directRet": 0, "threeoneRet": 0, "superRet": 0}, {"lotteryId": "99301", "lotterySeriesCode": 3, "lotterySeriesName": "11\\\\u90095\\\\u7cfb", "awardGroupId": 24, "awardName": "\\\\u5956\\\\u91d1\\\\u7ec41782", "directRet": 0, "threeoneRet": 0, "superRet": 0}, {"lotteryId": "99302", "lotterySeriesCode": 3, "lotterySeriesName": "11\\\\u90095\\\\u7cfb", "awardGroupId": 26, "awardName": "\\\\u5956\\\\u91d1\\\\u7ec41620", "directRet": 0, "threeoneRet": 0, "superRet": 0}, {"lotteryId": "99303", "lotterySeriesCode": 3, "lotterySeriesName": "11\\\\u90095\\\\u7cfb", "awardGroupId": 29, "awardName": "\\\\u5956\\\\u91d1\\\\u7ec41782", "directRet": 0, "threeoneRet": 0, "superRet": 0}, {"lotteryId": "99306", "lotterySeriesCode": 3, "lotterySeriesName": "11\\\\u90095\\\\u7cfb", "awardGroupId": 192, "awardName": "\\\\u5956\\\\u91d1\\\\u7ec41782", "directRet": 0, "threeoneRet": 0, "superRet": 0}, {"lotteryId": "99401", "lotterySeriesCode": 5, "lotterySeriesName": "\\\\u53cc\\\\u8272\\\\u7403\\\\u7cfb", "awardGroupId": 107, "awardName": "\\\\u53cc\\\\u8272\\\\u7403\\\\u5956\\\\u91d1\\\\u7ec4", "directLimitRet": 950, "threeLimitRet": 950, "directRet": 0, "threeoneRet": 0, "superRet": 0}, {"lotteryId": "99501", "lotterySeriesCode": 6, "lotterySeriesName": "\\\\u5feb\\\\u4e50\\\\u5f69\\\\u7cfb", "awardGroupId": 188, "awardName": "\\\\u6df7\\\\u5408\\\\u5956\\\\u91d1\\\\u7ec4", "directRet": 0, "threeoneRet": 0, "superRet": 0}, {"lotteryId": "99502", "lotterySeriesCode": 6, "lotterySeriesName": "\\\\u5feb\\\\u4e50\\\\u5f69\\\\u7cfb", "awardGroupId": 190, "awardName": "\\\\u6df7\\\\u5408\\\\u5956\\\\u91d1\\\\u7ec4", "directRet": 0, "threeoneRet": 0, "superRet": 0}, {"lotteryId": "99601", "lotterySeriesCode": 7, "lotterySeriesName": "\\\\u5feb\\\\u4e50\\\\u5f69\\\\u7cfb", "awardGroupId": 189, "awardName": "\\\\u6df7\\\\u5408\\\\u5956\\\\u91d1\\\\u7ec4", "directRet": 0, "threeoneRet": 0, "superRet": 0}, {"lotteryId": "99602", "lotterySeriesCode": 7, "lotterySeriesName": "\\\\u5feb\\\\u4e50\\\\u5f69\\\\u7cfb", "awardGroupId": 203, "awardName": "\\\\u6df7\\\\u5408\\\\u5956\\\\u91d1\\\\u7ec4", "directRet": 0, "threeoneRet": 0, "superRet": 0}, {"lotteryId": "99604", "lotterySeriesCode": 7, "lotterySeriesName": "\\\\u5feb\\\\u4e50\\\\u5f69\\\\u7cfb", "awardGroupId": 213, "awardName": "\\\\u6df7\\\\u5408\\\\u5956\\\\u91d1\\\\u7ec4", "directRet": 0, "threeoneRet": 0, "superRet": 0}, {"lotteryId": "99605", "lotterySeriesCode": 7, "lotterySeriesName": "\\\\u5feb\\\\u4e50\\\\u5f69\\\\u7cfb", "awardGroupId": 207, "awardName": "\\\\u6df7\\\\u5408\\\\u5956\\\\u91d1\\\\u7ec4", "directRet": 0, "threeoneRet": 0, "superRet": 0}, {"lotteryId": "99701", "lotterySeriesCode": 9, "lotterySeriesName": "\\\\u516d\\\\u5408\\\\u7cfb", "awardGroupId": 202, "awardName": "\\\\u516d\\\\u5408\\\\u5f69\\\\u5956\\\\u91d1\\\\u7ec4", "directRet": 0, "threeoneRet": 0, "superRet": 0, "lhcYear": 0, "lhcColor": 0, "lhcFlatcode": 0, "lhcHalfwave": 0, "lhcOneyear": 0, "lhcNotin": 0, "lhcContinuein23": 0, "lhcContinuein4": 0, "lhcContinuein5": 0, "lhcContinuenotin23": 0, "lhcContinuenotin4": 0, "lhcContinuenotin5": 0, "lhcContinuecode": 0}, {"lotteryId": "99801", "lotterySeriesCode": 2, "lotterySeriesName": "3D\\\\u7cfb", "awardGroupId": 223, "awardName": "\\\\u5956\\\\u91d1\\\\u7ec41800", "directLimitRet": 450, "threeLimitRet": 450, "directRet": 0, "threeoneRet": 0, "superRet": 0}, {"lotteryId": "99901", "lotterySeriesCode": 11, "lotterySeriesName": "\\\\u9ad8\\\\u9891\\\\u5f69\\\\u7cfb", "awardGroupId": 243, "awardName": "\\\\u5956\\\\u91d1\\\\u7ec41800", "directLimitRet": 450, "directRet": 0, "threeoneRet": 0, "superRet": 0}]
                    }
        domain_dict = {0: "http://www.dev02.com",
                       1: "http:\\\\/\\\\/www2.joy188.com:888"
                      }
        OpenLink_data = {"type": 1, "days": -1, "infos":info_dict[envs],
                        "memo": "autoTest", "setUp": 1,"domain": domain_dict[envs]}
        param_data.update(OpenLink_data)
        data_['body']['param'] = param_data
        r = requests.post(env+'information/doRetSetting',data=json.dumps(data_),headers=App_header) 
        if r.json()['head']['status'] == 0:
            print('開戶連結創立成功')
            data_ = {"head":{"sowner":"","rowner":"","msn":"","msnsn":"","userId":"","userAccount":"",
            "sessionId":token_[user]},"body":{"param":{"CGISESSID":token_[user],"app_id":"10","come_from":"4",
            "appname":"1"},"pager":{"startNo":"","endNo":""}}}                                                                                     
            
            r = requests.post(env+'information/openLinkList',data=json.dumps(data_),headers=App_header) 
            result = r.json()['body']['result']['list'][0]
            #print(result)
            global regCode,new_token,exp,pid
            regCode = result['regCode']#回傳開戶 的 id
            new_token = result['urlstring'].split('token=')[1]#回傳 開戶 的token
            exp = result['urlstring'].split('exp=')[1].split('&')[0]
            pid = result['urlstring'].split('pid=')[1].split('&')[0]
            print('%s 的 開戶連結'%user)
            print("註冊連結: %s, 註冊碼: %s, 建置於: %s"%(result['urlstring'],result['regCode'],result['start']))
        else:
            print('創立失敗')
    @staticmethod
    def test_AppRegister():
        '''APP註冊'''
        #print(new_token)
        global AppRegister_user # 到時 會用這用戶 來綁銀行卡 ,安全問題/密碼
        user = env_dict['一般帳號'][envs]
        user_random = random.randint(1000,9999999)
        account_dict = {0:'hsiehapp%s'%user_random,1:'kerrapp%s'%user_random}
        AppRegister_user = account_dict[envs]
        data_ = {"head":{"sowner":"","rowner":"","msn":"","msnsn":"","userId":"","userAccount":""},
        "body":{"param":{"token":new_token,"accountName":AppRegister_user,
        "password":  loginpasssource,
        "cellphone":"", "qqAccount":"","wechat":"","id":int(regCode),"exp":exp,"pid":int(pid),"qq":'',
        "ip":"192.168.2.18","app_id":"10", "come_from":"4","appname":"1"},"pager":{"startNo":"","endNo":""}}} 
        
        r = requests.post(env+'user/register',data=json.dumps(data_),headers=App_header) 
        if r.json()['head']['status'] == 0:
            print('%s 註冊成功, 上級用戶: %s'%(AppRegister_user ,user))
        else:
            print('註冊失敗')
        login_data = Joy188Test3.Iapi_LoginData(username=AppRegister_user,uuid_=uuid,
                                                passwd=loginpasssource)
        r = requests.post(env+'front/login',data=json.dumps(login_data),headers= App_header)
        # 需登入新的用戶, 產生token ,後續綁卡 用
        token = r.json()['body']['result']['token']
        userid = r.json()['body']['result']['userid']
        token_.setdefault(AppRegister_user,token)
        userid_.setdefault(AppRegister_user,userid)
    
    @staticmethod
    def test_IapiSecurityPass():
        '''APP設置安全密碼'''
        user = AppRegister_user 
        data_ = Joy188Test3.IapiData(user)
        global passwd_info
        passwd_info = {
            0:["cd85fad371fd1c668b01c5d5f8d91354","b232f1fde130e8e27f5a9bcdb7b1b2e0"],
            1:["c229c901ef92cd889a2bc850f72be30b","249d9c0cdec6df9aa51753af03adeaac"]
        }# list[0] 是安全密碼, 1 是安全問題
        safePass  = {"newpass2": passwd_info[envs][0],
        "confirmNewpass2":passwd_info[envs][0]}
        param_data = data_["body"]["param"]
        param_data.update(safePass)
        data_['body']['param'] = param_data
        r = requests.post(env+'security/addSecpass',data=json.dumps(data_),
                          headers=App_header)# 安全密碼設定
        if r.json()['head']['status'] == 0:
            print('%s 安全密碼設定成功'%user)
        else:
            print('安全密碼設置確認')
    @staticmethod
    def test_IapiSecurityQues():
        '''APP設置安全問題'''
        user = AppRegister_user 
        data_ = Joy188Test3.IapiData(user)
        quests = [{"qid":1,"question":"\\u6211\\u5ba0\\u7269\\u7684\\u540d\\u5b57\\uff1f",
          "qpwd":passwd_info[envs][1] ,"isUsed":0},
         {"qid":2,"question":"\\u6211\\u6700\\u4eb2\\u5bc6\\u7684\\u670b\\u53cb\\u662f\\uff1f",
          "qpwd": passwd_info[envs][1],"isUsed":0},
         {"qid":3,"question":"\\u6211\\u6700\\u559c\\u6b22\\u7684\\u6f14\\u5458\\uff1f",
          "qpwd": passwd_info[envs][1],"isUsed":0}]# 安全問題
        param_data = data_["body"]["param"]
        param_data['quests'] = quests
        data_['body']['param'] = param_data
        r = requests.post(env+'security/safeQuestSet',data=json.dumps(data_),
                          headers=App_header)# 安全密碼設定
        if r.json()['head']['status'] == 0:
            print('%s 安全問題設定成功'%user)
        else:
            print('安全問題設置確認')
        
    @staticmethod
    def test_IapiCardBind():
        '''APP銀行綁卡'''
        global card
        while True:
            user = AppRegister_user 
            data_ = Joy188Test3.IapiData(user)#從新生成初始 data
            fake = Factory.create()
            card = (fake.credit_card_number(card_type='visa16'))#產生一個16位的假卡號
            bind_data = {"bankId":1,"bank":"安璞分行",
             "province":"內湖省","city":"內湖市",
                         "branch":"安璞銀行",
             "accountName":"kerr","account":"%s"%card,
            "secpass":passwd_info[envs][0],"bindCardType":0,"digitalWalletNumber":""}# 綁卡資訊
            param_data = data_["body"]["param"]
            param_data.update(bind_data)
            data_['body']['param'] = param_data
            r = requests.post(env+'security/cardBindingCommit',data=json.dumps(data_),
                              headers=App_header)# 綁一般銀酐卡
            if r.json()['head']['status'] == 0:
                print('%s 一般綁卡成功, 卡號: %s'%(user,card))
            else:
                print('一般綁卡確認')
                break
            data_ = Joy188Test3.IapiData(user)#從新生成初始 data 
            param_data = data_["body"]["param"]
            usdt_card = "usdt%s"%random.randint(100,100000)
            bind_data = {"bankId":1,"bank":"安璞分行",
             "province":"","city":"",
            "branch":"","accountName":"","account":"",
            "secpass":passwd_info[envs][0],"bindCardType":2,
                         "digitalWalletNumber":usdt_card }# usdt
            param_data.update(bind_data)
            data_['body']['param'] = param_data
            r = requests.post(env+'security/cardBindingCommit',data=json.dumps(data_),
                              headers=App_header)# 綁數字貨幣
            if r.json()['head']['status'] == 0:
                print('usdt綁卡成功, 卡號: %s'%(usdt_card))
            else:
                print('數字綁卡確認')
            break
    @staticmethod
    def test_IapiLockCard():
        '''APP綁卡立即鎖定'''
        user = AppRegister_user 
        data_ = Joy188Test3.IapiData(user)#從新生成初始 data
        lockid = Joy188Test.select_Lockid(Joy188Test.get_conn(envs),user)#　lockid 鎖卡
        param_data = data_["body"]["param"]
        param_data['lockedId'] = lockid[0] 
        data_['body']['param'] = param_data
        r = requests.post(env+'security/bankCardNowLock',data=json.dumps(data_),
                              headers=App_header)# 鎖定卡
        if r.json()['head']['status'] == 0:
            print('%s 卡號: %s 鎖定成功'%(user,card))
        else:
            print('綁卡鎖定確認')
        
    @staticmethod
    def test_IapiWithDraw():
        '''APP提現發起'''
        user =  env_dict['一般帳號'][envs]
        data_ = Joy188Test3.IapiData(user)
        money = random.randint(10,20)#  隨機金額
        bank_info = {
            0: ["8642018#2",8642018], 1:["25640091#7",25640091]
        }# 銀行卡資訊
        
        withdraw_data = {"bankinfo":bank_info[envs][0],"money":money,"originalCurrencyAmount":10}
        param_data = data_["body"]["param"]
        param_data.update(withdraw_data)
        data_['body']['param'] = param_data
        r = requests.post(env+'withdraw/verify',data=json.dumps(data_),headers=App_header)# 發起提限

        data_ = Joy188Test3.IapiData(user)#在呼叫一次  ,提限確認 需新的data
        commit_data = {"bindId":bank_info[envs][1],"money":money,"secpwd":
                       passwd_info[envs][0],
        "questionId":1,"questionpwd":passwd_info[envs][1],"serviceFeeFlag":0,
                "originalCurrencyAmount":10,"ipAddr":"168627247"} # 提限確認 ,安全問題 安全密碼
        param_data = data_["body"]["param"]
        param_data.update(commit_data)
        data_['body']['param'] = param_data
        r = requests.post(env+'withdraw/commit',data=json.dumps(data_),headers=App_header)# 發起提限

        if r.json()['head']['status'] == 0:
            sn = Joy188Test.select_WithDrawSn(Joy188Test.get_conn(envs),userid_[user])
            print('%s 發起提現,金額: %s 成功,單號: %s'%(user,money,sn))
        else:
            print('%s 發起提現失敗'%(user))

        
    @staticmethod
    def test_AppBalance():
        '''APP 4.0/第三方餘額'''
        threads = []
        user = env_dict['APP帳號'][envs]
        data_ =  Joy188Test3.IapiData(user)
        print('帳號: %s'%user)
        for third in third_list:
            if third == 'shaba':
                third = 'sb'
            t = threading.Thread(target=Joy188Test.APP_SessionPost,args=(third,'balance',data_))
            threads.append(t)
        for i in threads:
            i.start()
        for i in threads:
            i.join()
        r = requests.post(env+'/information/getBalance',data=json.dumps(data_),headers=App_header)
        balance =  r.json()['body']['result']['balance']
        print('4.0餘額: %s'%balance)


    @staticmethod
    def test_ApptransferIn():
        '''APP轉入'''
        user = env_dict['APP帳號'][envs]
        data_ =  Joy188Test3.IapiData(user)
        data_['body']['param']['amount'] = 10

        statu_list = []
        print('帳號: %s'%user)
        #third_list = ['gns','sb','im','ky','lc','city']
        for third in third_list:
            tran_url = 'Gns' if third=='gns' else 'Thirdly' # gns規則不同
            if third == 'shaba':
                third = 'sb'
            r = requests.post(env+'/%s/transferTo%s'%(third,tran_url),data=json.dumps(data_)
                              ,headers=App_header)
            #print(r.json())#列印出來
            status = r.json()['body']['result']['status']
            if status == 'Y':
                print('轉入%s金額 10'%third)
                statu_list.append(third)
            else:
                print('%s轉入失敗'%third)
        for third in statu_list:
            if third == 'sb':
                third = 'shaba'
            thirdly_status = Joy188Test.thirdly_tran(Joy188Test.my_con(evn=envs,third=third),
                                                     tran_type=0,
                third=third,user=user)# 先確認資料轉帳傳泰
            #print(thirdly_status)
            staut_mapping = thirdly_status[0][1]
            msg = '%s 轉帳單號: %s . '%(third,thirdly_status[0][0])
            if staut_mapping == '2':
                msg = msg +" 狀態成功"
            else:
                msg = msg +" 狀態待確認"
            sleep(3)
            print(msg)
            
            
        Joy188Test3.test_AppBalance()
    @staticmethod
    def test_ApptransferOut():
        '''APP轉出'''
        user = env_dict['APP帳號'][envs]
        data_ =  Joy188Test3.IapiData(user)
        data_['body']['param']['amount'] = 10

        statu_list = []
        print('帳號: %s'%user)
        for third in third_list:# PC 沙巴 是 shaba , iapi 是 sb
            if third == 'shaba':
                third = 'sb'
            r = requests.post(env+'/%s/transferToFF'%third,data=json.dumps(data_),headers=App_header)
            #print(r.json())
            status = r.json()['body']['result']['status']
            if status == 'Y':
                print('%s轉出金額 10'%third)
                statu_list.append(third)
            else:
                print('%s轉出失敗'%third)
        for third in statu_list:
            if third == 'sb':
                third = 'shaba'
            thirdly_status= Joy188Test.thirdly_tran(Joy188Test.my_con(evn=envs,third=third),
            tran_type=1,third=third,user=user)# 先確認資料轉帳傳泰
            staut_mapping = thirdly_status[0][1]
            msg = '%s 轉帳單號: %s . '%(third,thirdly_status[0][0])
            if staut_mapping == '2':
                msg = msg +" 狀態成功"
            else:
                msg = msg +" 狀態待確認"
            sleep(3)
            print(msg)

        Joy188Test3.test_AppBalance()
    @staticmethod
    def test_AppcheckPassword():
        '''更換密碼'''
        user = env_dict['玩家'][envs]
        print('用戶: %s'%user)
        Joy188Test.select_userPass(Joy188Test.get_conn(envs),user)
        if password[0] == 'fa0c0fd599eaa397bd0daba5f47e7151':#123qwe
            newpass = "3bf6add0828ee17c4603563954473c1e"#amberrd  新密碼
            oldpass = 'fa0c0fd599eaa397bd0daba5f47e7151'# 原本的密碼
            msg = '新密碼為amberrd'
            print('舊密碼 為123qwe')
        else:# 密碼為amberrd
            newpass = "fa0c0fd599eaa397bd0daba5f47e7151"
            oldpass = "3bf6add0828ee17c4603563954473c1e"
            msg = '新密碼為123qwe'
            print('舊密碼為 amberrd')
        data_ = {"head":{"sowner":"","rowner":"","msn":"","msnsn":"","userId":"","userAccount":"",
        "sessionId":token_[user]},"body":{"pager":{"startNo":"1","endNo":"99999"},
        "param":{"CGISESSID":token_[user],"newpass":newpass,
        "oldpass": oldpass,
        #new,comfirm皆為新密買  ,old為救密碼
        "confirmNewpass":newpass,"app_id":"9","come_from":"3","appname":"1"}}}
        #3bf6add0828ee17c4603563954473c1e 為amberrd 加密 , # fa0c0fd599eaa397bd0daba5f47e7151 為123qwe
        r = requests.post(env+'/security/modifyLoginpass/',data=json.dumps(data_),
                          headers=App_header)#確認密碼皆口
        #print(r.text)
        if r.json()['head']['status'] == 0:
            print("密碼更換成功"+msg)
            print('重新登入')
            login_data = {
            "head": {
                "sessionId": ''
            },
            "body": {
                "param": {
                "username": user+"|"+ 'f009b92edc4333fd',
                "loginpassSource":newpass,
                "appCode": 1,
                "uuid": 'f009b92edc4333fd',
                "loginIp": 2130706433,
                "device": 2,
                "app_id": 9,
                "come_from": "3",
                "appname": "1"
            }
            }
            }
            
            r = requests.post(env+'front/login',data=json.dumps(login_data),headers=App_header)
            if r.json()['head']['status'] ==0:
                print('登入成功')
        else:
            print(r.json())
            print('失敗')
    


# In[160]:


envs = 0


# In[118]:


Joy188Test.test_Login()


# In[161]:


Joy188Test3.test_iapiLogin()


# In[162]:


Joy188Test3.test_OpenLink()


# In[167]:


Joy188Test3.test_AppRegister()


# In[292]:


Joy188Test.test_CancelOrder()


# In[172]:


Joy188Test3.test_IapiCardBind()


# In[169]:


Joy188Test3.test_IapiSecurityPass()


# In[168]:


Joy188Test3.test_IapiSecurityQues()


# In[176]:


Joy188Test3.test_IapiLockCard()


# In[387]:


Joy188Test.test_LotteryPlanSubmit()


# In[316]:


Joy188Test.test_LotterySubmit()


# In[322]:


if __name__ == '__main__':
    suite = unittest.TestSuite()
    test = [Joy188Test('test_Login'),Joy188Test('test_LotterySubmit')
             ,Joy188Test('test_LotteryPlanSubmit'),Joy188Test('test_tranUser')]
    
    suite.addTests(test)

    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite)
    


# In[177]:


#自動化測試報告
envs = 1# 0 dev , 1 : 188
if __name__ == '__main__':
    suite = unittest.TestSuite()
    order_dict= {}# 存放 order_code 和 orderid
    
    tests = [Joy188Test('test_Login'),Joy188Test('test_redEnvelope'),Joy188Test('test_LotterySubmit'),
             Joy188Test('test_CancelOrder'),Joy188Test('test_LotteryPlanSubmit'),
             Joy188Test('test_ThirdHome'),Joy188Test('test_188'),Joy188Test('test_chart'),
    Joy188Test('test_thirdBalance'),Joy188Test('test_transferin'),Joy188Test('test_transferout'),
    Joy188Test('test_tranUser'),Joy188Test('test_ChargeLimit')]
    
    tests2 = [Joy188Test2('test_safepersonal'),Joy188Test2('test_applycenter')
    ,Joy188Test2('test_safecenter'),Joy188Test2('test_bindcard'),Joy188Test2('test_bindcardUs')]
      
    app = [Joy188Test3('test_iapiLogin'),Joy188Test3('test_iapiSubmit'),
           Joy188Test3('test_IapiCancelSubmit'),
           Joy188Test3('test_OpenLink'),
           Joy188Test3('test_AppRegister'),
           Joy188Test3('test_IapiSecurityPass'),Joy188Test3('test_IapiSecurityQues'),
           Joy188Test3('test_IapiCardBind'),Joy188Test3('test_IapiLockCard'),
           Joy188Test3('test_IapiRecharge'),
           Joy188Test3('test_IapiWithDraw'),Joy188Test3('test_iapiCheckIn'),
           Joy188Test3('test_AppBalance'),
           Joy188Test3('test_ApptransferIn'),Joy188Test3('test_ApptransferOut'),
           Joy188Test3('test_AppcheckPassword'),Joy188Test3('test_IapiTransfer')
          ]

    test = [Joy188Test('test_Login'), Joy188Test('test_redEnvelope'),
            Joy188Test('test_tranUser'),Joy188Test('test_ChargeLimit')]
    
    

    suite.addTests(tests)
    suite.addTests(tests2)
    suite.addTests(app)

    #suite.addTests(test)
    
    #suite.addTests(except_)
    now = time.strftime('%Y_%m_%d^%H-%M-%S')
    filename = now + u'自動化測試' + '.html'
    fp = open(filename, 'wb')
    runner = HTMLTestRunner.HTMLTestRunner(
            stream=fp,
            title=u'測試報告',
            description=u'環境: %s '%post_url
            )
    runner.run(suite)
    fp.close()


# In[ ]:


#ipynb檔  轉成 python檔
def IpynbToPython(): 
    try:
        get_ipython().system('jupyter nbconvert --to python joy188_test.ipynb   ')
    except:
        pass
IpynbToPython()

