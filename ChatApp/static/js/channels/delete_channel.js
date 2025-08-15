
export const initDeleteChannelModal = () => {
  const deleteChannelModal = document.getElementById("delete_channel-modal");
  const deletePageButtonClose = document.getElementById("delete-page-close-button");


  // モーダル内のXボタンが押された時にモーダルを非表示にする
  deletePageButtonClose.addEventListener("click", () => {
    deleteChannelModal.style.display = "none";
  });

};