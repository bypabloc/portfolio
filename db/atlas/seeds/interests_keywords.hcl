# Atlas Seed: interests_keywords
# Generado: 2025-09-23T22:04:31.826335
# Total filas: 21

plan "seed_interests_keywords" {
  migration = <<-SQL
    -- Seeds para tabla interests_keywords
    INSERT INTO interests_keywords (id, status, created_at, updated_at, interest_id, keyword_id) VALUES
    ('b5a64487-2b64-4c8d-93bf-0a41d0e30275', 'active', '2024-11-05 03:45:32', NULL, '107bffe2-a92c-425a-a52d-702e22c3d517', '56aa6a30-9805-419f-8a54-c69d72d460cd'),
    ('d2dc2ac6-ae01-498c-851f-ce6b53e53166', 'active', '2024-11-05 03:45:32', NULL, 'fca2e098-f28d-4ac2-a720-d28bdc2db3b7', 'c98e7a4c-9245-4580-920f-274b8bd8d7c4'),
    ('4e96d8da-ce4d-4eb4-b1f0-9707512c0a9c', 'active', '2024-11-05 03:45:32', NULL, 'fca2e098-f28d-4ac2-a720-d28bdc2db3b7', '56aa6a30-9805-419f-8a54-c69d72d460cd'),
    ('2094b5da-6d2d-4e9f-b96b-9f8c2d4dec3e', 'active', '2024-11-05 03:45:32', NULL, '0433c0bc-4b4e-44ab-8709-68763ba5b997', '55eac891-f42c-4083-82ab-c0574170cb77'),
    ('dda5447e-1cfa-4392-8390-cc32b402071c', 'active', '2024-11-05 03:45:32', NULL, 'c83f3a20-dc31-4614-a1da-0db0442118f7', '76a66280-64c7-454c-a0e1-e1302ff8545a'),
    ('9b6d6f1a-a11d-4939-847c-41e0de618e7a', 'active', '2024-11-05 03:45:32', NULL, '703594f0-83a9-4185-8eec-72746add6283', '6a16e182-6785-4f2d-910a-6e49c5aa9d18'),
    ('ca196fcd-e4d5-42a1-af79-6ed829b262de', 'active', '2024-11-05 03:45:32', NULL, 'e50c8956-1c83-425e-8b16-cd38928039f7', '76a66280-64c7-454c-a0e1-e1302ff8545a'),
    ('85d9bc2e-d161-4b86-834c-d7ab1bf37518', 'active', '2024-11-05 03:45:32', NULL, 'c1f17efc-dff5-4cb9-b2e8-09ad86179275', '0e4015c5-2989-4de7-9b1d-8166e0141b16'),
    ('bb2f28be-97cc-4375-a99a-f49a149e5e80', 'active', '2024-11-05 03:45:32', NULL, '4975771d-ae4f-4f6b-b0b9-a98d7ec8452f', 'c98e7a4c-9245-4580-920f-274b8bd8d7c4'),
    ('c2a92f61-b1fd-4ac9-a1c2-54041eeff112', 'active', '2024-11-05 03:45:32', NULL, '3a5d95b6-118f-4991-b910-840a8e9dd63e', '005e8383-bcb2-48ec-aed7-22d806027a44'),
    ('6f276dcc-8cb6-483a-8370-afc7a0cf6f50', 'active', '2024-11-05 03:45:32', NULL, '69df5a0a-4fc4-4477-830e-260ae5dd6a00', '93004f9c-f2d6-45bd-8fa9-9dfaf3d2cfb1'),
    ('81ff317d-e482-4a02-aac3-2d8005a93dad', 'active', '2024-11-05 03:45:32', NULL, '5f07c11d-ed04-487d-9e90-7c04cd5e2337', '19adecf0-4c74-4175-810d-7086a4dda003'),
    ('7e5b9449-04ea-479a-aba5-1f91db92ef7e', 'active', '2024-11-05 03:45:32', NULL, '8b5f1904-adae-453b-905c-d94abec4d2bc', '5c093de5-0cf7-4415-bb73-7218719ff2cf'),
    ('0f0b0ecd-25e7-40c5-a1b3-ce0dd2a5050e', 'active', '2024-11-05 03:45:32', NULL, 'ec26b6cf-a0ce-455b-a572-2e9a395802d0', 'b7329175-9717-4685-a6ee-1ecf80c46cb6'),
    ('d61ff3dc-c36a-43f3-a1de-00d05133952e', 'active', '2024-11-05 03:45:32', NULL, '5beba69c-34ec-433f-9deb-6c788bf41bea', '76a66280-64c7-454c-a0e1-e1302ff8545a'),
    ('7145c397-abf2-45d0-b311-1ed1d366620b', 'active', '2024-11-05 03:45:32', NULL, '7541fe66-8b2a-4f43-a1b3-b48ad4be6753', 'a251089e-39d8-41ad-b89d-5021f8d176c3'),
    ('afc4845b-7864-46b9-baf4-8f61bb9ed1d1', 'active', '2024-11-05 03:45:32', NULL, '853f36ec-ae98-4732-9d16-262c1e7ad0b8', 'f4b3880e-32ad-4a6c-aa99-9f9ad1db8476'),
    ('0f94aa34-abae-4b03-ae42-763ff5dc15f2', 'active', '2024-11-05 03:45:32', NULL, 'a168e681-7cde-4a3b-a2e5-abff36949503', 'e3bc39ef-1219-4c5a-b495-d652e35e95c8'),
    ('fb29b40e-48bd-4d0c-bda8-8b968d1e9252', 'active', '2024-11-05 03:45:32', NULL, 'e2da95e2-ac72-48c8-af26-2721f03061ff', 'e3590a54-913d-409b-8886-5cd031ac1f4c'),
    ('10f76922-2e9b-449c-b1d3-dd8bd8d7a461', 'active', '2024-11-05 03:45:32', NULL, 'eb9ea89c-990b-4456-89b2-94c093ed7e81', 'd0f01a5f-21b1-41a6-8e1f-e293198174de'),
    ('f27c774d-ed3a-4d21-92b1-b7e784907abb', 'active', '2024-11-05 03:45:32', NULL, 'a97dc957-2293-4e7f-9a95-f5e871b45ac9', '5044c60e-065c-4361-9f26-741af4c95ced');
  SQL
}

locals {
  interests_keywords_columns = ['id', 'status', 'created_at', 'updated_at', 'interest_id', 'keyword_id']
  interests_keywords_row_count = 21
}

# Test básico para validar la tabla
test "schema" "interests_keywords_exists" {
  exec {
    sql = "SELECT COUNT(*) FROM information_schema.tables WHERE table_name = 'interests_keywords';"
    output = "1"
  }
}
