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

@app.route('/profile/cache', methods=['GET'])
def cache_profile():
    email = request.args.get('email')
    db = MySQLdb.connect(host="localhost", user=DB_USER, passwd=DB_PASSWD, db=DB_NAME, charset='utf8')
    cursor = db.cursor()
    sql = """SELECT * FROM users WHERE email='%(email)s'"""%{'email':email}
    cursor.execute(sql)
    data = cursor.fetchall()
    user = dict()
    for rec in data:
        uid, login, password,email, name, surname = rec
        user['profile_id'] = uid
        user['email']=email
        user['password']=password
    db.close()

    if len(user) == 0:
        abort(404)
    return jsonify(user)

@app.route('/profile', methods=['GET'])
def get_list_user():
    db = MySQLdb.connect(host="localhost", user=DB_USER, passwd=DB_PASSWD, db=DB_NAME, charset='utf8')
    cursor = db.cursor()
    sql = """SELECT * FROM users"""
    cursor.execute(sql)
    data = cursor.fetchall()
    users = []
    for rec in data:
        user = dict()
        uid, login, password,email, name, surname = rec
        sql = """SELECT DISTINCT  ins.uid,ins.interest_id,inter.text FROM interests ins JOIN interest inter ON inter.id=ins.interest_id WHERE uid='%(user_id)s'"""%{'user_id':uid}
        cursor.execute(sql)
        data_inter = cursor.fetchall()
        user['uid'] = uid
        user['login'] = login
        user['password']=password
        user['email']=email
        interests = []
        for inter in data_inter:
            interests.append({'interest':inter[2]})
        user['interests'] = interests
        user['name']=unicode(name)
        user['surname'] = unicode(surname)
        users.append(user)
    db.close()

    if len(users) == 0:
        abort(404)
    return jsonify(users)

@app.route('/profile/<int:user_id>', methods=['GET'])
def get_task(user_id):

    db = MySQLdb.connect(host="localhost", user=DB_USER, passwd=DB_PASSWD, db=DB_NAME, charset='utf8')
    cursor = db.cursor()
    sql = """SELECT DISTINCT  ins.uid,ins.interest_id,inter.text FROM interests ins JOIN interest inter ON inter.id=ins.interest_id WHERE uid='%(user_id)s'"""%{'user_id':user_id}
    cursor.execute(sql)
    data_inter = cursor.fetchall()
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
        user['name']=name.encode('utf8')
        user['surname'] = unicode(surname)
        interests = []
        for inter in data_inter:
            interests.append({'interest':inter[2]})
        user['interests'] = interests
    db.close()

    if len(user) == 0:
        abort(404)
    return jsonify(user)


@app.route('/auth/registration', methods=['POST'])
def create_profile():
    if not request.json:
        abort(400)
    print request.json
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
    if 'interests' in request.json and type(request.json['interests']) is not list:
        abort(400)
    if 'login'  in request.json:
        login = request.json.get('login')
#    else:
#        abort(400)
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
    sql = """SELECT * FROM users WHERE email='%(email)s'"""%{'email':email}
    cursor.execute(sql)
    data = cursor.fetchall()
    if len(data)!=0:
        abort(422)

    sql = """INSERT INTO users (login,password,name,surname,email) VALUE ('%(login)s','%(password)s','%(name)s','%(surname)s','%(email)s')""" % \
          {'login': login,'password': password,'name': name,'surname':surname,'email': email}
    cursor.execute(sql)
    uid = cursor.lastrowid
    print uid
    if 'interests'  in request.json:
	    interests = request.json.get('interests')
	    print interests
	    for interest in interests:
	    #    print interest['interest']
	        sql = """SELECT * FROM interest WHERE text like '%(text)s' """%{'text':interest['interest']}
	        cursor.execute(sql)
	        interest_id=cursor.fetchall()
	        for id in interest_id:
	#            print id
	            cursor.execute("""INSERT INTO interests (interest_id,uid) VALUE ('%(interest_id)s','%(uid)s')"""%{'interest_id':id[0],'uid':uid})

    db.commit()
    db.close()

    return jsonify({'uid': uid}), 201



@app.route('/profile/search', methods=['POST'])
def get_array_users():
    if not request.json:
        abort(400)
    print request.json
    if 'uid'  in request.json and type(request.json['uid']) != list:
        abort(400)

    if 'uid'  in request.json:
        uid = request.json.get('uid')
    else:
        abort(400)
    print uid
    if len(uid) == 0:
	abort(404)
    uid_list=str(uid).strip('[]')
    db = MySQLdb.connect(host="localhost", user=DB_USER, passwd=DB_PASSWD, db=DB_NAME, charset='utf8')
    cursor = db.cursor()
    sql = """SELECT * FROM users WHERE uid in (%(uid_list)s)""" % {'uid_list': uid_list}
    print sql
    cursor.execute(sql)
    data = cursor.fetchall()
    if len(data)==0:
        abort(404)

    users=[]
    for rec in data:
        user = dict()
        uid, login, password, email, name, surname = rec
        user['uid'] = uid
        user['login'] = login
        user['email'] = email
        user['name'] = name.encode('utf8')
        user['surname'] = unicode(surname)
        users.append(user)
    db.commit()
    db.close()

    return jsonify({'users': users}), 201


@app.route('/profile', methods=['POST'])
def edit_profile():
    print request.json
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
    if 'uid' in request.json and type(request.json['uid']) is not int:
        abort(400)
    if 'interests' in request.json and type(request.json['interests']) is not list:
        abort(400)

    if 'uid'  in request.json:
        uid = request.json.get('uid')
    else:
        abort(400)
    if 'login'  in request.json:
        login = request.json.get('login')
 #   else:
 #       abort(400)
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
    sql = """SELECT * FROM users WHERE uid='%(user_id)s'"""%{'user_id':uid}
    cursor.execute(sql)
    data = cursor.fetchall()
    if len(data)==0:
        abort(404)
    if 'interests'  in request.json:
            interests = request.json.get('interests')
	    sql="""DELETE from interests WHERE uid='%(uid)s'"""%{'uid':uid}
	    cursor.execute(sql)
            db.commit()

            print interests
            for interest in interests:
            #    print interest['interest']
                sql = """SELECT * FROM interest WHERE text like '%(text)s' """%{'text':interest['interest']}
                cursor.execute(sql)
                interest_id=cursor.fetchall()
                for id in interest_id:
        #            print id
                    cursor.execute("""INSERT INTO interests (interest_id,uid) VALUE ('%(interest_id)s','%(uid)s')"""%{'interest_id':id[0],'uid':uid})

    sql = """ UPDATE users SET  login='%(login)s',password='%(password)s',name='%(name)s',surname='%(surname)s',email='%(email)s' WHERE uid='%(uid)s'""" % \
          {'login': login,'password': password,'name': name,'surname':surname,'email': email,'uid':uid}
    cursor.execute(sql)
    uid_new = cursor.lastrowid
    db.commit()
    db.close()

    return jsonify({'uid': uid}), 200


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

@app.errorhandler(400)
def not_found(error):
    return make_response(jsonify({'error': 'Bad request'}), 400)


if __name__ == '__main__':
    app.run(host='0.0.0.0',debug=True, port=5000)

