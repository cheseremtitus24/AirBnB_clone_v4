export HBNB_TYPE_STORAGE=db;
export HBNB_MYSQL_USER=hbnb_dev;
export    HBNB_MYSQL_PWD=hbnb_dev_pwd;
export    HBNB_MYSQL_HOST=localhost;
export    HBNB_MYSQL_DB=hbnb_dev_db;

gunicorn --bind 0.0.0.0:5003 web_dynamic.2-hbnb:app
