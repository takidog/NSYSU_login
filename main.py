import requests
from flask import Flask, jsonify, request

from nsysu import sso_login
from nsysu import selcrs_login

app = Flask(__name__)


@app.route("/selcrs/login", methods=['POST'])
def selcrs_login_flask():
    try:
        content = request.json
        username = content['username']
        password = content['password']
    except:
        return jsonify(),500

    session = requests.session()
    res = selcrs_login(session=session,username=username,password=password)
    try:
        if res.status_code != 200:
            #login error
            return jsonify(),500
    except:
        return jsonify(),500
       
    data = {
        'data':[]
    }
    for k,v in session.cookies.get_dict().items():
        data['data'].append({
            'name':k,
            'value':v
        })

    return jsonify(data), 200





@app.route("/sso/login", methods=['POST'])
def sso_login_flask():
    try:
        content = request.json
        username = content['username']
        password = content['password']
    except:
        return jsonify(),500
    #always create new session for bypass verification code.
    session = requests.session()
    
    res = sso_login(session=session,username=username,password=password)

    try:
        if res.status_code != 200 and res.json()['s'] != 200:
            #login error
            return jsonify(),500
    except:
        return jsonify(),500

    data = {
        'data':[]
    }
    for k,v in session.cookies.get_dict().items():
        data['data'].append({
            'name':k,
            'value':v
        })

    return jsonify(data), 200




if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5050, debug=True)
