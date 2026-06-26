-- Banco de Dados: grade_horaria
-- Arquivo: database/schema.sql

CREATE TABLE escolas (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(150) NOT NULL,
    cidade VARCHAR(100),
    estado VARCHAR(50),
    ativo BOOLEAN DEFAULT TRUE,
    criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE professores (
    id SERIAL PRIMARY KEY,
    escola_id INTEGER NOT NULL REFERENCES escolas(id) ON DELETE CASCADE,
    nome VARCHAR(150) NOT NULL,
    email VARCHAR(150),
    telefone VARCHAR(30),
    ativo BOOLEAN DEFAULT TRUE,
    trabalha_outra_escola BOOLEAN DEFAULT FALSE,
    observacoes TEXT,
    criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE disciplinas (
    id SERIAL PRIMARY KEY,
    escola_id INTEGER NOT NULL REFERENCES escolas(id) ON DELETE CASCADE,
    nome VARCHAR(100) NOT NULL,
    ativo BOOLEAN DEFAULT TRUE,
    criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE configuracao_horaria (
    id SERIAL PRIMARY KEY,
    escola_id INTEGER NOT NULL REFERENCES escolas(id) ON DELETE CASCADE,
    nome VARCHAR(100) NOT NULL,
    aulas_por_dia INTEGER NOT NULL,
    duracao_aula_minutos INTEGER NOT NULL,
    duracao_intervalo_minutos INTEGER NOT NULL,
    tem_aula_segunda BOOLEAN DEFAULT TRUE,
    tem_aula_terca BOOLEAN DEFAULT TRUE,
    tem_aula_quarta BOOLEAN DEFAULT TRUE,
    tem_aula_quinta BOOLEAN DEFAULT TRUE,
    tem_aula_sexta BOOLEAN DEFAULT TRUE,
    tem_aula_sabado BOOLEAN DEFAULT FALSE,
    ativo BOOLEAN DEFAULT TRUE,
    criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE turmas (
    id SERIAL PRIMARY KEY,
    escola_id INTEGER NOT NULL REFERENCES escolas(id) ON DELETE CASCADE,
    configuracao_horaria_id INTEGER NOT NULL REFERENCES configuracao_horaria(id),
    nome VARCHAR(50) NOT NULL,
    serie VARCHAR(50) NOT NULL,
    turno VARCHAR(30) NOT NULL,
    ativo BOOLEAN DEFAULT TRUE,
    criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE disponibilidade_professor (
    id SERIAL PRIMARY KEY,
    professor_id INTEGER NOT NULL REFERENCES professores(id) ON DELETE CASCADE,
    dia_semana VARCHAR(20) NOT NULL,
    numero_aula INTEGER NOT NULL,
    disponivel BOOLEAN DEFAULT TRUE
);

CREATE TABLE professor_disciplina (
    professor_id INTEGER NOT NULL REFERENCES professores(id) ON DELETE CASCADE,
    disciplina_id INTEGER NOT NULL REFERENCES disciplinas(id) ON DELETE CASCADE,
    PRIMARY KEY (professor_id, disciplina_id)
);

CREATE TABLE professor_turma (
    professor_id INTEGER NOT NULL REFERENCES professores(id) ON DELETE CASCADE,
    turma_id INTEGER NOT NULL REFERENCES turmas(id) ON DELETE CASCADE,
    PRIMARY KEY (professor_id, turma_id)
);

CREATE TABLE carga_horaria (
    id SERIAL PRIMARY KEY,
    turma_id INTEGER NOT NULL REFERENCES turmas(id) ON DELETE CASCADE,
    disciplina_id INTEGER NOT NULL REFERENCES disciplinas(id) ON DELETE CASCADE,
    quantidade_aulas_semana INTEGER NOT NULL,
    permite_aula_dupla BOOLEAN DEFAULT TRUE,
    permite_aula_tripla BOOLEAN DEFAULT FALSE,
    exige_distribuicao_semanal BOOLEAN DEFAULT FALSE,
    quantidade_minima_dias_semana INTEGER DEFAULT 1,
    criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE turma_disciplina (
    turma_id INTEGER NOT NULL REFERENCES turmas(id) ON DELETE CASCADE,
    disciplina_id INTEGER NOT NULL REFERENCES disciplinas(id) ON DELETE CASCADE,
    PRIMARY KEY (turma_id, disciplina_id)
);