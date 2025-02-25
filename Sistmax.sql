DROP DATABASE IF EXISTS sistmax;
CREATE DATABASE sistmax;
USE Sistmax;

-- Tabela de planos de assinatura (criar primeiro)
CREATE TABLE planos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome ENUM('básico', 'pro', 'premium') NOT NULL UNIQUE,
    preco DECIMAL(10,2) NOT NULL COMMENT 'Preço do plano',
    descricao TEXT COMMENT 'Descrição do plano',
    duracao_meses INT NOT NULL DEFAULT 1 COMMENT 'Duração do plano em meses'  -- Definido o valor padrão como 12
);

-- Inserindo planos padrões
INSERT INTO planos (nome, preco, descricao) VALUES 
('básico', 20.90, 'Plano gratuito com anúncios'),
('pro', 39.90, 'Plano pago sem anúncios e com qualidade HD'),
('premium', 55.90, 'Plano pago com conteúdo 4K e múltiplos dispositivos');

-- Tabela de usuários (criar após a tabela planos)
CREATE TABLE usuarios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    senha VARCHAR(255) NOT NULL,  -- Alterado para 255 caracteres para acomodar o hash
    data_criacao DATETIME DEFAULT CURRENT_TIMESTAMP,
    tipo_usuario ENUM('básico', 'pro', 'premium') NOT NULL,
    plano_id INT,  -- Adicionada a coluna plano_id para vincular ao plano
    FOREIGN KEY (plano_id) REFERENCES planos(id)  -- Definindo chave estrangeira para a tabela planos
);

ALTER TABLE usuarios MODIFY senha VARCHAR(255);

-- Índice para melhorar buscas por email
CREATE INDEX idx_email ON usuarios(email);

-- Tabela de assinaturas
CREATE TABLE assinaturas (
    id INT AUTO_INCREMENT PRIMARY KEY,
    usuario_id INT NOT NULL,
    plano_id INT NOT NULL,
    data_inicio DATETIME NOT NULL,
    data_fim DATETIME DEFAULT NULL,
    status ENUM('ativa', 'inativa', 'cancelada') NOT NULL,
    FOREIGN KEY (usuario_id) REFERENCES usuarios(id) ON DELETE CASCADE,
    FOREIGN KEY (plano_id) REFERENCES planos(id) ON DELETE CASCADE
);

-- Tabela de filmes
CREATE TABLE filmes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    titulo VARCHAR(255) NOT NULL,
    ano INT NOT NULL,
    genero VARCHAR(100),
    diretor VARCHAR(255),
    duracao INT
);

-- Tabela de conteúdos (filmes e séries)
CREATE TABLE conteudos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    titulo VARCHAR(255) NOT NULL,
    descricao TEXT,
    categoria VARCHAR(100),
    ano_lancamento INT NOT NULL,
    tipo ENUM('filme', 'serie') NOT NULL,
    duracao_minutos INT,
    classificacao_indicativa VARCHAR(50)
);

-- Índice para melhorar buscas por título de conteúdo
CREATE INDEX idx_titulo ON conteudos(titulo);

-- Tabela de episódios (aplicável para séries)
CREATE TABLE episodios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    conteudo_id INT NOT NULL,
    temporada INT NOT NULL,
    numero_episodio INT NOT NULL,
    titulo VARCHAR(255) NOT NULL,
    duracao_minutos INT NOT NULL,
    FOREIGN KEY (conteudo_id) REFERENCES conteudos(id) ON DELETE CASCADE
);

-- Histórico de visualizações
CREATE TABLE historico_visualizacoes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    usuario_id INT NOT NULL,
    conteudo_id INT NOT NULL,
    episodio_id INT DEFAULT NULL,
    data_visualizacao DATETIME DEFAULT CURRENT_TIMESTAMP,
    tempo_assistido INT NOT NULL COMMENT 'Tempo assistido em segundos',
    FOREIGN KEY (usuario_id) REFERENCES usuarios(id) ON DELETE CASCADE,
    FOREIGN KEY (conteudo_id) REFERENCES conteudos(id) ON DELETE CASCADE,
    FOREIGN KEY (episodio_id) REFERENCES episodios(id) ON DELETE SET NULL
);

-- Tabela de recomendações
CREATE TABLE recomendacoes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    usuario_id INT NOT NULL,
    conteudo_id INT NOT NULL,
    motivo TEXT,
    FOREIGN KEY (usuario_id) REFERENCES usuarios(id) ON DELETE CASCADE,
    FOREIGN KEY (conteudo_id) REFERENCES conteudos(id) ON DELETE CASCADE
);

-- Tabela de avaliações
CREATE TABLE avaliacoes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    usuario_id INT NOT NULL,
    conteudo_id INT NOT NULL,
    nota FLOAT NOT NULL,
    comentario TEXT,
    data_avaliacao DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (usuario_id) REFERENCES usuarios(id) ON DELETE CASCADE,
    FOREIGN KEY (conteudo_id) REFERENCES conteudos(id) ON DELETE CASCADE
);

-- Tabela de downloads
CREATE TABLE downloads (
    id INT AUTO_INCREMENT PRIMARY KEY,
    usuario_id INT NOT NULL,
    conteudo_id INT NOT NULL,
    episodio_id INT DEFAULT NULL,
    data_download DATETIME DEFAULT CURRENT_TIMESTAMP,
    expiracao DATETIME DEFAULT NULL,
    FOREIGN KEY (usuario_id) REFERENCES usuarios(id) ON DELETE CASCADE,
    FOREIGN KEY (conteudo_id) REFERENCES conteudos(id) ON DELETE CASCADE,
    FOREIGN KEY (episodio_id) REFERENCES episodios(id) ON DELETE SET NULL
);

-- Tabela de favoritos
CREATE TABLE favoritos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    usuario_id INT NOT NULL,
    conteudo_id INT NOT NULL,
    data_adicao DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (usuario_id) REFERENCES usuarios(id) ON DELETE CASCADE,
    FOREIGN KEY (conteudo_id) REFERENCES conteudos(id) ON DELETE CASCADE
);
