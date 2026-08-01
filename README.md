# REMADA

Sistema inteligente para geração automática de grades horárias escolares.

O REMADA é uma plataforma web desenvolvida para automatizar a construção de grades horárias escolares. Utilizando otimização por restrições com Google OR-Tools CP-SAT, o sistema gera grades consistentes respeitando matriz curricular, atribuições docentes, disponibilidade dos professores, carga horária, configurações por segmento e regras pedagógicas.

O objetivo é reduzir conflitos, retrabalho e o tempo gasto na montagem manual da grade.

---

## Tecnologias

- Python
- Flask
- PostgreSQL
- SQLAlchemy
- Google OR-Tools — CP-SAT
- HTML5
- Jinja2
- CSS3
- JavaScript ES6+
- Bootstrap 5
- Git e GitHub

---

## Funcionalidades

### Apresentação e identidade visual

- ✅ Landing page com identidade visual REMADA
- ✅ Dashboard administrativo
- ✅ Interface responsiva
- ✅ Navegação integrada entre cadastro, planejamento, geração e diagnóstico
- ✅ Componentes visuais com cards, indicadores, badges e estados operacionais

### Estrutura multi-escola

- ✅ Isolamento dos dados por escola
- ✅ Seleção da escola ativa por sessão
- ✅ Configurações independentes para cada instituição
- ✅ Disciplinas vinculadas à escola
- ✅ Criação automática de disciplinas padrão para novas escolas

### Cadastros

- ✅ Escolas
- ✅ Professores
- ✅ Disciplina de referência do professor
- ✅ Disciplinas com paleta de cores personalizável
- ✅ Turmas
- ✅ Configuração horária por segmento
- ✅ Suporte a Fundamental I, Fundamental II, Ensino Médio e Cursinho
- ✅ CRUD completo dos módulos principais

### Matriz curricular

- ✅ Matriz Turma × Disciplina
- ✅ Definição da quantidade semanal de aulas
- ✅ Capacidade semanal calculada conforme a configuração da turma
- ✅ Suporte a diferentes quantidades de aulas por segmento
- ✅ Salvamento automático
- ✅ Indicadores de carga incompleta, completa ou excedida
- ✅ Resumo das matrizes cadastradas

### Planejamento dos professores

- ✅ Cadastro básico separado da configuração pedagógica
- ✅ Limite semanal de aulas
- ✅ Atribuição Professor × Turma × Disciplina
- ✅ Um único professor pode assumir diferentes disciplinas
- ✅ Cálculo automático da carga atribuída
- ✅ Indicadores de carga completa, incompleta ou excedida
- ✅ Identificação de turmas e disciplinas sem professor
- ✅ Salvamento automático das atribuições

### Disponibilidade dos professores

- ✅ Grade semanal de disponibilidade
- ✅ Seleção individual por aula
- ✅ Atalho para marcar ou desmarcar um dia inteiro
- ✅ Suporte à 7ª aula do Ensino Médio
- ✅ Quantidade de horários conforme a configuração dos segmentos
- ✅ Salvamento automático em segundo plano
- ✅ Validação entre carga atribuída, limite semanal e horários disponíveis

### Diagnóstico

- ✅ Detecção de turma sem configuração horária
- ✅ Detecção de carga semanal acima da capacidade da turma
- ✅ Detecção de disciplina sem professor atribuído
- ✅ Detecção de professor sem disponibilidade
- ✅ Detecção de disponibilidade insuficiente
- ✅ Detecção de limite semanal excedido
- ✅ Mensagens orientadas para correção antes da geração

### Motor de geração

- ✅ Motor CP-SAT com Google OR-Tools
- ✅ Geração automática da grade
- ✅ Cumprimento exato da matriz curricular
- ✅ Bloqueio de choque de horário da turma
- ✅ Bloqueio de choque de horário do professor
- ✅ Respeito às disponibilidades cadastradas
- ✅ Respeito ao limite semanal do professor
- ✅ Limite de aulas da mesma disciplina por dia
- ✅ Preferência pelos primeiros horários
- ✅ Penalização de concentração excessiva da carga diária
- ✅ Distribuição pedagógica orientada por função objetivo
- ✅ Execução paralela com múltiplos trabalhadores
- ✅ Retorno de solução viável mesmo quando o ótimo não é provado dentro do tempo limite

### Histórico, visualização e exportação

- ✅ Salvamento das grades geradas no banco de dados
- ✅ Versionamento das gerações
- ✅ Visualização por turma
- ✅ Visão geral da escola
- ✅ Cores das disciplinas aplicadas à grade
- ✅ Exportação para Excel
- ✅ Impressão e exportação em PDF
- ✅ Layout específico para impressão

---

## Marco atual

O fluxo principal já funciona de ponta a ponta:

```text
Configuração da escola
        ↓
Cadastro de turmas
        ↓
Matriz curricular
        ↓
Cadastro de professores
        ↓
Atribuição de turmas e disciplinas
        ↓
Disponibilidade dos professores
        ↓
Diagnóstico
        ↓
Geração automática
        ↓
Histórico, visualização e exportação
```

No teste completo mais recente, o motor processou:

- 7 turmas
- 15 professores
- 17 disciplinas
- 504 registros de disponibilidade
- 78 atribuições docentes
- 78 itens de matriz curricular
- 2.550 variáveis de decisão

O CP-SAT encontrou uma solução viável para toda a escola e melhorou progressivamente a função objetivo durante os 30 segundos de otimização.

---

## Estrutura do projeto

```text
REMADA/
├── models/                      # Modelos SQLAlchemy
├── routes/                      # Rotas e endpoints Flask
├── services/                    # Regras de negócio
│   ├── motor/
│   │   ├── cp_sat/              # Solver, restrições, objetivo e diagnóstico
│   │   └── guloso/              # Algoritmo auxiliar ou legado
│   └── ...
├── static/
│   ├── css/                     # Estilos da aplicação
│   ├── js/                      # Scripts da interface
│   └── ...
├── templates/                   # Templates Jinja2
├── tests/                       # Testes e documentação de homologação
├── docs/                        # Documentação técnica
├── app.py                       # Ponto de entrada da aplicação
├── config.py                    # Configurações
├── requirements.txt             # Dependências
└── README.md
```

---

## Roadmap

### Concluído

- ✅ Modelagem do banco de dados e relacionamentos
- ✅ Estrutura multi-escola
- ✅ CRUDs completos dos módulos fundamentais
- ✅ Configuração horária por segmento
- ✅ Matriz curricular com salvamento automático
- ✅ Planejamento integrado dos professores
- ✅ Atribuição Professor × Turma × Disciplina
- ✅ Disponibilidade semanal dos professores
- ✅ Diagnóstico preventivo
- ✅ Motor CP-SAT funcional
- ✅ Geração completa de múltiplas turmas
- ✅ Histórico das versões geradas
- ✅ Visualização por turma e visão geral
- ✅ Exportação para Excel
- ✅ Impressão e exportação em PDF

### Próximas etapas

- 🚧 Ajustes finos de UX nas telas de cadastro e planejamento
- 🚧 Filtros visuais por segmento, disciplina e professor
- 🚧 Progresso do solver em tempo real na interface
- 🚧 Relatório detalhado das penalidades da solução
- 🚧 Preferências pedagógicas configuráveis por escola
- 🚧 Redução de janelas dos professores
- 🚧 Regras específicas para aulas duplas e distribuição semanal
- 🚧 Métricas de qualidade da grade
- 🚧 Testes automatizados de integridade e conflito
- 🚧 Permissões e perfis de usuário
- 🚧 Preparação para implantação em produção

---

## Visão do produto

O REMADA está sendo desenvolvido como uma plataforma SaaS especializada na geração inteligente de grades horárias escolares.

A proposta é oferecer a coordenadores e gestores uma solução moderna para cadastrar a estrutura da escola, planejar a atuação dos professores, validar inconsistências e gerar automaticamente grades horárias por meio de algoritmos de otimização.

---

## Status

🟡 Em desenvolvimento ativo

**Último marco alcançado:** fluxo completo funcionando do cadastro à geração, com CRUD multi-escola, planejamento de professores, diagnóstico preventivo, motor CP-SAT, histórico, visualização e exportação.

---

## Autor

**Silas Simião da Silva**
