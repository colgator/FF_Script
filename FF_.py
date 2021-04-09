class Env:
    def __init__(self):
        self.env_dict = {'測試總代': ['hsieh000','kerr000'] ,'一般帳號': ['hsieh001','kerr001'],'合營1940': ['hsiehwin1940test','kerrwin1940test'],'轉入/轉出':['hsiehthird001','kerrthird001'],'APP帳號': ['hsiehapp001','kerrapp001'],'玩家':['hsieh0620','kerr010'],'APP合營': ['hsiehwin','kerrwin1940' ]}
class Lottery:
    def __init__(self):
        self.lottery_dict = {
        'cqssc':[u'重慶','99101'],'xjssc':[u'新彊時彩','99103'],'tjssc':[u'天津時彩','99104'],'hljssc':[u'黑龍江','99105'],'llssc':[u'樂利時彩','99106'],'shssl':[u'上海時彩','99107'],'jlffc':[u'吉利分彩','99111'],'slmmc':[u'順利秒彩','99112'],'txffc':[u'騰訊分彩','99114'],'btcffc':[u'比特幣分彩','99115'],'fhjlssc':[u'吉利時彩','99116'],'sd115':[u'山東11選5','99301'],'jx115':[u"江西11選5",'99302'],'gd115':[u'廣東11選5','99303'],'sl115':[u'順利11選5','99306'],'jsk3':[u'江蘇快3','99501'],'ahk3':[u'安徽快3','99502'],'jsdice':[u'江蘇骰寶','99601'],'jldice1':[u'吉利骰寶(娛樂)','99602'],'jldice2':[u'吉利骰寶(至尊)','99603'],'fc3d':[u'3D','99108'],'p5':[u'排列5','99109'],'lhc':[u'六合彩','99701'],'btcctp':[u'快開','99901'],'pk10':[u"pk10",'99202'],'v3d':[u'吉利3D','99801'], 'xyft':[u'幸運飛艇','99203'],'fhxjc':[u'鳳凰新疆','99118'],'fhcqc':[u'鳳凰重慶','99117'],'n3d':[u'越南3d','99124'],'np3':[u'越南福利彩','99123'],'pcdd':[u'PC蛋蛋','99204'],'xyft168':[u'幸運飛艇168','99205'], 'fckl8':[u'福彩快樂8','99206'],'ptxffc':[u'奇趣腾讯分分彩','99125'],'hn60':[u'多彩河内分分彩','99126'],'hnffc':[u'河内分分彩','99119'],'hn5fc':[u'河内五分彩','99120']}
        self.lottery_sh = ['cqssc','xjssc','tjssc','hljssc','llssc','jlffc','slmmc','txffc','fhjlssc','btcffc','fhcqc','fhxjc','hnffc','hn5fc','hn60','ptxffc']
        self.lottery_sh2000 = ['cqssc','xjssc','tjssc','hljssc','fhjlssc','fhcqc','fhxjc','hn5fc']
        self.lottery_3d = ['v3d']
        self.lottery_115 = ['sd115','jx115','gd115','sl115']
        self.lottery_k3 = ['ahk3','jsk3']
        self.lottery_sb = ['jsdice',"jldice1",'jldice2']
        self.lottery_fun = ['pk10','xyft','xyft168']
        self.lottery_noRed = ['fc3d','n3d','np3','p5']#沒有紅包
        self.cancel_lottery_list = ['cqssc','xjssc','tjssc','hljssc','fhjlssc','xyft','pk10','fc3d','p5','n3d','np3']# 撤消彩種
        
        self.LotterySsh_group = {'wuxing':{'zhixuan':['fushi'],
            'zuxuan':['zuxuan120','zuxuan60','zuxuan30','zuxuan20','zuxuan10''zuxuan5'],
            'budingwei':['ermabudingwei','sanmabudingwei'],
            'quwei':['yifanfengshun','haoshichengshuang','sanxingbaoxi','sijifacai']},
        'sixing': {'zhixuan':['fushi'],
            'zuxuan':['zuxuan24','zuxuan12','zuxuan6','zuxuan4'],
            'budingwei':['ermabudingwei','yimabudingwei']},
        'qiansan': {'zhixuan':['fushi','hezhi','kuadu'],
            'zuxuan':['hezhi','baodan','zusan','zuliu'],
            'budingwei': ['ermabudingwei','yimabudingwei']},
        'housan': {'zhixuan':['fushi','hezhi','kuadu'],
            'zuxuan':['hezhi','baodan','zusan','zuliu'],
            'budingwei':['ermabudingwei','yimabudingwei']},
        'zhongsan': {'zhixuan':['fushi','hezhi','kuadu'],
            'zuxuan':['hezhi','baodan','zusan','zuliu'],
            'budingwei':['ermabudingwei','yimabudingwei']},
        'qianer': {'zhixuan':['fushi','hezhi','kuadu'],
            'zuxuan':['hezhi','baodan','fushi']},
        'houer':{'zhixuan':['fushi','hezhi','kuadu'],
            'zuxuan':['hezhi','baodan','fushi']},
        'yixing': {'dingweidan':['fushi']},
        'housan_2000' : {'zhixuan':['fushi','hezhi','kuadu'],
            'zuxuan': ['hezhi','baodan','zusan','zuliu'],
            'budingwei': ['ermabudingwei','yimabudingwei']},
        'houer_2000':{'zhixuan':['fushi','hezhi','kuadu'],
            'zuxuan':['hezhi','baodan','fushi'] },
        'yixing_2000':{'dingweidan':['fushi']},
            'daxiaodanshuang': {'dxds':['zonghe','qianyi','qianer','houyi','houer']},
            'longhu': {'longhudou':['fushi'] }
        }
        self.Lottery115_group = {'xuanyi': {'qiansanyimabudingwei':['fushi'],
            'dingweidan':['fushi'], 'renxuanyizhongyi': ['fushi']},
        'xuaner': {'qianerzhixuan':['zhixuanfushi'],'qianerzuxuan':['zuxuanfushi','zuxuandantuo'],'renxuanerzhonger':['renxuanfushi','renxuandantuo']},
        'xuansan': {'qiansanzhixuan':['zhixuanfushi'],'qiansanzuxuan':['zuxuanfushi','zuxuandantuo'],'renxuansanzhongsan':['renxuanfushi','renxuandantuo']},
        'xuansi': {'renxuansizhongsi':['fushi','dantuo']},
        'xuanwu': {'renxuanwuzhongwu':['fushi','dantuo']},
        'xuanliu':{'renxuanliuzhongwu':['fushi','dantuo']},
        'xuanqi':{'renxuanqizhongwu':['fushi','dantuo']},
        'xuanba':{'renxuanbazhongwu': ['fushi','dantuo'] },
        'quwei':{'normal':['dingdanshuang','caizhongwei']}
        }
class Third:
    def __init__(self):
        self.third_list = ['gns','shaba','im','ky','lc','city','bg','yb','pg']
