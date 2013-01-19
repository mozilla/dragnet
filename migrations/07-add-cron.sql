DROP INDEX `unique_index` on dll_file;
CREATE UNIQUE INDEX `unique_index` ON dll_file (file_name, debug, debug_filename);
INSERT INTO `auth_user` (username, first_name, is_staff, is_active, is_superuser, last_login, date_joined) VALUES ('system', 'System', 0, 0, 0, NOW(), NOW());