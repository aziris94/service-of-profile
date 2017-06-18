#!flask/bin/python
from flask import Flask, jsonify, abort
import MySQLdb
import string

app = Flask(__name__)

@app.route('/todo/api/v1.0/tasks', methods=['GET'])
def get_users():
    return jsonify({'tasks': tasks})

@app.route('/profile/<int:user_id>', methods=['GET'])
def get_task(user_id):

    db = MySQLdb.connect(host="localhost", user="root", passwd="root", db="users", charset='utf8')
    cursor = db.cursor()
    sql = """SELECT * FROM users WHERE uid='%(user_id)s'"""%{'user_id':user_id}
    cursor.execute(sql)
    data = cursor.fetchall()
    sql = """SELECT DISTINCT  ins.uid,ins.interest_id,inter.text FROM interests ins JOIN interest inter ON inter.id=ins.interest_id WHERE uid='%(user_id)s'"""%{'user_id':user_id}
    cursor.execute(sql)
    data_inter = cursor.fetchall()
    sql = """SELECT DISTINCT  friends.friend_id,users.login FROM users JOIN friends  ON users.uid=friends.friend_id WHERE friends.uid='%(user_id)s' """%{'user_id':user_id}
    cursor.execute(sql)
    data_friend = cursor.fetchall()
    sql = """SELECT DISTINCT  friends.uid,users.login FROM users JOIN friends  ON users.uid=friends.uid WHERE friends.friend_id='%(user_id)s'"""%{'user_id':user_id}
    cursor.execute(sql)
    data_friend1 = cursor.fetchall()
    user = dict()

    for rec in data:
        uid, login, password,email, name = rec
        user['uid'] = uid
        user['login'] = login
        user['password']=password
        user['email']=email
        user['name']=unicode(name)
        interests = []
        for inter in data_inter:
            interests.append({'id':inter[1],'text':inter[2]})
        user['interests'] = interests
        friends = []
        for friend in data_friend1+data_friend:
            friends.append({'uid':friend[0],'login':friend[1]})
        user['friends'] = friends
        #print unicode(name)

    db.close()

    if len(user) == 0:
        abort(404)
    return jsonify(user)

from flask import make_response

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

@app.errorhandler(400)
def not_found(error):
    return make_response(jsonify({'error': 'Bad request'}), 400)

from flask import request

@app.route('/auth/registration', methods=['POST'])
def create_task():
    if not request.json:
        abort(400)
    if 'login'  in request.json and type(request.json['login']) != unicode:
        abort(400)
    if 'password'  in request.json and type(request.json['password']) is not unicode:
        abort(400)
    if 'name'  in request.json and type(request.json['name']) is not unicode:
        abort(400)
    if 'email'  in request.json and type(request.json['email']) is not unicode:
        abort(400)
    # if 'interests' in request.json and type(request.json['interests']) is not list:
    #     abort(400)
    db = MySQLdb.connect(host="localhost", user="root", passwd="root", db="users", charset='utf8')
    cursor = db.cursor()
    sql = """INSERT INTO users (login,password,name,email) VALUE ('%(login)s','%(password)s','%(name)s','%(email)s')""" % \
          {'login': request.json.get('login'),'password': request.json.get('password'),'name': request.json.get('name'),'email': request.json.get('email')}
    cursor.execute(sql)
    uid = cursor.lastrowid
    # interests = request.json.get('interests')
    # print interests
    #
    # for interest in interests:
    #     print interest['text']
    #     sql = """SELECT * FROM interest WHERE text like '%(text)s' """%{'text':interest['text']}
    #     cursor.execute(sql)
    #     interest_id=cursor.fetchall()
    #     for id in interest_id:
    #         print id
    #         cursor.execute("""INSERT INTO interests (interest_id,uid) VALUE ('%(interest_id)s','%(uid)s')"""%{'interest_id':id[0],'uid':uid})
    db.commit()
    db.close()

    return jsonify({'uid': uid}), 201

if __name__ == '__main__':
    app.run(debug=True)
