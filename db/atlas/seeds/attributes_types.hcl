# Atlas Seed: attributes_types
# Generado: 2025-09-23T22:04:31.825296
# Total filas: 8

plan "seed_attributes_types" {
  migration = <<-SQL
    -- Seeds para tabla attributes_types
    INSERT INTO attributes_types (id, status, created_at, updated_at, code_name, name, type) VALUES
    ('240f7dc8-87dc-4269-93cd-cbce82a3523d', 'active', '2024-11-05 03:44:13', NULL, 'email', 'Email', 'text'),
    ('c4c0c925-4938-40c1-8a21-148526640e8b', 'active', '2024-11-05 03:44:13', NULL, 'phone', 'Phone', 'text'),
    ('5723e027-d840-4be5-86ea-567a098f3765', 'active', '2024-11-05 03:44:13', NULL, 'url', 'URL', 'text'),
    ('36c0037d-e498-4a5e-8af3-46d2c55e3082', 'active', '2024-11-05 03:44:13', NULL, 'label', 'Label', 'text'),
    ('ed55d1cb-09c3-4071-b7b9-7ce6dd16dfae', 'active', '2024-11-05 03:44:13', NULL, 'names', 'Names', 'text'),
    ('585d0fef-55b3-4ea3-918a-d413155760a5', 'active', '2024-11-05 03:44:13', NULL, 'lastName', 'Last Name', 'text'),
    ('fb988a8f-6c2e-4d05-bc98-9a1c2419aa73', 'active', '2024-11-05 03:44:13', NULL, 'summary', 'Summary', 'text'),
    ('06a06f52-9a76-4330-967a-58f3e1c1cd2f', 'active', '2024-11-05 03:44:13', NULL, 'location', 'Location', 'object');
  SQL
}

locals {
  attributes_types_columns = ['id', 'status', 'created_at', 'updated_at', 'code_name', 'name', 'type']
  attributes_types_row_count = 8
}

# Test básico para validar la tabla
test "schema" "attributes_types_exists" {
  exec {
    sql = "SELECT COUNT(*) FROM information_schema.tables WHERE table_name = 'attributes_types';"
    output = "1"
  }
}
