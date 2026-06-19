DROP TABLE IF EXISTS votos CASCADE;
DROP TABLE IF EXISTS opcoes CASCADE;
DROP TABLE IF EXISTS enquetes CASCADE;
DROP TABLE IF EXISTS usuarios CASCADE;

CREATE TABLE usuarios (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    email VARCHAR(255) NOT NULL UNIQUE,
    senha VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE enquetes (
    id SERIAL PRIMARY KEY,
    titulo VARCHAR(255) NOT NULL,
    descricao TEXT,
    usuario_id INTEGER NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_enquete_usuario
        FOREIGN KEY (usuario_id)
        REFERENCES usuarios(id)
        ON DELETE CASCADE
);

CREATE TABLE opcoes (
    id SERIAL PRIMARY KEY,
    texto VARCHAR(255) NOT NULL,
    enquete_id INTEGER NOT NULL,

    CONSTRAINT fk_opcao_enquete
        FOREIGN KEY (enquete_id)
        REFERENCES enquetes(id)
        ON DELETE CASCADE
);

CREATE TABLE votos (
    id SERIAL PRIMARY KEY,

    usuario_id INTEGER NOT NULL,
    enquete_id INTEGER NOT NULL,
    opcao_id INTEGER NOT NULL,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_voto_usuario
        FOREIGN KEY (usuario_id)
        REFERENCES usuarios(id)
        ON DELETE CASCADE,

    CONSTRAINT fk_voto_enquete
        FOREIGN KEY (enquete_id)
        REFERENCES enquetes(id)
        ON DELETE CASCADE,

    CONSTRAINT fk_voto_opcao
        FOREIGN KEY (opcao_id)
        REFERENCES opcoes(id)
        ON DELETE CASCADE,

    CONSTRAINT unique_usuario_enquete
        UNIQUE (usuario_id, enquete_id)
);