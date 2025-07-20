$Env:HBNB_MYSQL_USER = 'root'
$Env:HBNB_MYSQL_PWD = 'cheserem'
$Env:HBNB_MYSQL_HOST = 'localhost'
$Env:HBNB_MYSQL_DB = 'hbnb_dev_db'
$Env:HBNB_TYPE_STORAGE = 'db'
$Env:HBNB_API_PORT = '5001'

del migrations
flask --app .\api\v1\app.py db init

"insert data into db using the insertdata.sql file"

update migrations
flask db migrate -m "Initial migration"

