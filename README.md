# Grade Horária

Sistema web para geração automática de grades horárias escolares.

## Objetivo

Automatizar a construção de grades horárias escolares, respeitando disponibilidade dos professores, carga horária das disciplinas, turmas, turnos e restrições de horário.

## Problema que o sistema resolve

Muitas escolas já possuem sistemas para notas, faltas e cadastros, mas a montagem da grade horária ainda costuma ser feita manualmente por coordenadores ou professores.

O objetivo deste sistema é reduzir esse trabalho manual e ajudar a escola a gerar horários de forma rápida, organizada e sem conflitos.

## Tecnologias

* Python
* Flask
* PostgreSQL
* HTML/CSS
* JavaScript
* SQLAlchemy
* Git / GitHub

---

## Funcionalidades atuais

* Cadastro de Escolas
* Cadastro de Professores
* Cadastro de Disciplinas
* Cadastro de Turmas
* Cadastro de Disponibilidade dos Professores
* Cadastro de Carga Horária
* Relacionamento Professor × Disciplina
* Relacionamento Professor × Turma
* Relacionamento Turma × Disciplina
* Geração automática de grades horárias
* Validação automática de conflitos
* Sistema de penalidades para otimização da grade

---

## Roadmap

### Fase 0 — Estrutura do Projeto

* [x] Criar estrutura de pastas
* [x] Criar ambiente virtual
* [x] Instalar Flask
* [x] Rodar aplicação local
* [x] Configurar Git
* [x] Publicar projeto no GitHub

---

### Fase 1 — Modelagem do Negócio

* [x] Definir entidades
* [x] Definir regras de negócio
* [x] Definir conflitos obrigatórios
* [x] Definir restrições opcionais
* [x] Projetar o motor de geração

---

### Fase 2 — Banco de Dados

* [x] Instalar PostgreSQL
* [x] Criar banco de dados
* [x] Criar schema.sql
* [x] Modelar todas as tabelas
* [x] Integrar SQLAlchemy

---

### Fase 3 — CRUDs

* [x] Escolas
* [x] Professores
* [x] Disciplinas
* [x] Turmas
* [x] Disponibilidade
* [x] Carga Horária
* [x] Professor × Disciplina
* [x] Professor × Turma
* [x] Turma × Disciplina

---

### Fase 4 — Motor de Geração

* [x] Definir algoritmo inicial
* [x] Implementar validação de conflitos
* [x] Implementar distribuição de aulas
* [x] Implementar cálculo de penalidades
* [x] Implementar análise de inviabilidade
* [ ] Otimização da grade

---

### Fase 5 — Interface Web

* [ ] Dashboard
* [ ] Tela de Escolas
* [ ] Tela de Professores
* [ ] Tela de Disciplinas
* [ ] Tela de Turmas
* [ ] Tela de Disponibilidade
* [ ] Tela de Geração
* [ ] Visualização da Grade
* [ ] Relatórios

---

### Fase 6 — Deploy

* [ ] Deploy em produção
* [ ] Domínio próprio
* [ ] Testes de carga
* [ ] Documentação da API

---

## Status

🟡 Em desenvolvimento

### Progresso Atual

* ✅ Modelagem concluída
* ✅ Banco de dados integrado
* ✅ CRUDs principais implementados
* ✅ Motor de geração funcional
* ✅ Sistema de penalidades implementado
* 🚧 Próxima etapa: análise de inviabilidade e otimização da grade

---

## Estrutura do Projeto

```
grade-horaria/

├── models/
├── routes/
├── services/
│   └── motor/
│       ├── gerador.py
│       ├── alocador.py
│       ├── aulas.py
│       ├── estrutura.py
│       ├── validacoes.py
│       ├── heuristicas.py
│       └── penalidades.py
├── database/
├── templates/
├── static/
└── app.py
```
