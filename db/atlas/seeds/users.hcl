# Atlas Seed: users
# Generado: 2025-09-23T22:04:31.825123
# Total filas: 1

plan "seed_users" {
  migration = <<-SQL
    -- Seeds para tabla users
    INSERT INTO users (id, status, created_at, updated_at, username) VALUES
    ('c1819969-be87-420f-a7b3-31ad05001182', 'active', '2024-11-05 03:44:03', NULL, 'bypabloc');
  SQL
}

locals {
  users_columns = ['id', 'status', 'created_at', 'updated_at', 'username']
  users_row_count = 1
}

# Test básico para validar la tabla
test "schema" "users_exists" {
  exec {
    sql = "SELECT COUNT(*) FROM information_schema.tables WHERE table_name = 'users';"
    output = "1"
  }
}
