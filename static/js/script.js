let modalProf = null;
let modalDisciplina = null;
let modalTurma = null;

function abrirModalCadastro() {
    document.getElementById("formNovoProfessor").reset();
    document.getElementById("professorId").value = "";
    document.getElementById("modalNovoProfessorLabel").innerText = "Cadastrar Novo Professor";

    const selectDisciplinas = document.getElementById("disciplinasProfessor");

    if (selectDisciplinas) {
        Array.from(selectDisciplinas.options).forEach(option => {
            option.selected = false;
        });
    }

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

    const selectDisciplinas = document.getElementById("disciplinasProfessor");
    const disciplinasSelecionadas = botao.dataset.disciplinas
        ? botao.dataset.disciplinas.split(",")
        : [];

    if (selectDisciplinas) {
        Array.from(selectDisciplinas.options).forEach(option => {
            option.selected = disciplinasSelecionadas.includes(option.value);
        });
    }

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

function abrirModalCadastroTurma() {
    document.getElementById("formTurma").reset();
    document.getElementById("turmaId").value = "";
    document.getElementById("modalTurmaLabel").innerText = "Cadastrar Turma";

    if (!modalTurma) {
        modalTurma = new bootstrap.Modal(document.getElementById("modalTurma"));
    }

    modalTurma.show();
}

function abrirModalEdicaoTurma(botao) {
    document.getElementById("turmaId").value = botao.dataset.id;
    document.getElementById("nomeTurma").value = botao.dataset.nome;
    document.getElementById("serieTurma").value = botao.dataset.serie;
    document.getElementById("turnoTurma").value = botao.dataset.turno;

    document.getElementById("modalTurmaLabel").innerText = "Editar Turma";

    if (!modalTurma) {
        modalTurma = new bootstrap.Modal(document.getElementById("modalTurma"));
    }

    modalTurma.show();
}

function deletarTurma(id, nome) {
    if (confirm(`Tem certeza que deseja remover a turma "${nome}"?`)) {
        fetch(`/turmas/${id}`, {
            method: "DELETE"
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

            const selectDisciplinas = document.getElementById("disciplinasProfessor");

            const disciplinasSelecionadas = selectDisciplinas
                ? Array.from(selectDisciplinas.selectedOptions).map(option => Number(option.value))
                : [];

            const payload = {
                nome: document.getElementById("nomeProfessor").value,
                email: document.getElementById("emailProfessor").value,
                telefone: document.getElementById("telefoneProfessor").value,
                disciplinas_ids: disciplinasSelecionadas
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

    const formTurma = document.getElementById("formTurma");

    if (formTurma) {
        formTurma.addEventListener("submit", function (e) {
            e.preventDefault();

            const id = document.getElementById("turmaId").value;
            const url = id ? `/turmas/${id}` : "/turmas";
            const metodo = id ? "PUT" : "POST";

            const payload = {
                nome: document.getElementById("nomeTurma").value,
                serie: document.getElementById("serieTurma").value,
                turno: document.getElementById("turnoTurma").value
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

    const abaSalva = localStorage.getItem("abaCadastroAtiva");

    if (abaSalva) {
    const botaoAba = document.querySelector(`[data-bs-target="${abaSalva}"]`);

    if (botaoAba) {
        const tab = new bootstrap.Tab(botaoAba);
        tab.show();
    }
    }

    document.querySelectorAll('#cadastrosTabs button[data-bs-toggle="tab"]').forEach(botao => {
    botao.addEventListener("shown.bs.tab", function (e) {
        localStorage.setItem("abaCadastroAtiva", e.target.dataset.bsTarget);
    });
    });


});