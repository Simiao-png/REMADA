let modalProf = null;

function abrirModalCadastro() {
    document.getElementById("formNovoProfessor").reset();
    document.getElementById("professorId").value = "";
    document.getElementById("escolaIdProf").value = "1"; // Valor padrão seguro para passar no banco
    document.getElementById("modalNovoProfessorLabel").innerText = "Cadastrar Novo Professor";
    
    if(!modalProf) modalProf = new bootstrap.Modal(document.getElementById('modalNovoProfessor'));
    modalProf.show();
}

function abrirModalEdicao(botao) {
    document.getElementById("professorId").value = botao.dataset.id;
    document.getElementById("nomeProfessor").value = botao.dataset.nome;
    document.getElementById("emailProfessor").value = botao.dataset.email || "";
    document.getElementById("telefoneProfessor").value = botao.dataset.telefone || "";
    document.getElementById("escolaIdProf").value = botao.dataset.escola || "1";

    document.getElementById("modalNovoProfessorLabel").innerText = "Editar Professor";

    if (!modalProf) {
        modalProf = new bootstrap.Modal(document.getElementById("modalNovoProfessor"));
    }

    modalProf.show();
}

function deletarProfessor(id, nome) {
    if (confirm(`Tem certeza que deseja remover o professor "${nome}"?`)) {
        fetch(`/professores/${id}`, { method: "DELETE" })
        .then(response => { if (response.ok) window.location.reload(); });
    }
}

document.addEventListener("DOMContentLoaded", function () {
    
    // --- ESCUDO DA TELA DE ESCOLAS ---
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
            }).then(response => { if (response.ok) window.location.reload(); });
        });
    }

    // --- FORMULÁRIO DE SALVAMENTO DE PROFESSORES ---
    const formNovoProfessor = document.getElementById("formNovoProfessor");
    if (formNovoProfessor) {
        formNovoProfessor.addEventListener("submit", function (e) {
            e.preventDefault();

            const idProfRaw = document.getElementById("professorId").value;
            const temIdValido = idProfRaw && idProfRaw.trim() !== "";

            const url = temIdValido ? `/professores/${idProfRaw.trim()}` : "/professores";
            const metodo = temIdValido ? "PUT" : "POST";

            // Montamos o payload completo com todas as chaves que seu backend exige!
            const payload = {
                nome: document.getElementById("nomeProfessor").value,
                email: document.getElementById("emailProfessor").value,
                telefone: document.getElementById("telefoneProfessor").value,
                escola_id: parseInt(document.getElementById("escolaIdProf").value) || 1
            };

            fetch(url, {
                method: metodo,
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify(payload)
            })
            .then(async response => {
                if (response.ok) {
                    window.location.reload();
                } else {
                    const dadosErro = await response.text();
                    alert(`Erro no Backend (${response.status}): ${dadosErro}`);
                }
            })
            .catch(error => console.error("Erro:", error));
        });
    }
});