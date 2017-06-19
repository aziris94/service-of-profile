# service-of-profile
http://127.0.0.1:5000


password хранится как md5 от строки

CREATE TABLE `users` (

     `uid` int(10) unsigned NOT NULL AUTO_INCREMENT COMMENT 'Primary Key: Unique user ID.',
     `login` varchar(60) NOT NULL DEFAULT '' COMMENT 'Unique user name.',
     `password` varchar(128) NOT NULL DEFAULT '' COMMENT 'User’s password (hashed).',
     `email` varchar(254) DEFAULT '' COMMENT 'User’s e-mail address.',
     `name` varchar(60) NOT NULL DEFAULT '' COMMENT 'user name.',
     `surname` varchar(60) NOT NULL DEFAULT '' COMMENT 'user name.',
       PRIMARY KEY (`uid`),
       UNIQUE KEY `login` (`login`),
       UNIQUE KEY `email` (`email`)
     ) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='Stores user data.';


GET /profile/<user_id>

Получение профиля пользователя

Ответ:

{

        "email": "3@mail.ru",   
        "surname": "", 
        "login": "vika",  
        "name": "\u0412\u0438\u043a\u0430",   
        "password": "eccbc87e4b5ce2fe28308fd9f2a7baf3",   
        "uid": 3
}



Ошибка:

{

        'error': 'Not found'        
}

Создание профиля
POST /auth/registration

Param:

{

	"login":"ilya",
	"password":"a87ff679a2f3e71d9181a67b7542122c",
	"name":"Илья",
	"surname": "Кочетов"
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


Изменение профиля

POST /profile

Param:

{
	
	"profile_id": 9,
	"login":"ilya",
	"password":"a87ff679a2f3e71d9181a67b7542122c",
	"name":"Илья",
	"surname": "Кочетов"
	"email":"3@mail.ru",
}


Ответ:

HTTP/1.0 200 OK

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

