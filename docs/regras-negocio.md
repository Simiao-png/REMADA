# Regras de Negócio

---

## 📥 Informações fornecidas pela escola

Para que o sistema consiga gerar uma grade horária, a escola deverá informar os seguintes dados.

### 🏫 Turmas

* Quantidade de turmas
* Nome da turma
* Série/Ano
* Turno
* Quantidade de aulas por dia

### 📚 Disciplinas

* Nome da disciplina
* Quantidade de aulas semanais por turma
* Permite aulas duplas?
* Permite aulas triplas?
* Exige distribuição semanal?
* Quantidade mínima de dias na semana

### 👨‍🏫 Professores

* Nome
* Disciplinas que pode lecionar
* Turmas em que pode atuar
* Disponibilidade semanal
* Trabalha em outra escola? (Sim/Não)
* Observações e restrições específicas

### 📅 Disponibilidade

* Dias disponíveis
* Horários disponíveis
* Dias bloqueados
* Horários bloqueados

---

## 🚫 Regras Obrigatórias

Estas regras nunca podem ser violadas.

* Um professor não pode estar em duas turmas no mesmo horário.
* Uma turma não pode ter duas disciplinas no mesmo horário.
* A carga horária semanal da disciplina deve ser cumprida.
* A disponibilidade do professor deve ser respeitada.
* Toda turma deve possuir grade horária completa.
* Toda disciplina deve possuir professor habilitado.
* O professor só pode ser alocado para disciplinas que esteja autorizado a lecionar.
* O professor só pode ser alocado para turmas que esteja autorizado a atender.
* A grade deve respeitar a quantidade de aulas diárias definida para cada turno.

---

## ⭐ Preferências

Estas regras devem ser respeitadas sempre que possível.

* Evitar janelas para os professores.
* Distribuir disciplinas ao longo da semana.
* Concentrar a carga horária do professor em menos dias.
* Evitar horários ociosos entre aulas.
* Evitar aulas triplas.
* Priorizar aulas duplas quando necessário.
* Minimizar conflitos de disponibilidade.
* Evitar excesso de aulas consecutivas para o mesmo professor.
* Evitar excesso de aulas consecutivas da mesma disciplina para uma turma.
* Priorizar grades mais equilibradas ao longo da semana.

---

## ⚠️ Penalidades

São situações que não impedem a geração da grade, mas reduzem sua qualidade.

### 🟢 Penalidade Baixa

* Professor com uma janela na semana.
* Disciplina concentrada em poucos dias.
* Pequenos desequilíbrios na distribuição semanal.

### 🟡 Penalidade Média

* Professor com múltiplas janelas.
* Muitas aulas consecutivas no mesmo dia.
* Professor comparecendo à escola para poucas aulas no dia.

### 🔴 Penalidade Alta

* Aulas triplas.
* Grande quantidade de janelas.
* Professor com horário excessivamente fragmentado.
* Disciplina excessivamente concentrada em um único dia.

---

## ❌ Situações de Inviabilidade

O sistema deve informar claramente quando uma grade não puder ser gerada.

### Exemplos

* Professor insuficiente para determinada disciplina.
* Disponibilidade incompatível com a carga horária exigida.
* Disciplina obrigatória sem horário disponível.
* Excesso de restrições impostas pela escola.
* Conflitos impossíveis de resolver.
* Ausência de professor habilitado para determinada disciplina.
* Quantidade de aulas exigidas superior à disponibilidade existente.

---

## 🎯 Objetivo do Motor de Geração

Gerar a melhor grade possível respeitando:

1. Todas as regras obrigatórias.
2. O maior número possível de preferências.
3. A menor quantidade possível de penalidades.
4. A menor quantidade possível de conflitos.

---

## 📊 Indicadores de Qualidade da Grade

Após gerar a grade, o sistema poderá apresentar:

* Quantidade de conflitos encontrados.
* Quantidade de janelas geradas.
* Quantidade de aulas duplas.
* Quantidade de aulas triplas.
* Distribuição semanal das disciplinas.
* Índice geral de qualidade da grade.
* Quantidade de professores com horários fragmentados.
* Quantidade de professores com apenas uma aula em determinado dia.

---

## 🏆 Resultado Esperado

O sistema deverá gerar uma grade:

* Válida.
* Completa.
* Sem conflitos obrigatórios.
* Com o menor número possível de penalidades.
* Fácil de administrar pela coordenação.
* Confortável para professores e alunos.
* Compatível com a realidade operacional da escola.

---
