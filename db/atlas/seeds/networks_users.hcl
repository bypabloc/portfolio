# Atlas Seed: networks_users
# Generado: 2025-09-23T22:04:31.825768
# Total filas: 5

plan "seed_networks_users" {
  migration = <<-SQL
    -- Seeds para tabla networks_users
    INSERT INTO networks_users (id, status, created_at, updated_at, network_id, user_id, contact_info, url) VALUES
    ('072b41cd-5df3-460e-808d-39fbce746948', 'active', '2024-11-05 03:44:21', NULL, '9c3b5049-aba3-48b3-b858-0a372f9af9cf', 'c1819969-be87-420f-a7b3-31ad05001182', 51918490148, NULL),
    ('d3b1cd56-1cfb-4563-9cca-9cdd91b10244', 'active', '2024-11-05 03:44:21', NULL, '253010e7-1b55-409a-bd52-6c4efd112692', 'c1819969-be87-420f-a7b3-31ad05001182', 51918490148, NULL),
    ('f7f77955-f73b-4893-9031-8bef04d8df98', 'active', '2024-11-05 03:44:21', NULL, '21f0ebb7-5fe0-4382-8129-5e8a82ccbbaf', 'c1819969-be87-420f-a7b3-31ad05001182', 'pacg1991@gmail.com', NULL),
    ('0ba0c0b2-326c-4878-9229-95a154814c41', 'active', '2024-11-05 03:44:21', NULL, '43e96f18-dca5-474e-9bf9-5db43e73400d', 'c1819969-be87-420f-a7b3-31ad05001182', 'bypabloc', NULL),
    ('8d1e1835-c3b7-481d-9685-53941f839c3b', 'active', '2024-11-05 03:44:21', NULL, '915a7d0f-236f-4ba7-9741-15111cfb0c6c', 'c1819969-be87-420f-a7b3-31ad05001182', 'bypabloc', NULL);
  SQL
}

locals {
  networks_users_columns = ['id', 'status', 'created_at', 'updated_at', 'network_id', 'user_id', 'contact_info', 'url']
  networks_users_row_count = 5
}

# Test básico para validar la tabla
test "schema" "networks_users_exists" {
  exec {
    sql = "SELECT COUNT(*) FROM information_schema.tables WHERE table_name = 'networks_users';"
    output = "1"
  }
}
