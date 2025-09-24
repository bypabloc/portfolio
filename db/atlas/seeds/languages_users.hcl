# Atlas Seed: languages_users
# Generado: 2025-09-23T22:04:31.825725
# Total filas: 2

plan "seed_languages_users" {
  migration = <<-SQL
    -- Seeds para tabla languages_users
    INSERT INTO languages_users (id, status, created_at, updated_at, user_id, language_id, code_name, fluency) VALUES
    ('f1bf6202-f0e6-4704-8997-149f8ecb3ccd', 'active', '2024-11-05 03:44:41', NULL, 'c1819969-be87-420f-a7b3-31ad05001182', '76c7d8cb-d351-469d-bc0a-168cbaf00cf2', 'es-bypabloc', 'Nativo'),
    ('5c8e9fe5-e696-4c3a-97c0-d09a42924617', 'active', '2024-11-05 03:44:41', NULL, 'c1819969-be87-420f-a7b3-31ad05001182', '749b8353-348a-4750-a8b0-d975a2321790', 'en-bypabloc', 'Intermedio en lectura y básico en escritura y habla');
  SQL
}

locals {
  languages_users_columns = ['id', 'status', 'created_at', 'updated_at', 'user_id', 'language_id', 'code_name', 'fluency']
  languages_users_row_count = 2
}

# Test básico para validar la tabla
test "schema" "languages_users_exists" {
  exec {
    sql = "SELECT COUNT(*) FROM information_schema.tables WHERE table_name = 'languages_users';"
    output = "1"
  }
}
