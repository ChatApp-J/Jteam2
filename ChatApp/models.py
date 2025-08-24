from flask import abort
import pymysql
from util.DB import DB
import random, string
import hashlib
from werkzeug.utils import secure_filename
import os

db_pool = DB.init_db_pool()

ALLOWED_EXTENSIONS =['png', 'jpg', 'jpeg', 'gif']#拡張子を確認のため
UPLOAD_FOLDER = os.path.join('static','uploads')

#ユーザークラス
class User:
    @classmethod
    def create(cls, uid,name, email, nickname, password,salt):
        conn = db_pool.get_conn()
        try:
            with conn.cursor() as cur:#SQLを操作するためにカーソルを取得
                #データを入れ込む所をカーソルに教える%sは目印
                sql = "INSERT INTO users (uid, name, email, nickname, password, salt) VALUES (%s, %s, %s, %s, %s, %s);" 
                #実行して埋め込み
                cur.execute(sql, ( uid,name, email, nickname,password, salt))
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
           
    @classmethod #ソルトをランダムに作成
    def random_name(cls, n):
        randlst =[random.choice(string.ascii_letters +string.digits) for i in range(10)]
        return  ''.join(randlst)
    
    @classmethod #一万回のハッシュ化
    def stretching(cls,salt_password):
        h =salt_password #最初の値をhに代入
        for _ in range(10000):
            h= hashlib.sha256(h.encode("utf-8")).hexdigest()
        return h
    
#メッセージクラス
class Message:
    @classmethod
    def create(cls, uid, cid, message):
        conn = db_pool.get_conn()
        try:
            with conn.cursor() as cur:
                sql = "INSERT INTO messages(uid, cid, message) VALUES(%s,%s,%s);"
                cur.execute(sql, (uid,cid, message,))#タプル型で渡さないといけないため最後もカンマが必要
                conn.commit()
        except pymysql.Error as e:
            print(f"エラーが発生しています:{e}")
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
            
            
    @classmethod
    def get_all(cls, cid):
        conn = db_pool.get_conn()
        try:
            with conn.cursor() as cur:
                sql = 'SELECT id, u.uid, nickname, message FROM messages AS m INNER JOIN users AS u ON m.uid = u.uid WHERE m.cid = %s ORDER BY m.id ASC;'
                #messagesのuidとusersのuidを結合しメッセージを取得したいチャンネルIDの行だけ残し欲しい列のid, u.uid, nickname, messageを取り出しIDが小さい順で並び替え
                cur.execute(sql,(cid),)#ユーザーが選択したチャンネルIDをsqlに渡す
                message = cur.fetchall()#cur.executeで受けっとた全てをmessageに代入
                return message
        except pymysql.Error as e:
            print(f'エラーが発生しています：{e}')
            abort(500)
        finally:
            db_pool.release(conn)
            
    @classmethod
    def delete_message_owner(cls, message_id, uid, cid):
        conn = db_pool.get_conn()
        try:
           with conn.cursor() as cur:
               sql = "DELETE FROM messages WHERE id=%s AND uid=%s AND cid=%s LIMIT 1;"
               cur.execute(sql, (message_id, uid, cid))#前列で作ったsql文を使いメッセージIDを削除
               count=cur.rowcount
               conn.commit()
               return count
        except pymysql.Error as e:
           print(f'エラーが発生しています：{e}')
           abort(500)
        finally:
           db_pool.release(conn)
           
           
   
    @classmethod
    def allowed_file(cls, filename):
        if '.' in filename and filename.rsplit('.',1)[1].lower() in ALLOWED_EXTENSIONS:#拡張子の確認
            return True
        else:
            return False  
    
    @classmethod
    def save_images(cls,file):
        if not file:
            return None
        
                
#チャンネルクラス
class Channel:
    @classmethod
    #チャンネル新規作成に使うcreate関数を定義。引数としてname,description,created_byを渡す
    def create(cls, name, description, created_by):
        #（一度返却した）データベース接続プールからコネクションを取得してconnに代入
        conn = db_pool.get_conn()
        #tryの中でSQLクエリの実行などを行う
        try:
            #コネクションからカーソル（操作用のオブジェクト）を取得する
            with conn.cursor() as cur:
                #channelsテーブルにuid,name,descriptionを追加する
                #VALUE (%s, %s, %s)はプレースホルダ。安全に値を埋め込むためのもの
                sql = 'INSERT INTO channels(name, description, created_by) VALUES (%s, %s, %s);'
                #sqlを実行
                cur.execute(sql, (name, description, created_by))
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
    def update(cls, name, description, id):
        conn = db_pool.get_conn()
        try:
            with conn.cursor() as cur:
                #channelsテーブルの該当のidにおける、uid,name,descriptionを更新する
                sql = 'UPDATE channels SET name=%s, description=%s WHERE id=%s;'
                cur.execute(sql,(name, description, id,))
                conn.commit()
        except pymysql.Error as e:
            print(f'エラーが発生しています：{e}')
            abort(500)
        finally:
            db_pool.release(conn)

    @classmethod
    def delete(cls,id):
        conn = db_pool.get_conn()
        try:
            with conn.cursor() as cur:
                #channelsテーブルの該当のidを削除する
                sql = 'DELETE FROM channels WHERE id=%s;'
                cur.execute(sql,(id,))
                conn.commit()
        except pymysql.Error as e:
            print(f'エラーが発生しています：{e}')
            abort(500)
        finally:
            db_pool.release(conn)












# メッセージクラス
