-- cria e seleciona o banco de dados
CREATE DATABASE IF NOT EXISTS oficina_mecanica;
USE oficina_mecanica;

-- tabela de clientes
CREATE TABLE clientes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(150) NOT NULL,
    telefone VARCHAR(20) NOT NULL,
    CONSTRAINT uq_clientes_nome_telefone UNIQUE (nome, telefone)
);

-- tabela de mecânicos
CREATE TABLE mecanicos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(150) NOT NULL,
    nivel VARCHAR(50) NOT NULL
);

-- tabela de tipos de serviço
CREATE TABLE tipos_servico (
    id INT AUTO_INCREMENT PRIMARY KEY,
    descricao VARCHAR(100) NOT NULL
);

-- tabela de ordens de serviço
CREATE TABLE ordens_servico (
    id INT AUTO_INCREMENT PRIMARY KEY,
    cliente_id INT NOT NULL,
    tipo_servico_id INT NOT NULL,
    mecanico_id INT,
    descricao TEXT NOT NULL,
    modelo_veiculo VARCHAR(100) NOT NULL,
    status VARCHAR(50) DEFAULT 'aberta',
    prioridade VARCHAR(50),
    num_ordem INT,
    data_criacao DATETIME DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_os_cliente
        FOREIGN KEY (cliente_id)
        REFERENCES clientes(id),
    CONSTRAINT fk_os_tipo_servico
        FOREIGN KEY (tipo_servico_id)
        REFERENCES tipos_servico(id),
    CONSTRAINT fk_os_mecanico
        FOREIGN KEY (mecanico_id)
        REFERENCES mecanicos(id)
);

-- tabela de histórico
CREATE TABLE historico (
    id INT AUTO_INCREMENT PRIMARY KEY,
    ordem_id INT NOT NULL,
    mecanico_id INT NOT NULL,
    solucao_aplicada TEXT,
    data_finalizacao DATETIME DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_historico_ordem
        FOREIGN KEY (ordem_id)
        REFERENCES ordens_servico(id),
    CONSTRAINT fk_historico_mecanico
        FOREIGN KEY (mecanico_id)
        REFERENCES mecanicos(id)
);

-- mecânicos cadastrados por nível
INSERT INTO mecanicos (nome, nivel) VALUES
('Antonio Vieira',    'mecanico chefe'),
('Renato Barbosa',    'mecanico chefe'),
('Eduardo Teixeira',  'mecanico'),
('Vinicius Moraes',   'mecanico'),
('Diego Carvalho',    'mecanico'),
('Anderson Reis',     'auxiliar de mecanico'),
('Leandro Pinto',     'auxiliar de mecanico'),
('Cristiano Nunes',   'auxiliar de mecanico'),
('William Mendes',    'estagiario'),
('Samuel Rocha',      'estagiario');

-- tipos de serviço disponíveis
INSERT INTO tipos_servico (descricao) VALUES
('Troca de óleo'),
('Revisão de freios'),
('Revisão geral'),
('Serviço elétrico'),
('Serviço de motor'),
('Suspensão e direção'),
('Ar-condicionado'),
('Alinhamento e balanceamento'),
('Troca de pneus'),
('Diagnóstico eletrônico');
