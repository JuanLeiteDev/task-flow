// Ocultar ou mostrar sidebar
let botaoMenu = document.querySelectorAll('button.menu-botao');
let sideBar = document.querySelector('aside');

botaoMenu.forEach(botao => {
    botao.addEventListener('click', (verificarEstado) => {
        if(sideBar.classList.contains('oculto')) sideBar.classList.remove('oculto');
        else sideBar.classList.add('oculto');
    })
})

// Alterar cor das tags baseado no estado
let tagsTarefas = document.querySelectorAll('.titulo>div>.tag')
let blocoTarefas = document.querySelectorAll('article.tarefa')
blocoTarefas.forEach(tarefa => {
    console.log(tarefa)
    tag = tarefa.querySelector('.titulo>div>.tag')
    switch (tag.innerText) {
        case 'ATRASADA':
            tag.style.backgroundColor = "rgb(255, 0, 0)";
            tag.style.borderColor = "rgb(115, 0, 0)";
            break;
        case 'PENDENTE':
            tag.style.backgroundColor = "rgb(255, 251, 0)";
            tag.style.borderColor = "rgb(87, 81, 0)";
            break;
        case 'CONCLUÍDA':
            tag.style.backgroundColor = "rgb(56, 255, 0)";
            tag.style.borderColor = "rgb(2, 58, 0)";
            break;
    }
})

// Validar dados do formulário
let formulario = document.querySelector('#formulario')
let botao = document.querySelector('#botao-criar')

formulario.addEventListener('submit', (validarDados))

function validarDados() {
    formulario.preventDefault()
    alert("Não enviado")
    formulario.reset()
}