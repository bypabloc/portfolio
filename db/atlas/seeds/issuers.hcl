# Atlas Seed: issuers
# Generado: 2025-09-23T22:04:31.825584
# Total filas: 2

plan "seed_issuers" {
  migration = <<-SQL
    -- Seeds para tabla issuers
    INSERT INTO issuers (id, status, created_at, updated_at, code_name, name, url) VALUES
    ('32e79762-e98f-43b3-b660-31ae9ebc33f4', 'active', '2024-11-05 03:44:06', NULL, 'udemy', 'Udemy', 'https://udemy.com'),
    ('a5ac58e4-2ec7-44b3-a3bb-1f0c2df0611e', 'active', '2024-11-05 03:44:06', NULL, 'devtalles', 'DevTalles', 'https://cursos.devtalles.com');
  SQL
}

locals {
  issuers_columns = ['id', 'status', 'created_at', 'updated_at', 'code_name', 'name', 'url']
  issuers_row_count = 2
}

# Test básico para validar la tabla
test "schema" "issuers_exists" {
  exec {
    sql = "SELECT COUNT(*) FROM information_schema.tables WHERE table_name = 'issuers';"
    output = "1"
  }
}
