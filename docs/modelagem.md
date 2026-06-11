# Modelagem do Sistema

---

## 👨‍🏫 Professor

Representa o docente que poderá ser alocado na grade horária.

### 📌 Campos principais

* Nome
* E-mail
* Telefone
* Ativo
* Trabalha em outra escola?
* Observações

### 🔗 Relações

* Disciplinas que pode lecionar
* Turmas em que pode atuar
* Disponibilidade semanal
* Restrições específicas

### ⚠️ Regras

* Um professor pode lecionar mais de uma disciplina.
* Um professor pode atuar em mais de uma turma.
* Um professor não pode estar em duas turmas no mesmo horário.
* O sistema deve respeitar a disponibilidade do professor.
* O sistema deve evitar janelas sempre que possível.
* O professor pode ter limite de aulas por dia.
* O professor pode trabalhar em outra escola.

---

## 📚 Disciplina

Representa uma matéria oferecida pela escola.

### 📌 Campos principais

* Nome

### 🔗 Relações

* Pode aparecer em várias turmas.
* Pode ser lecionada por mais de um professor.

### ⚠️ Regras

* Uma disciplina pode exigir aulas duplas.
* Aulas triplas devem ser evitadas por padrão.
* Uma disciplina pode exigir distribuição mínima ao longo da semana.
* Uma disciplina pode precisar aparecer todos os dias.

---

## 🏫 Turma

Representa uma turma que receberá aulas ao longo da semana.

### 📌 Campos principais

* Nome
* Série
* Turno
* Quantidade de aulas por dia

### 🔗 Relações

* Possui várias disciplinas.
* Possui uma carga horária semanal por disciplina.

### ⚠️ Regras

* Uma turma não pode ter duas disciplinas no mesmo horário.
* Toda carga horária semanal deve ser preenchida.

---

## 📊 Carga Horária

Representa a quantidade de aulas que uma disciplina deve ter em uma turma.

### 📌 Campos principais

* Turma
* Disciplina
* Quantidade de aulas semanais
* Permite aula dupla?
* Permite aula tripla?
* Exige distribuição semanal?
* Quantidade mínima de dias na semana

### ⚠️ Regras

* Cada turma deve ter sua carga horária definida por disciplina.
* O sistema deve cumprir a quantidade de aulas semanais definida.
* Aulas duplas são permitidas normalmente.
* Aulas triplas devem ser evitadas ou bloqueadas por padrão.

---

## 📅 Disponibilidade

Representa os horários em que um professor pode ser alocado.

### 📌 Campos principais

* Professor
* Dia da semana
* Número da aula
* Disponível ou indisponível

### ⚠️ Regras

* O sistema deve respeitar integralmente a disponibilidade cadastrada.
* Horários bloqueados não podem ser utilizados.

---

## 🧩 Grade

Representa o resultado final gerado pelo sistema.

### 📌 Definição

* Conjunto de aulas alocadas para todas as turmas e professores.

### ⚠️ Regras

* Deve respeitar todas as restrições obrigatórias.
* Deve minimizar conflitos e janelas.
* Deve indicar se a grade é viável ou inviável.

---

## 📝 Aula Alocada

Representa uma aula posicionada em um slot específico da grade.

### 📌 Campos principais

* Professor
* Turma
* Disciplina
* Dia da semana
* Número da aula

---

## 🚨 Conflito

Representa uma situação que impede ou prejudica a geração da grade.

### 📌 Campos principais

* Tipo
* Descrição
* Severidade

### ⚠️ Exemplos

* Professor em duas turmas no mesmo horário.
* Disciplina sem professor disponível.
* Carga horária impossível de completar.
* Excesso de janelas.
* Aula tripla indesejada.
* Restrição incompatível com a disponibilidade cadastrada.

---