# Atlas Seed: project_url_types
# Generado: 2025-09-23T22:04:31.825841
# Total filas: 2

plan "seed_project_url_types" {
  migration = <<-SQL
    -- Seeds para tabla project_url_types
    INSERT INTO project_url_types (id, status, created_at, updated_at, code_name, name, icons) VALUES
    ('1b44fc21-afc2-4dbc-98c9-47f58a21c236', 'active', '2024-11-05 03:51:08', NULL, 'github', 'GitHub', '{"default":"i-ant-design-github-outlined","dark":"i-ant-design-github-filled"}'),
    ('167cab5e-56e8-4275-a48b-4d47dc5a3f38', 'active', '2024-11-05 03:51:08', NULL, 'website', 'Website', '{"default":"i-clarity-world-line","dark":"i-clarity-world-solid"}');
  SQL
}

locals {
  project_url_types_columns = ['id', 'status', 'created_at', 'updated_at', 'code_name', 'name', 'icons']
  project_url_types_row_count = 2
}

# Test básico para validar la tabla
test "schema" "project_url_types_exists" {
  exec {
    sql = "SELECT COUNT(*) FROM information_schema.tables WHERE table_name = 'project_url_types';"
    output = "1"
  }
}
