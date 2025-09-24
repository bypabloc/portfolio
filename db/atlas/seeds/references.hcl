# Atlas Seed: references
# Generado: 2025-09-23T22:04:31.825907
# Total filas: 10

plan "seed_references" {
  migration = <<-SQL
    -- Seeds para tabla references
    INSERT INTO references (id, status, created_at, updated_at, user_id, code_name, name, reference, position, url, employer_id, scrapping_recommendation) VALUES
    ('137e0f5e-e685-4697-aa0d-504caf4b3112', 'active', '2024-11-05 03:44:47', NULL, 'c1819969-be87-420f-a7b3-31ad05001182', 'alan-vergara-bravo', 'Alan Vergara Bravo', 'Compañero de equipo', 'software Architect Developer', 'https://www.linkedin.com/in/alan-vergara-bravo-b17164145', '9ea9b2cc-bda6-4520-98de-a92e04bc0303', '{"linkedin":"https://www.linkedin.com/in/bypabloc/details/recommendations","elementId":"profilePagedListComponent-ACoAACeoGgsB5cPxfqr-T2ylRvqy6qRWe6TgZfc-RECOMMENDATIONS-VIEW-DETAILS-profileTabSection-RECEIVED-RECOMMENDATIONS-NONE-es-ES-0"}'),
    ('d6605b2e-2757-4c9f-827d-9ad62d0cfa46', 'active', '2024-11-05 03:44:47', NULL, 'c1819969-be87-420f-a7b3-31ad05001182', 'alejandra-medina-briceno', 'Alejandra Medina Briceño', 'Compañero de equipo', 'Diseñadora UX/UI', 'https://www.linkedin.com/in/alejandra-medinab', '9ea9b2cc-bda6-4520-98de-a92e04bc0303', '{"linkedin":"https://www.linkedin.com/in/bypabloc/details/recommendations","elementId":"profilePagedListComponent-ACoAACeoGgsB5cPxfqr-T2ylRvqy6qRWe6TgZfc-RECOMMENDATIONS-VIEW-DETAILS-profileTabSection-RECEIVED-RECOMMENDATIONS-NONE-es-ES-1"}'),
    ('921f39df-7748-4e1d-ba6e-6a5b9ef5df92', 'active', '2024-11-05 03:44:47', NULL, 'c1819969-be87-420f-a7b3-31ad05001182', 'baldomero-aguila', 'Baldomero Águila', 'Compañero de equipo', 'Desarrollador Mobile', 'https://www.linkedin.com/in/baldomero', '9ea9b2cc-bda6-4520-98de-a92e04bc0303', NULL),
    ('568fe395-8f2c-48dd-95a2-acdb59342201', 'active', '2024-11-05 03:44:47', NULL, 'c1819969-be87-420f-a7b3-31ad05001182', 'cristian-fuentes', 'Cristian Fuentes', 'Compañero de equipo', 'Desarrollador Full Stack', 'https://www.linkedin.com/in/csfuente', '9ea9b2cc-bda6-4520-98de-a92e04bc0303', NULL),
    ('6c118060-1428-46f8-bbd1-38781e751ab5', 'active', '2024-11-05 03:44:47', NULL, 'c1819969-be87-420f-a7b3-31ad05001182', 'helis-montes', 'Helis Montes', 'Compañero de equipo', 'Desarrollador Full Stack', 'https://www.linkedin.com/in/helis-montes', '9ea9b2cc-bda6-4520-98de-a92e04bc0303', NULL),
    ('c1bda514-105d-486a-bf0d-848f898ab4f4', 'active', '2024-11-05 03:44:47', NULL, 'c1819969-be87-420f-a7b3-31ad05001182', 'edder-ramirez', 'Edder Ramírez', 'Compañero de equipo', 'Desarrollador Full Stack', 'https://www.linkedin.com/in/edderleonardo', '9ea9b2cc-bda6-4520-98de-a92e04bc0303', NULL),
    ('746f8964-0ebb-451f-8c23-5f6c35eaa7ab', 'active', '2024-11-05 03:44:47', NULL, 'c1819969-be87-420f-a7b3-31ad05001182', 'jose-namoc', 'José Namoc', 'Compañero de equipo', 'Desarrollador Full Stack', 'https://www.linkedin.com/in/jose-namoc-lopez', '4cb15527-1282-4a55-9041-e5deb08b884f', '{"linkedin":"https://www.linkedin.com/in/bypabloc/details/recommendations","elementId":"profilePagedListComponent-ACoAACeoGgsB5cPxfqr-T2ylRvqy6qRWe6TgZfc-RECOMMENDATIONS-VIEW-DETAILS-profileTabSection-RECEIVED-RECOMMENDATIONS-NONE-es-ES-6"}'),
    ('32053574-de59-4ebf-b117-446cc2faeddd', 'active', '2024-11-05 03:44:47', NULL, 'c1819969-be87-420f-a7b3-31ad05001182', 'jacnelly-colmenarez', 'Jacnelly Colmenarez', 'Compañera de equipo', 'UI/UX Designer', 'https://www.linkedin.com/in/jacnelly-colmenarez', '4cb15527-1282-4a55-9041-e5deb08b884f', '{"linkedin":"https://www.linkedin.com/in/bypabloc/details/recommendations","elementId":"profilePagedListComponent-ACoAACeoGgsB5cPxfqr-T2ylRvqy6qRWe6TgZfc-RECOMMENDATIONS-VIEW-DETAILS-profileTabSection-RECEIVED-RECOMMENDATIONS-NONE-es-ES-3"}'),
    ('d041095e-d488-41ce-a0fe-91278fb2eb52', 'active', '2024-11-05 03:44:47', NULL, 'c1819969-be87-420f-a7b3-31ad05001182', 'felipe-rivera', 'Felipe Rivera', 'Trabajé en la misma empresa', 'Talent Acquisition Lead', 'https://www.linkedin.com/in/frtavonatti', NULL, NULL),
    ('ed95d240-dea3-4bb6-b2a7-cf6c0d927f9b', 'active', '2024-11-05 03:44:47', NULL, 'c1819969-be87-420f-a7b3-31ad05001182', 'samuel-esponiza', 'Samuel Esponiza', 'Estudié en la misma universidad y trabajé en proyectos juntos', 'Desarrollador Full Stack', 'https://www.linkedin.com/in/samuelespinozac', NULL, '{"linkedin":"https://www.linkedin.com/in/bypabloc/details/recommendations","elementId":"profilePagedListComponent-ACoAACeoGgsB5cPxfqr-T2ylRvqy6qRWe6TgZfc-RECOMMENDATIONS-VIEW-DETAILS-profileTabSection-RECEIVED-RECOMMENDATIONS-NONE-es-ES-4"}');
  SQL
}

locals {
  references_columns = ['id', 'status', 'created_at', 'updated_at', 'user_id', 'code_name', 'name', 'reference', 'position', 'url', 'employer_id', 'scrapping_recommendation']
  references_row_count = 10
}

# Test básico para validar la tabla
test "schema" "references_exists" {
  exec {
    sql = "SELECT COUNT(*) FROM information_schema.tables WHERE table_name = 'references';"
    output = "1"
  }
}
