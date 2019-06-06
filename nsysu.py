import requests
from bs4 import BeautifulSoup
import execjs

load_js = execjs.compile(open("md5.js", 'r').read())

def get_key(session):

    url = 'https://sso.nsysu.edu.tw/index.php/passport/login'
    html = session.get(url).text
    
    parser = BeautifulSoup(html,'html.parser')
    js_text = parser.find_all('script')[-2].text
    key = js_text[js_text.find('var _key = "')+12:js_text.find("function chec")-4]
    return key

def selcrs_login(session,username,password):

    session.verify = False
    session.headers.update({
            'Accept': '*/*',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7,ja;q=0.6',
            'Origin': 'null',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36'
        })
    url = 'http://selcrs.nsysu.edu.tw/scoreqry/sco_query_prs_sso2.asp'
    data = {
        'SID':username,
        'PASSWD':load_js.call('base64_md5',password),
        'ACTION':'0',
        'INTYPE':'1'
        }
    res = session.post(url=url , data=data)

    return res
    
def sso_login(session,username,password):
    #login main system sso
    session.verify = False
    session.headers.update({
            'Accept': '*/*',
            'Referer': 'https://sso.nsysu.edu.tw/index.php/passport/login',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7,ja;q=0.6',
            'Origin': 'https://sso.nsysu.edu.tw',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36'
        })
    key = get_key(session)    

    password_b64 = load_js.call('base64_md5', password)
    s_value = load_js.call("hex_hmac_md5", key, password_b64)

    url = 'https://sso.nsysu.edu.tw/index.php'
    data = {
        'action': 'passport',
        'op': 'dologin',
        'forward':'',
        's': s_value,
        'user': username,
        'password': password_b64,
        'imageField': ' 登 入 ',
        'remember_chkbox':'',
    }

    res = session.post(url=url,data=data)

    return res
if __name__ == "__main__":
    sess = requests.session()
    login(session=sess, username='', password='')
