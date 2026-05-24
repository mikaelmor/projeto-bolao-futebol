USE goalpoint_def;

ALTER TABLE usuarios
  ADD COLUMN foto_perfil_url VARCHAR(255) NULL AFTER senha_hash;
