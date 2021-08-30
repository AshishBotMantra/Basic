from flask import Flask, request,jsonify, make_response
from datetime import datetime, timedelta, timezone
import jwt
from functools import wraps

app = Flask(__name__)

app.config['SECRET_KEY'] = 'thisissecretkey'

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.args.get('token')
        print(token)
        if not token:
            return jsonify({"message":"token is missing"}), 403
        try:
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms='HS256')
        except:
            return jsonify({"message":"token is invalid"}), 403
        return f(*args, **kwargs)
    return decorated

@app.route('/unprotected')
def unprotected():
    return "home"
@app.route('/protected')
@token_required
def protected():
    return jsonify({"message":"only for those who have valid token"})

@app.route('/login')
def login():
    auth = request.authorization

    if auth.username == 'Ashish' and auth.password == 'Ashish@1234':
        token = jwt.encode({'user': auth.username, 'exp': datetime.now(timezone.utc) + timedelta(seconds=10)},
                           app.config['SECRET_KEY'])
        return jsonify({"token" : token})
    return make_response("could not verify", 401, {"www-authenticate":"Basic login='login required"})



if __name__ == "__main__":
    app.run(debug=True)

