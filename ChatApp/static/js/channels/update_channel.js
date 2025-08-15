
export const initUpdateChannelModal = () => {
  const updateChannelModal = document.getElementById("update_channel-modal");
  const updatePageButtonClose = document.getElementById("update-page-close-button");


  // モーダル内のXボタンが押された時にモーダルを非表示にする
  updatePageButtonClose.addEventListener("click", () => {
    updateChannelModal.style.display = "none";
  });

};