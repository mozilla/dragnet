ALTER TABLE dll_file DROP INDEX `filename_unqiue`;
CREATE UNIQUE INDEX `unique_index` ON dll_file (file_name, md5_hash, debug);