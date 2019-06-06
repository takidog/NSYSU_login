import requests


if __name__ == "__main__":
    data= requests.post(url='http://127.0.0.1:5050/login',json={'username':'','password':''})
    print(data)
    print(data.json()['data']['PHPSESSID'])
