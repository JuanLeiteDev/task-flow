let botaoMenu = document.querySelectorAll('button.menu-botao');
let sideBar = document.querySelector('aside');

botaoMenu.forEach(botao => {
    botao.addEventListener('click', (verificarEstado) => {
        if(sideBar.classList.contains('oculto')) sideBar.classList.remove('oculto');
        else sideBar.classList.add('oculto');
    })
})

let tagsTarefas = document.querySelectorAll('.titulo>div>.tag')
let blocoTarefas = document.querySelectorAll('article.tarefa')
blocoTarefas.forEach(tarefa => {
    console.log(tarefa)
    tag = tarefa.querySelector('.titulo>div>.tag')
    switch (tag.innerText) {
        case 'Atrasada':
            tag.style.backgroundColor = "rgb(102, 12, 12)";
            tag.style.borderColor = "rgb(229, 0, 0)";
            tarefa.style.backgroundColor = "rgb(102, 12, 12)";
            break;
        case 'Pendente':
            tag.style.backgroundColor = "rgb(169, 134, 0)";
            tag.style.borderColor = "rgb(255, 239, 0)";
            tarefa.style.backgroundColor = "rgb(169, 134, 0)";
            break;
        case 'Concluída':
            tag.style.backgroundColor = "rgb(29, 121, 3)";
            tag.style.borderColor = "rgb(8, 255, 0)";
            tarefa.style.backgroundColor = "rgb(29, 121, 3)";
            break;
    }
})