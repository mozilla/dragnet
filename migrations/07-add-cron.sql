DROP INDEX `unique_index` on dll_file;
CREATE UNIQUE INDEX `unique_index_3489dh2` ON dll_file (file_name, debug, debug_filename);