DROP TABLE IF EXISTS qrcode;
DROP TABLE IF EXISTS aluno;
DROP TABLE IF EXISTS professor;
DROP TABLE IF EXISTS turma;
DROP TABLE IF EXISTS grupo;
DROP TABLE IF EXISTS transacao;
DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS convite;
DROP TABLE IF EXISTS item_loja;
DROP TABLE IF EXISTS item_comprado;

CREATE TABLE user (
    matricula INTEGER PRIMARY KEY NOT NULL,
    senha TEXT NOT NULL,
    tipo TEXT CHECK(tipo IN ('aluno', 'professor')) NOT NULL,
    nome TEXT,
    email TEXT
);

CREATE TABLE aluno (
    matricula INTEGER NOT NULL,
    id_grupo INTEGER,
    saldo INTEGER NOT NULL DEFAULT 0,
    id_turma INTEGER,
    FOREIGN KEY (matricula) REFERENCES user (matricula),
    FOREIGN KEY (id_turma) REFERENCES turma (id_turma),
    FOREIGN KEY (id_grupo) REFERENCES grupo (id_grupo)
);

CREATE TABLE professor (
    matricula INTEGER NOT NULL,
    FOREIGN KEY (matricula) REFERENCES user (matricula)
);


CREATE TABLE turma (
  id_turma INTEGER PRIMARY KEY AUTOINCREMENT,
  nome TEXT NOT NULL,
  professor_matricula INTEGER NOT NULL,
  FOREIGN KEY (professor_matricula) REFERENCES professor (matricula)
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
    qtd_usos INTEGER NOT NULL,
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
    id_grupo INTEGER NOT NULL,
    convidado_matricula INTEGER NOT NULL,
    FOREIGN KEY (id_grupo) REFERENCES grupo (id_grupo),
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

-- INSERTS INICIAIS PARA TESTES

INSERT INTO user (matricula, senha, tipo, nome, email) VALUES (1, 'scrypt:32768:8:1$NOgQlSaLqt2lJEdZ$f73dd2078bedd534b641577ec64a5b379e06c2473b9def9ee683dcf91e7ac2e4482eada8a7a1ee13e54991050b8b3b0dba7a287d6586dfcfbdd5ae2de922fae3', 'aluno', 'a', 'a@a');
INSERT INTO user (matricula, senha, tipo, nome, email) VALUES (2, 'scrypt:32768:8:1$NOgQlSaLqt2lJEdZ$f73dd2078bedd534b641577ec64a5b379e06c2473b9def9ee683dcf91e7ac2e4482eada8a7a1ee13e54991050b8b3b0dba7a287d6586dfcfbdd5ae2de922fae3', 'aluno', 'b', 'b@b');
INSERT INTO user (matricula, senha, tipo, nome, email) VALUES (3, 'scrypt:32768:8:1$NOgQlSaLqt2lJEdZ$f73dd2078bedd534b641577ec64a5b379e06c2473b9def9ee683dcf91e7ac2e4482eada8a7a1ee13e54991050b8b3b0dba7a287d6586dfcfbdd5ae2de922fae3', 'professor', 'c', 'c@c');
INSERT INTO user (matricula, senha, tipo, nome, email) VALUES (4, 'scrypt:32768:8:1$NOgQlSaLqt2lJEdZ$f73dd2078bedd534b641577ec64a5b379e06c2473b9def9ee683dcf91e7ac2e4482eada8a7a1ee13e54991050b8b3b0dba7a287d6586dfcfbdd5ae2de922fae3', 'aluno', 'd', 'd@d');

INSERT INTO aluno (matricula, id_grupo, saldo, id_turma) VALUES (1, 1, 100, 1);
INSERT INTO aluno (matricula, id_grupo, saldo, id_turma) VALUES (2, 1, 100, 1);
INSERT INTO aluno (matricula, id_grupo, saldo, id_turma) VALUES (4, null, 100, null);
INSERT INTO professor (matricula) VALUES (3);

INSERT INTO turma (nome, professor_matricula) VALUES ('turma1', 3);

INSERT INTO grupo (nome, descricao, criador_matricula) VALUES ('grupo1', 'descricao', 1);

INSERT INTO convite (id_grupo, convidado_matricula) VALUES (1, 2);
INSERT INTO convite (id_grupo, convidado_matricula) VALUES (1, 4);

INSERT INTO item_loja (nome, valor) VALUES ('item1', 10);
INSERT INTO item_loja (nome, valor) VALUES ('item2', 20);
INSERT INTO item_loja (nome, valor) VALUES ('item3', 30);

INSERT INTO transacao (emissor_id, receptor_id, valor) VALUES (1, 2, 10);
INSERT INTO transacao (emissor_id, receptor_id, valor) VALUES (2, 1, 20);
INSERT INTO transacao (emissor_id, receptor_id, valor) VALUES (1, 2, 30);
INSERT INTO transacao (emissor_id, receptor_id, valor) VALUES (2, 4, 120);

INSERT INTO item_comprado (item_id, aluno_id) VALUES (1, 1);
INSERT INTO item_comprado (item_id, aluno_id) VALUES (2, 1);

INSERT INTO qrcode (token, valor, validade_data, qtd_usos) VALUES ('123', 10, '2020-12-12 12:12:12', 10);
INSERT INTO qrcode (token, valor, validade_data, qtd_usos) VALUES ('456', 20, '2025-12-12 12:12:12', 10);
INSERT INTO qrcode (token, valor, validade_data, qtd_usos) VALUES ('789', 30, '2024-12-12 12:12:12', 10);
