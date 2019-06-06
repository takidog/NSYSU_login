import requests
from flask import Flask, jsonify, request

from nsysu import login

app = Flask(__name__)





@app.route("/login", methods=['POST'])
def start_job():
    try:
        content = request.json
        username = content['username']
        password = content['password']
    except:
        return jsonify(),500
    #always create new session for bypass verification code.
    session = requests.session()
    res = login(session=session,username=username,password=password)
    try:
        if res.status_code != 200 and res.json()['s'] != 200:
            #login error
            return jsonify(),500
    except:
        return jsonify(),500
       
    data = {
        'data':session.cookies.get_dict()
    }

    return jsonify(data), 200




if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5050, debug=True)
