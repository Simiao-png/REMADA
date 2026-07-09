# REMADA

Sistema inteligente para geração automática de grades horárias escolares.

O REMADA automatiza um dos processos mais complexos da gestão escolar: a construção da grade horária. A plataforma organiza o fluxo de configuração da escola, valida inconsistências antes da geração da grade e distribui as aulas de forma inteligente, reduzindo conflitos e o tempo gasto na montagem manual.

---

# Objetivo

Desenvolver uma plataforma web moderna capaz de gerar grades horárias escolares de forma automática, utilizando algoritmos de validação, heurísticas e otimização para produzir distribuições eficientes, equilibradas e viáveis.

O REMADA foi concebido para atender escolas de pequeno, médio e grande porte, oferecendo uma experiência simples para o usuário e um motor robusto de geração de horários.

---

# Problema que o REMADA resolve

Mesmo com a evolução dos sistemas de gestão escolar, a montagem da grade horária continua sendo um processo manual em muitas instituições.

Esse trabalho costuma envolver:

- diversas planilhas;
- inúmeros testes até encontrar uma solução viável;
- conflitos entre professores, disciplinas e turmas;
- retrabalho constante.

O REMADA automatiza esse processo, detectando problemas antes da geração da grade e construindo automaticamente uma distribuição inteligente das aulas.

---

# Tecnologias

- Python
- Flask
- PostgreSQL
- SQLAlchemy
- HTML5
- CSS3
- JavaScript
- Bootstrap 5
- Git
- GitHub

---

# Funcionalidades Implementadas

## Configuração da Escola

- ✅ Cadastro de Professores
- ✅ Cadastro de Disciplinas
- ✅ Cadastro de Turmas
- ✅ Cadastro de Disponibilidade dos Professores
- ✅ Cadastro de Carga Horária

## Relacionamentos

- ✅ Professor × Disciplina
- ✅ Professor × Turma
- ✅ Turma × Disciplina

## Motor Inteligente

- ✅ Geração automática da grade
- ✅ Sistema de penalidades
- ✅ Heurísticas de alocação
- ✅ Diagnóstico de inviabilidade

## Validações

- ✅ Carga horária maior que a capacidade da turma
- ✅ Professor sem disponibilidade
- ✅ Disciplina sem professor
- ✅ Professor com carga horária incompatível
- ✅ Professor vinculado à disciplina, mas não à turma

---

# Interface Web

O REMADA passou a ser desenvolvido com foco em experiência do usuário.

A configuração da escola foi reorganizada em um fluxo único, reduzindo a quantidade de telas e simplificando o processo de cadastro.

Atualmente a interface possui:

- ✅ Dashboard
- ✅ Central de Cadastros
    - Professores
    - Disciplinas
    - Turmas
- ✅ Modais de cadastro e edição
- ✅ Navegação por abas
- ✅ Persistência da aba ativa
- 🚧 Planejamento
- 🚧 Motor
- 🚧 Diagnóstico

---

# Roadmap

## Fase 1 — Estrutura

- [x] Estrutura inicial
- [x] Flask
- [x] Git
- [x] GitHub

---

## Fase 2 — Modelagem

- [x] Definição das entidades
- [x] Modelagem do banco
- [x] Regras de negócio
- [x] Arquitetura do motor

---

## Fase 3 — Backend

### CRUDs

- [x] Professores
- [x] Disciplinas
- [x] Turmas
- [x] Disponibilidades
- [x] Carga Horária
- [x] Professor × Disciplina
- [x] Professor × Turma
- [x] Turma × Disciplina

---

## Fase 4 — Motor Inteligente

- [x] Estrutura da grade
- [x] Geração automática
- [x] Heurísticas
- [x] Penalidades
- [x] Diagnóstico de inviabilidade
- [ ] Otimização da grade

---

## Fase 5 — Interface

- [x] Dashboard
- [x] Central de Cadastros
- [x] Professores
- [x] Disciplinas
- [x] Turmas
- [ ] Planejamento
- [ ] Disponibilidades
- [ ] Carga Horária
- [ ] Motor
- [ ] Diagnóstico
- [ ] Visualização da grade

---

## Fase 6 — Relatórios

- [ ] PDF
- [ ] Excel
- [ ] Impressão da Grade
- [ ] Relatórios de conflitos

---

## Fase 7 — Plataforma

- [ ] Autenticação
- [ ] Multi-escolas (SaaS)
- [ ] Painel Administrativo
- [ ] Deploy
- [ ] API Pública

---

# Status

🟡 Em desenvolvimento

## Progresso

- ✅ Modelagem concluída
- ✅ Banco de dados concluído
- ✅ CRUDs concluídos
- ✅ Motor funcional
- ✅ Diagnóstico de inviabilidade
- ✅ Interface Web iniciada
- 🚧 Planejamento
- 🚧 Otimização do Motor

---

# Estrutura do Projeto

```
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
│   └── base.html
├── app.py
├── config.py
└── README.md
```

---

# Visão de Produto

O REMADA está sendo desenvolvido como uma plataforma SaaS especializada em geração inteligente de grades horárias escolares.

A proposta é oferecer uma experiência guiada, intuitiva e eficiente, conduzindo o usuário desde a configuração inicial da escola até a geração automática da grade, reduzindo a complexidade do processo e permitindo que coordenadores pedagógicos foquem na gestão acadêmica em vez da montagem manual dos horários.