# Grade Horária

Sistema web para geração automática de grades horárias escolares.

## Objetivo

Automatizar a construção de grades horárias escolares, respeitando disponibilidade dos professores, carga horária das disciplinas, turmas, turnos e restrições de horário.

## Problema que o sistema resolve

Muitas escolas já possuem sistemas para notas, faltas e cadastros, mas a montagem da grade horária ainda costuma ser feita manualmente por coordenadores ou professores.

O objetivo deste sistema é reduzir esse trabalho manual e ajudar a escola a gerar horários de forma mais rápida, organizada e sem conflitos.

## Tecnologias

- Python
- Flask
- PostgreSQL
- HTML/CSS/JavaScript
- Git/GitHub

## MVP

- Cadastro de professores
- Cadastro de disciplinas
- Cadastro de turmas
- Cadastro de disponibilidade dos professores
- Definição de carga horária por turma/disciplina
- Geração automática da grade
- Relatório de conflitos/divergências
- Exportação da grade

## Roadmap

### Fase 0 - Estrutura do projeto

- [x] Criar estrutura de pastas
- [x] Criar ambiente virtual
- [x] Instalar Flask
- [x] Rodar aplicação local
- [x] Configurar Git
- [x] Subir projeto para o GitHub

### Fase 1 - Modelagem do negócio

- [x] Definir entidades principais
- [x] Definir regras de negócio
- [x] Definir conflitos obrigatórios
- [x] Definir restrições opcionais
- [x] Definir funcionamento do motor de geração

### Fase 2 - Banco de dados

## Fase 2 — Banco de Dados

- [x] Instalar PostgreSQL
- [x] Modelar tabela professores
- [x] Modelar tabela disciplinas
- [x] Modelar tabela turmas
- [x] Modelar tabela disponibilidade
- [x] Modelar tabela carga_horaria
- [x] Criar schema.sql
- [x] Criar banco local
- [x] Definir relacionamentos entre entidades

## Status

🟡 Em desenvolvimento