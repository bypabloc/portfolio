# Atlas Seed: works_technical_skills
# Generado: 2025-09-23T22:04:31.826282
# Total filas: 50

plan "seed_works_technical_skills" {
  migration = <<-SQL
    -- Seeds para tabla works_technical_skills
    INSERT INTO works_technical_skills (id, status, created_at, updated_at, work_id, technical_skill_id) VALUES
    ('7dac5b91-6654-401f-aa2a-17aced3f9550', 'active', '2024-11-05 03:46:28', NULL, '99927fa8-736b-4d8f-b302-a795e1610a58', '345f953c-d2a9-4503-bf75-ffe232829774'),
    ('e75b0ace-56fc-4c7c-9caa-ddda6fa813c6', 'active', '2024-11-05 03:46:28', NULL, '99927fa8-736b-4d8f-b302-a795e1610a58', '7a350f7b-978f-4fa9-b10e-f30a4be32140'),
    ('50ef35f0-fcd6-4b53-acc4-a199d5e476cb', 'active', '2024-11-05 03:46:28', NULL, '99927fa8-736b-4d8f-b302-a795e1610a58', '1522fe72-4e97-4412-8458-330742d6545a'),
    ('90384f60-cf09-436a-8bcb-40548627f7e2', 'active', '2024-11-05 03:46:28', NULL, '99927fa8-736b-4d8f-b302-a795e1610a58', '33c2264e-f818-4eb9-819d-e202f2dbf6b8'),
    ('36f65a94-1980-4a7d-9130-0ac5f1778d4a', 'active', '2024-11-05 03:46:28', NULL, '99927fa8-736b-4d8f-b302-a795e1610a58', '0b3eca7d-0c48-4979-b97b-40c0057d8d8e'),
    ('45e2bb67-8627-46f2-8ef2-fe1c706f5fba', 'active', '2024-11-05 03:46:28', NULL, '99927fa8-736b-4d8f-b302-a795e1610a58', '4b4e296f-a9a2-4ca3-84c9-bba1349ec732'),
    ('f1709d59-07b3-4d4c-8ea1-5f5ebc6d0256', 'active', '2024-11-05 03:46:28', NULL, '99927fa8-736b-4d8f-b302-a795e1610a58', '62ff3306-c8f8-4522-a06c-80acb5033579'),
    ('4ba9b1cb-f1ff-4470-81d2-45bdb86f1dc8', 'active', '2024-11-05 03:46:28', NULL, '99927fa8-736b-4d8f-b302-a795e1610a58', '345f953c-d2a9-4503-bf75-ffe232829774'),
    ('7ca761d8-edcc-46c4-854f-6a019e01460f', 'active', '2024-11-05 03:46:28', NULL, '3786d7c6-4242-4457-81e5-c102618cff4b', '2c558182-4abc-43ab-baa2-16549f314b5b'),
    ('ffb65cf2-c31d-476e-836d-a239b9abf1d2', 'active', '2024-11-05 03:46:28', NULL, '3786d7c6-4242-4457-81e5-c102618cff4b', '38045df5-168f-4bf2-832e-3d2b387e542f'),
    ('8f699e74-faab-4258-8a92-f891bfa07c5a', 'active', '2024-11-05 03:46:28', NULL, '3786d7c6-4242-4457-81e5-c102618cff4b', '7a350f7b-978f-4fa9-b10e-f30a4be32140'),
    ('9913611b-4a36-4078-a8f6-fae85445bcbf', 'active', '2024-11-05 03:46:28', NULL, '3786d7c6-4242-4457-81e5-c102618cff4b', '1522fe72-4e97-4412-8458-330742d6545a'),
    ('3d2acc8a-ace2-4b2d-abbb-7a505e4c9109', 'active', '2024-11-05 03:46:28', NULL, '3786d7c6-4242-4457-81e5-c102618cff4b', '1d76df3e-e720-415c-b466-9afdff9f51c7'),
    ('ab2cc4a0-9e1d-46bb-b36c-6f074025f757', 'active', '2024-11-05 03:46:28', NULL, '19d75303-1fc9-43d2-a8a0-dac991787513', '5e44606c-6638-42f7-b942-3ba709b6ac15'),
    ('8353a8c3-cb98-47e1-9972-c69b1af620fa', 'active', '2024-11-05 03:46:28', NULL, '19d75303-1fc9-43d2-a8a0-dac991787513', '2c826599-e414-420c-ad70-a6468abb61dd'),
    ('9434f884-36e9-494f-bd3e-76eb6cc32afe', 'active', '2024-11-05 03:46:28', NULL, '19d75303-1fc9-43d2-a8a0-dac991787513', '01c95d24-0e9e-4d2b-bebc-ebe953956db8'),
    ('253c460c-be44-4500-ad7b-57df394a3d24', 'active', '2024-11-05 03:46:28', NULL, '19d75303-1fc9-43d2-a8a0-dac991787513', 'b68fce3c-36cf-499e-b50c-cb8d02cc4140'),
    ('1ea0ad72-18ba-42ee-a8f8-bef875af078f', 'active', '2024-11-05 03:46:28', NULL, 'ce08f30e-b0c0-46ba-9dba-4f6ec41b8ed8', '6a0bc669-ffc4-4d2d-a962-c3e3908d0a47'),
    ('73aa66cf-8e16-415c-871e-613632189a58', 'active', '2024-11-05 03:46:28', NULL, 'ce08f30e-b0c0-46ba-9dba-4f6ec41b8ed8', 'caf983c9-57ea-414d-9c27-db2918bb493c'),
    ('58d7d999-afe4-4d34-9147-3d8e0e0068b7', 'active', '2024-11-05 03:46:28', NULL, 'ce08f30e-b0c0-46ba-9dba-4f6ec41b8ed8', '18252393-5722-4c4d-b565-6e0c81e6783e'),
    ('077aba48-e5ea-46d1-aca1-8604e6bcda46', 'active', '2024-11-05 03:46:28', NULL, 'ce08f30e-b0c0-46ba-9dba-4f6ec41b8ed8', '4ce4fa68-5a69-468e-8257-0e6e06c3e605'),
    ('af80f5e4-1d48-42ea-a224-bbcd0fcf43ee', 'active', '2024-11-05 03:46:28', NULL, 'ce08f30e-b0c0-46ba-9dba-4f6ec41b8ed8', '37977b9b-afb8-470f-80fd-ebb3a1d03611'),
    ('0de92ced-4947-42c3-8985-653faeeada68', 'active', '2024-11-05 03:46:28', NULL, 'eadc5459-61a5-40e6-aca3-6afa23c6245d', '279e8e9e-74c0-4a2d-84a5-89498bd3d810'),
    ('e4b5d14c-ce68-4c79-b776-264cbae4d0e8', 'active', '2024-11-05 03:46:28', NULL, 'eadc5459-61a5-40e6-aca3-6afa23c6245d', 'fcae64e6-a748-496d-8b75-781e2e2c4248'),
    ('ada838b0-0cf0-4bf5-a533-ca15236b2bae', 'active', '2024-11-05 03:46:28', NULL, 'eadc5459-61a5-40e6-aca3-6afa23c6245d', 'd5c7a99d-07e4-49b6-aadd-388bdce81d45'),
    ('aadec967-1612-42d3-bf71-d34c0a9a4490', 'active', '2024-11-05 03:46:28', NULL, 'eadc5459-61a5-40e6-aca3-6afa23c6245d', '7423e816-8813-48eb-a9b6-e81b35e86e70'),
    ('b5358b7f-0f1b-4243-926e-7d0600de1960', 'active', '2024-11-05 03:46:28', NULL, 'eadc5459-61a5-40e6-aca3-6afa23c6245d', 'a82b3747-86ee-4196-a4b4-469d4002ed81'),
    ('b60bdd76-3651-485f-9b33-985f2e6012ab', 'active', '2024-11-05 03:46:28', NULL, 'eadc5459-61a5-40e6-aca3-6afa23c6245d', '872de34a-ec8f-4b81-bb94-7aba9294ecdd'),
    ('6a041857-6d42-4d73-9ed9-587784d663fe', 'active', '2024-11-05 03:46:28', NULL, 'ea042a61-9c8f-4560-97ed-d828b574940f', '747b3050-5b33-4cf8-b07c-b7f0b551835b'),
    ('a6e2993d-8c4e-45f2-9ba3-db6ebbba6662', 'active', '2024-11-05 03:46:28', NULL, 'ea042a61-9c8f-4560-97ed-d828b574940f', '81584e13-d652-45cd-ae2f-68324cbda054'),
    ('c9fbba3b-eef4-489c-bf6a-d7e5c2465349', 'active', '2024-11-05 03:46:28', NULL, 'ea042a61-9c8f-4560-97ed-d828b574940f', '6a46a59c-55f1-48a5-aa06-46e74581f19a'),
    ('0e2b8d76-e82e-4a45-82cf-b79b46adf062', 'active', '2024-11-05 03:46:28', NULL, 'ea042a61-9c8f-4560-97ed-d828b574940f', 'c76f2842-947c-4f3a-8b50-da56fe1612fe'),
    ('05021118-3653-45ce-bb03-8347f1f8c8ac', 'active', '2024-11-05 03:46:28', NULL, 'ea042a61-9c8f-4560-97ed-d828b574940f', '7933efae-4bef-430c-9a8b-98be945f2260'),
    ('0538030e-7b58-4178-8c71-8f061107cf7f', 'active', '2024-11-05 03:46:28', NULL, '3706a632-f7ae-4c9b-93d4-5ffc464dda99', '733d7808-679e-445d-b321-c601491eb0b8'),
    ('4c0c4d87-413d-4208-afc5-99a355ba40c3', 'active', '2024-11-05 03:46:28', NULL, '3706a632-f7ae-4c9b-93d4-5ffc464dda99', '70436d46-bae5-46f8-9ce8-c3ce0ed71f7d'),
    ('88611fc4-4070-4ce1-84ac-d3a9ca69e70b', 'active', '2024-11-05 03:46:28', NULL, '3706a632-f7ae-4c9b-93d4-5ffc464dda99', 'aff49dd5-4a69-43c4-8f86-3829b58635d7'),
    ('09af716a-497f-4d2e-8a1b-2e05b1bec153', 'active', '2024-11-05 03:46:28', NULL, '3706a632-f7ae-4c9b-93d4-5ffc464dda99', '9bcfea3f-5839-430b-bc54-9ff027bac26c'),
    ('0ae95468-c594-432d-b6c1-a757dd62242f', 'active', '2024-11-05 03:46:28', NULL, '3706a632-f7ae-4c9b-93d4-5ffc464dda99', 'ba892ff0-4beb-4046-be4f-bc93e49be0a6'),
    ('cc8f65b7-9ca9-4ce4-8543-cdc4834643a6', 'active', '2024-11-05 03:46:28', NULL, '3706a632-f7ae-4c9b-93d4-5ffc464dda99', 'af33d7b8-70ec-4df1-8ef1-3e6732c7112f'),
    ('71475acb-57b8-48c1-a945-6d6c272a03b8', 'active', '2024-11-05 03:46:28', NULL, '3706a632-f7ae-4c9b-93d4-5ffc464dda99', '0df3e8e7-0c95-4f85-a72e-6c8c18e0baf2'),
    ('273c21cf-3e30-41cc-9d32-c8d69ec9fb45', 'active', '2024-11-05 03:46:28', NULL, 'ffd32209-b089-48e1-8760-f680a5bd7f50', '6edf343d-8c6a-40e3-ada6-fce8d02d53ed'),
    ('0208fa8a-1a22-4dd0-be08-dab4563542b8', 'active', '2024-11-05 03:46:28', NULL, 'ffd32209-b089-48e1-8760-f680a5bd7f50', '56016d50-8737-46cd-8443-d7ec4f736e64'),
    ('434a1a8e-c082-43cf-a4fe-d850481f410a', 'active', '2024-11-05 03:46:28', NULL, 'ffd32209-b089-48e1-8760-f680a5bd7f50', 'bc6a29dd-8272-4b14-9247-4a0c14d0abe2'),
    ('a5314860-fe04-49b9-83ef-61a069c65418', 'active', '2024-11-05 03:46:28', NULL, 'ffd32209-b089-48e1-8760-f680a5bd7f50', 'f57d23b2-e890-4b10-844f-b549f7923fad'),
    ('4c6fbb39-cf0a-4b84-bc6f-a72ebf875502', 'active', '2024-11-05 03:46:28', NULL, 'ffd32209-b089-48e1-8760-f680a5bd7f50', '7005222a-840e-44ca-85db-edd46943f480'),
    ('48fb2e0d-fac9-484a-b16f-f31b12349fab', 'active', '2024-11-05 03:46:28', NULL, 'c14c5c8a-9489-4127-b08e-e8d87ac51e66', 'df9e0f3f-3825-4d4d-9c4f-e2a320e70c83'),
    ('e883378f-545e-4149-ba65-f206c4c9b0b2', 'active', '2024-11-05 03:46:28', NULL, 'c14c5c8a-9489-4127-b08e-e8d87ac51e66', '6e6dff96-e51d-405b-92e1-e1e696360286'),
    ('91ecbcd2-cfa0-43b9-bc9e-aaaa86397552', 'active', '2024-11-05 03:46:28', NULL, 'c14c5c8a-9489-4127-b08e-e8d87ac51e66', '06c33a71-e925-4752-8938-0a6bc739cf3b'),
    ('4756c02a-5491-4587-b56b-5f9e9572e05b', 'active', '2024-11-05 03:46:28', NULL, 'c14c5c8a-9489-4127-b08e-e8d87ac51e66', 'c26fa02f-e2d4-4ec9-877b-fb4377087a72'),
    ('cf2bc631-a22f-4c90-be5a-a0e8b20d1531', 'active', '2024-11-05 03:46:28', NULL, 'c14c5c8a-9489-4127-b08e-e8d87ac51e66', 'e98f620a-51fb-47ac-a824-364b8be2012c');
  SQL
}

locals {
  works_technical_skills_columns = ['id', 'status', 'created_at', 'updated_at', 'work_id', 'technical_skill_id']
  works_technical_skills_row_count = 50
}

# Test básico para validar la tabla
test "schema" "works_technical_skills_exists" {
  exec {
    sql = "SELECT COUNT(*) FROM information_schema.tables WHERE table_name = 'works_technical_skills';"
    output = "1"
  }
}
