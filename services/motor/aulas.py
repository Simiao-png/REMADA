from models.professor_disciplina import ProfessorDisciplina


def criar_fila_aulas(cargas_horarias):

    fila = []

    for carga in cargas_horarias:

        professor = ProfessorDisciplina.query.filter_by(
            disciplina_id=carga.disciplina_id
        ).first()

        professor_id = None

        if professor:
            professor_id = professor.professor_id

        for _ in range(carga.quantidade_aulas_semana):

            fila.append({
                "turma_id": carga.turma_id,
                "disciplina_id": carga.disciplina_id,
                "professor_id": professor_id
            })

    return fila