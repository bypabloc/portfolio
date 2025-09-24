# Atlas Seed: publishers
# Generado: 2025-09-23T22:04:31.825890
# Total filas: 1

plan "seed_publishers" {
  migration = <<-SQL
    -- Seeds para tabla publishers
    INSERT INTO publishers (id, status, created_at, updated_at, code_name, name, url) VALUES
    ('027fe51d-8797-4c84-8ad8-581192d543a5', 'active', '2024-11-05 03:44:06', NULL, 'medium', 'Medium', 'https://medium.com');
  SQL
}

locals {
  publishers_columns = ['id', 'status', 'created_at', 'updated_at', 'code_name', 'name', 'url']
  publishers_row_count = 1
}

# Test básico para validar la tabla
test "schema" "publishers_exists" {
  exec {
    sql = "SELECT COUNT(*) FROM information_schema.tables WHERE table_name = 'publishers';"
    output = "1"
  }
}
