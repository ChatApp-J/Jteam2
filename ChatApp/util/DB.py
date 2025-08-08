import os
import pymysql
from pymysqlpool.pool import Pool #ライブラリ

class DB:
    @classmethod
    def init_db_pool(cls):
        pool = Pool(
            host=os.getenv('DB_HOST'),
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASSWORD'),
            database=os.getenv('DB_DATABASE'),
            max_size=5,
            charset="utf8mb4",
            cursorclass=pymysql.cursors.DictCursor) #DictCursorはカラム名も一緒に表示してくれる（辞書形式で）
        pool.init()#接続する準備
        return pool #関数ないで作ったpoolを他のところで使えるようにしている