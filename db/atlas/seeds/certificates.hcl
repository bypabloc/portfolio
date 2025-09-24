# Atlas Seed: certificates
# Generado: 2025-09-23T22:04:31.825402
# Total filas: 11

plan "seed_certificates" {
  migration = <<-SQL
    -- Seeds para tabla certificates
    INSERT INTO certificates (id, status, created_at, updated_at, user_id, title, date, issuer_id, url) VALUES
    ('a2371ed2-fb2a-4fcf-9c9b-bf83b093eccb', 'active', '2024-11-05 03:44:36', NULL, 'c1819969-be87-420f-a7b3-31ad05001182', 'Docker - Guía práctica de uso para desarrolladores', '2023-04-20T00:00:00.000Z', 'a5ac58e4-2ec7-44b3-a3bb-1f0c2df0611e', 'https://cursos.devtalles.com/certificates/f7qc3ju28w'),
    ('7530c52a-5054-441a-856f-e8ab300f7d5d', 'active', '2024-11-05 03:44:36', NULL, 'c1819969-be87-420f-a7b3-31ad05001182', 'Node - Autenticación Rest con Clean Architecture', '2023-08-15T00:00:00.000Z', 'a5ac58e4-2ec7-44b3-a3bb-1f0c2df0611e', 'https://cursos.devtalles.com/certificates/91cxyahzil'),
    ('ca70b363-9b0a-4552-8273-3808d7801f47', 'active', '2024-11-05 03:44:36', NULL, 'c1819969-be87-420f-a7b3-31ad05001182', 'Principios SOLID y Clean Code', '2023-11-05T00:00:00.000Z', 'a5ac58e4-2ec7-44b3-a3bb-1f0c2df0611e', 'http://ude.my/UC-ddf92744-e69f-47ab-b28d-c4f7b569b7d4'),
    ('e6d96d80-63c1-4f86-8f32-71b4db67cec3', 'active', '2024-11-05 03:44:36', NULL, 'c1819969-be87-420f-a7b3-31ad05001182', 'Next.js: El framework de React para producción', '2024-01-04T00:00:00.000Z', '32e79762-e98f-43b3-b660-31ae9ebc33f4', 'http://ude.my/UC-8297be13-d656-4e62-b64b-642819930c71'),
    ('19c2aa14-4bcf-4b0c-a18a-7a942cccce3e', 'active', '2024-11-05 03:44:36', NULL, 'c1819969-be87-420f-a7b3-31ad05001182', 'React: De cero a experto ( Hooks y MERN )', '2023-11-13T00:00:00.000Z', '32e79762-e98f-43b3-b660-31ae9ebc33f4', 'http://ude.my/UC-6f8fa099-e631-459d-a139-989d441a1b21'),
    ('b93fb01f-0b52-4b29-9b06-1c5d1aa77c71', 'active', '2024-11-05 03:44:36', NULL, 'c1819969-be87-420f-a7b3-31ad05001182', 'Vue.js - Intermedio: Lleva tus bases al siguiente nivel', '2023-03-22T00:00:00.000Z', '32e79762-e98f-43b3-b660-31ae9ebc33f4', 'http://ude.my/UC-b8d6554e-4cb9-49dd-becb-a5dbfdcf6f26'),
    ('649c7802-c367-4166-9e8a-765bbcbff916', 'active', '2024-11-05 03:44:36', NULL, 'c1819969-be87-420f-a7b3-31ad05001182', 'Vue.js: De cero a experto', '2023-05-30T00:00:00.000Z', '32e79762-e98f-43b3-b660-31ae9ebc33f4', 'http://ude.my/UC-a217906e-84eb-40dc-9303-36de5b71e0cc'),
    ('d171973f-a8c2-435a-9a7b-36b3ebd89dda', 'active', '2024-11-05 03:44:36', NULL, 'c1819969-be87-420f-a7b3-31ad05001182', 'SQL de cero: Tu guía práctica con PostgreSQL', '2023-02-12T00:00:00.000Z', '32e79762-e98f-43b3-b660-31ae9ebc33f4', 'http://ude.my/UC-afb98ee6-8704-4b20-9e1f-15bdacf2c76d'),
    ('642f95bb-8130-4a13-8b49-5ff4cbea993a', 'active', '2024-11-05 03:44:36', NULL, 'c1819969-be87-420f-a7b3-31ad05001182', 'NodeJS: De cero a experto', '2023-02-12T00:00:00.000Z', '32e79762-e98f-43b3-b660-31ae9ebc33f4', 'http://ude.my/UC-9acb44f1-27c6-402e-9dae-8a04bf3d424b'),
    ('14d989ec-5cb9-4ea7-8777-4fce25e64c4e', 'active', '2024-11-05 03:44:36', NULL, 'c1819969-be87-420f-a7b3-31ad05001182', 'Nest: Desarrollo backend escalable con Node', '2023-02-12T00:00:00.000Z', '32e79762-e98f-43b3-b660-31ae9ebc33f4', 'http://ude.my/UC-810baa94-7f51-4c54-b631-d62b4af77806'),
    ('8a667022-0184-4cfd-b3dd-d59f6ba6fd94', 'active', '2024-11-05 03:44:36', NULL, 'c1819969-be87-420f-a7b3-31ad05001182', 'JavaScript moderno: Guía para dominar el lenguaje', '2023-07-29T00:00:00.000Z', '32e79762-e98f-43b3-b660-31ae9ebc33f4', 'http://ude.my/UC-516bd9e6-59a0-4f28-b3bf-db2539d158d9');
  SQL
}

locals {
  certificates_columns = ['id', 'status', 'created_at', 'updated_at', 'user_id', 'title', 'date', 'issuer_id', 'url']
  certificates_row_count = 11
}

# Test básico para validar la tabla
test "schema" "certificates_exists" {
  exec {
    sql = "SELECT COUNT(*) FROM information_schema.tables WHERE table_name = 'certificates';"
    output = "1"
  }
}
