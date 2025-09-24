# Atlas Seed: users_interests
# Generado: 2025-09-23T22:04:31.826053
# Total filas: 20

plan "seed_users_interests" {
  migration = <<-SQL
    -- Seeds para tabla users_interests
    INSERT INTO users_interests (id, status, created_at, updated_at, user_id, interest_id) VALUES
    ('f6f17fc0-a1b3-4937-a66f-4ae93e194f87', 'active', '2024-11-05 03:45:42', NULL, 'c1819969-be87-420f-a7b3-31ad05001182', '107bffe2-a92c-425a-a52d-702e22c3d517'),
    ('05c9a870-ecef-4676-936a-bd61e5020035', 'active', '2024-11-05 03:45:42', NULL, 'c1819969-be87-420f-a7b3-31ad05001182', 'fca2e098-f28d-4ac2-a720-d28bdc2db3b7'),
    ('01e9c92b-a3ff-4ccd-9bb4-457286f0ec8d', 'active', '2024-11-05 03:45:42', NULL, 'c1819969-be87-420f-a7b3-31ad05001182', '0433c0bc-4b4e-44ab-8709-68763ba5b997'),
    ('56f02743-74b2-4a4d-98dd-a22978882fa2', 'active', '2024-11-05 03:45:42', NULL, 'c1819969-be87-420f-a7b3-31ad05001182', 'c83f3a20-dc31-4614-a1da-0db0442118f7'),
    ('615e41df-a9cf-4713-8b9c-397df6c4c8f9', 'active', '2024-11-05 03:45:42', NULL, 'c1819969-be87-420f-a7b3-31ad05001182', '703594f0-83a9-4185-8eec-72746add6283'),
    ('bed372db-641a-4a60-8a02-e3055e3e7148', 'active', '2024-11-05 03:45:42', NULL, 'c1819969-be87-420f-a7b3-31ad05001182', 'e50c8956-1c83-425e-8b16-cd38928039f7'),
    ('fed5db89-60af-42fa-80a1-5d1d6e994617', 'active', '2024-11-05 03:45:42', NULL, 'c1819969-be87-420f-a7b3-31ad05001182', 'c1f17efc-dff5-4cb9-b2e8-09ad86179275'),
    ('f1f5c61c-ccfc-4a5d-b023-324bdfee35b1', 'active', '2024-11-05 03:45:42', NULL, 'c1819969-be87-420f-a7b3-31ad05001182', '4975771d-ae4f-4f6b-b0b9-a98d7ec8452f'),
    ('01a61e0b-6850-4a4f-be79-5be3d3645811', 'active', '2024-11-05 03:45:42', NULL, 'c1819969-be87-420f-a7b3-31ad05001182', '3a5d95b6-118f-4991-b910-840a8e9dd63e'),
    ('4cbee6a2-8672-4ceb-a269-15302145e3ab', 'active', '2024-11-05 03:45:42', NULL, 'c1819969-be87-420f-a7b3-31ad05001182', '69df5a0a-4fc4-4477-830e-260ae5dd6a00'),
    ('40d9c19c-4996-49c8-87d0-f9be4adb6583', 'active', '2024-11-05 03:45:42', NULL, 'c1819969-be87-420f-a7b3-31ad05001182', '5f07c11d-ed04-487d-9e90-7c04cd5e2337'),
    ('bef2eca5-e01c-4210-8cf8-b85bb24aa06b', 'active', '2024-11-05 03:45:42', NULL, 'c1819969-be87-420f-a7b3-31ad05001182', '8b5f1904-adae-453b-905c-d94abec4d2bc'),
    ('7f1b8c99-1fec-4c31-bf57-5212f6719139', 'active', '2024-11-05 03:45:42', NULL, 'c1819969-be87-420f-a7b3-31ad05001182', 'ec26b6cf-a0ce-455b-a572-2e9a395802d0'),
    ('a07a1af3-63fc-403e-95b3-76abb1d94bb6', 'active', '2024-11-05 03:45:42', NULL, 'c1819969-be87-420f-a7b3-31ad05001182', '5beba69c-34ec-433f-9deb-6c788bf41bea'),
    ('cdc8da1f-1c71-4495-9b67-49aa83cc54d7', 'active', '2024-11-05 03:45:42', NULL, 'c1819969-be87-420f-a7b3-31ad05001182', '7541fe66-8b2a-4f43-a1b3-b48ad4be6753'),
    ('7f026462-1275-4ba2-a3b6-170442209fca', 'active', '2024-11-05 03:45:42', NULL, 'c1819969-be87-420f-a7b3-31ad05001182', '853f36ec-ae98-4732-9d16-262c1e7ad0b8'),
    ('e9a1b2d8-e217-48e5-b010-2cd5ea92e92c', 'active', '2024-11-05 03:45:42', NULL, 'c1819969-be87-420f-a7b3-31ad05001182', 'a168e681-7cde-4a3b-a2e5-abff36949503'),
    ('b4ea9623-8ccb-4e85-9817-886ae05d6409', 'active', '2024-11-05 03:45:42', NULL, 'c1819969-be87-420f-a7b3-31ad05001182', 'e2da95e2-ac72-48c8-af26-2721f03061ff'),
    ('e645e958-18d4-4bae-9326-e9548eecbdaa', 'active', '2024-11-05 03:45:42', NULL, 'c1819969-be87-420f-a7b3-31ad05001182', 'eb9ea89c-990b-4456-89b2-94c093ed7e81'),
    ('355b2ca4-ea0b-4099-afd9-07a999ab9d72', 'active', '2024-11-05 03:45:42', NULL, 'c1819969-be87-420f-a7b3-31ad05001182', 'a97dc957-2293-4e7f-9a95-f5e871b45ac9');
  SQL
}

locals {
  users_interests_columns = ['id', 'status', 'created_at', 'updated_at', 'user_id', 'interest_id']
  users_interests_row_count = 20
}

# Test básico para validar la tabla
test "schema" "users_interests_exists" {
  exec {
    sql = "SELECT COUNT(*) FROM information_schema.tables WHERE table_name = 'users_interests';"
    output = "1"
  }
}
