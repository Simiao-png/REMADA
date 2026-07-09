# REMADA

Sistema inteligente para geração automática de grades horárias
escolares.

O REMADA automatiza um dos processos mais complexos da gestão escolar: a
construção da grade horária. A plataforma organiza os parâmetros da
escola por segmento, valida inconsistências antes da geração da grade e
distribui as aulas de forma inteligente, reduzindo conflitos e o tempo
gasto na montagem manual.

------------------------------------------------------------------------

# Últimas Atualizações

-   Parâmetros configurados por segmento.
-   Segmentos com configurações independentes de aulas por dia.
-   Cadastro de disciplinas com cores personalizadas.
-   Paleta de cores e opção **"Mais cores..."**.
-   Exibição colorida das disciplinas em toda a interface.
-   Correção do fluxo de salvamento dos parâmetros.

------------------------------------------------------------------------

# Tecnologias

-   Python
-   Flask
-   PostgreSQL
-   SQLAlchemy
-   HTML5
-   CSS3
-   JavaScript
-   Bootstrap 5
-   Git
-   GitHub

------------------------------------------------------------------------

# Funcionalidades Implementadas

## Configuração da Escola

-   ✅ Parâmetros por segmento
-   ✅ Cadastro de Professores
-   ✅ Cadastro de Disciplinas com cores personalizadas
-   ✅ Cadastro de Turmas
-   ✅ Cadastro de Disponibilidade dos Professores
-   ✅ Cadastro de Carga Horária

## Relacionamentos

-   ✅ Professor × Disciplina
-   ✅ Professor × Turma
-   ✅ Turma × Disciplina

## Motor Inteligente

-   ✅ Geração automática da grade
-   ✅ Sistema de penalidades
-   ✅ Heurísticas
-   ✅ Diagnóstico de inviabilidade

## Interface Web

-   ✅ Dashboard
-   ✅ Central de Cadastros
-   ✅ Planejamento
-   ✅ Disponibilidade dos Professores
-   ✅ Parâmetros por segmento
-   ✅ Disciplinas com cores
-   🚧 Carga Horária
-   🚧 Gerar Grade
-   🚧 Diagnóstico
-   🚧 Visualização da grade

------------------------------------------------------------------------

# Roadmap

## Backend

-   [x] CRUDs completos
-   [x] Configuração horária por segmento
-   [x] Motor funcional
-   [ ] Otimização do motor

## Interface

-   [x] Dashboard
-   [x] Cadastros
-   [x] Planejamento
-   [x] Disponibilidades
-   [ ] Carga Horária
-   [ ] Gerar Grade
-   [ ] Diagnóstico

------------------------------------------------------------------------

# Status

🟡 Em desenvolvimento

## Progresso

-   ✅ Banco de dados concluído
-   ✅ CRUDs concluídos
-   ✅ Motor funcional
-   ✅ Interface moderna consolidada
-   ✅ Configuração por segmentos
-   ✅ Disponibilidade dos professores
-   ✅ Disciplinas coloridas
-   🚧 Carga Horária
-   🚧 Otimização do Motor

------------------------------------------------------------------------

# Estrutura

``` text
REMADA/
├── models/
├── routes/
├── services/
│   └── motor/
├── static/
│   ├── css/
│   ├── js/
│   └── img/
├── templates/
│   ├── components/
│   ├── dashboard.html
│   ├── cadastros.html
│   ├── planejamento.html
│   └── base.html
├── app.py
├── config.py
└── README.md
```

------------------------------------------------------------------------

# Visão de Produto

O REMADA está sendo desenvolvido como uma plataforma SaaS especializada
em geração inteligente de grades horárias escolares.

Seu objetivo é permitir que coordenadores configurem a escola, planejem
disponibilidades, definam cargas horárias e gerem automaticamente grades
viáveis através de um fluxo simples, moderno e inteligente.
