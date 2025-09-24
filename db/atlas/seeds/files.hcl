# Atlas Seed: files
# Generado: 2025-09-23T22:04:31.825373
# Total filas: 8

plan "seed_files" {
  migration = <<-SQL
    -- Seeds para tabla files
    INSERT INTO files (id, status, created_at, updated_at, group_file_id, user_id, file_type_id, url, priority, description) VALUES
    ('829a2e2b-314c-40f6-aa03-da5bbf7eb4b2', 'active', '2024-11-05 03:44:53', NULL, '353f9e58-fdda-477f-964e-f5366507ec55', 'c1819969-be87-420f-a7b3-31ad05001182', 'dbebdff9-7edc-40dc-a149-d9ec4e3264f6', 'https://images-bypabloc.s3.sa-east-1.amazonaws.com/cv/2.avif', 2, NULL),
    ('5c9aac46-060b-4ef7-9d20-41d81d229e56', 'active', '2024-11-05 03:44:53', NULL, '353f9e58-fdda-477f-964e-f5366507ec55', 'c1819969-be87-420f-a7b3-31ad05001182', '89ec8bd0-469a-4086-a241-3bfbdd0cfede', 'https://images-bypabloc.s3.sa-east-1.amazonaws.com/cv/2.webp', 2, NULL),
    ('824230e5-91ae-4c1b-b87a-c3909b1ec67a', 'active', '2024-11-05 03:44:53', NULL, '353f9e58-fdda-477f-964e-f5366507ec55', 'c1819969-be87-420f-a7b3-31ad05001182', '863a16a1-8200-4cdd-9232-09879b8f576a', 'https://images-bypabloc.s3.sa-east-1.amazonaws.com/cv/2.jp2', 2, NULL),
    ('b78c4370-23b5-43ed-808c-4b4f8c090a70', 'active', '2024-11-05 03:44:53', NULL, '353f9e58-fdda-477f-964e-f5366507ec55', 'c1819969-be87-420f-a7b3-31ad05001182', 'c49f036a-d892-45d1-8acc-d607e8187fd2', 'https://images-bypabloc.s3.sa-east-1.amazonaws.com/cv/2.jpg', 2, NULL),
    ('46f64307-dbd2-43ed-b390-c1871eafd2bf', 'active', '2024-11-05 03:44:53', NULL, '353f9e58-fdda-477f-964e-f5366507ec55', 'c1819969-be87-420f-a7b3-31ad05001182', 'dbebdff9-7edc-40dc-a149-d9ec4e3264f6', 'https://images-bypabloc.s3.sa-east-1.amazonaws.com/cv/1.avif', 1, NULL),
    ('07455989-4aab-404b-89d8-748e23287f9c', 'active', '2024-11-05 03:44:53', NULL, '353f9e58-fdda-477f-964e-f5366507ec55', 'c1819969-be87-420f-a7b3-31ad05001182', '89ec8bd0-469a-4086-a241-3bfbdd0cfede', 'https://images-bypabloc.s3.sa-east-1.amazonaws.com/cv/1.webp', 1, NULL),
    ('7ea01a63-6476-4cb2-8a0e-3f8a22c13888', 'active', '2024-11-05 03:44:53', NULL, '353f9e58-fdda-477f-964e-f5366507ec55', 'c1819969-be87-420f-a7b3-31ad05001182', '863a16a1-8200-4cdd-9232-09879b8f576a', 'https://images-bypabloc.s3.sa-east-1.amazonaws.com/cv/1.jp2', 1, NULL),
    ('63a301f3-2303-46cc-b414-4c0a800d23fb', 'active', '2024-11-05 03:44:53', NULL, '353f9e58-fdda-477f-964e-f5366507ec55', 'c1819969-be87-420f-a7b3-31ad05001182', 'c49f036a-d892-45d1-8acc-d607e8187fd2', 'https://images-bypabloc.s3.sa-east-1.amazonaws.com/cv/1.jpg', 1, NULL);
  SQL
}

locals {
  files_columns = ['id', 'status', 'created_at', 'updated_at', 'group_file_id', 'user_id', 'file_type_id', 'url', 'priority', 'description']
  files_row_count = 8
}

# Test básico para validar la tabla
test "schema" "files_exists" {
  exec {
    sql = "SELECT COUNT(*) FROM information_schema.tables WHERE table_name = 'files';"
    output = "1"
  }
}
