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
    #@+node:2015.20150104084324.1762: *3* index
    @cherrypy.expose
    def index(self):
            html = '''
        <a href="word_1">學號及英文名子</a>
        <br>
        <a href="_9x9_1">乘法表</a>
        <br>
        <a href="guess_1">猜數字</a>
        '''        
            return html
    #@+node:2015.20150104084324.1764: *3* word_1
    @cherrypy.expose
    def word_1(self):
            html = '''
        <form method=POST action=word_2>
        請輸入您的學號或英文名子:
        <input type=text name=inp><br />
        <input type=submit value="輸入">
        '''        
            return html
    #@+node:2015.20150104084324.1768: *3* word_2
    @cherrypy.expose
    def word_2(slef,inp):
            inp = str(inp)
            def zero(row):
                zero = [
                "◇◇◆◆◆◆◇",
                "◇◆◇◇◇◆◆",
                "◇◆◇◇◇◆◆",
                "◇◆◇◇◆◇◆",
                "◇◆◇◆◆◇◆",
                "◇◆◇◆◇◇◆",
                "◇◆◆◇◇◇◆",
                "◇◆◆◇◇◇◆",
                "◇◇◆◆◆◆◇",
                ]
                return zero[row]
            def one(row):
                one = [
                "◇◇◇◆◇◇◇",
                "◇◇◆◆◇◇◇",
                "◇◇◇◆◇◇◇",
                "◇◇◇◆◇◇◇",
                "◇◇◇◆◇◇◇",
                "◇◇◇◆◇◇◇",
                "◇◇◇◆◇◇◇",
                "◇◇◇◆◇◇◇",
                "◇◆◆◆◆◆◆",
                ]
                return one[row]
            def two(row):
                two = [
                "◇◆◆◆◆◆◇",
                "◇◆◇◇◇◇◆",
                "◇◇◇◇◇◇◆",
                "◇◇◇◇◇◇◆",
                "◇◇◆◆◆◆◆",
                "◇◆◇◇◇◇◇",
                "◇◆◇◇◇◇◇",
                "◇◆◇◇◇◇◇",
                "◇◆◆◆◆◆◆",
                ]
                return two[row]
            def three(row):
                three = [
                "◇◆◆◆◆◆◇",
                "◇◇◇◇◇◇◆",
                "◇◇◇◇◇◇◆",
                "◇◇◇◇◇◇◆",
                "◇◆◆◆◆◆◇",
                "◇◇◇◇◇◇◆",
                "◇◇◇◇◇◇◆",
                "◇◇◇◇◇◇◆",
                "◇◆◆◆◆◆◇",
                ]
                return three[row]
            def four(row):
                four = [
                "◇◇◇◇◇◆◇",
                "◇◇◇◇◆◆◇",
                "◇◇◇◆◇◆◇",
                "◇◇◆◇◇◆◇",
                "◇◆◇◇◇◆◇",
                "◇◆◆◆◆◆◆",
                "◇◇◇◇◇◆◇",
                "◇◇◇◇◇◆◇",
                "◇◇◇◇◇◆◇",
                ]
                return four[row]
            def five(row):
                five = [
                "◇◆◆◆◆◆◆",
                "◇◆◇◇◇◇◇",
                "◇◆◇◇◇◇◇",
                "◇◆◇◇◇◇◇",
                "◇◆◆◆◆◆◇",
                "◇◇◇◇◇◇◆",
                "◇◇◇◇◇◇◆",
                "◇◇◇◇◇◇◆",
                "◇◆◆◆◆◆◇",
                ]
                return five[row]
            def six(row):
                six = [
                "◇◇◆◆◆◆◇",
                "◇◆◇◇◇◇◆",
                "◇◆◇◇◇◇◇",
                "◇◆◇◇◇◇◇",
                "◇◆◆◆◆◆◇",
                "◇◆◇◇◇◇◆",
                "◇◆◇◇◇◇◆",
                "◇◆◇◇◇◇◆",
                "◇◇◆◆◆◆◇",
                ]
                return six[row]
            def seven(row):
                seven = [
                "◇◆◆◆◆◆◆",
                "◇◆◇◇◇◇◆",
                "◇◇◇◇◇◇◆",
                "◇◇◇◇◇◆◇",
                "◇◇◇◇◆◇◇",
                "◇◇◇◆◇◇◇",
                "◇◇◇◆◇◇◇",
                "◇◇◇◆◇◇◇",
                "◇◇◇◆◇◇◇",
                ]
                return seven[row]
            def eight(row):
                eight = [
                "◇◇◆◆◆◆◇",
                "◇◆◇◇◇◇◆",
                "◇◆◇◇◇◇◆",
                "◇◆◇◇◇◇◆",
                "◇◇◆◆◆◆◇",
                "◇◆◇◇◇◇◆",
                "◇◆◇◇◇◇◆",
                "◇◆◇◇◇◇◆",
                "◇◇◆◆◆◆◇",
                ]
                return eight[row]
            def nine(row):
                nine = [
                "◇◇◆◆◆◆◇",
                "◇◆◇◇◇◇◆",
                "◇◆◇◇◇◇◆",
                "◇◆◇◇◇◇◆",
                "◇◇◆◆◆◆◆",
                "◇◇◇◇◇◇◆",
                "◇◇◇◇◇◇◆",
                "◇◇◇◇◇◇◆",
                "◇◇◆◆◆◆◇",
                ]
                return nine[row]
            def A(row):
                A = [
                "◇◇◆◆◆◆◇",
                "◇◆◇◇◇◇◆",
                "◇◆◇◇◇◇◆",
                "◇◆◇◇◇◇◆",
                "◇◆◇◇◇◇◆",
                "◇◆◆◆◆◆◆",
                "◇◆◇◇◇◇◆",
                "◇◆◇◇◇◇◆",
                "◇◆◇◇◇◇◆",
                ]
                return A[row]
            def B(row):
                B = [
                "◇◆◆◆◆◆◇",
                "◇◆◇◇◇◇◆",
                "◇◆◇◇◇◇◆",
                "◇◆◇◇◇◇◆",
                "◇◆◆◆◆◆◇",
                "◇◆◇◇◇◇◆",
                "◇◆◇◇◇◇◆",
                "◇◆◇◇◇◇◆",
                "◇◆◆◆◆◆◇",
                ]
                return B[row]
            def C(row):
                C = [
                "◇◇◆◆◆◆◇",
                "◇◆◇◇◇◇◆",
                "◇◆◇◇◇◇◇",
                "◇◆◇◇◇◇◇",
                "◇◆◇◇◇◇◇",
                "◇◆◇◇◇◇◇",
                "◇◆◇◇◇◇◇",
                "◇◆◇◇◇◇◆",
                "◇◇◆◆◆◆◇",
                ]
                return C[row]
            def D(row):
                D = [
                "◇◆◆◆◆◇◇",
                "◇◆◇◇◇◆◇",
                "◇◆◇◇◇◇◆",
                "◇◆◇◇◇◇◆",
                "◇◆◇◇◇◇◆",
                "◇◆◇◇◇◇◆",
                "◇◆◇◇◇◇◆",
                "◇◆◇◇◇◆◇",
                "◇◆◆◆◆◇◇",
                ]
                return D[row]
            def E(row):
                E = [
                "◇◆◆◆◆◆◆",
                "◇◆◇◇◇◇◇",
                "◇◆◇◇◇◇◇",
                "◇◆◇◇◇◇◇",
                "◇◆◆◆◆◆◇",
                "◇◆◇◇◇◇◇",
                "◇◆◇◇◇◇◇",
                "◇◆◇◇◇◇◇",
                "◇◆◆◆◆◆◆",
                ]
                return E[row]
            def F(row):
                F = [
                "◇◆◆◆◆◆◆",
                "◇◆◇◇◇◇◇",
                "◇◆◇◇◇◇◇",
                "◇◆◇◇◇◇◇",
                "◇◆◆◆◆◆◇",
                "◇◆◇◇◇◇◇",
                "◇◆◇◇◇◇◇",
                "◇◆◇◇◇◇◇",
                "◇◆◇◇◇◇◇",
                ]
                return F[row]
            def G(row):
                G = [
                "◇◇◆◆◆◆◇",
                "◇◆◇◇◇◇◆",
                "◇◆◇◇◇◇◇",
                "◇◆◇◇◇◇◇",
                "◇◆◇◇◇◇◇",
                "◇◆◇◇◇◆◆",
                "◇◆◇◇◇◇◆",
                "◇◆◇◇◇◇◆",
                "◇◇◆◆◆◆◇",
                ]
                return G[row]
            def H(row):
                H = [
                "◇◆◇◇◇◇◆",
                "◇◆◇◇◇◇◆",
                "◇◆◇◇◇◇◆",
                "◇◆◇◇◇◇◆",
                "◇◆◆◆◆◆◆",
                "◇◆◇◇◇◇◆",
                "◇◆◇◇◇◇◆",
                "◇◆◇◇◇◇◆",
                "◇◆◇◇◇◇◆",
                ]
                return H[row]
            def I(row):
                I = [
                "◇◆◆◆◆◆◆",
                "◇◇◇◆◇◇◇",
                "◇◇◇◆◇◇◇",
                "◇◇◇◆◇◇◇",
                "◇◇◇◆◇◇◇",
                "◇◇◇◆◇◇◇",
                "◇◇◇◆◇◇◇",
                "◇◇◇◆◇◇◇",
                "◇◆◆◆◆◆◆",
                ]
                return I[row]
            def J(row):
                J = [
                "◇◇◇◇◇◇◆",
                "◇◇◇◇◇◇◆",
                "◇◇◇◇◇◇◆",
                "◇◇◇◇◇◇◆",
                "◇◇◇◇◇◇◆",
                "◇◇◇◇◇◇◆",
                "◇◆◇◇◇◇◆",
                "◇◆◇◇◇◇◆",
                "◇◇◆◆◆◆◇",
                ]
                return J[row]
            def K(row):
                K = [
                "◇◆◇◇◇◇◆",
                "◇◆◇◇◇◆◇",
                "◇◆◇◇◆◇◇",
                "◇◆◇◆◇◇◇",
                "◇◆◆◇◇◇◇",
                "◇◆◇◆◇◇◇",
                "◇◆◇◇◆◇◇",
                "◇◆◇◇◇◆◇",
                "◇◆◇◇◇◇◆",
                ]
                return K[row]
            def L(row):
                L = [
                "◇◆◇◇◇◇◇",
                "◇◆◇◇◇◇◇",
                "◇◆◇◇◇◇◇",
                "◇◆◇◇◇◇◇",
                "◇◆◇◇◇◇◇",
                "◇◆◇◇◇◇◇",
                "◇◆◇◇◇◇◇",
                "◇◆◇◇◇◇◇",
                "◇◆◆◆◆◆◆",
                ]
                return L[row]
            def M(row):
                M = [
                "◇◆◇◇◇◇◆",
                "◇◆◆◇◇◆◆",
                "◇◆◆◆◆◆◆",
                "◇◆◇◆◆◇◆",
                "◇◆◇◆◆◇◆",
                "◇◆◇◇◇◇◆",
                "◇◆◇◇◇◇◆",
                "◇◆◇◇◇◇◆",
                "◇◆◇◇◇◇◆",
                ]
                return M[row]
            def N(row):
                N = [
                "◇◆◇◇◇◇◆",
                "◇◆◆◇◇◇◆",
                "◇◆◆◆◇◇◆",
                "◇◆◇◆◇◇◆",
                "◇◆◇◆◆◇◆",
                "◇◆◇◇◆◇◆",
                "◇◆◇◇◆◆◆",
                "◇◆◇◇◇◆◆",
                "◇◆◇◇◇◇◆",
                ]
                return N[row]
            def O(row):
                O = [
                "◇◇◆◆◆◆◇",
                "◇◆◇◇◇◇◆",
                "◇◆◇◇◇◇◆",
                "◇◆◇◇◇◇◆",
                "◇◆◇◇◇◇◆",
                "◇◆◇◇◇◇◆",
                "◇◆◇◇◇◇◆",
                "◇◆◇◇◇◇◆",
                "◇◇◆◆◆◆◇",
                ]
                return O[row]
            def P(row):
                P = [
                "◇◆◆◆◆◆◇",
                "◇◆◇◇◇◇◆",
                "◇◆◇◇◇◇◆",
                "◇◆◇◇◇◇◆",
                "◇◆◆◆◆◆◇",
                "◇◆◇◇◇◇◇",
                "◇◆◇◇◇◇◇",
                "◇◆◇◇◇◇◇",
                "◇◆◇◇◇◇◇",
                ]
                return P[row]
            def Q(row):
                Q = [
                "◇◇◆◆◆◆◇",
                "◇◆◇◇◇◇◆",
                "◇◆◇◇◇◇◆",
                "◇◆◇◇◇◇◆",
                "◇◆◇◇◇◇◆",
                "◇◆◇◇◇◇◆",
                "◇◆◇◇◆◇◆",
                "◇◆◇◇◇◆◆",
                "◇◇◆◆◆◆◆",
                ]
                return Q[row]
            def R(row):
                R = [
                "◇◆◆◆◆◆◇",
                "◇◆◇◇◇◇◆",
                "◇◆◇◇◇◇◆",
                "◇◆◇◇◇◇◆",
                "◇◆◆◆◆◆◇",
                "◇◆◇◇◆◇◇",
                "◇◆◇◇◇◆◇",
                "◇◆◇◇◇◇◆",
                "◇◆◇◇◇◇◆",
                ]
                return R[row]
            def S(row):
                S = [
                "◇◇◆◆◆◆◇",
                "◇◆◇◇◇◇◆",
                "◇◆◇◇◇◇◇",
                "◇◆◇◇◇◇◇",
                "◇◇◆◆◆◆◇",
                "◇◇◇◇◇◇◆",
                "◇◇◇◇◇◇◆",
                "◇◆◇◇◇◇◆",
                "◇◇◆◆◆◆◇",
                ]
                return S[row]
            def T(row):
                T = [
                "◇◆◆◆◆◆◆",
                "◇◇◇◆◇◇◇",
                "◇◇◇◆◇◇◇",
                "◇◇◇◆◇◇◇",
                "◇◇◇◆◇◇◇",
                "◇◇◇◆◇◇◇",
                "◇◇◇◆◇◇◇",
                "◇◇◇◆◇◇◇",
                "◇◇◇◆◇◇◇",
                ]
                return T[row]
            def U(row):
                U = [
                "◇◆◇◇◇◇◆",
                "◇◆◇◇◇◇◆",
                "◇◆◇◇◇◇◆",
                "◇◆◇◇◇◇◆",
                "◇◆◇◇◇◇◆",
                "◇◆◇◇◇◇◆",
                "◇◆◇◇◇◇◆",
                "◇◆◇◇◇◇◆",
                "◇◇◆◆◆◆◇",
                ]
                return U[row]
            def V(row):
                V = [
                "◇◆◇◇◇◇◆",
                "◇◆◇◇◇◇◆",
                "◇◆◇◇◇◇◆",
                "◇◆◇◇◇◇◆",
                "◇◆◇◇◇◇◆",
                "◇◆◇◇◇◇◆",
                "◇◇◆◇◇◆◇",
                "◇◇◆◇◇◆◇",
                "◇◇◇◆◆◇◇",
                ]
                return V[row]
            def W(row):
                W = [
                "◇◆◇◇◇◇◆",
                "◇◆◇◇◇◇◆",
                "◇◆◇◇◇◇◆",
                "◇◆◇◆◆◇◆",
                "◇◆◇◆◆◇◆",
                "◇◆◇◆◆◇◆",
                "◇◆◆◆◆◆◆",
                "◇◇◆◇◇◆◇",
                "◇◇◆◇◇◆◇",
                ]
                return W[row]
            def X(row):
                X = [
                "◇◆◇◇◇◇◆",
                "◇◆◇◇◇◇◆",
                "◇◇◆◇◇◆◇",
                "◇◇◇◆◆◇◇",
                "◇◇◇◆◆◇◇",
                "◇◇◇◆◆◇◇",
                "◇◇◆◇◇◆◇",
                "◇◆◇◇◇◇◆",
                "◇◆◇◇◇◇◆",
                ]
                return X[row]
            def Y(row):
                Y = [
                "◇◆◇◇◇◇◆",
                "◇◆◇◇◇◇◆",
                "◇◆◇◇◇◇◆",
                "◇◇◆◇◇◆◇",
                "◇◇◇◆◆◇◇",
                "◇◇◇◆◇◇◇",
                "◇◇◇◆◇◇◇",
                "◇◇◇◆◇◇◇",
                "◇◇◇◆◇◇◇",
                ]
                return Y[row]
            def Z(row):
                Z = [
                "◇◆◆◆◆◆◆",
                "◇◇◇◇◇◇◆",
                "◇◇◇◇◇◆◆",
                "◇◇◇◇◆◆◇",
                "◇◇◇◆◆◇◇",
                "◇◇◆◆◇◇◇",
                "◇◆◆◇◇◇◇",
                "◇◆◇◇◇◇◇",
                "◇◆◆◆◆◆◆",
                ]
                return Z[row]
            row = 9
            symboldict = {"0": zero ,"1": one,"2": two,"3": three,
            "4": four,"5": five,"6": six,"7": seven,"8": eight,"9": nine,
            "A": A,"B": B,"C": C,"D": D,"E": E,"F": F,"G": G,"H": H,"I": I,
            "J": J,"K": K,"L": L,"M": M,"N": N,"O": O,"P": P,"Q": Q,"R": R,
            "S": S,"T": T,"U": U,"V": V,"W": W,"X": X,"Y": Y,"Z": Z}
            word = ""
            inp = inp.upper()
            for a in range(row):
                for b in inp:
                    word += symboldict[b](a)
                word += "<br>"
            return word
    #@+node:2015.20150104084324.1770: *3* _9x9_1
    @cherrypy.expose
    def _9x9_1(self):
            html = '''
        <form method=POST action=_9x9_2>
        請輸入您所想要的九九乘法表中的極小值:
        <input type=text name=min><br />
        請輸入您所想要的九九乘法表中的極大值:
        <input type=text name=max><br />
        請輸入您所想要的九九乘法表相乘的極小值:
        <input type=text name=start><br />
        請輸入您所想要的九九乘法表相乘的極大值:
        <input type=text name=end><br />
        <input type=submit value="輸入">
        '''        
            return html
    #@+node:2015.20150104084324.1772: *3* _9x9_2
    @cherrypy.expose
    def _9x9_2 (slef,min,max,start,end):
        min = int(min)
        max = int(max)
        end = int(end)
        start = int(start)
        time=""
        for a in range(min,max+1):
            for b in range(start,end+1):
                time += str(a) + 'x' + str(b) + '=' + str(a*b) + '&nbsp'
            time +="<br>"
        return time
    #@+node:2015.20150104084324.1774: *3* fix
    @cherrypy.expose
    def fix (slef):
        html = '''
        <marquee scrolldelay="280" scrollamount="5" hspace="500">
        此功能尚未開放,敬請期待
        '''
        return html
    #@+node:2014fall.20141215194146.1791: *3* guess_1
    @cherrypy.expose
    def guess_1(self, guess=None):
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
