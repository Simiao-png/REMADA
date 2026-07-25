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