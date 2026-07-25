# REMADA

Sistema inteligente para geração automática de grades horárias escolares.

O REMADA automatiza um dos processos mais complexos da gestão escolar: a construção da grade horária. A plataforma organiza os parâmetros da escola por segmento, valida inconsistências antes da geração e distribui automaticamente as aulas, respeitando disponibilidade, matriz curricular e vínculos entre professores, disciplinas e turmas.

---

# Últimas Atualizações

- ✅ Implementação do novo motor de geração com Google OR-Tools CP-SAT.
- ✅ Criação de 1.080 variáveis de decisão no cenário de testes.
- ✅ Geração automática de uma grade viável com 120 aulas alocadas.
- ✅ Respeito à carga semanal definida na matriz curricular.
- ✅ Controle de conflito de professor no mesmo horário.
- ✅ Controle de conflito de turma no mesmo horário.
- ✅ Respeito à disponibilidade dos professores.
- ✅ Limite diário de aulas da mesma disciplina.
- ✅ Função objetivo para melhorar a distribuição da grade.
- ✅ Penalização de disciplinas em dias consecutivos.
- ✅ Penalização de aulas nos últimos horários.
- ✅ Penalização de concentração excessiva da carga diária do professor.
- ✅ Extração e exibição da solução no frontend.
- ✅ Visualização da grade por turma e em visão geral.
- ✅ Diagnóstico inicial de cenários inviáveis.
- ✅ Preservação do motor guloso como alternativa e base de comparação.

---

# Tecnologias

- Python
- Flask
- PostgreSQL
- SQLAlchemy
- Google OR-Tools
- CP-SAT
- HTML5
- CSS3
- JavaScript
- Bootstrap 5
- Git
- GitHub

---

# Funcionalidades Implementadas

## Configuração da Escola

- ✅ Parâmetros por segmento
- ✅ Quantidade de aulas por dia
- ✅ Duração das aulas
- ✅ Configuração dos dias letivos
- ✅ Cadastro de professores
- ✅ Cadastro de disciplinas
- ✅ Cadastro de turmas
- ✅ Disponibilidade dos professores

## Relacionamentos

- ✅ Professor × Disciplina
- ✅ Professor × Turma
- ✅ Turma × Disciplina
- ✅ Professor × Segmento
- ✅ Turma × Configuração Horária

## Planejamento

- ✅ Definição da matriz curricular por turma
- ✅ Definição das aulas semanais por disciplina
- ✅ Distribuição das turmas entre os professores
- ✅ Associação dos professores às disciplinas
- ✅ Definição da disponibilidade semanal
- ✅ Validação dos vínculos necessários para geração da grade

## Motor de Geração

- ✅ Motor guloso inicial
- ✅ Nova arquitetura separada por motores
- ✅ Motor de otimização CP-SAT
- ✅ Criação das variáveis de decisão
- ✅ Restrições obrigatórias
- ✅ Função objetivo
- ✅ Execução do solver
- ✅ Extração da solução
- ✅ Diagnóstico de inviabilidade
- ✅ Geração completa de grade
- ✅ Alocação de todas as aulas do cenário de testes

## Interface

- ✅ Dashboard
- ✅ Central de Cadastros
- ✅ Planejamento
- ✅ Disponibilidade dos Professores
- ✅ Gerar Grade
- ✅ Visualização por turma
- ✅ Visão geral da grade
- ✅ Identificação visual das disciplinas por cores
- ✅ Exibição de professor e disciplina
- 🚧 Diagnóstico detalhado
- 🚧 Configuração das preferências de otimização

---

# Motor CP-SAT

O REMADA utiliza o resolvedor CP-SAT do Google OR-Tools para encontrar grades horárias que atendam simultaneamente às regras obrigatórias da escola.

Cada variável de decisão representa a possibilidade de uma aula ser atribuída a uma combinação de:

```text
Turma
Disciplina
Professor
Dia
Horário

Exemplo conceitual:

(6º A, Matemática, Professor 1, Segunda-feira, 1ª aula)

O solver decide quais combinações devem ser ativadas para construir uma grade válida.

Restrições Obrigatórias
A carga semanal de cada disciplina deve ser cumprida.
Uma turma não pode ter duas aulas no mesmo horário.
Um professor não pode atender duas turmas simultaneamente.
A disponibilidade cadastrada do professor deve ser respeitada.
A quantidade máxima diária de aulas da mesma disciplina deve ser respeitada.
Apenas professores vinculados simultaneamente à turma e à disciplina podem ser alocados.
Critérios de Otimização
Evitar aulas nos últimos horários.
Evitar concentração excessiva de aulas do professor no mesmo dia.
Melhorar a distribuição das disciplinas durante a semana.
Penalizar a repetição da mesma disciplina em dias consecutivos.
Primeiro Resultado

No cenário inicial de testes, o motor apresentou:

Variáveis criadas: 1.080
Status: FEASIBLE
Aulas alocadas: 120
Tempo de execução: aproximadamente 30 segundos

O status FEASIBLE indica que o solver encontrou uma solução válida dentro do limite de tempo configurado.

Arquitetura do Motor
services/
└── motor/
    ├── cp_sat/
    │   ├── __init__.py
    │   ├── modelo.py
    │   ├── variaveis.py
    │   ├── restricoes.py
    │   ├── objetivo.py
    │   ├── solver.py
    │   ├── extrator.py
    │   └── diagnostico.py
    │
    ├── guloso/
    │   ├── alocador.py
    │   ├── aulas.py
    │   ├── debug_penalidades.py
    │   ├── estado.py
    │   ├── heuristicas.py
    │   ├── otimizador.py
    │   ├── penalidades.py
    │   └── validacoes.py
    │
    ├── carregador.py
    ├── estrutura.py
    ├── grade_service.py
    ├── inviabilidade.py
    └── seed.py
Fluxo do CP-SAT
carregador.py
      ↓
grade_service.py
      ↓
solver.py
      ↓
modelo.py
      ↓
variaveis.py
restricoes.py
objetivo.py
      ↓
CpSolver
      ↓
extrator.py
      ↓
grade exibida no frontend
Roadmap
Backend
 CRUDs principais
 Configuração horária por segmento
 Relacionamentos do planejamento
 Matriz curricular por turma
 Disponibilidade dos professores
 Motor guloso inicial
 Estrutura modular dos motores
 Motor CP-SAT
 Restrições obrigatórias
 Função objetivo inicial
 Extração da solução
 Geração completa da grade
 Validador automático da grade gerada
 Diagnóstico detalhado de inviabilidade
 Otimização das penalidades
 Configuração das preferências da escola
 Testes automatizados do motor
 Comparação de desempenho entre motores
Interface
 Dashboard
 Cadastros
 Planejamento
 Disponibilidade
 Gerar Grade
 Visualização por turma
 Visão geral
 Tela detalhada de diagnóstico
 Configuração das preferências do motor
 Edição manual da grade gerada
 Exportação da grade
 Impressão e geração de PDF
Status

🟡 Em desenvolvimento — motor de geração funcional.

Progresso
✅ Banco de dados estruturado
✅ CRUDs principais concluídos
✅ Planejamento concluído
✅ Configuração por segmentos
✅ Disponibilidade dos professores
✅ Relacionamentos entre professores, turmas e disciplinas
✅ Matriz curricular por turma
✅ Motor guloso preservado
✅ Motor CP-SAT implementado
✅ Geração automática funcionando
✅ 120 aulas alocadas no cenário de testes
✅ Visualização completa da grade
🚧 Diagnóstico inteligente
🚧 Validação automática
🚧 Otimização da qualidade da grade
Estrutura Geral
REMADA/
├── models/
├── routes/
├── services/
│   ├── motor/
│   │   ├── cp_sat/
│   │   └── guloso/
│   ├── disponibilidade_professor_service.py
│   ├── professor_service.py
│   └── ...
├── static/
│   ├── css/
│   ├── js/
│   └── img/
├── templates/
│   ├── components/
│   ├── dashboard.html
│   ├── cadastros.html
│   ├── planejamento.html
│   ├── gerar_grade.html
│   └── base.html
├── app.py
├── config.py
├── requirements.txt
└── README.md
Fluxo do Sistema
Configurar os parâmetros da escola.
Configurar os horários por segmento.
Cadastrar disciplinas.
Cadastrar professores.
Definir os segmentos de atuação dos professores.
Cadastrar turmas.
Definir a matriz curricular das turmas.
Informar a disponibilidade dos professores.
Associar professores às disciplinas.
Associar professores às turmas.
Executar as validações iniciais.
Gerar automaticamente a grade horária.
Visualizar a grade por turma ou em visão geral.
Próxima Etapa

A próxima etapa será dedicada à lapidação do motor CP-SAT.

As prioridades são:

criar um validador automático da solução;
melhorar o diagnóstico de cenários inviáveis;
evitar janelas nos horários dos professores;
melhorar a distribuição das disciplinas;
configurar preferências por escola;
reduzir o tempo necessário para encontrar soluções melhores;
ampliar os testes com cenários maiores e mais complexos.
Visão de Produto

O REMADA está sendo desenvolvido como uma plataforma SaaS especializada em geração inteligente de grades horárias escolares.

Seu objetivo é permitir que coordenadores configurem toda a estrutura da escola, realizem o planejamento dos professores e gerem automaticamente grades consistentes por meio de um fluxo simples, moderno e inteligente.

O sistema combina validações, regras pedagógicas, algoritmos heurísticos e otimização por restrições para reduzir conflitos e transformar um processo normalmente manual em uma operação automatizada e confiável.