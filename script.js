// ノードをクリックしたときのアクション
document.querySelectorAll('.node').forEach(node => {
  node.addEventListener('click', () => {
    alert(`${node.textContent} がクリックされました！`);
  });
});
