from flask import Flask, render_template, request, flash, redirect, url_for


app = Flask(__name__)


#トップページの表示
@app.route('/', methods = ['GET'])
def top ():
    return render_template('top/top.html')


#サインアップページの表示
@app.route('/signup', methods = ['GET'])
def signup ():
    return render_template('top/signup.html')


#サインアップの処理


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
