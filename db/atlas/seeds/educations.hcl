# Atlas Seed: educations
# Generado: 2025-09-23T22:04:31.825450
# Total filas: 3

plan "seed_educations" {
  migration = <<-SQL
    -- Seeds para tabla educations
    INSERT INTO educations (id, status, created_at, updated_at, user_id, institution_id, code_name, area, learn, study_type, start_date, end_date) VALUES
    ('0091d351-f3ba-4f87-9fd8-e0d7d903ef45', 'active', '2024-11-05 03:44:30', NULL, 'c1819969-be87-420f-a7b3-31ad05001182', 'ced3de3e-fc5a-46bf-a958-c7ca156f0c3c', 'udemy-web-development-bypabloc', 'Desarrollo Web', 'En Udemy he tomado varios cursos de desarrollo web, entre ellos: JavaScript, React, Vue, Node, SQL, entre otros. Con la misma filosofía de aprender a mi ritmo y a mi tiempo pero siempre aprendiendo.', 'course', '2017-04-01T00:00:00.000Z', NULL),
    ('b651f447-1f6e-4ad1-aedc-6f6fbff8a173', 'active', '2024-11-05 03:44:30', NULL, 'c1819969-be87-420f-a7b3-31ad05001182', '0c41d325-8545-43fb-b13d-bb4d83e59b2b', 'youtube-web-development-bypabloc', 'Desarrollo Web', 'Cuando comencé a introducirme en el curso de programación en 2013, accedí a material gratuito y de paga que existía en ese momento en linea, hasta el día de hoy no paro de aprender', 'course', '2012-04-20T00:00:00.000Z', NULL),
    ('40779100-c079-4c42-9e3e-283c8f69cb81', 'active', '2024-11-05 03:44:30', NULL, 'c1819969-be87-420f-a7b3-31ad05001182', '03f6e5db-aeec-4cf4-83d6-46ffa1eb4083', 'uptyab-informatics-engineering-bypabloc', 'Ingeniería Informática', 'Estudié Ingeniería Informática en la UPTYAB, donde adquirí conocimientos en programación, bases de datos, redes, sistemas operativos, entre otros.', 'bachelorDegree', '2011-03-01T00:00:00.000Z', '2016-03-01T00:00:00.000Z');
  SQL
}

locals {
  educations_columns = ['id', 'status', 'created_at', 'updated_at', 'user_id', 'institution_id', 'code_name', 'area', 'learn', 'study_type', 'start_date', 'end_date']
  educations_row_count = 3
}

# Test básico para validar la tabla
test "schema" "educations_exists" {
  exec {
    sql = "SELECT COUNT(*) FROM information_schema.tables WHERE table_name = 'educations';"
    output = "1"
  }
}
