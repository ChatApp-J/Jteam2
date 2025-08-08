from flask import Flask, render_template, request, flash, redirect, url_for, session
import re
import uuid
import hashlib
from models import User
import os
from datetime import timedelta


EMAIL_PATTERN = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9._%+-]+\.[a-zA-z]{2,}$"
SESSION_DAYS= 30
app = Flask(__name__)

app.secret_key = os.getenv('SECRET_KEY'or uuid.uuid4().hex)#.envから秘密鍵を読み込む　なかったら生成する
app.permanent_session_lifetime = timedelta(days=SESSION_DAYS)# セッションの日数を計算


#トップページの表示
@app.route('/', methods = ['GET'])
def top ():
    return render_template('top/top.html')


#サインアップページの表示
@app.route('/signup', methods = ['GET'])
def signup ():
    return render_template('top/signup.html')


#サインアップの処理
@app.route('/signup', methods = ['POST'])
def signup_create():#関数を制作しrequestを使用し登録内容を取得
    name = request.form.get('name')
    email = request.form.get("email")
    nickname =request.form.get("nickname")
    password = request.form.get("password")
    confirm_password = request.form.get("confirm_password")
    if name==" " or email==" " or nickname ==  " " or password == " " or confirm_password == " ":
        flash("空のフォームがあります。記入してください。")
        
    elif password != confirm_password:
        flash("パスワードが違います")
       
    elif re.fullmatch (EMAIL_PATTERN,email) is None:
        flash("メールアドレスが正しくありません")
        
    else:
        uid = uuid.uuid4()
        #任意の文字列を加えることでより複雑なハッシュ化をする　salt
        salt = "Solty"
        salt_password = password+salt
        password = hashlib.sha256(salt_password.encode("utf-8")).hexdigest()
        registered_user = User.find_by_email(email)#データベースに同じアドレスを探す
            
        if registered_user != None:#もし同じアドレスがあったら
                flash('既に登録されているようです')
        else:
            User.create(uid, name, email, nickname,password)
            UserId = str(uid)
            session['uid'] = UserId
            return redirect(url_for('channels_view'))
    return redirect(url_for('signup'))
        
    
    
    
    
    #ログインページの表示
#画面の取得なのでGETメソッド
@app.route('/login', methods=['GET'])
#ログイン画面の定義
# render_templateを使い、templatesフォルダ内のlogin.htmlが返る
def login_view():
    return render_template('top/login.html')


#ログインの処理


#ログアウトの処理


#チャンネル一覧ページ（ホーム？）の表示



# チャンネル（ルーム？）の作成


# チャンネル（ルーム？）の更新


# チャンネル（ルーム？）の削除


# チャンネル詳細ページ（ルーム）の表示（各チャンネル内で、そのチャンネルに属している全メッセージを表示させる）


# メッセージの投稿


# メッセージの削除


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
