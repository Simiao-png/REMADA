let modalProf = null;
let modalDisciplina = null;
let modalTurma = null;

let dadosPlanejamento = null;


function abrirModalCadastro() {
    document.getElementById("formNovoProfessor").reset();
    document.getElementById("professorId").value = "";
    document.getElementById("modalNovoProfessorLabel").innerText =
        "Cadastrar Novo Professor";

    const selectDisciplinas =
        document.getElementById("disciplinasProfessor");

    if (selectDisciplinas) {
        Array.from(selectDisciplinas.options).forEach(option => {
            option.selected = false;
        });
    }

    document.querySelectorAll(".segmento-professor").forEach(check => {
        check.checked = false;
    });

    const trabalhaOutraEscola =
        document.getElementById("trabalhaOutraEscolaProfessor");

    if (trabalhaOutraEscola) {
        trabalhaOutraEscola.checked = false;
    }

    const observacoes =
        document.getElementById("observacoesProfessor");

    if (observacoes) {
        observacoes.value = "";
    }

    if (!modalProf) {
        modalProf = new bootstrap.Modal(
            document.getElementById("modalNovoProfessor")
        );
    }

    modalProf.show();
}


function abrirModalEdicao(botao) {
    document.getElementById("professorId").value =
        botao.dataset.id;

    document.getElementById("nomeProfessor").value =
        botao.dataset.nome;

    const segmentosSelecionados = botao.dataset.segmentos
        ? botao.dataset.segmentos.split(",").filter(Boolean)
        : [];

    document.querySelectorAll(".segmento-professor").forEach(check => {
        check.checked = segmentosSelecionados.includes(check.value);
    });

    const selectDisciplinas =
        document.getElementById("disciplinasProfessor");

    const disciplinasSelecionadas = botao.dataset.disciplinas
        ? botao.dataset.disciplinas.split(",").filter(Boolean)
        : [];

    if (selectDisciplinas) {
        Array.from(selectDisciplinas.options).forEach(option => {
            option.selected =
                disciplinasSelecionadas.includes(option.value);
        });
    }

    const trabalhaOutraEscola =
        document.getElementById("trabalhaOutraEscolaProfessor");

    if (trabalhaOutraEscola) {
        trabalhaOutraEscola.checked =
            botao.dataset.outraEscola === "true";
    }

    const observacoes =
        document.getElementById("observacoesProfessor");

    if (observacoes) {
        observacoes.value =
            botao.dataset.observacoes || "";
    }

    document.getElementById("modalNovoProfessorLabel").innerText =
        "Editar Professor";

    if (!modalProf) {
        modalProf = new bootstrap.Modal(
            document.getElementById("modalNovoProfessor")
        );
    }

    modalProf.show();
}


function deletarProfessor(id, nome) {
    if (
        confirm(
            `Tem certeza que deseja remover o professor "${nome}"?`
        )
    ) {
        fetch(`/professores/${id}`, {
            method: "DELETE"
        }).then(async response => {
            if (response.ok) {
                window.location.reload();
            } else {
                const erro = await response.text();

                alert(
                    `Erro no Backend (${response.status}): ${erro}`
                );
            }
        });
    }
}


function abrirModalCadastroDisciplina() {
    document.getElementById("formDisciplina").reset();
    document.getElementById("disciplinaId").value = "";

    document.getElementById("modalDisciplinaLabel").innerText =
        "Cadastrar Disciplina";

    if (!modalDisciplina) {
        modalDisciplina = new bootstrap.Modal(
            document.getElementById("modalDisciplina")
        );
    }

    modalDisciplina.show();
}


const cor = document.getElementById("corDisciplina");

if (cor) {
    cor.value = "#2563EB";
}


function abrirModalEdicaoDisciplina(botao) {
    document.getElementById("disciplinaId").value =
        botao.dataset.id;

    document.getElementById("nomeDisciplina").value =
        botao.dataset.nome;

    document.getElementById("modalDisciplinaLabel").innerText =
        "Editar Disciplina";

    const cor = document.getElementById("corDisciplina");

    if (cor) {
        cor.value = botao.dataset.cor || "#2563EB";
    }

    if (!modalDisciplina) {
        modalDisciplina = new bootstrap.Modal(
            document.getElementById("modalDisciplina")
        );
    }

    modalDisciplina.show();
}


function deletarDisciplina(id, nome) {
    if (
        confirm(
            `Tem certeza que deseja remover a disciplina "${nome}"?`
        )
    ) {
        fetch(`/disciplinas/${id}`, {
            method: "DELETE"
        }).then(async response => {
            if (response.ok) {
                window.location.reload();
            } else {
                const erro = await response.text();

                alert(
                    `Erro no Backend (${response.status}): ${erro}`
                );
            }
        });
    }
}


function alternarStatusDisciplina(id, nome) {
    if (
        confirm(
            `Deseja alterar o status da disciplina "${nome}"?`
        )
    ) {
        fetch(`/disciplinas/${id}/status`, {
            method: "PATCH"
        }).then(async response => {
            if (response.ok) {
                window.location.reload();
            } else {
                const erro = await response.text();

                alert(
                    `Erro no Backend (${response.status}): ${erro}`
                );
            }
        });
    }
}


function abrirModalCadastroTurma() {
    document.getElementById("formTurma").reset();
    document.getElementById("turmaId").value = "";

    document.getElementById("modalTurmaLabel").innerText =
        "Cadastrar Turma";

    if (!modalTurma) {
        modalTurma = new bootstrap.Modal(
            document.getElementById("modalTurma")
        );
    }

    modalTurma.show();
}


function abrirModalEdicaoTurma(botao) {
    document.getElementById("turmaId").value =
        botao.dataset.id;

    document.getElementById("nomeTurma").value =
        botao.dataset.nome;

    document.getElementById("serieTurma").value =
        botao.dataset.serie;

    document.getElementById("turnoTurma").value =
        botao.dataset.turno;

    document.getElementById("modalTurmaLabel").innerText =
        "Editar Turma";

    if (!modalTurma) {
        modalTurma = new bootstrap.Modal(
            document.getElementById("modalTurma")
        );
    }

    modalTurma.show();
}


function deletarTurma(id, nome) {
    if (
        confirm(
            `Tem certeza que deseja remover a turma "${nome}"?`
        )
    ) {
        fetch(`/turmas/${id}`, {
            method: "DELETE"
        }).then(async response => {
            if (response.ok) {
                window.location.reload();
            } else {
                const erro = await response.text();

                alert(
                    `Erro no Backend (${response.status}): ${erro}`
                );
            }
        });
    }
}


function carregarDadosPlanejamento() {
    const elemento =
        document.getElementById("dadosPlanejamento");

    if (!elemento) {
        return;
    }

    dadosPlanejamento = JSON.parse(elemento.textContent);
}


function buscarProfessorPlanejamento(professorId) {
    if (!dadosPlanejamento) {
        return null;
    }

    return dadosPlanejamento.professores.find(
        professor =>
            String(professor.id) === String(professorId)
    );
}


function carregarProfessorDisponibilidade() {
    const selectProfessor =
        document.getElementById("professorDisponibilidade");

    if (!selectProfessor || !dadosPlanejamento) {
        return;
    }

    const professorId = selectProfessor.value;

    const professor =
        buscarProfessorPlanejamento(professorId);

    if (!professor) {
        return;
    }

    const nomeProfessor =
        document.getElementById(
            "nomeProfessorDisponibilidade"
        );

    const disciplinasProfessor =
        document.getElementById(
            "disciplinasProfessorDisponibilidade"
        );

    if (nomeProfessor) {
        nomeProfessor.innerText = professor.nome;
    }

    if (disciplinasProfessor) {
        if (
            professor.disciplinas &&
            professor.disciplinas.length > 0
        ) {
            disciplinasProfessor.innerHTML =
                professor.disciplinas
                    .map(
                        disciplina =>
                            `<span class="badge bg-primary-subtle text-primary me-1">${disciplina}</span>`
                    )
                    .join("");
        } else {
            disciplinasProfessor.innerHTML =
                `<span class="text-muted">Nenhuma disciplina vinculada</span>`;
        }
    }

    montarTabelaDisponibilidade(professor);
}


function montarTabelaDisponibilidade(professor) {
    const corpoTabela =
        document.getElementById(
            "corpoTabelaDisponibilidade"
        );

    if (!corpoTabela || !dadosPlanejamento) {
        return;
    }

    corpoTabela.innerHTML = "";

    dadosPlanejamento.numerosAulas.forEach(numeroAula => {
        const linha = document.createElement("tr");

        const colunaAula =
            document.createElement("td");

        colunaAula.className = "fw-semibold";
        colunaAula.innerText = `${numeroAula}ª aula`;

        linha.appendChild(colunaAula);

        dadosPlanejamento.diasSemana.forEach(dia => {
            const coluna =
                document.createElement("td");

            const disponivel =
                professor.disponibilidades.some(item =>
                    item.dia_semana === dia.valor &&
                    Number(item.numero_aula) ===
                        Number(numeroAula)
                );

            const botao =
                document.createElement("button");

            botao.type = "button";

            botao.className = disponivel
                ? "btn btn-sm btn-success disponibilidade-botao"
                : "btn btn-sm btn-outline-secondary disponibilidade-botao";

            botao.dataset.dia = dia.valor;
            botao.dataset.aula = numeroAula;

            botao.dataset.disponivel =
                disponivel ? "true" : "false";

            botao.innerText = disponivel ? "✓" : "—";

            botao.addEventListener(
                "click",
                function () {
                    alternarDisponibilidadeBotao(botao);
                }
            );

            coluna.appendChild(botao);
            linha.appendChild(coluna);
        });

        corpoTabela.appendChild(linha);
    });
}


function alternarDisponibilidadeBotao(botao) {
    const disponivel =
        botao.dataset.disponivel === "true";

    if (disponivel) {
        botao.dataset.disponivel = "false";

        botao.className =
            "btn btn-sm btn-outline-secondary disponibilidade-botao";

        botao.innerText = "—";
    } else {
        botao.dataset.disponivel = "true";

        botao.className =
            "btn btn-sm btn-success disponibilidade-botao";

        botao.innerText = "✓";
    }
}


function salvarDisponibilidadeProfessorAtual() {
    const selectProfessor =
        document.getElementById("professorDisponibilidade");

    if (!selectProfessor) {
        return;
    }

    const professorId = selectProfessor.value;

    const botoes =
        document.querySelectorAll(
            ".disponibilidade-botao"
        );

    const disponibilidades = [];

    botoes.forEach(botao => {
        if (botao.dataset.disponivel === "true") {
            disponibilidades.push({
                dia_semana: botao.dataset.dia,
                numero_aula:
                    Number(botao.dataset.aula)
            });
        }
    });

    fetch(
        `/disponibilidades/professor/${professorId}`,
        {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                disponibilidades: disponibilidades
            })
        }
    ).then(async response => {
        if (response.ok) {
            const professor =
                buscarProfessorPlanejamento(professorId);

            if (professor) {
                professor.disponibilidades =
                    disponibilidades;
            }

            alert(
                "Disponibilidade salva com sucesso!"
            );
        } else {
            const erro = await response.text();

            alert(
                `Erro no Backend (${response.status}): ${erro}`
            );
        }
    });
}


function montarPayloadParametrosSegmentos() {
    if (
        typeof salvarFormularioSegmentoAtual ===
        "function"
    ) {
        salvarFormularioSegmentoAtual();
    }

    if (
        typeof atualizarJsonSegmentosParametros ===
        "function"
    ) {
        atualizarJsonSegmentosParametros();
    }

    if (
        typeof parametrosPorSegmento !==
        "undefined"
    ) {
        return {
            segmentos: parametrosPorSegmento
        };
    }

    const campoJson =
        document.getElementById(
            "segmentosParametrosJson"
        );

    if (campoJson && campoJson.value) {
        return {
            segmentos:
                JSON.parse(campoJson.value)
        };
    }

    return {
        segmentos: {}
    };
}


document.addEventListener(
    "DOMContentLoaded",
    function () {

        const formPerfilEscola =
            document.getElementById(
                "formPerfilEscola"
            );

        if (formPerfilEscola) {
            formPerfilEscola.addEventListener(
                "submit",
                function (e) {
                    e.preventDefault();

                    const idEscola =
                        document.getElementById(
                            "escolaId"
                        ).value;

                    const payload = {
                        nome:
                            document.getElementById(
                                "nomeEscola"
                            ).value,

                        cidade:
                            document.getElementById(
                                "cidadeEscola"
                            ).value,

                        estado:
                            document.getElementById(
                                "estadoEscola"
                            ).value
                    };

                    fetch(
                        idEscola
                            ? `/escolas/${idEscola}`
                            : "/escolas",
                        {
                            method:
                                idEscola
                                    ? "PUT"
                                    : "POST",

                            headers: {
                                "Content-Type":
                                    "application/json"
                            },

                            body:
                                JSON.stringify(payload)
                        }
                    ).then(response => {
                        if (response.ok) {
                            window.location.reload();
                        }
                    });
                }
            );
        }


        const formParametros =
            document.getElementById(
                "formParametros"
            );

        if (formParametros) {
            formParametros.addEventListener(
                "submit",
                async function (e) {
                    e.preventDefault();

                    const payload =
                        montarPayloadParametrosSegmentos();

                    const response = await fetch(
                        "/configuracoes-horarias/parametros",
                        {
                            method: "POST",

                            headers: {
                                "Content-Type":
                                    "application/json"
                            },

                            body:
                                JSON.stringify(payload)
                        }
                    );

                    if (response.ok) {
                        alert(
                            "Parâmetros salvos com sucesso!"
                        );

                        window.location.reload();
                    } else {
                        const erro =
                            await response.text();

                        alert(
                            `Erro no Backend (${response.status}): ${erro}`
                        );
                    }
                }
            );
        }


        const formNovoProfessor =
            document.getElementById(
                "formNovoProfessor"
            );

        if (formNovoProfessor) {
            formNovoProfessor.addEventListener(
                "submit",
                function (e) {
                    e.preventDefault();

                    const id =
                        document.getElementById(
                            "professorId"
                        ).value;

                    const url = id
                        ? `/professores/${id}`
                        : "/professores";

                    const metodo = id
                        ? "PUT"
                        : "POST";

                    const selectDisciplinas =
                        document.getElementById(
                            "disciplinasProfessor"
                        );

                    const disciplinasSelecionadas =
                        selectDisciplinas
                            ? Array.from(
                                  selectDisciplinas.selectedOptions
                              ).map(option =>
                                  Number(option.value)
                              )
                            : [];

                    const segmentosSelecionados =
                        Array.from(
                            document.querySelectorAll(
                                ".segmento-professor:checked"
                            )
                        ).map(
                            item => item.value
                        );

                    if (
                        segmentosSelecionados.length === 0
                    ) {
                        alert(
                            "Selecione pelo menos um segmento."
                        );

                        return;
                    }

                    const trabalhaOutraEscola =
                        document.getElementById(
                            "trabalhaOutraEscolaProfessor"
                        );

                    const observacoes =
                        document.getElementById(
                            "observacoesProfessor"
                        );

                    const payload = {
                        nome:
                            document.getElementById(
                                "nomeProfessor"
                            ).value,

                        segmentos:
                            segmentosSelecionados,

                        disciplinas_ids:
                            disciplinasSelecionadas,

                        trabalha_outra_escola:
                            trabalhaOutraEscola
                                ? trabalhaOutraEscola.checked
                                : false,

                        observacoes:
                            observacoes
                                ? observacoes.value
                                : ""
                    };

                    fetch(url, {
                        method: metodo,

                        headers: {
                            "Content-Type":
                                "application/json"
                        },

                        body:
                            JSON.stringify(payload)
                    }).then(async response => {
                        if (response.ok) {
                            window.location.reload();
                        } else {
                            const erro =
                                await response.text();

                            alert(
                                `Erro no Backend (${response.status}): ${erro}`
                            );
                        }
                    });
                }
            );
        }


        const formDisciplina =
            document.getElementById(
                "formDisciplina"
            );

        if (formDisciplina) {
            formDisciplina.addEventListener(
                "submit",
                function (e) {
                    e.preventDefault();

                    const id =
                        document.getElementById(
                            "disciplinaId"
                        ).value;

                    const url = id
                        ? `/disciplinas/${id}`
                        : "/disciplinas";

                    const metodo = id
                        ? "PUT"
                        : "POST";

                    const payload = {
                        nome:
                            document.getElementById(
                                "nomeDisciplina"
                            ).value,

                        cor:
                            document.getElementById(
                                "corDisciplina"
                            ).value
                    };

                    fetch(url, {
                        method: metodo,

                        headers: {
                            "Content-Type":
                                "application/json"
                        },

                        body:
                            JSON.stringify(payload)
                    }).then(async response => {
                        if (response.ok) {
                            window.location.reload();
                        } else {
                            const erro =
                                await response.text();

                            alert(
                                `Erro no Backend (${response.status}): ${erro}`
                            );
                        }
                    });
                }
            );
        }


        const formTurma =
            document.getElementById(
                "formTurma"
            );

        if (formTurma) {
            formTurma.addEventListener(
                "submit",
                function (e) {
                    e.preventDefault();

                    const id =
                        document.getElementById(
                            "turmaId"
                        ).value;

                    const url = id
                        ? `/turmas/${id}`
                        : "/turmas";

                    const metodo = id
                        ? "PUT"
                        : "POST";

                    const payload = {
                        nome:
                            document.getElementById(
                                "nomeTurma"
                            ).value,

                        serie:
                            document.getElementById(
                                "serieTurma"
                            ).value,

                        turno:
                            document.getElementById(
                                "turnoTurma"
                            ).value
                    };

                    fetch(url, {
                        method: metodo,

                        headers: {
                            "Content-Type":
                                "application/json"
                        },

                        body:
                            JSON.stringify(payload)
                    }).then(async response => {
                        if (response.ok) {
                            window.location.reload();
                        } else {
                            const erro =
                                await response.text();

                            alert(
                                `Erro no Backend (${response.status}): ${erro}`
                            );
                        }
                    });
                }
            );
        }


        const abaSalva =
            localStorage.getItem(
                "abaCadastroAtiva"
            );

        if (abaSalva) {
            const botaoAba =
                document.querySelector(
                    `[data-bs-target="${abaSalva}"]`
                );

            if (botaoAba) {
                const tab =
                    new bootstrap.Tab(botaoAba);

                tab.show();
            }
        }


        document
            .querySelectorAll(
                '#cadastrosTabs button[data-bs-toggle="tab"]'
            )
            .forEach(botao => {
                botao.addEventListener(
                    "shown.bs.tab",
                    function (e) {
                        localStorage.setItem(
                            "abaCadastroAtiva",
                            e.target.dataset.bsTarget
                        );
                    }
                );
            });


        carregarDadosPlanejamento();


        const selectProfessorDisponibilidade =
            document.getElementById(
                "professorDisponibilidade"
            );

        if (selectProfessorDisponibilidade) {
            carregarProfessorDisponibilidade();

            selectProfessorDisponibilidade.addEventListener(
                "change",
                function () {
                    carregarProfessorDisponibilidade();
                }
            );
        }
    }
);


document
    .querySelectorAll(".disciplina-cor-bolinha")
    .forEach(el => {
        const cor =
            el.dataset.corDisciplina ||
            el.dataset.cor ||
            "#2563EB";

        el.style.backgroundColor = cor;
    });


document
    .querySelectorAll(".badge-disciplina-colorida")
    .forEach(el => {
        const cor =
            el.dataset.corDisciplina ||
            el.dataset.cor ||
            "#2563EB";

        el.style.backgroundColor =
            cor + "22";

        el.style.color = cor;

        el.style.border =
            "1px solid " + cor + "55";
    });