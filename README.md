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
- HTML5 / Jinja2
- CSS3
- JavaScript (ES6+)
- Bootstrap 5
- Git / GitHub

---

# Funcionalidades

## Apresentação e Identidade Visual
- ✅ Nova Landing Page/Tela de Entrada com identidade visual atualizada e marca REMADA
- ✅ Interface responsiva com suporte a temas e cards operacionais

## Cadastros
- ✅ Escolas (com isolamento multi-escola)
- ✅ Professores
- ✅ Disciplinas (com paleta de cores customizável)
- ✅ Turmas
- ✅ Configuração Horária por Segmento

## Planejamento Avançado
- ✅ Matriz Curricular (Turma × Disciplina)
- ✅ Atribuição de Carga Horária (Professor × Disciplina / Professor × Turma)
- ✅ **Grade de Disponibilidade dos Professores:**
  - Suporte estendido a até 7 aulas diárias (atendimento completo ao Ensino Médio)
  - Seleção por horário individual ou atalho por dia completo
  - Indicadores em tempo real: *Carga Contratada* vs *Horários Marcados*
  - Salvamento automático em segundo plano
- ✅ **Diagnóstico de Planejamento:**
  - Monitoramento dinâmico em tempo real do confronto entre *Total da Carga dos Professores* vs *Necessidade das Turmas*

## Motor de Geração
- ✅ Motor CP-SAT utilizando Google OR-Tools
- ✅ Geração automática da grade
- ✅ Controle rigoroso de choques de horário (professores e turmas)
- ✅ Respeito às janelas e disponibilidades cadastradas
- ✅ Distribuição equilibrada da matriz semanal

## Visualização e Exportação
- ✅ Visualização de Grade por Turma e Visão Geral da Escola
- ✅ Módulo dedicado para Impressão e Exportação em PDF com ajuste de layout para impressão (print CSS)

---

# Estrutura do Projeto

```text
REMADA/
├── models/                      # Modelos do Banco de Dados (SQLAlchemy)
├── routes/                      # Rotas e Endpoints da Aplicação
├── services/                    # Regras de Negócio e Serviços
│   ├── motor/                   # Motores de Otimização
│   │   ├── cp_sat/              # Solver OR-Tools CP-SAT
│   │   └── guloso/              # Algoritmo auxiliar/legado
│   └── ...
├── static/                      # Arquivos Estáticos (CSS, JS, Imagens, Logo)
├── templates/                   # Templates Jinja2 (HTML)
├── app.py                       # Ponto de Entrada da Aplicação Flask
└── README.md


Roadmap
Concluído
✅ Modelagem do banco de dados e relacionamentos

✅ CRUDs completos dos módulos fundamentais

✅ Módulo de Planejamento com indicadores e suporte à 7ª aula

✅ Configuração flexível por segmento e escola

✅ Motor de Otimização CP-SAT funcional

✅ Visualização da grade por turma / visão geral

✅ Exportação e Impressão otimizada em PDF

Próximas Etapas
🚧 Ajustes finos no acionamento e progresso em tempo real do motor na interface

🚧 Validação automática e relatórios de penalidades pedagógicas

🚧 Parâmetros customizáveis de preferências por escola (ex: evitar aulas duplas isoladas)

🚧 Painel avançado de métricas e diagnósticos da grade gerada

Visão do Produto
O REMADA está sendo desenvolvido como uma plataforma SaaS especializada na geração inteligente de grades horárias escolares.

O objetivo é oferecer uma solução moderna para coordenadores e gestores escolares, permitindo configurar toda a estrutura da escola e gerar automaticamente grades horárias consistentes por meio de algoritmos de otimização.

Status
🟡 Em desenvolvimento ativo

Último marco alcançado: Implementação dos contadores dinâmicos de planejamento, suporte à 7ª aula no Ensino Médio, atualização da landing page/identidade visual e módulo de impressão em PDF.