// Ocultar ou mostrar sidebar
const botaoMenu = document.querySelectorAll('button.menu-botao');
const sideBar = document.querySelector('aside');

botaoMenu.forEach(botao => {
    botao.addEventListener('click', () => {
        if (sideBar.classList.contains('oculto')) {
            sideBar.classList.remove('oculto');
        } else {
            sideBar.classList.add('oculto');
        }
    });
});


// Alterar cor das tags baseado no estado
const blocoTarefas = document.querySelectorAll('article.tarefa');

blocoTarefas.forEach(tarefa => {
    const tag = tarefa.querySelector('.titulo>div>.tag');

    if(!tag) return;

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
});

// Apagar uma tarefa
const botaoApagar = document.querySelectorAll('.botao-apagar');
const notificacao = document.querySelector('#confirmacao-apagar');
const btnConfirma = document.querySelector('#confirmar-apagar');
const btnCancela = document.querySelector('#cancelar-apagar');
let idTarefaSelecionada = null;
let artigoTarefaSelecionada = null;


botaoApagar.forEach(botao => {
    botao.addEventListener('click', () => {
        idTarefaSelecionada = Number(botao.dataset.id);        
        artigoTarefaSelecionada = botao.closest('article.tarefa');

        notificacao.classList.remove('oculto-notify')
    });
});

if(btnConfirma){
    btnConfirma.addEventListener('click', async () => {
        notificacao.classList.add('oculto-notify')
    
        if (!idTarefaSelecionada || !artigoTarefaSelecionada) {
            return;
        }
    
        try {
            const resposta = await fetch(`/apagar/${idTarefaSelecionada}`, {
                method: 'POST'
            });
    
            const dados = await resposta.json();
    
            if (!resposta.ok || !dados.sucesso) {
                alert(dados.erro || "Erro ao apagar tarefa.");
                return;
            }
    
            artigoTarefaSelecionada.remove();
    
        } catch (erro) {
            alert("Erro de conexão com o servidor.");
        }
    });
}

if(btnCancela){
    btnCancela.addEventListener('click', () => {
        notificacao.classList.add('oculto-notify')
    
        idTarefaSelecionada = null;
        artigoTarefaSelecionada = null;
    });
}


// Validar dados do formulário
const formulario = document.querySelector('#formulario');

if(formulario){
    formulario.addEventListener('submit', (evento) => {
        limparErros();

        let erros = validarInputs();
        console.log(erros)

        if (Object.keys(erros).length > 0) {
            evento.preventDefault();
            mostrarErros(erros);
        }
    });
}

function validarInputs(){
    const erros = {};
    const ESTADOS = ["Pendente", "Atrasada", "Concluída"];

    const titulo = formulario.titulo.value.trim();
    const descricao = formulario.desc.value.trim();
    const categoria = formulario.cat.value.trim();
    const estado = formulario.status.value.trim();
    const dataLimite = formulario.limite.value.trim();

    if (!titulo) {
        erros.titulo = "O título é obrigatório.";
    } else if (titulo.length > 20) {
        erros.titulo = "O título deve ter no máximo 20 caracteres.";
    }

    if (descricao.length > 200) {
        erros.desc = "O tamanho máximo da descrição é de 200 caracteres.";
    }

    if (categoria.length > 30) {
        erros.cat = "A categoria deve ter no máximo 30 caracteres.";
    }

    if (!ESTADOS.includes(estado)) {
        erros.status = "Estado inválido.";
    }

    if (dataLimite) {
        const data = new Date(dataLimite);

        if (isNaN(data.getTime())) {
            erros.limite = "Data inválida.";
        }
    }

    return erros;
}

function limparErros() {
    const elementosComErro = formulario.querySelectorAll('.input-erro');
    formulario.querySelectorAll('p.erro').forEach(erro => erro.remove());

    elementosComErro.forEach(elemento => {
        elemento.classList.remove('input-erro');
    });
}

function mostrarErros(erros){
    for(let campo in erros){
        const input = formulario.elements[campo];

        if (!input) continue;

        input.classList.add('input-erro');

        const mensagem = document.createElement('p');
        mensagem.classList.add('erro');
        mensagem.innerText = erros[campo];

        input.closest('.campo').appendChild(mensagem);
    }
}
