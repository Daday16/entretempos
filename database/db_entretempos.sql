CREATE DATABASE IF NOT EXISTS db_pi_entretempos;
USE db_pi_entretempos;


-- Cria a tabela responsável pelos usuários.
CREATE TABLE `usuarios` (
  `id_usuario` int NOT NULL AUTO_INCREMENT,
  `nome_usuario` varchar(100) NOT NULL,
  `email` varchar(100) NOT NULL,
  `senha` varchar(255) NOT NULL,
  `data_nascimento` date NOT NULL,
  `data_cadastro` datetime DEFAULT CURRENT_TIMESTAMP,
  `moedas` int NOT NULL DEFAULT '0',
  PRIMARY KEY (`id_usuario`),
  UNIQUE KEY `email` (`email`)
) ENGINE=InnoDB AUTO_INCREMENT=13 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;


-- Cria a tabela responsável pelos grupos.
CREATE TABLE `grupos` (
  `id_grupo` int NOT NULL AUTO_INCREMENT,
  `titulo` varchar(100) NOT NULL,
  `fk_usuario` int DEFAULT NULL,
  PRIMARY KEY (`id_grupo`),
  KEY `fk_grupo_usuario` (`fk_usuario`),
  CONSTRAINT `fk_grupo_usuario`
    FOREIGN KEY (`fk_usuario`)
    REFERENCES `usuarios` (`id_usuario`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;


-- Cria a tabela responsável pelos perfis dos usuários.
CREATE TABLE `perfis` (
  `id_perfil` int NOT NULL AUTO_INCREMENT,
  `fk_usuario` int NOT NULL,
  `objetivo` varchar(255) NOT NULL,
  `nivel_programacao` varchar(100) NOT NULL,
  `tempo_diario` int NOT NULL,
  `dias_disponiveis` varchar(255) NOT NULL,
  `dificuldade_foco` varchar(255) NOT NULL,
  PRIMARY KEY (`id_perfil`),
  KEY `fk_usuario` (`fk_usuario`),
  CONSTRAINT `perfis_ibfk_1`
    FOREIGN KEY (`fk_usuario`)
    REFERENCES `usuarios` (`id_usuario`)
) ENGINE=InnoDB AUTO_INCREMENT=12 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;


-- Cria a tabela responsável pelos Pomodoros.
CREATE TABLE `pomodoros` (
  `id_pomodoro` int NOT NULL AUTO_INCREMENT,
  `duracao` int NOT NULL,
  `dthr_inicio` datetime NOT NULL,
  `dthr_termino` datetime DEFAULT NULL,
  `fk_usuario` int NOT NULL,
  PRIMARY KEY (`id_pomodoro`),
  KEY `fk_pomodoro_usuario` (`fk_usuario`),
  CONSTRAINT `fk_pomodoro_usuario`
    FOREIGN KEY (`fk_usuario`)
    REFERENCES `usuarios` (`id_usuario`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;


-- Cria a tabela responsável pela recuperação de senha.
CREATE TABLE `recuperacao_senha` (
  `id_recuperacao` int NOT NULL AUTO_INCREMENT,
  `fk_usuario` int NOT NULL,
  `codigo` varchar(10) NOT NULL,
  `expira_em` datetime NOT NULL,
  `usado` tinyint(1) NOT NULL DEFAULT '0',
  PRIMARY KEY (`id_recuperacao`),
  KEY `fk_usuario` (`fk_usuario`),
  CONSTRAINT `recuperacao_senha_ibfk_1`
    FOREIGN KEY (`fk_usuario`)
    REFERENCES `usuarios` (`id_usuario`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;


-- Cria a tabela responsável pelas tarefas.
CREATE TABLE `tarefas` (
  `id_tarefa` int NOT NULL AUTO_INCREMENT,
  `titulo` varchar(100) NOT NULL,
  `descricao` text,
  `dthr_prazo` datetime DEFAULT NULL,
  `frequencia` int DEFAULT '0',
  `despertar` tinyint(1) DEFAULT '0',
  `status` varchar(20) NOT NULL DEFAULT 'PENDENTE',
  `fk_grupo` int DEFAULT NULL,
  PRIMARY KEY (`id_tarefa`),
  KEY `fk_grupo` (`fk_grupo`),
  CONSTRAINT `tarefas_ibfk_1`
    FOREIGN KEY (`fk_grupo`)
    REFERENCES `grupos` (`id_grupo`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;


-- Cria a tabela de relacionamento entre usuários e tarefas.
CREATE TABLE `usuario_rel_tarefas` (
  `fk_rel_usuario` int NOT NULL,
  `fk_rel_tarefas` int NOT NULL,
  PRIMARY KEY (`fk_rel_usuario`,`fk_rel_tarefas`),
  KEY `fk_rel_tarefas` (`fk_rel_tarefas`),
  CONSTRAINT `usuario_rel_tarefas_ibfk_1`
    FOREIGN KEY (`fk_rel_usuario`)
    REFERENCES `usuarios` (`id_usuario`),
  CONSTRAINT `usuario_rel_tarefas_ibfk_2`
    FOREIGN KEY (`fk_rel_tarefas`)
    REFERENCES `tarefas` (`id_tarefa`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;


-- Cria a tabela responsável por armazenar as trilhas de estudos.
CREATE TABLE `trilhas` (
  `id_trilha` int NOT NULL AUTO_INCREMENT,
  `fk_usuario` int NOT NULL,
  `titulo` varchar(255) NOT NULL,
  `descricao` text,
  PRIMARY KEY (`id_trilha`),
  KEY `fk_trilha_usuario` (`fk_usuario`),
  CONSTRAINT `fk_trilha_usuario`
    FOREIGN KEY (`fk_usuario`)
    REFERENCES `usuarios` (`id_usuario`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;


-- Cria a tabela responsável por armazenar as etapas de cada trilha.
CREATE TABLE `etapas_trilha` (
  `id_etapa` int NOT NULL AUTO_INCREMENT,
  `fk_trilha` int NOT NULL,
  `titulo` varchar(255) NOT NULL,
  `descricao` text,
  `ordem` int NOT NULL,
  PRIMARY KEY (`id_etapa`),
  KEY `fk_etapa_trilha` (`fk_trilha`),
  CONSTRAINT `fk_etapa_trilha`
    FOREIGN KEY (`fk_trilha`)
    REFERENCES `trilhas` (`id_trilha`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Cria a tabela responsável por armazenar os assuntos de cada etapa.
CREATE TABLE `assuntos_trilha` (
  `id_assunto` int NOT NULL AUTO_INCREMENT,
  `fk_etapa` int NOT NULL,
  `assunto` varchar(255) NOT NULL,
  `ordem` int NOT NULL,
  PRIMARY KEY (`id_assunto`),
  KEY `fk_assunto_etapa` (`fk_etapa`),
  CONSTRAINT `fk_assunto_etapa`
    FOREIGN KEY (`fk_etapa`)
    REFERENCES `etapas_trilha` (`id_etapa`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;