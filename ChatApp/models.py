from flask import abort
import pymysql
from util.DB import DB


db_pool = DB.init_db_pool()

#ユーザークラス
class User:
    @classmethod
    def create(cls, uid, name, email, nickname, password):
        conn = db_pool.get_conn()
        try:
            with conn.cursor() as cur:#SQLを操作するためにカーソルを取得
                #データを入れ込む所をカーソルに教える%sは目印
                sql = "INSERT INTO users (uid, name, email, nickname, password) VALUES (%s, %s, %s, %s, %s);" 
                #実行して埋め込み
                cur.execute(sql, (uid, name, email, nickname,password))
                #変更を反映する
                conn.commit()
        except pymysql.Error as e:# この関数をeと呼ぶ
            print(f"エラーが発生しています:{e}")
            abort(500)
        finally:#エラーが発生してもしなくてもする処理
            db_pool.release(conn)#使わなくなったpoolを返却


    @classmethod
    def find_by_email(cls,email):
        conn = db_pool.get_conn()
        try:
            with conn.cursor() as cur:#SQLを操作するためにカーソルを取得
                sql ="SELECT * FROM users WHERE email=%s"#emailの空欄を作っておく　最終的にここのと同じアドレスを探してってこと
                cur.execute(sql, (email,))#前のコードで比べた結果
                user = cur.fetchone()
                return user
        except pymysql.Error as e:
           print(f'エラーが発生しています：{e}')
           abort(500)
        finally:
           db_pool.release(conn)
