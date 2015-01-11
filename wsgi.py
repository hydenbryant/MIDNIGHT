#@+leo-ver=5-thin
#@+node:2014fall.20141212095015.1775: * @file wsgi.py
# coding=utf-8
# 上面的程式內容編碼必須在程式的第一或者第二行才會有作用

################# (1) 模組導入區
# 導入 cherrypy 模組, 為了在 OpenShift 平台上使用 cherrypy 模組, 必須透過 setup.py 安裝


#@@language python
#@@tabwidth -4

#@+<<declarations>>
#@+node:2014fall.20141212095015.1776: ** <<declarations>> (wsgi)
import cherrypy
# 導入 Python 內建的 os 模組, 因為 os 模組為 Python 內建, 所以無需透過 setup.py 安裝
import os
# 導入 random 模組
import random

################# (2) 廣域變數設定區
# 確定程式檔案所在目錄, 在 Windows 下有最後的反斜線
_curdir = os.path.join(os.getcwd(), os.path.dirname(__file__))
# 設定在雲端與近端的資料儲存目錄
if 'OPENSHIFT_REPO_DIR' in os.environ.keys():
    # 表示程式在雲端執行
    download_root_dir = os.environ['OPENSHIFT_DATA_DIR']
    data_dir = os.environ['OPENSHIFT_DATA_DIR']
else:
    # 表示程式在近端執行
    download_root_dir = _curdir + "/local_data/"
    data_dir = _curdir + "/local_data/"

'''以下為近端 input() 與 for 迴圈應用的程式碼, 若要將程式送到 OpenShift 執行, 除了採用 CherryPy 網際框架外, 還要轉為 html 列印
# 利用 input() 取得的資料型別為字串
toprint = input("要印甚麼內容?")
# 若要將 input() 取得的字串轉為整數使用, 必須利用 int() 轉換
repeat_no = int(input("重複列印幾次?"))
for i in range(repeat_no):
    print(toprint)
'''
#@-<<declarations>>
#@+others
#@+node:2014fall.20141212095015.1777: ** class main
################# (3) 程式類別定義區
# 以下改用 CherryPy 網際框架程式架構
# 以下為 Hello 類別的設計內容, 其中的 object 使用, 表示 Hello 類別繼承 object 的所有特性, 包括方法與屬性設計
class main(object):

    # Hello 類別的啟動設定
    _cp_config = {
    'tools.encode.encoding': 'utf-8',
    'tools.sessions.on' : True,
    'tools.sessions.storage_type' : 'file',
    #'tools.sessions.locking' : 'explicit',
    # session 以檔案儲存, 而且位於 data_dir 下的 tmp 目錄
    'tools.sessions.storage_path' : data_dir+'/tmp',
    # session 有效時間設為 60 分鐘
    'tools.sessions.timeout' : 60
    }

    #@+others
    #@+node:2014fall.20141212095015.2004: *3* __init__
    def __init__(self):
        # 配合透過案例啟始建立所需的目錄
        if not os.path.isdir(data_dir+'/tmp'):
            os.mkdir(data_dir+'/tmp')
        if not os.path.isdir(data_dir+"/downloads"):
            os.mkdir(data_dir+"/downloads")
        if not os.path.isdir(data_dir+"/images"):
            os.mkdir(data_dir+"/images")
    #@+node:2014fall.20141212095015.1778: *3* index_orig
    # 以 @ 開頭的 cherrypy.expose 為 decorator, 用來表示隨後的成員方法, 可以直接讓使用者以 URL 連結執行
    @cherrypy.expose
    # index 方法為 CherryPy 各類別成員方法中的內建(default)方法, 當使用者執行時未指定方法, 系統將會優先執行 index 方法
    # 有 self 的方法為類別中的成員方法, Python 程式透過此一 self 在各成員方法間傳遞物件內容
    def index_orig(self,html=""):
        return html
    #@+node:2014fall.20141212095015.1779: *3* text
    @cherrypy.expose
    def text(self, txt=""):
        return txt
    #@+node:2014fall.20141215194146.1791: *3* guess_1
    @cherrypy.expose
    def index(self, guess=None):
        # 將標準答案存入 answer session 對應區
        theanswer = random.randint(1, 100)
        thecount = 0
        # 將答案與計算次數變數存進 session 對應變數
        cherrypy.session['answer'] = theanswer
        cherrypy.session['count'] = thecount
        # 印出讓使用者輸入的超文件表單
        outstring = '''
    <form method=POST action=guess_2>
    請輸入您所猜的整數:
    <input type=text name=guess><br />
    <input type=submit value=send>
    </form>
    '''
        return outstring
    #@+node:2014fall.20141215194146.1793: *3* guess_2
    @cherrypy.expose
    def guess_2(self, guess=None):
        # 假如使用者直接執行 doCheck, 則設法轉回根方法
        if guess is None:
            raise cherrypy.HTTPRedirect("/")
        # 從 session 取出 answer 對應資料, 且處理直接執行 doCheck 時無法取 session 值情況
        try:
            theanswer = int(cherrypy.session.get('answer'))
        except:
            raise cherrypy.HTTPRedirect("/")
        # 經由表單所取得的 guess 資料型別為 string
        try:
            theguess = int(guess)
        except:
            return "錯誤 " + self.guess_3()
        # 每執行 doCheck 一次,次數增量一次
        #cherrypy.session['count']  += 1
        # 答案與所猜數字進行比對
        if theanswer < theguess:
            return'''<span style="color: yellow">再小點''' + self.guess_3()
        elif theanswer > theguess:
            return '''<span style="color: yellow">再大點''' + self.guess_3()
        else:
            # 已經猜對, 從 session 取出累計猜測次數
            thecount = cherrypy.session.get('count')
            return '''
            <a href=''>再猜</a>
            '''
    #@+node:2014fall.20141215194146.1789: *3* guess_3
    def guess_3(self):
        # 印出讓使用者輸入的超文件表單
        outstring = '''
    <form method=POST action=guess_2>
    請輸入您所猜的整數:
    <input type=text name=guess><br />
    <input type=submit value=send>
    '''
        return outstring
    #@-others
#@-others
################# (4) 程式啟動區
# 配合程式檔案所在目錄設定靜態目錄或靜態檔案
application_conf = {'/static':{
        'tools.staticdir.on': True,
        # 程式執行目錄下, 必須自行建立 static 目錄
        'tools.staticdir.dir': _curdir+"/static"},
        '/downloads':{
        'tools.staticdir.on': True,
        'tools.staticdir.dir': data_dir+"/downloads"},
        '/images':{
        'tools.staticdir.on': True,
        'tools.staticdir.dir': data_dir+"/images"}
    }

if 'OPENSHIFT_REPO_DIR' in os.environ.keys():
    # 表示在 OpenSfhit 執行
    application = cherrypy.Application(main(), config=application_conf)
else:
    # 表示在近端執行
    cherrypy.quickstart(main(), config=application_conf)
########################### 4. 安排啟動設定
# 配合程式檔案所在目錄設定靜態目錄或靜態檔案
application_conf = {'/static':{
        'tools.staticdir.on': True,
        # 程式執行目錄下, 必須自行建立 static 目錄
        'tools.staticdir.dir': _curdir+"/static"},
        '/downloads':{
        'tools.staticdir.on': True,
        'tools.staticdir.dir': data_dir+"/downloads"},
        '/images':{
        'tools.staticdir.on': True,
        'tools.staticdir.dir': data_dir+"/images"}
    }
  
########################### 5. 在近端或遠端啟動程式
# 利用 HelloWorld() class 產生案例物件
root = main()
# 假如在 os 環境變數中存在 'OPENSHIFT_REPO_DIR', 表示程式在 OpenShift 環境中執行
if 'OPENSHIFT_REPO_DIR' in os.environ.keys():
    # 雲端執行啟動
    application = cherrypy.Application(root, config = application_conf)
else:
    # 近端執行啟動時, 可以設定埠號與對應 IP
    '''
    # (設定三)
    cherrypy.server.socket_port = 8083
    cherrypy.server.socket_host = '127.0.0.1'
    # 若加上下列兩行,  表示要以 https 啟動
    cherrypy.server.ssl_certificate = 'v:/certificates/ssl_cert.pem'
    cherrypy.server.ssl_private_key = 'v:/certificates/ssl_cert.pem'
    '''
    # http 將在  8080 啟動 (設定一)
    cherrypy.config.update({'server.socket_port': 8080, 'server.socket_host': '127.0.0.1'})
    '''
    # 只有在 https 模式啟動, 則上下 http 與 https 設定均去除, 只留下 (設定四)
    cherrypy.config.update({'server.socket_port': 443, 'server.socket_host': '127.0.0.1',
                        'server.ssl_certificate': 'v:/certificates/ssl_cert.pem',
                        'server.ssl_private_key': 'v:/certificates/ssl_cert.pem'})
    '''
  
    # https 將在 443 啟動 (設定二)
    from cherrypy._cpserver import Server
    server = Server()
    server.socket_port = 443
    server.socket_host = '127.0.0.1'
    server.ssl_certificate = 'v:/certificates/ssl_cert.pem'
    server.ssl_private_key = 'v:/certificates/ssl_cert.pem'
    server.subscribe()
  
    cherrypy.quickstart(root, config = application_conf)
#@-leo
