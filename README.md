# REMADA

Sistema inteligente para geração automática de grades horárias escolares.

O REMADA automatiza um dos processos mais complexos da gestão escolar: a construção da grade horária. A plataforma organiza os parâmetros da escola por segmento, valida inconsistências antes da geração da grade e distribui as aulas de forma inteligente, reduzindo conflitos e o tempo gasto na montagem manual.

---

# Últimas Atualizações

- ✅ Configuração horária independente por segmento.
- ✅ Cadastro de disciplinas com cores personalizadas.
- ✅ Associação Professor × Disciplina.
- ✅ Associação Professor × Turma.
- ✅ Associação Turma × Disciplina.
- ✅ Cadastro de carga horária semanal dos professores.
- ✅ Controle de atribuição da carga horária.
- ✅ Situação automática da carga dos professores (Completa, Faltam e Excedeu).
- ✅ Validação da disponibilidade mínima conforme a carga horária semanal.
- ✅ Correção da exibição das disciplinas na tela de disponibilidade.

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

- ✅ Parâmetros por segmento
- ✅ Cadastro de Professores
- ✅ Cadastro de Disciplinas
- ✅ Cadastro de Turmas
- ✅ Disponibilidade dos Professores
- ✅ Carga Horária dos Professores

## Relacionamentos

- ✅ Professor × Disciplina
- ✅ Professor × Turma
- ✅ Turma × Disciplina

## Planejamento

- ✅ Definição da carga horária semanal
- ✅ Distribuição das turmas por professor
- ✅ Controle automático da carga atribuída
- ✅ Situação da carga (Completa, Faltam e Excedeu)
- ✅ Validação da disponibilidade mínima

## Interface

- ✅ Dashboard
- ✅ Central de Cadastros
- ✅ Planejamento
- ✅ Disponibilidade dos Professores
- ✅ Carga Horária
- 🚧 Gerar Grade
- 🚧 Diagnóstico
- 🚧 Visualização da Grade

---

# Roadmap

## Backend

- [x] CRUDs completos
- [x] Configuração horária por segmento
- [x] Relacionamentos do planejamento
- [x] Controle de carga horária
- [ ] Motor de geração da grade
- [ ] Otimização do motor

## Interface

- [x] Dashboard
- [x] Cadastros
- [x] Planejamento
- [x] Disponibilidade
- [x] Carga Horária
- [ ] Gerar Grade
- [ ] Diagnóstico
- [ ] Visualização da Grade

---

# Status

🟡 Em desenvolvimento

## Progresso

- ✅ Banco de dados concluído
- ✅ CRUDs concluídos
- ✅ Planejamento concluído
- ✅ Configuração por segmentos
- ✅ Disponibilidade dos professores
- ✅ Controle da carga horária
- ✅ Relacionamentos entre professores, turmas e disciplinas
- 🚧 Motor de geração automática
- 🚧 Diagnóstico inteligente
- 🚧 Otimização do algoritmo

---

# Estrutura

```text
REMADA/
├── models/
├── routes/
├── services/
│   ├── motor/
│   ├── carga_horaria_service.py
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
│   └── base.html
├── app.py
├── config.py
└── README.md
```

---

# Fluxo do Sistema

1. Configurar os parâmetros da escola.
2. Cadastrar disciplinas.
3. Cadastrar professores.
4. Definir os segmentos de atuação.
5. Definir a carga horária semanal.
6. Cadastrar turmas.
7. Definir a matriz curricular das turmas.
8. Informar a disponibilidade dos professores.
9. Distribuir as turmas entre os professores.
10. Gerar automaticamente a grade horária.

---

# Próxima Etapa

O próximo grande marco do REMADA é o desenvolvimento do motor de geração automática da grade horária.

O algoritmo utilizará todas as informações cadastradas (segmentos, carga horária, disponibilidade, matriz curricular e vínculos entre professores, disciplinas e turmas) para construir automaticamente uma grade viável, minimizando conflitos e distribuindo as aulas de forma equilibrada.

---

# Visão de Produto

O REMADA está sendo desenvolvido como uma plataforma SaaS especializada em geração inteligente de grades horárias escolares.

Seu objetivo é permitir que coordenadores configurem toda a estrutura da escola, realizem o planejamento dos professores e gerem automaticamente grades horárias consistentes através de um fluxo simples, moderno e inteligente.