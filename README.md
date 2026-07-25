# REMADA

Sistema inteligente para geração automática de grades horárias escolares.

O REMADA é uma plataforma web desenvolvida para automatizar a construção de grades horárias escolares. Utilizando otimização por restrições (CP-SAT), o sistema gera grades consistentes respeitando disponibilidade dos professores, matriz curricular, carga horária e regras pedagógicas, reduzindo conflitos e o tempo gasto no planejamento manual.

---

# Tecnologias

- Python
- Flask
- PostgreSQL
- SQLAlchemy
- Google OR-Tools (CP-SAT)
- HTML5
- CSS3
- JavaScript
- Bootstrap 5
- Git
- GitHub

---

# Funcionalidades

## Cadastros

- ✅ Escolas
- ✅ Professores
- ✅ Disciplinas
- ✅ Turmas
- ✅ Configuração Horária por Segmento

## Planejamento

- ✅ Disponibilidade dos Professores
- ✅ Professor × Disciplina
- ✅ Professor × Turma
- ✅ Turma × Disciplina
- ✅ Matriz Curricular

## Motor de Geração

- ✅ Motor CP-SAT utilizando Google OR-Tools
- ✅ Geração automática da grade
- ✅ Controle de conflitos entre professores
- ✅ Controle de conflitos entre turmas
- ✅ Respeito à disponibilidade
- ✅ Respeito à carga horária semanal
- ✅ Distribuição inteligente das aulas
- 🚧 Diagnóstico avançado
- 🚧 Otimização da função objetivo

---

# Estrutura

```text
REMADA/
├── models/
├── routes/
├── services/
│   ├── motor/
│   │   ├── cp_sat/
│   │   └── guloso/
│   └── ...
├── static/
├── templates/
├── app.py
└── README.md
```

---

# Roadmap

## Concluído

- ✅ Banco de dados
- ✅ CRUDs principais
- ✅ Planejamento
- ✅ Configuração por segmentos
- ✅ Motor CP-SAT
- ✅ Geração automática da grade
- ✅ Visualização da grade

## Próximas Etapas

- 🚧 Diagnóstico inteligente
- 🚧 Validação automática da grade
- 🚧 Otimização das penalidades
- 🚧 Preferências configuráveis por escola
- 🚧 Exportação da grade
- 🚧 Impressão em PDF

---

# Visão do Produto

O REMADA está sendo desenvolvido como uma plataforma SaaS especializada na geração inteligente de grades horárias escolares.

O objetivo é oferecer uma solução moderna para coordenadores e gestores escolares, permitindo configurar toda a estrutura da escola e gerar automaticamente grades horárias consistentes por meio de algoritmos de otimização.

---

## Status

🟡 Em desenvolvimento

**Último marco alcançado:** implementação do novo motor CP-SAT para geração automática de grades horárias.