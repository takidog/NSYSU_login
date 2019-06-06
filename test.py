import requests


if __name__ == "__main__":
    username = ''
    password = ''
    data= requests.post(url='http://127.0.0.1:5050/sso/login',json={'username':username,'password':password})
    print(data)
    print(data.json())

    data= requests.post(url='http://127.0.0.1:5050/selcrs/login',json={'username':username,'password':password})
    print(data)
    print(data.json())