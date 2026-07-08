let modalProf = null;
let modalDisciplina = null;

function abrirModalCadastro() {
    document.getElementById("formNovoProfessor").reset();
    document.getElementById("professorId").value = "";
    document.getElementById("modalNovoProfessorLabel").innerText = "Cadastrar Novo Professor";

    if (!modalProf) {
        modalProf = new bootstrap.Modal(document.getElementById("modalNovoProfessor"));
    }

    modalProf.show();
}

function abrirModalEdicao(botao) {
    document.getElementById("professorId").value = botao.dataset.id;
    document.getElementById("nomeProfessor").value = botao.dataset.nome;
    document.getElementById("emailProfessor").value = botao.dataset.email || "";
    document.getElementById("telefoneProfessor").value = botao.dataset.telefone || "";

    document.getElementById("modalNovoProfessorLabel").innerText = "Editar Professor";

    if (!modalProf) {
        modalProf = new bootstrap.Modal(document.getElementById("modalNovoProfessor"));
    }

    modalProf.show();
}

function deletarProfessor(id, nome) {
    if (confirm(`Tem certeza que deseja remover o professor "${nome}"?`)) {
        fetch(`/professores/${id}`, {
            method: "DELETE"
        }).then(response => {
            if (response.ok) {
                window.location.reload();
            }
        });
    }
}

function abrirModalCadastroDisciplina() {
    document.getElementById("formDisciplina").reset();
    document.getElementById("disciplinaId").value = "";
    document.getElementById("modalDisciplinaLabel").innerText = "Cadastrar Disciplina";

    if (!modalDisciplina) {
        modalDisciplina = new bootstrap.Modal(document.getElementById("modalDisciplina"));
    }

    modalDisciplina.show();
}

function abrirModalEdicaoDisciplina(botao) {
    document.getElementById("disciplinaId").value = botao.dataset.id;
    document.getElementById("nomeDisciplina").value = botao.dataset.nome;

    document.getElementById("modalDisciplinaLabel").innerText = "Editar Disciplina";

    if (!modalDisciplina) {
        modalDisciplina = new bootstrap.Modal(document.getElementById("modalDisciplina"));
    }

    modalDisciplina.show();
}

function deletarDisciplina(id, nome) {
    if (confirm(`Tem certeza que deseja remover a disciplina "${nome}"?`)) {
        fetch(`/disciplinas/${id}`, {
            method: "DELETE"
        }).then(response => {
            if (response.ok) {
                window.location.reload();
            }
        });
    }
}

function alternarStatusDisciplina(id, nome) {
    if (confirm(`Deseja alterar o status da disciplina "${nome}"?`)) {
        fetch(`/disciplinas/${id}/status`, {
            method: "PATCH"
        }).then(async response => {
            if (response.ok) {
                window.location.reload();
            } else {
                const erro = await response.text();
                alert(`Erro no Backend (${response.status}): ${erro}`);
            }
        });
    }
}

document.addEventListener("DOMContentLoaded", function () {

    const formPerfilEscola = document.getElementById("formPerfilEscola");

    if (formPerfilEscola) {
        formPerfilEscola.addEventListener("submit", function (e) {
            e.preventDefault();

            const idEscola = document.getElementById("escolaId").value;

            const payload = {
                nome: document.getElementById("nomeEscola").value,
                cidade: document.getElementById("cidadeEscola").value,
                estado: document.getElementById("estadoEscola").value
            };

            fetch(idEscola ? `/escolas/${idEscola}` : "/escolas", {
                method: idEscola ? "PUT" : "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify(payload)
            }).then(response => {
                if (response.ok) {
                    window.location.reload();
                }
            });
        });
    }

    const formNovoProfessor = document.getElementById("formNovoProfessor");

    if (formNovoProfessor) {
        formNovoProfessor.addEventListener("submit", function (e) {
            e.preventDefault();

            const id = document.getElementById("professorId").value;
            const url = id ? `/professores/${id}` : "/professores";
            const metodo = id ? "PUT" : "POST";

            const payload = {
                nome: document.getElementById("nomeProfessor").value,
                email: document.getElementById("emailProfessor").value,
                telefone: document.getElementById("telefoneProfessor").value
            };

            fetch(url, {
                method: metodo,
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify(payload)
            }).then(async response => {
                if (response.ok) {
                    window.location.reload();
                } else {
                    const erro = await response.text();
                    alert(`Erro no Backend (${response.status}): ${erro}`);
                }
            });
        });
    }

    const formDisciplina = document.getElementById("formDisciplina");

    if (formDisciplina) {
        formDisciplina.addEventListener("submit", function (e) {
            e.preventDefault();

            const id = document.getElementById("disciplinaId").value;
            const url = id ? `/disciplinas/${id}` : "/disciplinas";
            const metodo = id ? "PUT" : "POST";

            const payload = {
                nome: document.getElementById("nomeDisciplina").value
            };

            fetch(url, {
                method: metodo,
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify(payload)
            }).then(async response => {
                if (response.ok) {
                    window.location.reload();
                } else {
                    const erro = await response.text();
                    alert(`Erro no Backend (${response.status}): ${erro}`);
                }
            });
        });
    }
});