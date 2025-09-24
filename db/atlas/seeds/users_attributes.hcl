# Atlas Seed: users_attributes
# Generado: 2025-09-23T22:04:31.825251
# Total filas: 8

plan "seed_users_attributes" {
  migration = <<-SQL
    -- Seeds para tabla users_attributes
    INSERT INTO users_attributes (id, status, created_at, updated_at, code_name, user_id, attribute_type_id, attribute_value) VALUES
    ('aeaaf9dc-eccf-4ae4-a94e-4886bfb51b79', 'active', '2024-11-05 03:44:18', NULL, 'names-bypabloc', 'c1819969-be87-420f-a7b3-31ad05001182', 'ed55d1cb-09c3-4071-b7b9-7ce6dd16dfae', 'Pablo Alexander'),
    ('d06bc285-7fa8-4dec-aa93-65f705d9cd59', 'active', '2024-11-05 03:44:18', NULL, 'lastName-bypabloc', 'c1819969-be87-420f-a7b3-31ad05001182', '585d0fef-55b3-4ea3-918a-d413155760a5', 'Contreras Guevara'),
    ('57af7767-0990-492e-8da7-d0cb52f180b0', 'active', '2024-11-05 03:44:18', NULL, 'email-bypabloc', 'c1819969-be87-420f-a7b3-31ad05001182', '240f7dc8-87dc-4269-93cd-cbce82a3523d', 'pacg1991@gmail.com'),
    ('217e9693-d092-48d8-b897-c004bf5cd838', 'active', '2024-11-05 03:44:18', NULL, 'phone-bypabloc', 'c1819969-be87-420f-a7b3-31ad05001182', 'c4c0c925-4938-40c1-8a21-148526640e8b', '+51 918490148'),
    ('a4db3420-e762-412b-93bd-42d0d838346b', 'active', '2024-11-05 03:44:18', NULL, 'url-bypabloc', 'c1819969-be87-420f-a7b3-31ad05001182', '5723e027-d840-4be5-86ea-567a098f3765', 'https://pablo-c.com'),
    ('877c070c-8ca7-4b42-8cdd-33ed1e925b1c', 'active', '2024-11-05 03:44:18', NULL, 'label-bypabloc', 'c1819969-be87-420f-a7b3-31ad05001182', '36c0037d-e498-4a5e-8af3-46d2c55e3082', 'Ingeniero de software con más de 8 años de experiencia'),
    ('f603081b-bd38-43ab-8275-6434e4027316', 'active', '2024-11-05 03:44:18', NULL, 'summary-bypabloc', 'c1819969-be87-420f-a7b3-31ad05001182', 'fb988a8f-6c2e-4d05-bc98-9a1c2419aa73', 'Ingeniero de software con más de 8 años de experiencia, especializado en desarrollo Full Stack con Python y JavaScript. Experto en crear soluciones tecnológicas con Vue, Django, microservicios y AWS, he desarrollado con éxito y liderado la implementación de sistemas ERP y plataformas fintech, mejorando significativamente la eficiencia operativa y la experiencia del usuario. Habilidoso en la coordinación y motivación de equipos, me adapto fácilmente a entornos dinámicos y desafiantes, siempre enfocado en la calidad y la innovación.'),
    ('be5800df-c455-4c51-8e79-4fe2ed233e60', 'active', '2024-11-05 03:44:18', NULL, 'location-bypabloc', 'c1819969-be87-420f-a7b3-31ad05001182', '06a06f52-9a76-4330-967a-58f3e1c1cd2f', '{"address":"","postalCode":"15009","city":"Lima","countryCode":"PE","region":"Perú"}');
  SQL
}

locals {
  users_attributes_columns = ['id', 'status', 'created_at', 'updated_at', 'code_name', 'user_id', 'attribute_type_id', 'attribute_value']
  users_attributes_row_count = 8
}

# Test básico para validar la tabla
test "schema" "users_attributes_exists" {
  exec {
    sql = "SELECT COUNT(*) FROM information_schema.tables WHERE table_name = 'users_attributes';"
    output = "1"
  }
}
