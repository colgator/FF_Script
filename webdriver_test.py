#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import unittest
from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.common.exceptions import WebDriverException 
from selenium.common.exceptions import InvalidSelectorException
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import  ElementClickInterceptedException
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import ElementNotVisibleException
from selenium.common.exceptions import ElementNotInteractableException
from time import sleep
import HTMLTestRunner
import re
import random
import cx_Oracle


# In[42]:


#ipynb檔  轉成 python檔
def IpynbToPython(): 
    try:
        get_ipython().system('jupyter nbconvert --to python webdriver_request_test.ipynb   ')
    except:
        pass
IpynbToPython()


# In[ ]:


dr = webdriver.Chrome()
id_ = dr.find_element_by_id
xpath = dr.find_element_by_xpath
class_ = dr.find_element_by_class_name
css = dr.find_element_by_css_selector
link = dr.find_element_by_link_text


# In[ ]:


dr.quit()


# In[ ]:


dr.refresh()


# In[ ]:


def login(env,user):
    global em_url,www_url,envs 
    try:
        if env == 'joy188': 
            envs = 1
            www_url = 'http://www2.%s.com/'%env
            em_url = 'http://em.%s.com/'%env
            dr.get(www_url)
            password = 'amberrd'
        elif env in ['dev02','dev03','fh82dev02']:
            envs = 0
            www_url = 'http://www.%s.com/'%env
            em_url = 'http://em.%s.com/'%env
            dr.get(www_url)
            password = '123qwe'
        elif env == 'xinu88':
            www_url = 'https://www.%s.com/'%env
            em_url = 'https://em.%s.com/'%env
            dr.get(www_url)
            password = 'real$0823'
        dr.find_element_by_id('J-user-name').send_keys(user)
        dr.find_element_by_id('J-user-password').send_keys(password)
        dr.find_element_by_id('J-form-submit').click()
        sleep(3)
    except NoSuchElementException as e:
        print(e)
    except ElementClickInterceptedException as e:
        print(e)
        
login('dev02','hsieh001')


# In[ ]:


dr.refresh()


# In[ ]:


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
def select_userUrl(conn,user):
    with conn.cursor() as cursor:
        sql = "select url from user_url url_ inner join user_customer user_ on url_.creator = user_.id         where user_.account = '%s' and url_.days = -1 and rownum = 1         and url_.gmt_created > to_date('2020-01-01','YYYY-MM-DD') and url_.type=1"%user
       # print(sql)
        cursor.execute(sql)
        rows = cursor.fetchall()
        user_url = []

        for i in rows:
            user_url.append(i[0])
        return user_url
    conn.close()


# In[ ]:


select_userUrl(get_conn(envs),'hsieh001')


# In[ ]:


www_url


# In[ ]:


register_dic = []
for i in range(3):# 先生成咬產生的新用戶,  num 為你要生成幾個代理  
    new_user = '%s%s'%(user,random.randint(10,10000))
    register_dic.append(new_user)


# In[ ]:


dr.refresh()


# In[ ]:


test = ['hsieh000', 'hsieh0001613', 'hsieh0004782', 'hsieh0001091']
for a,b in enumerate(test):
    print(a,b)


# In[ ]:


def register_USER(user,num):#要生成幾條 ,num :5 .user 往下開出五 層
    register_dic = []# 從放要新開戶的 用戶 ,
    register_dic.append(user)#第一個元素自己, num為5 ,該列表就會有6哥
    for i in range(num):# 先生成咬產生的新用戶,  num 為你要生成幾個代理  
        new_user = '%s%s'%(user,random.randint(10,10000))
        register_dic.append(new_user)
    print(register_dic)
    for index,user_ in enumerate(register_dic):# 從列表取出
        if index == len(register_dic) - 1 :# index 從0 開始取. register_dic 列表會有自己用戶,所以須-1
            return 'done'
        register_url = select_userUrl(get_conn(envs),user_)# 自己的開戶連結
        
        print('%s. %s的開戶連結: %s'%(index,user_,register_url))
        dr.get(www_url+'register?'+register_url[0])
        if envs == 0:
            password = '123qwe'
        elif envs == 1:
            password = 'amberrd'
        else:
            print('生產')
        new_user= register_dic[index+1]
        id_('J-input-username').send_keys(new_user)#新的用戶明,register_dic 的下一個元素, 
        id_('J-input-password').send_keys(password)#密碼
        id_('J-input-password2').send_keys(password)#罵馬確認
        id_('J-button-submit').click()
        print('%s註冊成功'%new_user)
        #register_dic.append(new_user)
        sleep(1)
    
    
register_USER('hsieh000',3)


# In[ ]:


register_dic


# In[ ]:


#webdriver 註冊 
def register_user(num,register_url,register_name):#num數量,註冊連結.註冊用戶名
    for i in range(1,num,1):
        while True:
            try:
                dr.get(register_url)
                if '188' in register_url:
                    password = 'amberrd'
                elif 'dev' in register_url:
                    password = '123qwe'
                else:
                    print('註冊連結網域確認')
                    break
                id_('J-input-username').send_keys('%s%s'%(register_name,'{:03d}'.format(i)))
                id_('J-input-password').send_keys(password)
                id_('J-input-password2').send_keys(password)
                id_('J-button-submit').click()
                if dr.current_url == '%sindex'%www_url:
                    break
                else:
                    register_user = '%s%s'%(register_name,'{:03d}'.format(i))
                    print('%s註冊成功'%register_user)
                dr.get(www_url)#最後回首頁
                break
            except ElementNotInteractableException:
                pass
                break
            except NoSuchElementException :
                pass
                break

register_user(num=10,register_url='http://www2.joy188.com/8c8/hdwydE',register_name='kerr1220')


# In[ ]:


def fund_test():
    fund_type = {'expressRecharge':'網銀','netRemit':'銀行卡充值','unionpayRecharge':'快捷','alipay':'支付寶','alipay2':'支付寶2',
    'wechat':'微信','wechat2':'微信2','wechatFixed':'微信定額','unionpayqr':'銀聯掃馬',
    'alipayTransBank':'支付保轉銀行卡','alipayFixed':'支付保定額','usdtRecharge':'usdt',
    'wechatTransBank':'微信轉銀行卡'}
    fund_index = {'1':'網銀','0':'銀行卡充值','3':'快捷','4':'支付寶','16':'支付寶2',
    '5':'微信','17':'微信2','10':'微信定額','8':'銀聯掃馬',
    '8':'支付保轉銀行卡','11':'支付保定額','12':'usdt','15':'微信轉銀行卡'}


    for fund in fund_index.keys():
        try:
            print(fund_index[fund])
            dr.get('http://www.dev02.com/fund/index?type=%s'%fund)#id_element(fund)
            if fund in ['0','1']:
                if id_('selectBank').text =='- 请选择银行 -':

                    id_('icoName').click()#充值銀行 點選 ,會顯示 各種方式
                    class_('CCB').click()#建設銀行
                else:
                    pass
                id_('chargeamount').send_keys('100')#充值金額輸入
                id_('J-Submit').click()#發起


            elif fund in ['10','11']:
                link('100').click()
                id_('J-next-step').click()
            else:
                id_('chargeamount').send_keys('100')#充值金額輸入
                id_('J-next-step').click()#發起

        except ElementClickInterceptedException:
            pass


# In[ ]:


dr.get(www_url)


# In[ ]:


id_('app-download-btn').get_attribute('href')


# In[ ]:


soup = BeautifulSoup(dr.page_source,'lxml')
href_list = [i.get('href') for i in soup.find_all('a',href=re.compile("^[#n]+"))]
print(href_list)


# In[ ]:


soup = BeautifulSoup(dr.page_source,'lxml')
#href = soup.find_all('a')#href=re.compile("^(/)")
href_list = [i.get('href') for i in soup.find_all('a',href=re.compile("^(/)"))]
dr_url = []#存拜訪過的url
href_set = set(href_list)
print(href_set)
#print(id_('mobileAPPdownload').get_attribute('href'))#下載首頁
#id_('app-download-btn').get_attribute('href') ,首頁才有


# In[ ]:


def footp_list():#足跡驗證
    soup = BeautifulSoup(dr.page_source,'lxml')
    foot_list = soup.find_all('div',{'class':'footp-list'})
    foot_list = list(foot_list[0])
    foot_dict = {}
    for i in foot_list:
        foot_dict[i.text] = i['href']
    print('我得足跡: %s'%foot_dict)
footp_list()


# In[ ]:


id_('new-showAllBall').click()


# In[ ]:


for i in element_list:#上方導航覽 跑一遍
   id_(i).click()
   sleep(0.5)


# In[ ]:


element_list = ['new-showAllBall','headerLottery','J-btn-card','live','J-btn-sport','J-btn-esport',
'J-btn-egames', 'J-btn-download','footprint']
while True:
    for i in href_set:
        try:
            if i[-1] == '/':
                i = i[:-1]
            if 'lhc' in i:
                dr.refresh()
            if 'em' in i:
                dr.get('http:%s'%i)
            elif 'pt' in i :
                dr.get('http:%s'%i)
            elif i in dr_url:
                pass
                break
            else:
                dr.get(www_url+i)
            print(dr.title)
            print(dr.current_url)
            print('APP下載中心連結'+id_('mobileAPPdownload').get_attribute('href'))
            id_('new-showAllBall').click()
            footp_list()
            for i in element_list:#上方導航覽 跑一遍
                id_(i).click()
                sleep(0.5)
            dr_url.append(i)
        except NoSuchElementException as e:

            if 'mobileAPPdownload' in str(e):
                print('此頁沒有下載中心')
            else:
                print(e)
            continue
        except ElementClickInterceptedException as e:
            if 'id="new-showAllBal' in str(e):
                print('刷新餘額功能確認')
            else:
                print(e)
            continue
    break
    


# In[ ]:


url_list = [dr.current_url]
list_href = []#存放抓的url
lottery_list = []#彩種清單
thirdy_list = []#第三方清單 

def test_soup():
    global list_href,url_list,len_list
    #url_list.append(dr.current_url)
    soup = BeautifulSoup(dr.page_source,'lxml')
    
    href = soup.find_all('a',href=re.compile("^(/)"))#正則,  /開頭的url
    href_list = [i.get('href') for i in href]
    list_href = set(href_list)
       
    #print(soup)
test_soup()


# In[ ]:


def game_info():#遊戲說明頁
    for i in lottery_list:
        try:
            print(i)

            dr.get(em_url+'/gameBet/%s'%i)
            soup = BeautifulSoup(dr.page_source,'lxml')
            if i == 'jsdice' :
                element = 'shortcuts'
            elif i == 'jldice1':
                element = 'shortcuts'
            elif i == 'jldece2':
                element = 'shortcuts'
            else:
                element = 'lottery-tipslink'


            #print(soup)
            for a in soup.find_all('div',{'class':element}):
                print(a.find_all('a')[0])
                print(a.find_all('a')[1])
        except IndexError:
            pass


# In[ ]:


def assert_text(text,element):
    if text in id_(element).text:
        pass
    else:
        print('缺少 %s'%text)
def assert_url(element,url):
    if css(element).get_attribute('href') in url:
        pass
    else:
        print('%s ,有誤'%css(element).text)
def test_header():
    while True:
        try:
            '''
            if id_('hiddBall').get_attribute('style') == 'display: inline;':#判斷 餘額是否顯示
                pass
            else:
                id_('showAllBall').click()
            '''    
            element_list = ['new-showAllBall','headerLottery','J-btn-card','live','J-btn-sport','J-btn-esport',
            'J-btn-egames', 'J-btn-download','footprint']
            for i in element_list:
                id_(i).click()
                sleep(0.5)
            #assert_text('钱包','spanBall')
            #assert_text('联盟防伪认证','lm-QrCode')
            
            assert_text('我的足迹','footprint')
            assert_text('消息','msg-title')
            assert_text('域名中心','doaminCheck') 
            assert_text('首页','honeindex')
            assert_text('彩票','headerLottery')
            assert_text('棋牌','card')
            assert_text('真人','live') 
            assert_text('体育','sport')
            assert_text('电竞','esport')
            assert_text('电子游艺','egames')
            assert_text('下载中心','downloadCenter')
            
            assert_url('a#mobileAPPdownload','http://ios1.phl5b.org/mobileApp/index.html')
            assert_url('a#PTClientcenter','http://download.ph158nb.com:9527/pt/fh_pt_client.exe')
            assert_url('a#DCSafecenter','http://ios1.phl5b.org/safeApp/index.html')
            assert_url('a#infofhx',"http://www.ph158.cc/")
            assert_url('a#doaminCheck','https://www.ph158.info/')
            js="var action=document.documentElement.scrollTop=10000"
            dr.execute_script(js)#視窗往下移
            sleep(1)
            if '2003-2019' in xpath('//*[@id="jsFooter"]/div/p[1]').text:
                print('copyright ok')
            else:
                print(xpath('//*[@id="jsFooter"]/div/p[1]').text)
            
            break

        except NoSuchElementException as e:
            if 'jsFooter' in str(e):
                print('無需copyright')
            else:                
                pass
            
            break
        except ElementClickInterceptedException as e:
            pass
            dr.refresh()
        except ElementNotInteractableException as e:
            print('此頁導航覽 為舊版')
            break
test_header()


# In[ ]:


a = len_list# 用來控制 ,拜訪完 首頁 後抓取的完後,就不再 抓取
for i in range(len_list):
    #print(list_href[i])
    if list_href[i][-1] == '/':  #避免有些 相同頁面, 不一致url問題
        list_href[i] == list_href[0:-1]
    else:
        pass
    if 'em' in list_href[i]:
        url_ = 'http:%s'%list_href[i]
        #dr.get('http:%s'%list_href[i])
    elif 'www' in list_href[i]:
        url_ = 'http:%s'%list_href[i]
        #dr.get('http:%s'%list_href[i])
    elif 'pt' in list_href[i]:
        url_ = 'http:%s'%list_href[i]
    elif list_href[i] in lottery_list:
        url_ = em_url + 'gameBet/%s'%list_href[i]
    elif list_href[i] in thirdy_list:
        if list_href[i]  == 'fhll':
            url_ =  www_url + 'fhll/home/77101'
        elif list_href[i] == 'shaba':
            url_ = www_url + 'shaba/home?act=sports'
        else:
            if list_href[i][0]  == '/':# 抓取url 統一規則, 避免com 後面有兩個斜線
                list_href[i] = list_href[i][1:]
            else:
                pass
            url_ = www_url+'%s/home'%list_href[i]
    
    else:
        url_ = www_url+list_href[i]
        #dr.get(www_url+list_href[i])
    #print(url_)
    if url_ in url_list:# 已經訪問過的  url
        pass
    elif 'll115' in url_:#沒使用的連結 
        pass
    elif 'jxssc' in url_:
        pass
    elif '?' in url_:
        pass
    else:
        url_list.append(url_)
        #print(url_list)
        dr.get(url_)
        if 'gns' in url_:
            try:
                xpath('/html/body/div[9]/a').click()
                xpath('/html/body/div[10]/a').click()
            except ElementNotInteractableException:
                pass
        else:    
            pass
        test_header()
        print(dr.title)    
        print(dr.current_url)
        print('-------------------------')
        # 一開始從首頁抓的 數量 , 和   list_href 持續抓取後的  去比對, len_list抓完手頁後,為固定值
        test_soup()
        
'''        
for i in list_href[a:]:
    if '//' == i[-1] :  
        i == i[0:-1]
    else:
        pass
    if '//' in i:
        url_ = 'http:'+ i
    elif 'chart' in i:
        url_ = em_url + i
    else:
        url_ = www_url+i
    
    if url_ in url_list:# 已經訪問過的  url
        pass
    elif '?' in url_:
        pass
    else:
        test_header()
        print(dr.title)    
        #print(dr.current_url
        print('-------------------------')
'''


# In[ ]:



def test_fhll():#真人不同帳號投注腳本
    for i in range(1,9,1):
        if i == 1:
            dr.get('http://www.dev02.com')
        else:
            dr.get('http://www.dev02.com/login')
        try:
            id_('J-user-name').send_keys('hsieh00%s'%i)
            id_('J-user-password').send_keys('123qwe')
            id_('J-form-submit').click()
            sleep(3)
            dr.get('http://www.dev02.com/fhll/home/77104')
            sleep(3)
            if id_('popIntro').is_displayed():#第一次近來用戶,會有彈窗
                id_('popIntro').click()
            else:
                pass
            dr.switch_to.frame(0)#切換Iframe
            for i in range(3):
                for i in range(1,6,1):
                    xpath('//*[@id="J-balls-main-panel"]/div/div[2]/ul/li[%s]/div[2]/a[2]'%i).click()

                id_('J-fast-submit').click()#立即投注

                css('a.btn.confirm').click()#確認按鈕

                while True:#投注確認完, 等投注彈窗出現
                    if css('a.btn.closeTip').is_displayed():
                        css('a.btn.closeTip').click()
                        break
                    else:
                        continue
        except WebDriverException:
            break
        except ElementNotVisibleException:
            break


# In[ ]:


def xpath_fushi(element1,element2):
    fushi_element = "//dd[@data-type='%s.%s.fushi']"%(element1,element2)
    return fushi_element


# In[ ]:


Joy188Test.LINK("确 认").click()


# In[ ]:


Joy188Test.game_ssh('no')


# In[ ]:


element_list = Joy188Test.normal_type('houer')#return 元素列表
for i in element_list: #普通,五星玩法 元素列表
   Joy188Test.css_element(i)


# In[ ]:


dr.refresh()


# In[ ]:


Joy188Test.test_jsdice()


# In[ ]:


Joy188Test.id_element('J-submit-order')#馬上投注


# In[ ]:


Joy188Test.xpath_element('//*[@id="J-dice-bar"]/div[5]/a[1]')
Joy188Test.result()
Joy188Test.XPATH('/html/body/div[14]/a[1]').click()


# In[ ]:


Joy188Test.xpath_element('/html/body/div[14]/a[1]')


# In[ ]:


for i in range(5):
    Joy188Test.css_element('a.btn.btn-important')


# In[ ]:


import time
if __name__ == '__main__':
    suite = unittest.TestSuite()
    test_submit = [Joy188Test('test_cqssc'),Joy188Test('test_hljssc'),Joy188Test('test_xjssc'),
                  Joy188Test('test_fhcqc'),Joy188Test('test_fhxjc'),Joy188Test('test_btcffc'),
                  ]
    
    
    test_ = [Joy188Test('test_jsdice')]
    
    suite.addTests(test_)
    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite)
    '''
    
    
    now = time.strftime('%Y_%m_%d %H-%M-%S')
    filename = now + u'自動化測試' + '.html'
    fp = open(filename, 'wb')
    runner = HTMLTestRunner.HTMLTestRunner(
            stream=fp,
            title=u'測試報告',
            description=u'環境: 188'
            )
    runner.run(suite)
    fp.close()
    '''
    


# In[ ]:


Joy188Test.ID('diceCup').is_displayed()


# In[ ]:


dr = webdriver.Chrome()


# In[ ]:


xpath = dr.find_element_by_xpath
class_ = dr.find_element_by_class_name
css = dr.find_element_by_css_selector
link = dr.find_element_by_link_text


# In[ ]:


element = css("div.j-ui-miniwindow.pop.w-9")
if element.is_displayed():
    link("确 认").click()
else:
    print('a')


# In[ ]:


css('dd.qianer').click()#change > ul.play-select-gameType > li:nth-child(3)


# In[ ]:


xpath('//*[@id="change"]/ul[1]/li[3]').click()


# In[ ]:


xpath('//li[@game-mode="special"]').click()


# In[ ]:


dr.find_element_by_css_selector('li.sixing.current > dl.zhixuan > dd.danshi').click()


# In[ ]:


dr.refresh()

