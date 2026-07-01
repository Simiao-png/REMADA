# Changelog de Homologação

Este documento registra todas as descobertas realizadas durante os testes do sistema.

---

# 01/07/2026

## Teste realizado

Primeiro teste End-to-End utilizando uma escola fictícia.

---

## Descobertas

### ✅ Escola

Cadastro funcionando corretamente.

---

### ✅ Configuração Horária

Cadastro funcionando corretamente.

Melhoria identificada:

- POST poderia retornar o ID criado.

---

### ⚠ Turmas

Problemas encontrados:

- Campo `configuracao_horaria_id` obrigatório sem validação.
- Campo `serie` obrigatório sem validação.
- Sistema permite cadastrar turmas duplicadas.

Correção realizada:

- Exclusão das turmas duplicadas utilizando DELETE.

---

## Melhorias adicionadas ao backlog

- Retornar objeto criado em todos os POST.
- Criar validação amigável para campos obrigatórios.
- Impedir duplicidade de turmas.

---

## Situação do projeto

Escola................. ✅
Configuração Horária... ✅
Turmas................. ✅
Disciplinas............ ⏳
Professores............ ⏳
Disponibilidades....... ⏳
Motor.................. ⏳