let botaoMenu = document.querySelectorAll('button.menu-botao');
let sideBar = document.querySelector('aside');

botaoMenu.forEach(botao => {
    botao.addEventListener('click', (verificarEstado) => {
        const estadoAtual = window.getComputedStyle(sideBar);
        console.log(estadoAtual.right)
        if(estadoAtual.right == '0px') sideBar.classList.add('oculto');
        else sideBar.classList.remove('oculto');
    })
})
