let modalDisciplina = null;
let modalTurma = null;

let dadosPlanejamento = null;


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

    document.getElementById("segmentoTurma").value =
        botao.dataset.segmento;

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

    dadosPlanejamento = JSON.parse(
        elemento.textContent
    );
}


function buscarProfessorPlanejamento(
    professorId
) {
    if (!dadosPlanejamento) {
        return null;
    }

    return dadosPlanejamento.professores.find(
        professor =>
            String(professor.id) ===
            String(professorId)
    );
}


let temporizadorSalvamentoDisponibilidade =
    null;

let salvandoDisponibilidade = false;

let salvamentoDisponibilidadePendente =
    false;


function atualizarStatusDisponibilidade(
    tipo,
    mensagem
) {
    const status =
        document.getElementById(
            "statusSalvamentoDisponibilidade"
        );

    if (!status) {
        return;
    }

    const configuracoes = {
        neutro: {
            classe: "text-muted",
            icone: "bi-cloud-check"
        },

        salvando: {
            classe: "text-primary",
            icone: "bi-arrow-repeat"
        },

        salvo: {
            classe: "text-success",
            icone: "bi-check-circle-fill"
        },

        erro: {
            classe: "text-danger",
            icone: "bi-exclamation-circle-fill"
        }
    };

    const configuracao =
        configuracoes[tipo] ||
        configuracoes.neutro;

    status.className =
        `small ${configuracao.classe} ` +
        "d-inline-flex align-items-center gap-2";

    status.innerHTML =
        `<i class="bi ${configuracao.icone}"></i>` +
        mensagem;
}


function carregarProfessorDisponibilidade() {
    const selectProfessor =
        document.getElementById(
            "professorDisponibilidade"
        );

    if (
        !selectProfessor ||
        !dadosPlanejamento
    ) {
        return;
    }

    const professor =
        buscarProfessorPlanejamento(
            selectProfessor.value
        );

    if (!professor) {
        return;
    }

    const nomeProfessor =
        document.getElementById(
            "nomeProfessorDisponibilidade"
        );

    if (nomeProfessor) {
        nomeProfessor.innerText =
            professor.nome;
    }

    montarTabelaDisponibilidade(
        professor
    );

    atualizarStatusDisponibilidade(
        "neutro",
        "Salvamento automático"
    );
}


function montarTabelaDisponibilidade(
    professor
) {
    const corpoTabela =
        document.getElementById(
            "corpoTabelaDisponibilidade"
        );

    if (
        !corpoTabela ||
        !dadosPlanejamento
    ) {
        return;
    }

    corpoTabela.innerHTML = "";

    dadosPlanejamento.numerosAulas.forEach(
        numeroAula => {
            const linha =
                document.createElement("tr");

            const colunaAula =
                document.createElement("td");

            colunaAula.className =
                "fw-semibold";

            colunaAula.innerText =
                `${numeroAula}ª aula`;

            linha.appendChild(
                colunaAula
            );

            dadosPlanejamento.diasSemana.forEach(
                dia => {
                    const coluna =
                        document.createElement(
                            "td"
                        );

                    const disponivel = (
                        professor.disponibilidades ||
                        []
                    ).some(
                        item =>
                            item.dia_semana ===
                                dia.valor &&
                            Number(
                                item.numero_aula
                            ) ===
                                Number(
                                    numeroAula
                                )
                    );

                    const botao =
                        document.createElement(
                            "button"
                        );

                    botao.type = "button";

                    botao.className =
                        disponivel
                            ? "btn btn-sm " +
                              "btn-success " +
                              "disponibilidade-botao"
                            : "btn btn-sm " +
                              "btn-outline-secondary " +
                              "disponibilidade-botao";

                    botao.dataset.dia =
                        dia.valor;

                    botao.dataset.aula =
                        numeroAula;

                    botao.dataset.disponivel =
                        disponivel
                            ? "true"
                            : "false";

                    botao.innerText =
                        disponivel
                            ? "✓"
                            : "—";

                    botao.addEventListener(
                        "click",
                        function () {
                            alternarDisponibilidadeBotao(
                                botao
                            );
                        }
                    );

                    coluna.appendChild(
                        botao
                    );

                    linha.appendChild(
                        coluna
                    );
                }
            );

            corpoTabela.appendChild(
                linha
            );
        }
    );

    configurarCabecalhosDisponibilidade();
}


function aplicarEstadoDisponibilidade(
    botao,
    disponivel
) {
    botao.dataset.disponivel =
        disponivel
            ? "true"
            : "false";

    botao.className =
        disponivel
            ? "btn btn-sm btn-success " +
              "disponibilidade-botao"
            : "btn btn-sm " +
              "btn-outline-secondary " +
              "disponibilidade-botao";

    botao.innerText =
        disponivel
            ? "✓"
            : "—";
}


function alternarDisponibilidadeBotao(
    botao
) {
    const disponivel =
        botao.dataset.disponivel ===
        "true";

    aplicarEstadoDisponibilidade(
        botao,
        !disponivel
    );

    atualizarEstadoCabecalhoDia(
        botao.dataset.dia
    );

    agendarSalvamentoDisponibilidade();
}


function configurarCabecalhosDisponibilidade() {
    const cabecalhos =
        document.querySelectorAll(
            ".cabecalho-dia-disponibilidade[data-dia]"
        );

    cabecalhos.forEach(
        cabecalho => {
            if (
                cabecalho.dataset
                    .eventoConfigurado ===
                "true"
            ) {
                atualizarEstadoCabecalhoDia(
                    cabecalho.dataset.dia
                );

                return;
            }

            cabecalho.dataset
                .eventoConfigurado =
                "true";

            cabecalho.style.cursor =
                "pointer";

            cabecalho.title =
                "Clique para marcar ou " +
                "desmarcar todas as aulas " +
                "deste dia";

            cabecalho.addEventListener(
                "click",
                function () {
                    alternarDisponibilidadeDia(
                        cabecalho.dataset.dia
                    );
                }
            );

            atualizarEstadoCabecalhoDia(
                cabecalho.dataset.dia
            );
        }
    );
}


function obterBotoesDisponibilidadeDia(
    dia
) {
    return Array.from(
        document.querySelectorAll(
            `.disponibilidade-botao` +
            `[data-dia="${dia}"]`
        )
    );
}


function alternarDisponibilidadeDia(
    dia
) {
    const botoes =
        obterBotoesDisponibilidadeDia(
            dia
        );

    if (botoes.length === 0) {
        return;
    }

    const todosDisponiveis =
        botoes.every(
            botao =>
                botao.dataset.disponivel ===
                "true"
        );

    botoes.forEach(botao => {
        aplicarEstadoDisponibilidade(
            botao,
            !todosDisponiveis
        );
    });

    atualizarEstadoCabecalhoDia(
        dia
    );

    agendarSalvamentoDisponibilidade();
}


function atualizarEstadoCabecalhoDia(
    dia
) {
    const cabecalho =
        document.querySelector(
            `.cabecalho-dia-disponibilidade[data-dia="${dia}"]`
        );

    if (!cabecalho) {
        return;
    }

    const botoes =
        obterBotoesDisponibilidadeDia(
            dia
        );

    const todosDisponiveis =
        botoes.length > 0 &&
        botoes.every(
            botao =>
                botao.dataset.disponivel ===
                "true"
        );

    cabecalho.classList.toggle(
        "text-success",
        todosDisponiveis
    );

    cabecalho.classList.toggle(
        "fw-bold",
        todosDisponiveis
    );
}


function coletarDisponibilidadesMarcadas() {
    return Array.from(
        document.querySelectorAll(
            ".disponibilidade-botao"
        )
    )
        .filter(
            botao =>
                botao.dataset.disponivel ===
                "true"
        )
        .map(
            botao => ({
                dia_semana:
                    botao.dataset.dia,

                numero_aula:
                    Number(
                        botao.dataset.aula
                    )
            })
        );
}


function agendarSalvamentoDisponibilidade() {
    window.clearTimeout(
        temporizadorSalvamentoDisponibilidade
    );

    salvamentoDisponibilidadePendente =
        true;

    atualizarStatusDisponibilidade(
        "salvando",
        "Salvando..."
    );

    temporizadorSalvamentoDisponibilidade =
        window.setTimeout(
            salvarDisponibilidadeProfessorAtual,
            350
        );
}


async function salvarDisponibilidadeProfessorAtual() {
    const selectProfessor =
        document.getElementById(
            "professorDisponibilidade"
        );

    if (
        !selectProfessor ||
        salvandoDisponibilidade
    ) {
        return;
    }

    const professorId =
        selectProfessor.value;

    const professor =
        buscarProfessorPlanejamento(
            professorId
        );

    if (!professor) {
        return;
    }

    const disponibilidades =
        coletarDisponibilidadesMarcadas();

    salvandoDisponibilidade = true;

    salvamentoDisponibilidadePendente =
        false;

    atualizarStatusDisponibilidade(
        "salvando",
        "Salvando..."
    );

    try {
        const response =
            await fetch(
                `/disponibilidades/` +
                `professor/${professorId}`,
                {
                    method: "POST",

                    headers: {
                        "Content-Type":
                            "application/json"
                    },

                    body: JSON.stringify({
                        disponibilidades:
                            disponibilidades
                    })
                }
            );

        if (!response.ok) {
            const erro =
                await response.text();

            throw new Error(
                `Erro no Backend ` +
                `(${response.status}): ` +
                erro
            );
        }

        professor.disponibilidades =
            disponibilidades;

        atualizarStatusDisponibilidade(
            "salvo",
            "Salvo"
        );

    } catch (erro) {
        salvamentoDisponibilidadePendente =
            true;

        atualizarStatusDisponibilidade(
            "erro",
            "Erro ao salvar"
        );

        console.error(erro);

    } finally {
        salvandoDisponibilidade =
            false;

        if (
            salvamentoDisponibilidadePendente
        ) {
            window.setTimeout(
                salvarDisponibilidadeProfessorAtual,
                250
            );
        }
    }
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
            segmentos:
                parametrosPorSegmento
        };
    }

    const campoJson =
        document.getElementById(
            "segmentosParametrosJson"
        );

    if (
        campoJson &&
        campoJson.value
    ) {
        return {
            segmentos:
                JSON.parse(
                    campoJson.value
                )
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
                                JSON.stringify(
                                    payload
                                )
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

                    const response =
                        await fetch(
                            "/configuracoes-horarias/parametros",
                            {
                                method: "POST",

                                headers: {
                                    "Content-Type":
                                        "application/json"
                                },

                                body:
                                    JSON.stringify(
                                        payload
                                    )
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
                            `Erro no Backend ` +
                            `(${response.status}): ` +
                            erro
                        );
                    }
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

                    const url =
                        id
                            ? `/disciplinas/${id}`
                            : "/disciplinas";

                    const metodo =
                        id
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

                    fetch(
                        url,
                        {
                            method: metodo,

                            headers: {
                                "Content-Type":
                                    "application/json"
                            },

                            body:
                                JSON.stringify(
                                    payload
                                )
                        }
                    ).then(
                        async response => {
                            if (response.ok) {
                                window.location.reload();
                            } else {
                                const erro =
                                    await response.text();

                                alert(
                                    `Erro no Backend ` +
                                    `(${response.status}): ` +
                                    erro
                                );
                            }
                        }
                    );
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

                    const url =
                        id
                            ? `/turmas/${id}`
                            : "/turmas";

                    const metodo =
                        id
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

                        segmento:
                            document.getElementById(
                                "segmentoTurma"
                            ).value,

                        turno:
                            document.getElementById(
                                "turnoTurma"
                            ).value
                    };

                    fetch(
                        url,
                        {
                            method: metodo,

                            headers: {
                                "Content-Type":
                                    "application/json"
                            },

                            body:
                                JSON.stringify(
                                    payload
                                )
                        }
                    ).then(
                        async response => {
                            if (response.ok) {
                                window.location.reload();
                            } else {
                                const erro =
                                    await response.text();

                                alert(
                                    `Erro no Backend ` +
                                    `(${response.status}): ` +
                                    erro
                                );
                            }
                        }
                    );
                }
            );
        }


        carregarDadosPlanejamento();


        const selectProfessorDisponibilidade =
            document.getElementById(
                "professorDisponibilidade"
            );

        if (
            selectProfessorDisponibilidade
        ) {
            carregarProfessorDisponibilidade();

            selectProfessorDisponibilidade
                .addEventListener(
                    "change",
                    function () {
                        carregarProfessorDisponibilidade();
                    }
                );
        }
    }
);


document
    .querySelectorAll(
        ".disciplina-cor-bolinha"
    )
    .forEach(el => {
        const cor =
            el.dataset.corDisciplina ||
            el.dataset.cor ||
            "#2563EB";

        el.style.backgroundColor =
            cor;
    });


document
    .querySelectorAll(
        ".badge-disciplina-colorida"
    )
    .forEach(el => {
        const cor =
            el.dataset.corDisciplina ||
            el.dataset.cor ||
            "#2563EB";

        el.style.backgroundColor =
            cor + "22";

        el.style.color =
            cor;

        el.style.border =
            "1px solid " +
            cor +
            "55";
    });