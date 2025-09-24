# Atlas Seed: publications
# Generado: 2025-09-23T22:04:31.825863
# Total filas: 5

plan "seed_publications" {
  migration = <<-SQL
    -- Seeds para tabla publications
    INSERT INTO publications (id, status, created_at, updated_at, user_id, name, publisher_id, release_date, url, summary) VALUES
    ('f615cdea-ced9-4f41-8a87-338fea621d00', 'active', '2024-11-05 03:44:39', NULL, 'c1819969-be87-420f-a7b3-31ad05001182', 'Instalando Docker y Docker-compose en WSL2 Ubuntu sin Naufragar en el Intento', '027fe51d-8797-4c84-8ad8-581192d543a5', '2023-06-04T00:00:00.000Z', 'https://bypablo.medium.com/un-viaje-épico-en-código-instalando-docker-y-docker-compose-en-wsl2-ubuntu-sin-naufragar-en-el-b21f38a9571', '¿Como instalar Docker y Docker-compose en WSL2 sin fallar?'),
    ('82890651-143f-41a0-872c-1c6df535a397', 'active', '2024-11-05 03:44:39', NULL, 'c1819969-be87-420f-a7b3-31ad05001182', 'Explorando ''type'' e ''interface'' en TypeScript: Un Enfoque en el Universo Marvel', '027fe51d-8797-4c84-8ad8-581192d543a5', '2023-05-28T00:00:00.000Z', 'https://bypablo.medium.com/explorando-type-e-interface-en-typescript-un-enfoque-en-el-universo-marvel-4ad47317838e', '¿Cuál es la diferencia entre ''type'' e ''interface'' en TypeScript? ¿Cómo se aplican en el Universo Marvel?'),
    ('b52b1e75-be01-4114-9c35-64f7f8f33d21', 'active', '2024-11-05 03:44:39', NULL, 'c1819969-be87-420f-a7b3-31ad05001182', 'JavaScript vs TypeScript: ¡El choque de titanes que desencadena una guerra de tipos!', '027fe51d-8797-4c84-8ad8-581192d543a5', '2023-05-29T00:00:00.000Z', 'https://bypablo.medium.com/javascript-vs-typescript-el-choque-de-titanes-que-desencadena-una-guerra-de-tipos-dadc70c06766', '¿Cuál es la diferencia entre JavaScript y TypeScript? ¿Cuál es mejor?'),
    ('c5a30fa6-9202-44cb-84a8-801369724cc2', 'active', '2024-11-05 03:44:39', NULL, 'c1819969-be87-420f-a7b3-31ad05001182', '¡Bienvenidos a TypeScript, no más "undefined"!', '027fe51d-8797-4c84-8ad8-581192d543a5', '2023-05-30T00:00:00.000Z', 'https://bypablo.medium.com/bienvenidos-a-typescript-no-más-undefined-5e473f0f4670', '¿Qué es TypeScript? ¿Cómo se usa? ¿Por qué es mejor que JavaScript?'),
    ('a81adc6e-9bd9-4b98-a18f-59b1fdc13132', 'active', '2024-11-05 03:44:39', NULL, 'c1819969-be87-420f-a7b3-31ad05001182', 'Dominando el Mundo de los Tipos en TypeScript', '027fe51d-8797-4c84-8ad8-581192d543a5', '2023-05-31T00:00:00.000Z', 'https://bypablo.medium.com/dominando-el-mundo-de-los-tipos-en-typescript-e543eb42eb9c', '¿Qué son los tipos en TypeScript? ¿Cómo se usan? ¿Por qué son importantes?');
  SQL
}

locals {
  publications_columns = ['id', 'status', 'created_at', 'updated_at', 'user_id', 'name', 'publisher_id', 'release_date', 'url', 'summary']
  publications_row_count = 5
}

# Test básico para validar la tabla
test "schema" "publications_exists" {
  exec {
    sql = "SELECT COUNT(*) FROM information_schema.tables WHERE table_name = 'publications';"
    output = "1"
  }
}
