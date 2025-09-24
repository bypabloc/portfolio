# Atlas Seed: languages
# Generado: 2025-09-23T22:04:31.825705
# Total filas: 2

plan "seed_languages" {
  migration = <<-SQL
    -- Seeds para tabla languages
    INSERT INTO languages (id, status, created_at, updated_at, code_name, name) VALUES
    ('76c7d8cb-d351-469d-bc0a-168cbaf00cf2', 'active', '2024-11-05 03:44:07', NULL, 'es', 'Español'),
    ('749b8353-348a-4750-a8b0-d975a2321790', 'active', '2024-11-05 03:44:07', NULL, 'en', 'English');
  SQL
}

locals {
  languages_columns = ['id', 'status', 'created_at', 'updated_at', 'code_name', 'name']
  languages_row_count = 2
}

# Test básico para validar la tabla
test "schema" "languages_exists" {
  exec {
    sql = "SELECT COUNT(*) FROM information_schema.tables WHERE table_name = 'languages';"
    output = "1"
  }
}
