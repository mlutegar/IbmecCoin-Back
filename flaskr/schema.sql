DROP TABLE IF EXISTS qrcode;
DROP TABLE IF EXISTS aluno;
DROP TABLE IF EXISTS professor;
DROP TABLE IF EXISTS turma;
DROP TABLE IF EXISTS grupo;
DROP TABLE IF EXISTS transacao;
DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS convite;
DROP TABLE IF EXISTS item_loja;

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
  FOREIGN KEY (professor_id) REFERENCES professor (matricula)
);

CREATE TABLE transacao (
  id_trasacao INTEGER PRIMARY KEY AUTOINCREMENT,
  emissor_id INTEGER NOT NULL,
  receptor_id INTEGER NOT NULL,
  valor INTEGER NOT NULL,
  data TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (emissor_id) REFERENCES aluno (matricula),
    FOREIGN KEY (receptor_id) REFERENCES aluno (matricula)
);

CREATE TABLE qrcode (
    id_token INTEGER PRIMARY KEY AUTOINCREMENT,
    token text NOT NULL,
    valor INTEGER NOT NULL,
    validade_data TIMESTAMP NOT NULL,
    validade BOOLEAN NOT NULL DEFAULT 1
);

CREATE TABLE grupo (
    id_grupo INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    descricao TEXT,
    quantidade_max INTEGER DEFAULT 5,
    criador_matricula INTEGER NOT NULL,
    FOREIGN KEY (criador_matricula) REFERENCES aluno (matricula)
);

CREATE TABLE convite (
    id_convite INTEGER PRIMARY KEY AUTOINCREMENT,
    grupo_id INTEGER NOT NULL,
    convidado_matricula INTEGER NOT NULL,
    FOREIGN KEY (grupo_id) REFERENCES grupo (id_grupo),
    FOREIGN KEY (convidado_matricula) REFERENCES aluno (matricula)
);

CREATE TABLE item_loja (
    id_item INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    valor INTEGER NOT NULL
);

CREATE TABLE item_comprado (
    id_item_comprado INTEGER PRIMARY KEY AUTOINCREMENT,
    item_id INTEGER NOT NULL,
    aluno_id INTEGER NOT NULL,
    data_compra TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (item_id) REFERENCES item_loja (id_item),
    FOREIGN KEY (aluno_id) REFERENCES aluno (matricula)
);