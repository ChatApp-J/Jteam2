
import { initCreateChannelModal } from "/static/js/channels/create_channel.js";
import { initUpdateChannelModal } from "/static/js/channels/update_channel.js";
import { initDeleteChannelModal } from "/static/js/channels/delete_channel.js";
//update_channel.js内のupdate_channel-modalというidを探し、updateChannelModal変数に代入
const updateChannelModal = document.getElementById('update_channel-modal');
//delete_channel.js内のdelete_channel-modalというidを探し、deleteChannelModal変数に代入
const deleteChannelModal = document.getElementById('delete_channel-modal');


//createChannelsListという変数に、= () => {以下の内容（アロー関数として定義されたもの）を代入している
const createChannelsList = () => {
  //querySelector()はあらゆるHTML要素を取得できる 
  //クラス"channel-box"を持つ文書内の要素内、最初のものを返す
  //ここでは、html内を見て.channel-boxに一致する最初の要素を返す
  const ul = document.querySelector(".channel-box");
  //一度チャンネルリストを空にする
  //ulは指定している要素、ここでは""を代入している。つまり空ということ。
  //innerHTMLはHTML要素の<開始タグ>と<終了タグ>に内包されたものでテキストだけでなくHTML要素も認識できる
  ul.innerHTML = "";

  //新しくチャンネルが作られた時に表示する
  //Channel.get_all()で取得したチャンネル一覧が代入されたchannelsをjavascriptで使えるようにしたもの
  //channelはchannelsの１つ１つの要素
  //配列名.forEach(コールバック関数（配列の要素）);で使うが、今回はアロー関数を使用している
  channels.forEach((channel) => {
    //createElement(タグ名)、引数のタグ名で指定されたHTML要素を生成
    //今回は新しいa要素を生成
    const a = document.createElement("a");
    //新しいli要素を生成
    const li = document.createElement("li");
    li.classList.add("channel-set")
    //channelURLという変数にテンプレートリテラル（バッククォートで囲んだ範囲を文字列とするリテラル(ベタがきした文字や数字))を代入
    //文字列内で${変数名}と書くと、変数の値を埋め込むことができる
    //ここではリンクのパスを渡している(@app.routeの後に指定しているもの)
    const channelURL = `/channels/${channel.id}/messages`;
    //innerTextとはHTML要素の,<開始タグ>と<終了タグ>に内包されたテキストのみのこと
    //ここではchannelのnameをaに代入
    a.innerText = channel.name;
    //要素.setAttributre(属性名, 値) 属性を設定変更するためのメソッド
    //つまり、a要素にhrefをchannelURLと設定している
    a.setAttribute("href", channelURL);
    a.classList.add("channelname")
    //親要素.appendChild(子要素)
    //親要素liの末尾に子要素としてaを追加
    li.appendChild(a);
    //ulの末尾にliを追加
    ul.appendChild(li);
        
    // もしチャンネル作成者uidと自分のuidが同じだった場合は編集ボタンを追加
    if (uid === channel.created_by){
      //createElement(タグ名)、引数のタグ名で指定されたHTML要素を生成  
      const updateChannelButton = document.createElement('button')
      //innerHTMLはHTML要素の<開始タグ>と<終了タグ>に内包されたものでテキストだけでなくHTML要素も認識できる
      updateChannelButton.innerHTML =
        '<ion-icon name="pencil" style="color: #403C3C"></ion-icon>';
        //updateButtonにクラス名update-buttonを追加
        updateChannelButton.classList.add('update_channel-button'); 
        li.appendChild(updateChannelButton);
        //対象の要素.addEventListener(イベントの種類, 関数,false);でイベント処理を実行するメソッド
        //clickされたら{}内の処理を実行する
        updateChannelButton.addEventListener('click', () =>{
          //updateChannelModalを表示させる
          updateChannelModal.style.display = 'flex';
          const updateChannelForm = 
            document.getElementById('updateChannelForm');
            //文字列内で${変数名}と書くと、変数の値を埋め込むことができる
            //ここではendpoint変数にリンクのパスを渡している(@app.routeの後に指定しているもの)
            const endpoint = `/channels/update_channel/${channel.id}`;
            updateChannelForm.action = endpoint;
        });
    };        
            
    // もしチャンネル作成者uidと自分のuidが同じだった場合は削除ボタンを追加
    if (uid === channel.created_by) {
      const deleteChannelButton = document.createElement('button');
      deleteChannelButton.innerHTML =
        '<ion-icon name="trash-outline" style="color: #403C3C"></ion-icon>';
        deleteChannelButton.classList.add('delete_channel-button');
        li.appendChild(deleteChannelButton);
        // ゴミ箱ボタンが押された時にdeleteモーダルを表示させる
        deleteChannelButton.addEventListener('click', () => {
          deleteChannelModal.style.display = 'flex';

          const deleteChannelForm =
            document.getElementById("deleteChannelForm");

            const endpoint = `/channels/delete_channel/${channel.id}`;
            deleteChannelForm.action = endpoint;
        });
    };
    
    const channelDescriptionTooltip = document.createElement("div");
          channelDescriptionTooltip.style.display = "inline-Block";
          channelDescriptionTooltip.classList.add(
            "channel-description-tooltip"
          );
          channelDescriptionTooltip.appendChild(li);
          const tooltipBody = document.createElement("div");
          tooltipBody.classList.add("tooltip-body");
          tooltipBody.innerHTML = channel.description;
          channelDescriptionTooltip.appendChild(tooltipBody);
          ul.appendChild(channelDescriptionTooltip);


  });
    // チャンネル追加ボタンを付け加える
    const createChannelButton = document.createElement("ion-icon");
    createChannelButton.id = "create_channel-button";
    createChannelButton.name = "add-circle-outline";
    createChannelButton.style = "color: #403C3C";
    ul.appendChild(createChannelButton);
};
//initは変数、{}内に初期化したときに実行する処理を書く
//ここではcreateChannelListでまとめた全ての処理と先頭のでimportしたファイルを読み込んでいる
const init = () => {
  createChannelsList();          
  initCreateChannelModal();      
  initUpdateChannelModal();
  initDeleteChannelModal();
};
//DOMContentLoadedはDOMツリーの読み込み完了後に発火する
//DOMはブラウザがHTMLを解析する際に生成するデータ構造。各要素は階層構造（ツリー構造）で表現され、それをDOMツリーと呼ぶ
document.addEventListener('DOMContentLoaded', init);
