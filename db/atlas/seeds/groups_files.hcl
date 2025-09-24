# Atlas Seed: groups_files
# Generado: 2025-09-23T22:04:31.825354
# Total filas: 2

plan "seed_groups_files" {
  migration = <<-SQL
    -- Seeds para tabla groups_files
    INSERT INTO groups_files (id, status, created_at, updated_at, code_name, name, description, priority) VALUES
    ('353f9e58-fdda-477f-964e-f5366507ec55', 'active', '2024-11-05 03:44:10', NULL, 'profile', 'Profile', NULL, NULL),
    ('d4d22614-12fb-434f-b771-214cb2238f7b', 'active', '2024-11-05 03:44:10', NULL, 'projects', 'Projects', NULL, NULL);
  SQL
}

locals {
  groups_files_columns = ['id', 'status', 'created_at', 'updated_at', 'code_name', 'name', 'description', 'priority']
  groups_files_row_count = 2
}

# Test básico para validar la tabla
test "schema" "groups_files_exists" {
  exec {
    sql = "SELECT COUNT(*) FROM information_schema.tables WHERE table_name = 'groups_files';"
    output = "1"
  }
}
