DROP TABLE IF EXISTS tokenQrCode;
DROP TABLE IF EXISTS aluno;
DROP TABLE IF EXISTS professor;
DROP TABLE IF EXISTS turma;
DROP TABLE IF EXISTS transacao;

CREATE TABLE aluno (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  nome TEXT,
  matricula TEXT NOT NULL,
  email TEXT,
  senha TEXT NOT NULL,
  saldo INTEGER NOT NULL DEFAULT 0,
  turma_id INTEGER,
    FOREIGN KEY (turma_id) REFERENCES turma (id)
);

CREATE TABLE professor (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  nome TEXT,
  matricula TEXT NOT NULL,
  email TEXT,
  senha TEXT NOT NULL
);

CREATE TABLE turma (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  nome TEXT NOT NULL,
  professor_id INTEGER NOT NULL,
  FOREIGN KEY (professor_id) REFERENCES professor (id)
);

CREATE TABLE transacao (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  emissor_id INTEGER NOT NULL,
  receptor_id INTEGER NOT NULL,
  valor INTEGER NOT NULL,
  data TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (emissor_id) REFERENCES aluno (id),
    FOREIGN KEY (receptor_id) REFERENCES aluno (id)
);

CREATE TABLE tokenQrCode (
    token text primary key,
    used BOOLEAN NOT NULL DEFAULT 0
);