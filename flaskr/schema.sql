DROP TABLE IF EXISTS token_qr_code;
DROP TABLE IF EXISTS aluno;
DROP TABLE IF EXISTS professor;
DROP TABLE IF EXISTS turma;
DROP TABLE IF EXISTS grupo_transferencia;
DROP TABLE IF EXISTS transacao;
DROP TABLE IF EXISTS user;

CREATE TABLE user (
    matricula INTEGER PRIMARY KEY NOT NULL,
    senha TEXT NOT NULL,
    tipo TEXT CHECK(tipo IN ('aluno', 'professor')) NOT NULL,
    nome TEXT,
    email TEXT
);

CREATE TABLE aluno (
    matricula INTEGER NOT NULL,
    grupo_id INTEGER,
    saldo INTEGER NOT NULL DEFAULT 0,
    turma_id INTEGER,
    FOREIGN KEY (matricula) REFERENCES user (matricula),
    FOREIGN KEY (turma_id) REFERENCES turma (id_turma),
    FOREIGN KEY (grupo_id) REFERENCES grupo (id_grupo)
);

CREATE TABLE professor (
    matricula INTEGER NOT NULL,
    turma_id INTEGER,
    FOREIGN KEY (matricula) REFERENCES user (matricula)
);


CREATE TABLE turma (
  id_turma INTEGER PRIMARY KEY AUTOINCREMENT,
  nome TEXT NOT NULL,
  professor_id INTEGER NOT NULL,
  FOREIGN KEY (professor_id) REFERENCES professor (id_professor)
);

CREATE TABLE transacao (
  id_trasacao INTEGER PRIMARY KEY AUTOINCREMENT,
  emissor_id INTEGER NOT NULL,
  receptor_id INTEGER NOT NULL,
  valor INTEGER NOT NULL,
  data TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (emissor_id) REFERENCES aluno (id_aluno),
    FOREIGN KEY (receptor_id) REFERENCES aluno (id_aluno)
);

CREATE TABLE token_qr_code (
    id_token INTEGER PRIMARY KEY AUTOINCREMENT,
    token text NOT NULL,
    valor INTEGER NOT NULL,
    validade TIMESTAMP NOT NULL,
    used BOOLEAN NOT NULL DEFAULT 1
);

CREATE TABLE grupo (
    id_grupo INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    valor_max INTEGER NOT NULL,
    criador_matricula INTEGER NOT NULL,
    FOREIGN KEY (criador_matricula) REFERENCES aluno (matricula)
);