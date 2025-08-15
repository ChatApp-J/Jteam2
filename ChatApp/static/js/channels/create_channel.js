
export const initCreateChannelModal = () => {
  const createChannelModal = document.getElementById("create_channel-modal");
  const addPageButtonClose = document.getElementById("add-page-close-button");

  const createChannelButton = document.getElementById("create_channel-button");

  // モーダル表示ボタンが押された時にモーダルを表示する
  createChannelButton.addEventListener("click", () => {
    createChannelModal.style.display = "flex";
  });

  // モーダル内のXボタンが押された時にモーダルを非表示にする
  addPageButtonClose.addEventListener("click", () => {
    createChannelModal.style.display = "none";
  });

};