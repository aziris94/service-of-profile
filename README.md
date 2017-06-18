# service-of-profile
http://127.0.0.1:5000


password хранится как md5 от строки

CREATE TABLE `users` (

     `uid` int(10) unsigned NOT NULL AUTO_INCREMENT COMMENT 'Primary Key: Unique user ID.',
     `login` varchar(60) NOT NULL DEFAULT '' COMMENT 'Unique user name.',
     `password` varchar(128) NOT NULL DEFAULT '' COMMENT 'User’s password (hashed).',
     `email` varchar(254) DEFAULT '' COMMENT 'User’s e-mail address.',
     `name` varchar(60) NOT NULL DEFAULT '' COMMENT 'user name.',
       PRIMARY KEY (`uid`),
       UNIQUE KEY `login` (`login`)
     ) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='Stores user data.';

CREATE TABLE `interest` (

     `id` int(10) unsigned NOT NULL AUTO_INCREMENT COMMENT 'Primary Key: Unique interests  ID.',
     `text` varchar(60) NOT NULL DEFAULT '' COMMENT 'user name.',
       PRIMARY KEY (`id`)
     ) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='Stores interests data.';


CREATE TABLE `interests` (

     `interest_id` int(10) unsigned NOT NULL  COMMENT 'foreign Key: Unique interests  ID.',
     `uid` int(10) unsigned NOT NULL  COMMENT 'foreign Key: Unique user ID.',
       FOREIGN KEY (uid) REFERENCES users(uid)  ON DELETE CASCADE,
       FOREIGN KEY (interest_id) REFERENCES interest(id)  ON DELETE CASCADE
     ) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='Stores interests data.';

CREATE TABLE `friends` (

     `uid` int(10) unsigned NOT NULL  COMMENT 'foreign Key: Unique user ID.',
     `friend_id` int(10) unsigned NOT NULL  COMMENT 'foreign Key: Unique interests  ID.',
       FOREIGN KEY (uid) REFERENCES users(uid)  ON DELETE CASCADE,
       FOREIGN KEY (friend_id) REFERENCES users(uid)  ON DELETE CASCADE
     ) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='Stores interests data.';



GET /profile/<user_id>

Получение профиля пользователя

Ответ:

{
  "email": "3@mail.ru", 
  "friends": [
    {
      "login": "dima", 
      "uid": 2
    }, 
    {
      "login": "masha", 
      "uid": 8
    }
  ], 
  "interests": [
    {
      "id": 2, 
      "text": "Baby"
    }, 
    {
      "id": 5, 
      "text": "Computer"
    }, 
    {
      "id": 3, 
      "text": "Sport"
    }, 
    {
      "id": 4, 
      "text": "Science"
    }
  ], 
  "login": "vika", 
  "name": "\u0412\u0438\u043a\u0430", 
  "password": "eccbc87e4b5ce2fe28308fd9f2a7baf3", 
  "uid": 3
}

Ошибка:
{
	'error': 'Not found'
}

POST /auth/registration

Param:

{
	"login":"ilya",
	"password":"a87ff679a2f3e71d9181a67b7542122c",
	"name":"Илья",
	"email":"3@mail.ru",
}


Ответ:

HTTP/1.0 201 CREATED
Content-Type: application/json
Content-Length: 16
Server: Werkzeug/0.12.2 Python/2.7.12
Date: Sun, 18 Jun 2017 09:45:52 GMT

{
  "uid": 31
}


Ошибка:

{
	'error': 'Not found'
}


