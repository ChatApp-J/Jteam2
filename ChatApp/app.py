from flask import Flask, render_template, request, flash, redirect, url_for, session
import re
import uuid
import hashlib
from models import User, Message, Channel
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
    if name=="" or email=="" or nickname=="" or password=="" or confirm_password=="":
        flash("空のフォームがあります。記入してください。")
        
    elif password != confirm_password:
        flash("パスワードが違います")
       
    elif re.fullmatch (EMAIL_PATTERN,email) is None:
        flash("メールアドレスが正しくありません")
        
    else:
        uid = uuid.uuid4()
        #ランダムの文字列を加えることでより複雑なハッシュ化をする　salt
        salt = User.random_name(10)
        print(salt)
        salt_password = password+salt
        password=User.stretching(salt_password)
        registered_user = User.find_by_email(email)#データベースに同じアドレスを探す
            
        if registered_user != None:#もし同じアドレスがあったら
                flash('既に登録されているようです')
        else:
            User.create(uid, name, email, nickname,password,salt)
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
@app.route('/login', methods=['POST'])
def login_process():
    #ログイン画面のフォームに入力されたemailを取得
    email = request.form.get('email')
    #ログイン画面のフォームに入力されたpasswordを取得
    password = request.form.get('password')
    #もしemailあるいはpasswordがなければ
    if not email or not password:
        #空欄がありますと表示
        flash('空欄があります')
    #空欄がなければ
    else:
        #入力されたemailが新規登録で登録されたemailと一致しているか確認
        user = User.find_by_email(email)
        #もし一致せずuserがなければ、このユーザーは存在しませんと表示
        if user is None:
            flash('このユーザーは存在しません。')
        else:
            user = User.find_by_email(email)
            salt = user['salt'] 
            salt_password = password+salt
            password = User.stretching(salt_password)
            #入力されたパッシュ化されたpasswordとデータベースに登録されているそのユーザーのハッシュ化済みパスワードが一致しなければ 
            if password != user["password"]:
                #パスワードが間違っています！と表示
                flash('パスワードが間違っています！')
                return redirect(url_for('login_view')) 
            else:
                #パスワードが一致すれば、このuserのidをセッションに一時保存する
                session['uid'] = user["uid"]
                #チャンネル一覧ページに遷移
                return redirect(url_for('channels_view'))
    return redirect(url_for('login_view'))


#ログアウトの処理
@app.route('/logout')
def logout():
    #セッションに保存されている全ての情報を削除
    session.clear()
    #「ログアウトしました」と表示され、ログインページに遷移
    flash('ログアウトしました')
    return redirect(url_for('login_view'))


#チャンネル一覧ページの表示
@app.route('/channels', methods=['GET'])
def channels_view():
    #セッションからidを取得
    uid = session.get('uid')
    #もしidがなければログインされていないということなので、ログインページに遷移
    if uid is None:
        return redirect(url_for('login_view'))
    else:
        #idがあれば、チャンネルテーブル情報を全て取得
        channels = Channel.get_all()
        #ユーザーテーブルから　nicknameを取得する
        user = Message.find_by_uid(uid)
        nickname = user['nickname'] 
        #チャンネル一覧ページに遷移する
        return render_template('top/channels.html', channels=channels, nickname=nickname, uid=uid)


# チャンネルの作成
@app.route('/channels', methods=['POST'])
def create_channel():
    #セッションからidを取得
    uid = session.get('uid')
    #もしidがなければ、ログインしていないということなので、ログインページに遷移
    if uid is None:
        return redirect(url_for('login_view'))
    #フォームに入力されたchannnel_titleを取得して、name変数に代入
    name = request.form.get('channel_title')
    #フォームに入力されたchannel_descriptionを取得して、description変数に代入
    description = request.form.get('channel_description')
    #もしnameが空欄だったら
    if not name:
        #メッセージが表示
        flash('Channelの名前が空欄です')
    #空欄がなければ    
    else:
        #登録済みのチャンネルテーブルに、フォームに入力されたnameと同じnameがあるか確認
        exist_channel = Channel.find_by_name(name)
        #もし同じ名前のchannelがあったら
        if exist_channel:
            #「このチャンネルタイトルは既にあります」のメッセージが表示
            flash('このchannelの名前は既にあります')
        #同じ名前のchannelがなければ
        else:
            #nameとdescriptionが入った新しいchannelが作られる
            Channel.create(name, description, created_by=uid)
            #「新しいchannelを作成しました」のメッセージが表示
            flash('新しいchannelを作成しました')
            #作成したチャンネルが含まれた、更新されたチャンネル一覧ページに遷移
            return redirect(url_for('channels_view'))
    #途中条件に合致しなければ、更新前のチャンネル一覧ページに遷移
    return redirect(url_for('channels_view'))    


# チャンネルの編集、更新
@app.route('/channels/update_channel/<int:cid>', methods=['POST'])
def update_channel(cid):
    uid = session.get('uid')
    if uid is None:
        return redirect(url_for('login_view'))
    #編集、更新するchannelのid(cid)を探して、channel変数に代入
    channel = Channel.find_by_cid(cid)  
    #もし編集するchannelを作成したuidとログインしているユーザーのidが違ったら
    if channel['created_by'] != uid:
        #「このチャンネルの編集権限がありません」と表示
        flash('このChannelの編集権限がありません')
    #編集するchannelを作成したuidとログインしているユーザーのuidが同じだったら
    else:
        #編集フォームに入力されたchannel_titleを取得しname変数に代入
        name = request.form.get('channel_title')
        #編集フォームに入力されたchannel_descriptionを取得しdescription変数に代入
        description = request.form.get('channel_description')
        #もしnameが空欄か
        if not name:
            #メッセージが表示
            flash('Channelの名前が空欄です')
        #空欄でなければ
        else:
            #登録済みのチャンネルテーブルに、フォームに入力されたnameと同じnameがあるか確認
            exist_channel = Channel.find_by_name(name)
            #もし同じ名前のchannelがあったら、そしてそれが今編集中のチャンネル以外なら
            if exist_channel and exist_channel['id']!=cid:
                #「このチャンネルタイトルは既にあります」のメッセージが表示
                flash('このChannelの名前は既にあります')
            #同じ名前のchannelがなければ
            else:
                #channelに編集されたnameとdescriptionが入る
                Channel.update(name, description, cid)
                #「チャンネルを編集しました」のメッセージが表示
                flash('Channelを編集しました')
                #編集済みのchannelも含まれる更新されたチャンネル一覧ページに遷移
                return redirect(url_for('channels_view'))
    #途中条件に合致しなければ、更新前のチャンネル一覧ページに遷移
    return redirect(url_for('channels_view'))        
        

# チャンネルの削除
@app.route('/channels/delete_channel/<int:cid>', methods=['POST'])
def delete_channel(cid):
    uid = session.get('uid')
    if uid is None:
        return redirect(url_for('login_view'))
    #削除するchannelのid(cid)を探して、channel変数に代入
    channel = Channel.find_by_cid(cid)
    #もし削除するchannelを作成したidとログインしているユーザーのidが違ったら
    if channel['created_by'] != uid:
        #「このチャンネルの削除権限がありません」と表示
        flash('このChannelの削除権限がありません')
    #削除するchannelを作成したidとログインしているユーザーのidが同じだったら
    else:
        #該当のチャンネルを削除
        Channel.delete(cid)
        #「チャンネルを削除しました」のメッセージが表示
        flash('Channelを削除しました')
        #削除後のチャンネル一覧ページに遷移
        return redirect(url_for('channels_view'))
    #途中の条件に合致しなければ、削除せずチャンネル一覧ページに遷移
    return redirect(url_for('channels_view'))


# チャンネル詳細ページ（ルーム）の表示（各チャンネル内で、そのチャンネルに属している全メッセージを表示させる）
@app.route('/channels/<cid>/messages', methods=['GET'])
def detail(cid):
    uid = session.get('uid')
    if uid is None:
        return redirect(url_for('login_view'))
    #該当のchannelのid(cid)を探して、channel変数に代入
    channel = Channel.find_by_cid(cid)
    #該当のチャンネルのcidをもとにメッセージを全て取得して、messages変数に代入
    messages = Message.get_all(cid)
    #該当のチャンネルのメッセージ画面に遷移  
    return render_template('top/messages.html', messages=messages, channel=channel, uid=uid)

# メッセージの投稿
@app.route("/channels/<cid>/messages", methods=["POST"] )
def create_message(cid):#ユーザーがどのチャンネルに入ったかを受け取りそのチャンネルIDをcidに入れる
    uid=session.get('uid')#セッションの確認
    if uid is None: #Noneの場合は比べることが出来ないため　＝　ではなく　is　を使用する
        return redirect (url_for("login_view"))
    
    message = request.form.get("message") #フォームからメッセージを受け取る
    if message:
        Message.create(uid,cid,message)#DBに保存
    
    return redirect(url_for("detail", cid=cid))#今後app.routeが変更になっても関数が同じなら使えるためURL＿forを使用
    
        
# メッセージの削除
@app.route("/channels/<cid>/messages/<message_id>/delete", methods=["POST"])
def delete_message(cid,message_id):
    uid = session["uid"]
    if uid is None:
        return redirect (url_for("login_view"))
    
    message = Message.find(message_id)
    if message["uid"] !=uid:#もしセッションしているuidとメッセージuidが違ったら
        flash("このメッセージは削除できません")
        return redirect(url_for("detail",cid=cid))

    if message_id:
        Message.delete(message_id)
    return redirect (url_for("detail", cid=cid))
        


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
