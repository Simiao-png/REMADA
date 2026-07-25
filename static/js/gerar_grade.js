document.addEventListener("DOMContentLoaded", () => {
    iniciarTela();
});


const dias = [
    { chave: "segunda", nome: "Segunda" },
    { chave: "terca", nome: "Terça" },
    { chave: "quarta", nome: "Quarta" },
    { chave: "quinta", nome: "Quinta" },
    { chave: "sexta", nome: "Sexta" },
    { chave: "sabado", nome: "Sábado" }
];


let turmas = [];
let turmaAtivaId = null;
let resultadoMotorAtual = null;


function iniciarTela() {
    configurarAbasPrincipais();
    configurarBotaoGerar();
    exibirEstadoInicial();
}


function configurarBotaoGerar() {
    const botao = document.getElementById(
        "btnGerarGrade"
    );

    if (!botao) {
        return;
    }

    botao.addEventListener(
        "click",
        iniciarGeracao
    );
}


function configurarAbasPrincipais() {
    const botoes = document.querySelectorAll(
        ".grade-view-tab"
    );

    botoes.forEach(botao => {
        botao.addEventListener("click", () => {
            botoes.forEach(item => {
                item.classList.remove("active");
            });

            botao.classList.add("active");

            document
                .querySelectorAll(".grade-view")
                .forEach(view => {
                    view.classList.remove("active");
                });

            const nomeView = botao.dataset.view;

            if (nomeView === "turmas") {
                const viewTurmas =
                    document.getElementById(
                        "viewTurmas"
                    );

                if (viewTurmas) {
                    viewTurmas.classList.add(
                        "active"
                    );
                }
            }

            if (nomeView === "geral") {
                const viewGeral =
                    document.getElementById(
                        "viewGeral"
                    );

                if (viewGeral) {
                    viewGeral.classList.add(
                        "active"
                    );
                }
            }
        });
    });
}


function exibirEstadoInicial() {
    removerPainelDiagnostico();

    const abasTurmas = document.getElementById(
        "abasTurmas"
    );

    const gradeTurma = document.getElementById(
        "gradeTurma"
    );

    const gradeGeral = document.getElementById(
        "gradeGeral"
    );

    if (abasTurmas) {
        abasTurmas.innerHTML = "";
    }

    if (gradeTurma) {
        gradeTurma.innerHTML = `
            <div class="grade-estado-vazio">
                Clique em
                <strong>Gerar Grade</strong>
                para executar o motor.
            </div>
        `;
    }

    if (gradeGeral) {
        gradeGeral.innerHTML = `
            <div class="grade-estado-vazio">
                A visão geral será exibida
                depois da geração.
            </div>
        `;
    }
}


async function iniciarGeracao() {
    const botao = document.getElementById(
        "btnGerarGrade"
    );

    const progressoContainer =
        document.getElementById(
            "progressoContainer"
        );

    const barra = document.getElementById(
        "barraProgresso"
    );

    const texto = document.getElementById(
        "textoProgresso"
    );

    const titulo = document.getElementById(
        "tituloProgresso"
    );

    prepararInterfaceGeracao({
        botao,
        progressoContainer,
        barra,
        texto,
        titulo
    });

    try {
        atualizarProgresso(
            barra,
            texto,
            titulo,
            25,
            "Carregando os dados cadastrados..."
        );

        const resposta = await fetch(
            "/motor/gerar",
            {
                method: "POST",
                headers: {
                    "Accept": "application/json",
                    "Content-Type":
                        "application/json"
                }
            }
        );

        const dados = await resposta.json();

        resultadoMotorAtual = dados;

        atualizarProgresso(
            barra,
            texto,
            titulo,
            70,
            "Organizando a grade..."
        );

        if (!resposta.ok) {
            throw new Error(
                obterMensagemErro(dados)
            );
        }

        if (
            dados.status === "erro" ||
            dados.status === "inviavel"
        ) {
            throw new Error(
                obterMensagemErro(dados)
            );
        }

        if (!dados.grade) {
            throw new Error(
                "O motor não retornou uma grade."
            );
        }

        montarTurmasDaGrade(
            dados.grade
        );

        criarAbasTurmas();
        renderizarTurmaAtiva();
        renderizarVisaoGeral();

        atualizarProgresso(
            barra,
            texto,
            titulo,
            100,
            dados.status === "parcial"
                ? "Grade gerada parcialmente."
                : "Grade gerada com sucesso."
        );

        mostrarAulasNaoAlocadas(
            dados.nao_alocadas || []
        );

    } catch (erro) {
        resultadoMotorAtual = null;

        atualizarProgresso(
            barra,
            texto,
            titulo,
            100,
            "Não foi possível gerar a grade."
        );

        exibirErroNaTela(
            erro.message
        );

        window.alert(
            erro.message ||
            "Não foi possível gerar a grade."
        );

        console.error(
            "Erro ao executar o motor:",
            erro
        );

    } finally {
        restaurarBotaoGerar(botao);
    }
}


function prepararInterfaceGeracao({
    botao,
    progressoContainer,
    barra,
    texto,
    titulo
}) {
    removerPainelDiagnostico();

    if (progressoContainer) {
        progressoContainer.classList.remove(
            "d-none"
        );
    }

    atualizarProgresso(
        barra,
        texto,
        titulo,
        10,
        "Iniciando o motor..."
    );

    if (botao) {
        botao.disabled = true;

        botao.innerHTML = `
            <span
                class="spinner-border
                       spinner-border-sm
                       me-2"
                aria-hidden="true">
            </span>

            Gerando...
        `;
    }
}


function restaurarBotaoGerar(botao) {
    if (!botao) {
        return;
    }

    botao.disabled = false;

    botao.innerHTML = `
        <i class="bi bi-play-fill"></i>
        Gerar Grade
    `;
}


function atualizarProgresso(
    barra,
    texto,
    titulo,
    percentual,
    mensagem
) {
    if (barra) {
        barra.style.width =
            `${percentual}%`;

        barra.setAttribute(
            "aria-valuenow",
            percentual
        );
    }

    if (texto) {
        texto.textContent =
            `${percentual}%`;
    }

    if (titulo) {
        titulo.textContent = mensagem;
    }
}


function montarTurmasDaGrade(grade) {
    turmas = Object.entries(grade).map(
        ([turmaId, gradeTurma]) => {
            return {
                id: String(turmaId),

                nome: obterNomeTurma(
                    turmaId,
                    gradeTurma
                ),

                quantidadeAulas:
                    obterQuantidadeMaximaAulas(
                        gradeTurma
                    ),

                dias: Object.keys(
                    gradeTurma || {}
                )
            };
        }
    );

    turmaAtivaId = turmas.length > 0
        ? turmas[0].id
        : null;
}


function obterQuantidadeMaximaAulas(
    gradeTurma
) {
    if (
        !gradeTurma ||
        typeof gradeTurma !== "object"
    ) {
        return 0;
    }

    const quantidades = Object.values(
        gradeTurma
    )
        .filter(Array.isArray)
        .map(lista => lista.length);

    if (quantidades.length === 0) {
        return 0;
    }

    return Math.max(...quantidades);
}


function obterNomeTurma(
    turmaId,
    gradeTurma
) {
    for (
        const horarios of Object.values(
            gradeTurma || {}
        )
    ) {
        if (!Array.isArray(horarios)) {
            continue;
        }

        for (const aula of horarios) {
            if (!aula) {
                continue;
            }

            const nome = primeiroValor(
                aula.turma_nome,
                aula.nome_turma,
                aula.turmaNome,
                typeof aula.turma === "string"
                    ? aula.turma
                    : null
            );

            if (nome) {
                return nome;
            }
        }
    }

    return `Turma ${turmaId}`;
}


function criarAbasTurmas() {
    const container = document.getElementById(
        "abasTurmas"
    );

    if (!container) {
        return;
    }

    container.innerHTML = "";

    turmas.forEach(turma => {
        const botao = document.createElement(
            "button"
        );

        botao.type = "button";
        botao.className = "turma-tab";
        botao.dataset.turmaId = turma.id;
        botao.textContent = turma.nome;

        if (
            String(turma.id) ===
            String(turmaAtivaId)
        ) {
            botao.classList.add("active");
        }

        botao.addEventListener("click", () => {
            turmaAtivaId = turma.id;

            document
                .querySelectorAll(".turma-tab")
                .forEach(item => {
                    item.classList.remove(
                        "active"
                    );
                });

            botao.classList.add("active");

            renderizarTurmaAtiva();
        });

        container.appendChild(botao);
    });
}


function renderizarTurmaAtiva() {
    const container = document.getElementById(
        "gradeTurma"
    );

    if (!container) {
        return;
    }

    const turma = turmas.find(item => {
        return (
            String(item.id) ===
            String(turmaAtivaId)
        );
    });

    if (!turma) {
        container.innerHTML = `
            <div class="grade-estado-vazio">
                Nenhuma turma encontrada.
            </div>
        `;

        return;
    }

    const gradeTurma =
        resultadoMotorAtual.grade[
            turma.id
        ] || {};

    const diasTurma = obterDiasDaTurma(
        gradeTurma
    );

    container.innerHTML = "";

    const titulo = document.createElement(
        "div"
    );

    titulo.className = "grade-title";
    titulo.textContent = turma.nome;

    const grade = document.createElement(
        "div"
    );

    grade.className =
        "grade-grid grade-grid-turma";

    grade.style.gridTemplateColumns =
        `110px repeat(${diasTurma.length}, ` +
        "minmax(140px, 1fr))";

    grade.appendChild(
        criarCabecalho("Aula")
    );

    diasTurma.forEach(dia => {
        grade.appendChild(
            criarCabecalho(
                obterNomeDia(dia)
            )
        );
    });

    for (
        let numeroAula = 1;
        numeroAula <= turma.quantidadeAulas;
        numeroAula++
    ) {
        grade.appendChild(
            criarNumeroAula(numeroAula)
        );

        diasTurma.forEach(dia => {
            const horarios =
                gradeTurma[dia] || [];

            const aula =
                horarios[numeroAula - 1];

            grade.appendChild(
                criarCelulaAula(
                    aula,
                    turma,
                    dia,
                    numeroAula
                )
            );
        });
    }

    container.appendChild(titulo);
    container.appendChild(grade);
}


function renderizarVisaoGeral() {
    const container = document.getElementById(
        "gradeGeral"
    );

    if (!container) {
        return;
    }

    container.innerHTML = "";

    const diasDisponiveis =
        obterTodosDiasDisponiveis();

    if (diasDisponiveis.length === 0) {
        container.innerHTML = `
            <div class="grade-estado-vazio">
                Nenhum dia foi encontrado.
            </div>
        `;

        return;
    }

    diasDisponiveis.forEach(dia => {
        container.appendChild(
            criarGradeGeralDia(dia)
        );
    });
}


function criarGradeGeralDia(dia) {
    const bloco = document.createElement(
        "section"
    );

    bloco.className = "grade-geral-dia";

    const titulo = document.createElement(
        "div"
    );

    titulo.className =
        "grade-geral-dia-titulo";

    titulo.textContent =
        obterNomeDia(dia);

    const grade = document.createElement(
        "div"
    );

    grade.className =
        "grade-grid grade-grid-geral";

    grade.style.gridTemplateColumns =
        `110px repeat(${turmas.length}, ` +
        "minmax(140px, 1fr))";

    grade.appendChild(
        criarCabecalho("Aula")
    );

    turmas.forEach(turma => {
        grade.appendChild(
            criarCabecalho(turma.nome)
        );
    });

    const maiorQuantidadeAulas =
        obterMaiorQuantidadeAulasDoDia(
            dia
        );

    for (
        let numeroAula = 1;
        numeroAula <= maiorQuantidadeAulas;
        numeroAula++
    ) {
        grade.appendChild(
            criarNumeroAula(numeroAula)
        );

        turmas.forEach(turma => {
            const gradeTurma =
                resultadoMotorAtual.grade[
                    turma.id
                ] || {};

            const horarios =
                gradeTurma[dia];

            if (
                !Array.isArray(horarios) ||
                numeroAula > horarios.length
            ) {
                grade.appendChild(
                    criarCelulaIndisponivel()
                );

                return;
            }

            const aula =
                horarios[numeroAula - 1];

            grade.appendChild(
                criarCelulaAula(
                    aula,
                    turma,
                    dia,
                    numeroAula,
                    true
                )
            );
        });
    }

    bloco.appendChild(titulo);
    bloco.appendChild(grade);

    return bloco;
}


function criarCelulaAula(
    aula,
    turma,
    dia,
    numeroAula,
    visaoGeral = false
) {
    const celula = document.createElement(
        "div"
    );

    celula.className = visaoGeral
        ? "grade-cell grade-cell-geral"
        : "grade-cell";

    celula.dataset.turmaId = turma.id;
    celula.dataset.dia = dia;
    celula.dataset.aula = numeroAula;

    if (!aula) {
        celula.classList.add(
            "grade-cell-vazia"
        );

        celula.innerHTML = `
            <span class="grade-vazia">•</span>
        `;

        return celula;
    }

    const professor =
        obterNomeProfessor(aula);

    const disciplina =
        obterNomeDisciplina(aula);

    const cor =
        obterCorDisciplina(aula);

    celula.style.backgroundColor = cor;
    celula.style.color =
        obterCorTexto(cor);

    celula.innerHTML = `
        <span class="professor">
            ${escaparHtml(professor)}
        </span>

        <span class="disciplina">
            ${escaparHtml(disciplina)}
        </span>
    `;

    celula.title = [
        turma.nome,
        obterNomeDia(dia),
        `${numeroAula}ª aula`,
        professor,
        disciplina
    ]
        .filter(Boolean)
        .join(" • ");

    return celula;
}


function criarCelulaIndisponivel() {
    const celula = document.createElement(
        "div"
    );

    celula.className =
        "grade-cell grade-cell-indisponivel";

    return celula;
}


function criarCabecalho(texto) {
    const elemento = document.createElement(
        "div"
    );

    elemento.className = "grade-header";
    elemento.textContent = texto;

    return elemento;
}


function criarNumeroAula(numero) {
    const elemento = document.createElement(
        "div"
    );

    elemento.className = "grade-aula";
    elemento.textContent =
        `${numero}ª aula`;

    return elemento;
}


function obterDiasDaTurma(gradeTurma) {
    return dias
        .map(dia => dia.chave)
        .filter(chave => {
            return Array.isArray(
                gradeTurma[chave]
            );
        });
}


function obterTodosDiasDisponiveis() {
    const diasEncontrados = new Set();

    Object.values(
        resultadoMotorAtual.grade || {}
    ).forEach(gradeTurma => {
        Object.keys(
            gradeTurma || {}
        ).forEach(dia => {
            diasEncontrados.add(dia);
        });
    });

    return dias
        .map(dia => dia.chave)
        .filter(chave => {
            return diasEncontrados.has(
                chave
            );
        });
}


function obterMaiorQuantidadeAulasDoDia(
    dia
) {
    const quantidades = turmas.map(
        turma => {
            const gradeTurma =
                resultadoMotorAtual.grade[
                    turma.id
                ] || {};

            const horarios =
                gradeTurma[dia];

            return Array.isArray(horarios)
                ? horarios.length
                : 0;
        }
    );

    return Math.max(
        0,
        ...quantidades
    );
}


function obterNomeDia(chave) {
    const dia = dias.find(
        item => item.chave === chave
    );

    return dia
        ? dia.nome
        : chave;
}


function obterNomeProfessor(aula) {
    if (
        aula.professor &&
        typeof aula.professor === "object"
    ) {
        return primeiroValor(
            aula.professor.nome,
            aula.professor.name,
            `Professor ${
                aula.professor.id || ""
            }`
        );
    }

    return primeiroValor(
        aula.professor_nome,
        aula.nome_professor,
        aula.professorNome,
        typeof aula.professor === "string"
            ? aula.professor
            : null,
        aula.professor_id
            ? `Professor ${aula.professor_id}`
            : null,
        "Professor"
    );
}


function obterNomeDisciplina(aula) {
    if (
        aula.disciplina &&
        typeof aula.disciplina === "object"
    ) {
        return primeiroValor(
            aula.disciplina.nome,
            aula.disciplina.name,
            `Disciplina ${
                aula.disciplina.id || ""
            }`
        );
    }

    return primeiroValor(
        aula.disciplina_nome,
        aula.nome_disciplina,
        aula.disciplinaNome,
        typeof aula.disciplina === "string"
            ? aula.disciplina
            : null,
        aula.disciplina_id
            ? `Disciplina ${
                aula.disciplina_id
            }`
            : null,
        "Disciplina"
    );
}


function obterCorDisciplina(aula) {
    if (
        aula.disciplina &&
        typeof aula.disciplina === "object"
    ) {
        return primeiroValor(
            aula.disciplina.cor,
            aula.disciplina.color,
            "#e9ecef"
        );
    }

    return primeiroValor(
        aula.cor_disciplina,
        aula.disciplina_cor,
        aula.cor,
        aula.color,
        "#e9ecef"
    );
}


function obterMensagemErro(dados) {
    if (
        dados &&
        Array.isArray(dados.problemas) &&
        dados.problemas.length > 0
    ) {
        return dados.problemas
            .map(problema => {
                if (
                    typeof problema === "string"
                ) {
                    return problema;
                }

                return primeiroValor(
                    problema.mensagem,
                    problema.descricao,
                    problema.tipo,
                    JSON.stringify(problema)
                );
            })
            .join("\n");
    }

    return primeiroValor(
        dados?.mensagem,
        "O motor não conseguiu gerar a grade."
    );
}


function mostrarAulasNaoAlocadas(
    naoAlocadas
) {
    removerPainelDiagnostico();

    if (
        !Array.isArray(naoAlocadas) ||
        naoAlocadas.length === 0
    ) {
        return;
    }

    const painel = document.createElement(
        "section"
    );

    painel.id = "painelDiagnosticoGrade";

    painel.className =
        "alert alert-warning " +
        "border-0 shadow-sm mt-3";

    painel.innerHTML = `
        <div
            class="d-flex align-items-start
                   justify-content-between gap-3">

            <div>
                <h5 class="mb-1 fw-bold">
                    <i
                        class="bi bi-exclamation-triangle
                               me-2">
                    </i>

                    ${naoAlocadas.length}
                    aula(s) não alocada(s)
                </h5>

                <p class="mb-0 small">
                    Veja quem ficou de fora e
                    quais regras impediram a
                    alocação.
                </p>
            </div>

            <button
                type="button"
                class="btn-close"
                aria-label="Fechar"
                id="btnFecharDiagnosticoGrade">
            </button>
        </div>

        <div
            class="mt-3"
            id="listaDiagnosticosGrade">
        </div>
    `;

    inserirPainelDiagnostico(painel);

    const lista = painel.querySelector(
        "#listaDiagnosticosGrade"
    );

    naoAlocadas.forEach(
        (aula, indice) => {
            lista.appendChild(
                criarDiagnosticoAula(
                    aula,
                    indice
                )
            );
        }
    );

    const botaoFechar = painel.querySelector(
        "#btnFecharDiagnosticoGrade"
    );

    if (botaoFechar) {
        botaoFechar.addEventListener(
            "click",
            removerPainelDiagnostico
        );
    }

    painel.scrollIntoView({
        behavior: "smooth",
        block: "start"
    });
}


function inserirPainelDiagnostico(painel) {
    const progressoContainer =
        document.getElementById(
            "progressoContainer"
        );

    if (
        progressoContainer &&
        progressoContainer.parentElement
    ) {
        progressoContainer.insertAdjacentElement(
            "afterend",
            painel
        );

        return;
    }

    const referencia =
        document.querySelector(
            ".grade-view-tabs"
        ) ||
        document.getElementById(
            "viewTurmas"
        ) ||
        document.querySelector(
            "main"
        );

    if (!referencia) {
        return;
    }

    if (
        referencia.id === "viewTurmas" ||
        referencia.tagName === "MAIN"
    ) {
        referencia.prepend(painel);
        return;
    }

    referencia.insertAdjacentElement(
        "beforebegin",
        painel
    );
}


function criarDiagnosticoAula(
    aula,
    indice
) {
    const item = document.createElement(
        "details"
    );

    item.className =
        "bg-white rounded border " +
        "mb-2 overflow-hidden";

    if (indice === 0) {
        item.open = true;
    }

    const turma = primeiroValor(
        aula.turma_nome,
        aula.nome_turma,
        aula.turma_id
            ? `Turma ${aula.turma_id}`
            : null,
        "Turma não identificada"
    );

    const professor = primeiroValor(
        aula.professor_nome,
        aula.nome_professor,
        aula.professor_id
            ? `Professor ${aula.professor_id}`
            : null,
        "Professor não identificado"
    );

    const disciplina = primeiroValor(
        aula.disciplina_nome,
        aula.nome_disciplina,
        aula.disciplina_id
            ? `Disciplina ${aula.disciplina_id}`
            : null,
        "Disciplina não identificada"
    );

    const diagnostico =
        aula.diagnostico || {};

    const descricaoPrincipal = primeiroValor(
        diagnostico.descricao_principal,
        aula.motivo,
        "Nenhuma posição válida encontrada."
    );

    const resumo = Array.isArray(
        diagnostico.resumo
    )
        ? diagnostico.resumo
        : [];

    const totalHorarios =
        Number(
            diagnostico
                .total_horarios_analisados || 0
        );

    item.innerHTML = `
        <summary
            class="p-3 d-flex align-items-center
                   justify-content-between gap-3"
            style="
                cursor: pointer;
                list-style: none;
            ">

            <div>
                <strong>
                    ${escaparHtml(disciplina)}
                </strong>

                <span class="text-muted">
                    — ${escaparHtml(turma)}
                </span>

                <div class="small text-muted mt-1">
                    Professor:
                    ${escaparHtml(professor)}
                </div>
            </div>

            <span class="badge text-bg-warning">
                Não alocada
            </span>
        </summary>

        <div class="border-top p-3">
            <p class="mb-2">
                <strong>Causa principal:</strong>
                ${escaparHtml(
                    descricaoPrincipal
                )}
            </p>

            ${
                totalHorarios > 0
                    ? `
                        <p class="small text-muted mb-2">
                            ${totalHorarios}
                            horário(s) foram analisados.
                        </p>
                    `
                    : ""
            }

            ${montarResumoDiagnostico(resumo)}

            ${montarDetalhesHorarios(
                diagnostico.horarios_analisados
            )}
        </div>
    `;

    return item;
}


function montarResumoDiagnostico(resumo) {
    if (
        !Array.isArray(resumo) ||
        resumo.length === 0
    ) {
        return `
            <div class="small text-muted">
                O motor não retornou a contagem
                detalhada das rejeições.
            </div>
        `;
    }

    const linhas = resumo.map(item => {
        const descricao = primeiroValor(
            item.descricao,
            item.codigo,
            "Motivo não identificado"
        );

        const quantidade = Number(
            item.quantidade_horarios || 0
        );

        return `
            <li class="mb-1">
                ${escaparHtml(descricao)}

                <strong>
                    (${quantidade} horário(s))
                </strong>
            </li>
        `;
    }).join("");

    return `
        <div class="small">
            <strong>
                Horários rejeitados por regra:
            </strong>

            <ul class="mb-0 mt-2 ps-3">
                ${linhas}
            </ul>
        </div>
    `;
}


function montarDetalhesHorarios(
    horariosAnalisados
) {
    if (
        !Array.isArray(horariosAnalisados) ||
        horariosAnalisados.length === 0
    ) {
        return "";
    }

    const linhas = horariosAnalisados.map(
        horario => {
            const dia = obterNomeDia(
                horario.dia
            );

            const numeroAula = primeiroValor(
                horario.numero_aula,
                "-"
            );

            const descricao = primeiroValor(
                horario.descricao,
                horario.motivo,
                "Motivo não identificado"
            );

            return `
                <tr>
                    <td>${escaparHtml(dia)}</td>

                    <td>
                        ${escaparHtml(
                            `${numeroAula}ª aula`
                        )}
                    </td>

                    <td>
                        ${escaparHtml(descricao)}
                    </td>
                </tr>
            `;
        }
    ).join("");

    return `
        <details class="mt-3">
            <summary
                class="small fw-semibold"
                style="cursor: pointer;">

                Ver todos os horários analisados
            </summary>

            <div class="table-responsive mt-2">
                <table
                    class="table table-sm
                           table-bordered mb-0">

                    <thead>
                        <tr>
                            <th>Dia</th>
                            <th>Aula</th>
                            <th>Motivo</th>
                        </tr>
                    </thead>

                    <tbody>
                        ${linhas}
                    </tbody>
                </table>
            </div>
        </details>
    `;
}


function removerPainelDiagnostico() {
    const painel = document.getElementById(
        "painelDiagnosticoGrade"
    );

    if (painel) {
        painel.remove();
    }
}


function exibirErroNaTela(mensagem) {
    removerPainelDiagnostico();

    const gradeTurma = document.getElementById(
        "gradeTurma"
    );

    const gradeGeral = document.getElementById(
        "gradeGeral"
    );

    const conteudo = `
        <div class="grade-estado-vazio">
            <strong>
                Não foi possível gerar a grade.
            </strong>

            <br>

            ${escaparHtml(mensagem)}
        </div>
    `;

    if (gradeTurma) {
        gradeTurma.innerHTML = conteudo;
    }

    if (gradeGeral) {
        gradeGeral.innerHTML = conteudo;
    }
}


function primeiroValor(...valores) {
    return valores.find(valor => {
        return (
            valor !== undefined &&
            valor !== null &&
            valor !== ""
        );
    });
}


function escaparHtml(texto) {
    const elemento = document.createElement(
        "div"
    );

    elemento.textContent =
        String(texto || "");

    return elemento.innerHTML;
}


function obterCorTexto(cor) {
    if (
        !cor ||
        typeof cor !== "string" ||
        !cor.startsWith("#")
    ) {
        return "#172033";
    }

    let hexadecimal = cor.substring(1);

    if (hexadecimal.length === 3) {
        hexadecimal = hexadecimal
            .split("")
            .map(caractere => {
                return caractere + caractere;
            })
            .join("");
    }

    if (hexadecimal.length !== 6) {
        return "#172033";
    }

    const vermelho = parseInt(
        hexadecimal.substring(0, 2),
        16
    );

    const verde = parseInt(
        hexadecimal.substring(2, 4),
        16
    );

    const azul = parseInt(
        hexadecimal.substring(4, 6),
        16
    );

    const luminosidade =
        (
            vermelho * 299 +
            verde * 587 +
            azul * 114
        ) / 1000;

    return luminosidade > 160
        ? "#172033"
        : "#ffffff";
}