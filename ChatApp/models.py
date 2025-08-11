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


    @classmethod
    def find_by_uid(cls, uid):
        conn =db_pool.get_conn()
        try:
            with conn.cursor() as cur:
                sql = 'SELECT * FROM users WHERE uid=%s;'
                cur.execute(sql,(uid,))
                user = cur.fetchone()
            return user
            #見つかったユーザー情報を返す
        except pymysql.Error as e:
            print(f'エラーが発生しています：{e}')
            abort(500)
        finally:
            db_pool.release(conn)


#チャンネルクラス
class Channel:
    @classmethod
    #チャンネル新規作成に使うcreate関数を定義。引数としてuid,name,descriptionを渡す
    def create(cls, uid, name, description):
        #（一度返却した）データベース接続プールからコネクションを取得してconnに代入
        conn = db_pool.get_conn()
        #tryの中でSQLクエリの実行などを行う
        try:
            #コネクションからカーソル（操作用のオブジェクト）を取得する
            with conn.cursor() as cur:
                #channelsテーブルにuid,name,descriptionを追加する
                #VALUE (%s, %s, %s)はプレースホルダ。安全に値を埋め込むためのもの
                sql = 'INSERT INTO channels(uid, name, description) VALUES (%s, %s, %s);'
                #sqlを実行
                cur.execute(sql, (uid, name, description,))
                #データベースに変更を反映（保存）し、トランザクションを確定させる  
                conn.commit()
                #INSERT.UPDATE.DELETEの場合に使う
        
        #exceptの中ではエラーが発生した時の処理を行う
        #sql実行中にエラーが発生したら、pymysql.Errorでエラー内容を把握し、変数eに代入        
        except pymysql.Error as e:
            print(f'エラーが発生しています：{e}')
            #処理を途中で止めて、（）内のエラーステータスコードを返す
            abort(500)

        #finally:例外が発生した場合でも必ずコネクションをプールに返却する
        finally:
            db_pool.release(conn)


    @classmethod
    def get_all(cls):
        conn = db_pool.get_conn()
        try:
            with conn.cursor() as cur:
                #channelsテーブルの全てのカラムを取得する
                sql = 'SELECT * FROM channels;' 
                cur.execute(sql)
                #全てのチャンネルをとってくるだけなので、引数がない
                channels = cur.fetchall()
                #一致した全ての行をリストとして受け取る
            return channels 
        except pymysql.Error as e:
            print(f'エラーが発生しています：{e}')
            abort(500)
        finally:
            db_pool.release(conn)

    @classmethod
    def find_by_cid(cls, id):
        conn = db_pool.get_conn()
        try:
            with conn.cursor() as cur:
                #channlesテーブルの中の該当のidを取得
                sql = 'SELECT * FROM channels WHERE id=%s;'
                cur.execute(sql,(id,))
                channel = cur.fetchone()
            return channel
        except pymysql.Error as e:
            print(f'エラーが発生しています：{e}')
            abort(500)
        finally:
            db_pool.release(conn)

    @classmethod
    def find_by_name(cls, name):
        conn = db_pool.get_conn()
        try:
            with conn.cursor() as cur:
                #channelsテーブルの中から該当のnameを取得
                sql = 'SELECT * FROM channels WHERE name=%s;'
                cur.execute(sql, (name,))
                channel = cur.fetchone()
            return channel
        except pymysql.Error as e:
            print(f'エラーが発生しています：{e}')
            abort(500)
        finally:
            db_pool.release(conn)

    @classmethod
    def update(cls, name, description, cid):
        conn = db_pool.get_conn()
        try:
            with conn.cursor() as cur:
                #channelsテーブルの該当のidにおける、uid,name,descriptionを更新する
                sql = 'UPDATE channels SET name=%s, description=%s WHERE id=%s;'
                cur.execute(sql,(name, description, cid,))
                conn.commit()
        except pymysql.Error as e:
            print(f'エラーが発生しています：{e}')
            abort(500)
        finally:
            db_pool.release(conn)

    @classmethod
    def delete(cls,cid):
        conn = db_pool.get_conn()
        try:
            with conn.cursor() as cur:
                #channelsテーブルの該当のidを削除する
                sql = 'DELETE FROM channels WHERE id=%s;'
                cur.execute(sql,(cid,))
                conn.commit()
        except pymysql.Error as e:
            print(f'エラーが発生しています：{e}')
            abort(500)
        finally:
            db_pool.release(conn)












# メッセージクラス
