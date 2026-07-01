# Teste End-to-End — Grade Horária

## Objetivo

Validar o sistema completo simulando o cadastro de uma escola desde o início até a geração automática da grade horária.

---

# Fluxo do Teste

- [x] 1. Cadastrar Escola
- [x] 2. Cadastrar Configuração Horária
- [x] 3. Cadastrar Turmas
- [ ] 4. Cadastrar Disciplinas
- [ ] 5. Cadastrar Professores
- [ ] 6. Cadastrar Disponibilidades
- [ ] 7. Vincular Professor × Disciplina
- [ ] 8. Vincular Professor × Turma
- [ ] 9. Cadastrar Cargas Horárias
- [ ] 10. Executar Diagnóstico
- [ ] 11. Gerar Grade

---

# Dados Utilizados

## Escola

**POST /escolas**

```json
{
    "nome": "Colégio Teste Motor",
    "cidade": "São Paulo",
    "estado": "SP"
}
```

Resultado esperado

```json
{
    "mensagem": "Escola criada com sucesso!"
}
```

---

## Configuração Horária

**POST /configuracoes-horarias**

```json
{
    "escola_id": 7,
    "nome": "Manhã - 6 aulas",
    "aulas_por_dia": 6,
    "duracao_aula_minutos": 50,
    "duracao_intervalo_minutos": 20,
    "tem_aula_segunda": true,
    "tem_aula_terca": true,
    "tem_aula_quarta": true,
    "tem_aula_quinta": true,
    "tem_aula_sexta": true,
    "tem_aula_sabado": false,
    "ativo": true
}
```

Consultar

```
GET /configuracoes-horarias
```

Guardar o ID da configuração criada.

---

## Turmas

**POST /turmas**

### 6º Ano

```json
{
    "nome": "6º Ano",
    "escola_id": 7,
    "configuracao_horaria_id": 3,
    "serie": "6º Ano",
    "turno": "Manhã",
    "ativo": true
}
```

### 7º Ano

```json
{
    "nome": "7º Ano",
    "escola_id": 7,
    "configuracao_horaria_id": 3,
    "serie": "7º Ano",
    "turno": "Manhã",
    "ativo": true
}
```

### 8º Ano

```json
{
    "nome": "8º Ano",
    "escola_id": 7,
    "configuracao_horaria_id": 3,
    "serie": "8º Ano",
    "turno": "Manhã",
    "ativo": true
}
```

### 9º Ano

```json
{
    "nome": "9º Ano",
    "escola_id": 7,
    "configuracao_horaria_id": 3,
    "serie": "9º Ano",
    "turno": "Manhã",
    "ativo": true
}
```

Conferir

```
GET /turmas
```

---

## Disciplinas

**POST /disciplinas**

Cadastrar uma por vez.

```json
{ "nome": "Matemática" }
```

```json
{ "nome": "Português" }
```

```json
{ "nome": "História" }
```

```json
{ "nome": "Geografia" }
```

```json
{ "nome": "Ciências" }
```

```json
{ "nome": "Inglês" }
```

```json
{ "nome": "Arte" }
```

```json
{ "nome": "Educação Física" }
```

Conferir

```
GET /disciplinas
```

---

## Professores

**POST /professores**

Exemplo

```json
{
    "nome": "Ana Matemática",
    "email": "ana@teste.com",
    "telefone": "11999990001",
    "ativo": true
}
```

Cadastrar professores para:

- Matemática
- Português
- História
- Geografia
- Ciências
- Inglês
- Arte
- Educação Física

Conferir

```
GET /professores
```

---

## Disponibilidades

**POST /disponibilidades**

Exemplo

```json
{
    "professor_id": 1,
    "dia_semana": "segunda",
    "indice_horario": 1,
    "disponivel": true
}
```

Cadastrar:

- Segunda a Sexta
- 6 horários por dia
- Horários 1 ao 6

---

## Professor × Disciplina

**POST /professor-disciplinas**

```json
{
    "professor_id": 1,
    "disciplina_id": 1
}
```

---

## Professor × Turma

**POST /professor-turmas**

```json
{
    "professor_id": 1,
    "turma_id": 9
}
```

Repetir para todas as turmas.

---

## Carga Horária

**POST /cargas-horarias**

```json
{
    "turma_id": 9,
    "disciplina_id": 1,
    "quantidade_aulas_semana": 5,
    "permite_aula_dupla": true,
    "permite_aula_tripla": false,
    "exige_distribuicao_semanal": false,
    "quantidade_minima_dias_semana": 1
}
```

Carga sugerida:

| Disciplina | Aulas |
|------------|------:|
| Matemática | 5 |
| Português | 5 |
| História | 3 |
| Geografia | 3 |
| Ciências | 3 |
| Inglês | 2 |
| Arte | 2 |
| Educação Física | 2 |

Total:

```
25 aulas semanais
```

---

# Diagnóstico

```
GET /motor/diagnostico
```

Resultado esperado

```json
{
    "viavel": true,
    "problemas": []
}
```

---

# Geração da Grade

```
GET /motor/gerar
```

Resultado esperado

- Grade gerada com sucesso.
- Nenhuma turma em conflito.
- Nenhum professor em dois lugares ao mesmo tempo.
- Toda carga horária atendida.

---

# Bugs Encontrados

## Bug 001

**Descrição**

Turmas duplicadas podem ser cadastradas.

**Status**

- [ ] Corrigir

---

## Bug 002

**Descrição**

POST não retorna o ID do objeto criado.

**Status**

- [ ] Corrigir

---

## Bug 003

**Descrição**

Campos obrigatórios ausentes geram erro 500.

Campos encontrados:

- serie
- configuracao_horaria_id

**Status**

- [ ] Corrigir

---

# Melhorias Futuras

- Retornar o objeto criado em todos os POST.
- Validar campos obrigatórios antes da criação.
- Bloquear cadastro de turmas duplicadas.
- Criar mensagens de erro mais amigáveis.
- Criar cenário oficial de testes para homologação.

---

# Status do Teste

| Etapa | Status |
|--------|:------:|
| Escola | ✅ |
| Configuração Horária | ✅ |
| Turmas | ✅ |
| Disciplinas | ⏳ |
| Professores | ⏳ |
| Disponibilidades | ⏳ |
| Professor × Disciplina | ⏳ |
| Professor × Turma | ⏳ |
| Carga Horária | ⏳ |
| Diagnóstico | ⏳ |
| Geração da Grade | ⏳ |

---

**Última atualização:** 01/07/2026