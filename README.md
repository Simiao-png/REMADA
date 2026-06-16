# Grade Horária

Sistema web para geração automática de grades horárias escolares.

## Objetivo

Automatizar a construção de grades horárias escolares, respeitando disponibilidade dos professores, carga horária das disciplinas, turmas, turnos e restrições de horário.

## Problema que o sistema resolve

Muitas escolas já possuem sistemas para notas, faltas e cadastros, mas a montagem da grade horária ainda costuma ser feita manualmente por coordenadores ou professores.

O objetivo deste sistema é reduzir esse trabalho manual e ajudar a escola a gerar horários de forma mais rápida, organizada e sem conflitos.

## Tecnologias

* Python
* Flask
* PostgreSQL
* HTML/CSS/JavaScript
* Git/GitHub

## MVP

* Cadastro de professores
* Cadastro de disciplinas
* Cadastro de turmas
* Cadastro de disponibilidade dos professores
* Definição de carga horária por turma/disciplina
* Geração automática da grade
* Relatório de conflitos/divergências
* Exportação da grade

## Roadmap

### Fase 0 - Estrutura do projeto

* [x] Criar estrutura de pastas
* [x] Criar ambiente virtual
* [x] Instalar Flask
* [x] Rodar aplicação local
* [x] Configurar Git
* [x] Subir projeto para o GitHub

### Fase 1 - Modelagem do negócio

* [x] Definir entidades principais
* [x] Definir regras de negócio
* [x] Definir conflitos obrigatórios
* [x] Definir restrições opcionais
* [x] Definir funcionamento do motor de geração

### Fase 2 - Banco de Dados e Integração

* [x] Instalar PostgreSQL
* [x] Criar banco local
* [x] Criar schema.sql

#### Tabelas modeladas

* [x] escolas
* [x] professores
* [x] disciplinas
* [x] turmas
* [x] disponibilidade_professor
* [x] carga_horaria
* [x] professor_disciplina
* [x] professor_turma
* [x] turma_disciplina

#### Integração com Flask

* [x] Configurar SQLAlchemy
* [x] Criar models das entidades
* [x] Criar blueprints iniciais
* [x] Conectar aplicação ao PostgreSQL
* [x] Testar leitura das entidades cadastradas

### Fase 3 - CRUDs

* [ ] CRUD de Escolas
* [ ] CRUD de Professores
* [ ] CRUD de Disciplinas
* [ ] CRUD de Turmas
* [ ] CRUD de Disponibilidade
* [ ] CRUD de Carga Horária
* [ ] CRUD dos relacionamentos

### Fase 4 - Motor de Geração

* [ ] Implementar algoritmo de geração
* [ ] Validar conflitos
* [ ] Aplicar restrições obrigatórias
* [ ] Aplicar preferências e penalidades
* [ ] Gerar grade completa

### Fase 5 - Interface Web

* [ ] Dashboard
* [ ] Formulários de cadastro
* [ ] Visualização da grade
* [ ] Relatórios

### Fase 6 - Deploy

* [ ] Deploy da aplicação
* [ ] Configuração de domínio
* [ ] Testes em ambiente real

## Status

🟡 Em desenvolvimento

### Progresso atual

✅ Estrutura do projeto concluída

✅ Regras de negócio definidas

✅ Banco PostgreSQL modelado

✅ Models integrados ao Flask

✅ Primeiras consultas funcionando

🚧 Próxima etapa: desenvolvimento dos CRUDs
