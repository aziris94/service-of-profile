#!flask/bin/python
from flask import Flask, jsonify, abort
import MySQLdb
import string

from flask import make_response
from flask import request
DB_PASSWD="Y5sr27Kx"
DB_USER="profiles"
DB_NAME="db_profiles_profile"

# DB_PASSWD="root"
# DB_USER="root"
# DB_NAME="users"

app = Flask(__name__)

# @app.route('/todo/api/v1.0/tasks', methods=['GET'])
# def get_users():
#     return jsonify({'tasks': tasks})

@app.route('/profile/<int:user_id>', methods=['GET'])
def get_task(user_id):

    db = MySQLdb.connect(host="localhost", user=DB_USER, passwd=DB_PASSWD, db=DB_NAME, charset='utf8')
    cursor = db.cursor()
    sql = """SELECT * FROM users WHERE uid='%(user_id)s'"""%{'user_id':user_id}
    cursor.execute(sql)
    data = cursor.fetchall()
    user = dict()
    for rec in data:
        uid, login, password,email, name, surname = rec
        user['uid'] = uid
        user['login'] = login
        user['password']=password
        user['email']=email
        user['name']=unicode(name)
        user['surname'] = unicode(surname)
    db.close()

    if len(user) == 0:
        abort(404)
    return jsonify(user)


@app.route('/auth/registration', methods=['POST'])
def create_profile():
    if not request.json:
        abort(400)
    if 'login'  in request.json and type(request.json['login']) != unicode:
        abort(400)
    if 'password'  in request.json and type(request.json['password']) is not unicode:
        abort(400)
    if 'name'  in request.json and type(request.json['name']) is not unicode:
        abort(400)
    if 'surname'  in request.json and type(request.json['surname']) is not unicode:
        abort(400)
    if 'email'  in request.json and type(request.json['email']) is not unicode:
        abort(400)

    if 'login'  in request.json:
        login = request.json.get('login')
    else:
        abort(400)
    if 'password'  in request.json:
        password = request.json.get('password')
    else:
        abort(400)
    if 'name'  in request.json:
        name = request.json.get('name')
    else:
        name = ''
    if 'surname'  in request.json:
        surname = request.json.get('surname')
    else:
        surname = ''
    if 'email'  in request.json:
        email = request.json.get('email')
    else:
        abort(400)

    db = MySQLdb.connect(host="localhost", user=DB_USER, passwd=DB_PASSWD, db=DB_NAME, charset='utf8')
    cursor = db.cursor()

    sql = """INSERT INTO users (login,password,name,surname,email) VALUE ('%(login)s','%(password)s','%(name)s','%(surname)s','%(email)s')""" % \
          {'login': login,'password': password,'name': name,'surname':surname,'email': email}
    cursor.execute(sql)
    uid = cursor.lastrowid
    db.commit()
    db.close()

    return jsonify({'uid': uid}), 201


@app.route('/profile', methods=['POST'])
def edit_profile():
    if not request.json:
        abort(400)
    if 'login'  in request.json and type(request.json['login']) != unicode:
        abort(400)
    if 'password'  in request.json and type(request.json['password']) is not unicode:
        abort(400)
    if 'name'  in request.json and type(request.json['name']) is not unicode:
        abort(400)
    if 'surname'  in request.json and type(request.json['surname']) is not unicode:
        abort(400)
    if 'email'  in request.json and type(request.json['email']) is not unicode:
        abort(400)
    if 'profile_id' in request.json and type(request.json['profile_id']) is not int:
        abort(400)

    if 'profile_id'  in request.json:
        profile_id = request.json.get('profile_id')
    else:
        abort(400)
    if 'login'  in request.json:
        login = request.json.get('login')
    else:
        abort(400)
    if 'password'  in request.json:
        password = request.json.get('password')
    else:
        abort(400)
    if 'name'  in request.json:
        name = request.json.get('name')
    else:
        name = ''
    if 'surname'  in request.json:
        surname = request.json.get('surname')
    else:
        surname = ''
    if 'email'  in request.json:
        email = request.json.get('email')
    else:
        abort(400)

    db = MySQLdb.connect(host="localhost", user=DB_USER, passwd=DB_PASSWD, db=DB_NAME, charset='utf8')
    cursor = db.cursor()
    sql = """SELECT * FROM users WHERE uid='%(user_id)s'"""%{'user_id':profile_id}
    cursor.execute(sql)
    data = cursor.fetchall()
    if len(data)==0:
        abort(404)
    sql = """ UPDATE users SET  login='%(login)s',password='%(password)s',name='%(name)s',surname='%(surname)s',email='%(email)s' WHERE uid='%(uid)s'""" % \
          {'login': login,'password': password,'name': name,'surname':surname,'email': email,'uid':profile_id}
    cursor.execute(sql)
    uid = cursor.lastrowid
    db.commit()
    db.close()

    return jsonify({'uid': profile_id}), 200


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

@app.errorhandler(400)
def not_found(error):
    return make_response(jsonify({'error': 'Bad request'}), 400)


if __name__ == '__main__':
    app.run(debug=True)
