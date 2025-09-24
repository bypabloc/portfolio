# Atlas Seed: type_files
# Generado: 2025-09-23T22:04:31.825476
# Total filas: 4

plan "seed_type_files" {
  migration = <<-SQL
    -- Seeds para tabla type_files
    INSERT INTO type_files (id, status, created_at, updated_at, code_name, name, extension, mime, tag, priority) VALUES
    ('dbebdff9-7edc-40dc-a149-d9ec4e3264f6', 'active', '2024-11-05 03:44:04', NULL, 'avif', 'AVIF', 'avif', 'image/avif', 'source', 100),
    ('89ec8bd0-469a-4086-a241-3bfbdd0cfede', 'active', '2024-11-05 03:44:04', NULL, 'webp', 'WebP', 'webp', 'image/webp', 'source', 70),
    ('863a16a1-8200-4cdd-9232-09879b8f576a', 'active', '2024-11-05 03:44:04', NULL, 'jp2', 'JPEG2000', 'jp2', 'image/jpeg2000', 'source', 50),
    ('c49f036a-d892-45d1-8acc-d607e8187fd2', 'active', '2024-11-05 03:44:04', NULL, 'jpeg', 'JPEG', 'jpg', 'image/jpeg', 'img', 20);
  SQL
}

locals {
  type_files_columns = ['id', 'status', 'created_at', 'updated_at', 'code_name', 'name', 'extension', 'mime', 'tag', 'priority']
  type_files_row_count = 4
}

# Test básico para validar la tabla
test "schema" "type_files_exists" {
  exec {
    sql = "SELECT COUNT(*) FROM information_schema.tables WHERE table_name = 'type_files';"
    output = "1"
  }
}
