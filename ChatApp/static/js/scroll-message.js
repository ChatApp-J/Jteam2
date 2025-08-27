/*
各チャンネル詳細ページ内、ページ読み込み時に自動で下までスクロールする
*/

const element = document.getElementById("message-area");

element.scrollBy({
  // top: elementBottom - window.innerHeight + offset,
  top: 10000,
  behavior: "auto",
});

// console.log(element);
// console.log(offset);
// console.log(elementBottom);
// console.log(elementBottom - window.innerHeight + offset);
// console.log(window);
