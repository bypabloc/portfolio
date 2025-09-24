# Atlas Seed: awards
# Generado: 2025-09-23T22:04:31.825326
# Total filas: 2

plan "seed_awards" {
  migration = <<-SQL
    -- Seeds para tabla awards
    INSERT INTO awards (id, status, created_at, updated_at, user_id, code_name, title, date, awarder, summary, url) VALUES
    ('f228fef2-e1c6-43cf-9641-0530406a30e4', 'active', '2024-11-05 03:44:31', NULL, 'c1819969-be87-420f-a7b3-31ad05001182', 'innovator-destacame-2023', 'Premio a Innovador del año 2023 en Destacame', '2024-01-24T00:00:00.000Z', 'Destacame', 'Por liderar la implementación de soluciones tecnológicas innovadoras en la empresa, mejorando significativamente la eficiencia operativa y la experiencia del usuario.', 'https://heyzine.com/flip-book/cdc911b3d1.html'),
    ('08af3e9c-7a58-4ecb-afd9-9a5fb90f985d', 'active', '2024-11-05 03:44:31', NULL, 'c1819969-be87-420f-a7b3-31ad05001182', 'triple-alianza-lima-2020', 'Desafío Triple Alianza Lima', '2020-11-18T00:00:00.000Z', 'Incubagraria, 1551, StartUpUni', 'Por haber obtenido el 1er lugar en el sector Comercio del "Desafío Triple Alianza COVID-19", esto sucedió en mi experiencia en DIBAL.', 'https://1drv.ms/b/s!AoZaJmtucTrahbFAsRnMKiJDAxBlKg?e=9MKGjP');
  SQL
}

locals {
  awards_columns = ['id', 'status', 'created_at', 'updated_at', 'user_id', 'code_name', 'title', 'date', 'awarder', 'summary', 'url']
  awards_row_count = 2
}

# Test básico para validar la tabla
test "schema" "awards_exists" {
  exec {
    sql = "SELECT COUNT(*) FROM information_schema.tables WHERE table_name = 'awards';"
    output = "1"
  }
}
