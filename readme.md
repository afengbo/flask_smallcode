# flask_smallcode Food

- 数据库表结构生成models：
    > flask-sqlacodegen 'mysql://user:pwd@127.0.0.1/food_db' --tables food --outfile "common/models/food/Food.py"  --flask

- 启动服务
    > uwsgi --ini uwsgi.ini