# Atlas Seed: employers
# Generado: 2025-09-23T22:04:31.825500
# Total filas: 8

plan "seed_employers" {
  migration = <<-SQL
    -- Seeds para tabla employers
    INSERT INTO employers (id, status, created_at, updated_at, user_id, code_name, name, url, description, service_status) VALUES
    ('9ea9b2cc-bda6-4520-98de-a92e04bc0303', 'active', '2024-11-05 03:44:09', NULL, NULL, 'destacame', 'Destacame', 'https://destacame.cl', NULL, 'active'),
    ('20d1b17a-d133-4d38-838e-fcdcee5d6104', 'active', '2024-11-05 03:44:09', NULL, NULL, 'appinteli', 'AppInteli', 'https://appinteli.com', NULL, 'active'),
    ('1b68d3c9-e824-43c2-8330-6345947be509', 'active', '2024-11-05 03:44:09', NULL, NULL, 'goodmeal', 'GoodMeal', 'https://www.goodmeal.app', NULL, 'active'),
    ('4cb15527-1282-4a55-9041-e5deb08b884f', 'active', '2024-11-05 03:44:09', NULL, NULL, 'dibal', 'Dibal', 'https://dibal.pe', NULL, 'active'),
    ('70699519-1109-452c-a800-70b15ff77966', 'active', '2024-11-05 03:44:09', NULL, NULL, 'cofasa', 'Laboratorio Cofasa S.A.', 'https://laboratoriocofasa.com', NULL, 'active'),
    ('9c682bdf-49b6-4a06-afe0-e6de4f0a3176', 'active', '2024-11-05 03:44:09', NULL, NULL, 'iai', 'Instituto Autónomo de Infraestructura (IAI)', NULL, NULL, 'active'),
    ('33a56145-b99d-419c-a4f6-30a023730833', 'active', '2024-11-05 03:44:09', NULL, NULL, 'ipasme', 'Ministerio de Educación ''IPASME''', NULL, NULL, 'active'),
    ('30cb5f72-e464-47d3-8423-94e48d82e60d', 'active', '2024-11-05 03:44:09', NULL, NULL, 'corpoelec', 'CORPOELEC', NULL, NULL, 'active');
  SQL
}

locals {
  employers_columns = ['id', 'status', 'created_at', 'updated_at', 'user_id', 'code_name', 'name', 'url', 'description', 'service_status']
  employers_row_count = 8
}

# Test básico para validar la tabla
test "schema" "employers_exists" {
  exec {
    sql = "SELECT COUNT(*) FROM information_schema.tables WHERE table_name = 'employers';"
    output = "1"
  }
}
