DROP TABLE IF EXISTS token_qr_code;
DROP TABLE IF EXISTS tokenQrCode;
DROP TABLE IF EXISTS aluno;
DROP TABLE IF EXISTS professor;
DROP TABLE IF EXISTS turma;
DROP TABLE IF EXISTS transacao;
DROP TABLE IF EXISTS user;

CREATE TABLE user(
    id_user INTEGER PRIMARY KEY AUTOINCREMENT,
    matricula TEXT UNIQUE NOT NULL,
    senha TEXT NOT NULL,
    tipo TEXT NOT NULL
);

CREATE TABLE aluno (
  id_aluno INTEGER PRIMARY KEY AUTOINCREMENT,
  id_user INTEGER NOT NULL,
  nome TEXT,
  email TEXT,
  saldo INTEGER NOT NULL DEFAULT 0,
  turma_id INTEGER,
    FOREIGN KEY (turma_id) REFERENCES turma (id_turma),
    FOREIGN KEY (id_user) REFERENCES user (id_user)
);

CREATE TABLE professor (
  id_professor INTEGER PRIMARY KEY AUTOINCREMENT,
    id_user INTEGER NOT NULL,
  nome TEXT,
  email TEXT,
  turma_id INTEGER,
    FOREIGN KEY (id_user) REFERENCES user (id_user)
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