INSERT INTO usuarios (
    nome,
    email,
    senha
)
VALUES
(
    'Exemplo',
    'exemplo@email.com',
    'Exemplo123!'
);

INSERT INTO enquetes (
    titulo,
    descricao,
    usuario_id
)
VALUES
(
    'Melhor linguagem de programação',
    'Vote na sua favorita',
    1
);

INSERT INTO opcoes (
    texto,
    enquete_id
)
VALUES
('Python', 1),
('Java', 1),
('JavaScript', 1),
('C#', 1);