# REMADA

Sistema inteligente para geração automática de grades horárias escolares.

O REMADA automatiza a criação de grades horárias, respeitando disponibilidade dos professores, carga horária das disciplinas, turmas, turnos e regras pedagógicas, reduzindo conflitos e o tempo gasto na montagem manual dos horários.

---

## Objetivo

Desenvolver uma plataforma web capaz de gerar grades horárias escolares de forma inteligente, utilizando algoritmos de validação, heurísticas e otimização para produzir uma distribuição eficiente das aulas.

O projeto foi idealizado para atender escolas de pequeno, médio e grande porte, oferecendo uma solução moderna para um dos processos mais complexos da gestão escolar.

---

## Problema que o REMADA resolve

Apesar da evolução dos sistemas de gestão escolar, a construção da grade horária ainda é, em muitos casos, realizada manualmente.

Esse processo costuma consumir muitas horas de trabalho, gerar conflitos entre professores, turmas e disciplinas e exigir diversos ajustes até que uma grade viável seja encontrada.

O REMADA automatiza esse processo, detectando inconsistências antes da geração da grade e distribuindo as aulas de forma inteligente.

---

## Tecnologias

- Python
- Flask
- PostgreSQL
- SQLAlchemy
- HTML5
- CSS3
- JavaScript
- Bootstrap 5
- Git / GitHub

---

## Funcionalidades implementadas

### Cadastros

- ✅ Escolas
- ✅ Professores
- ✅ Disciplinas
- ✅ Turmas
- ✅ Disponibilidade dos Professores
- ✅ Carga Horária

### Relacionamentos

- ✅ Professor × Disciplina
- ✅ Professor × Turma
- ✅ Turma × Disciplina

### Motor de Geração

- ✅ Geração automática de grades
- ✅ Sistema de penalidades
- ✅ Heurísticas de alocação
- ✅ Análise automática de inviabilidade

### Validações implementadas

- ✅ Carga horária superior à capacidade da turma
- ✅ Professor sem disponibilidade
- ✅ Disciplina sem professor
- ✅ Professor com carga horária incompatível
- ✅ Professor vinculado à disciplina, mas não à turma

---

# Roadmap

## Fase 0 — Estrutura do Projeto

- [x] Estrutura inicial
- [x] Ambiente virtual
- [x] Flask
- [x] Git
- [x] GitHub

---

## Fase 1 — Modelagem

- [x] Definição das entidades
- [x] Regras de negócio
- [x] Restrições obrigatórias
- [x] Restrições opcionais
- [x] Arquitetura do motor

---

## Fase 2 — Banco de Dados

- [x] PostgreSQL
- [x] Modelagem
- [x] Schema SQL
- [x] SQLAlchemy

---

## Fase 3 — Backend

### CRUDs

- [x] Escolas
- [x] Professores
- [x] Disciplinas
- [x] Turmas
- [x] Disponibilidade
- [x] Carga Horária
- [x] Professor × Disciplina
- [x] Professor × Turma
- [x] Turma × Disciplina

---

## Fase 4 — Motor Inteligente

- [x] Estrutura da grade
- [x] Geração automática
- [x] Sistema de penalidades
- [x] Heurísticas de alocação
- [x] Análise de inviabilidade
- [ ] Otimização da grade

---

## Fase 5 — Interface Web

- [x] Estrutura base
- [x] Dashboard inicial
- [ ] Layout definitivo
- [ ] Tela de Escolas
- [ ] Tela de Professores
- [ ] Tela de Disciplinas
- [ ] Tela de Turmas
- [ ] Tela de Disponibilidade
- [ ] Tela de Geração
- [ ] Tela de Diagnóstico
- [ ] Visualização da Grade

---

## Fase 6 — Relatórios

- [ ] Exportação em PDF
- [ ] Exportação em Excel
- [ ] Impressão da grade
- [ ] Relatórios de conflitos

---

## Fase 7 — Deploy

- [ ] Deploy em produção
- [ ] Domínio próprio
- [ ] Autenticação
- [ ] Documentação da API

---

# Status

🟡 Em desenvolvimento

## Progresso Atual

- ✅ Modelagem concluída
- ✅ Banco de dados concluído
- ✅ CRUDs implementados
- ✅ Motor funcional
- ✅ Sistema de penalidades
- ✅ Análise de inviabilidade
- 🚧 Desenvolvimento da interface web

---

# Estrutura do Projeto

```
REMADA/

├── database/
├── docs/
├── models/
├── routes/
├── services/
│   └── motor/
│       ├── alocador.py
│       ├── aulas.py
│       ├── estrutura.py
│       ├── gerador.py
│       ├── heuristicas.py
│       ├── inviabilidade.py
│       ├── penalidades.py
│       └── validacoes.py
├── static/
│   ├── css/
│   ├── js/
│   └── img/
├── templates/
├── app.py
├── config.py
└── README.md
```

---

# Visão de Longo Prazo

O objetivo é transformar o REMADA em uma plataforma completa para geração inteligente de grades horárias escolares, oferecendo uma experiência moderna, intuitiva e eficiente para coordenadores pedagógicos e instituições de ensino.