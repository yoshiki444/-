document.querySelectorAll('.node').forEach(node => {
    node.addEventListener('click', (event) => {
        const target = event.currentTarget.getAttribute('data-target');
        if (target) {
            document.querySelector(target).scrollIntoView({ behavior: 'smooth' });
        } else {
            alert("終了です！");
        }
    });
});
