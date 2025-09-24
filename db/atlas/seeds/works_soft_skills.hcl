# Atlas Seed: works_soft_skills
# Generado: 2025-09-23T22:04:31.826229
# Total filas: 40

plan "seed_works_soft_skills" {
  migration = <<-SQL
    -- Seeds para tabla works_soft_skills
    INSERT INTO works_soft_skills (id, status, created_at, updated_at, work_id, skill_id) VALUES
    ('a4096530-706a-4dd3-8b6c-df8408f3c702', 'active', '2024-11-05 03:46:03', NULL, '99927fa8-736b-4d8f-b302-a795e1610a58', '9318f070-f6fc-400a-af72-e93f478cc505'),
    ('0f0bd93b-5b12-4fa2-9f85-7551c56d023f', 'active', '2024-11-05 03:46:03', NULL, '99927fa8-736b-4d8f-b302-a795e1610a58', 'd6a9740d-99ed-40a3-9405-823d57e4d1f3'),
    ('b91f5c15-3882-4bf4-b0f3-9053d6f68db5', 'active', '2024-11-05 03:46:03', NULL, '99927fa8-736b-4d8f-b302-a795e1610a58', '267a4b70-cb51-48d3-8bf0-e3a7e42a2df8'),
    ('05e87e8e-7ad4-4714-9ec6-d535bbd21caf', 'active', '2024-11-05 03:46:03', NULL, '3786d7c6-4242-4457-81e5-c102618cff4b', '5165d8d3-f46f-4951-9237-f794ce823063'),
    ('90b92ba3-508e-4d1e-8462-3aff50dfab7d', 'active', '2024-11-05 03:46:03', NULL, '3786d7c6-4242-4457-81e5-c102618cff4b', '0a0401b1-eef3-4431-ab41-6bcc0d4a0979'),
    ('6e1c2f5a-e035-43b3-a7a1-985777a60b3b', 'active', '2024-11-05 03:46:03', NULL, '3786d7c6-4242-4457-81e5-c102618cff4b', '05c85f6c-becf-4a0f-8b3d-4b486a0d6bf9'),
    ('70b22173-127a-4896-9d01-fe20a2a77948', 'active', '2024-11-05 03:46:03', NULL, '19d75303-1fc9-43d2-a8a0-dac991787513', 'f6b57e1f-2487-40e6-ab1c-66fd2e4ec081'),
    ('0aa95c5a-742a-4d56-a65c-79649dcba90d', 'active', '2024-11-05 03:46:03', NULL, '19d75303-1fc9-43d2-a8a0-dac991787513', '3c98b1a2-b1c8-4f0c-9a60-3c091d8d9643'),
    ('1204fbd9-4d6e-46fe-a83f-52099918b202', 'active', '2024-11-05 03:46:03', NULL, '19d75303-1fc9-43d2-a8a0-dac991787513', '36ff46cb-ddbb-4594-9fba-c36bb559bf47'),
    ('5dbf0c5b-a9fa-4f93-b687-1bad94b3cbcb', 'active', '2024-11-05 03:46:03', NULL, '19d75303-1fc9-43d2-a8a0-dac991787513', '8680b238-85b4-4d1d-ae0b-251610b80fd5'),
    ('60e43130-71dc-4c7e-a7e4-ca428457c3e4', 'active', '2024-11-05 03:46:03', NULL, '19d75303-1fc9-43d2-a8a0-dac991787513', 'f0d69041-ab71-4b4c-9a21-f9e3047dd305'),
    ('08099ae0-78ff-4adc-8bd6-8c50bd642545', 'active', '2024-11-05 03:46:03', NULL, '19d75303-1fc9-43d2-a8a0-dac991787513', '4e3672d0-d9eb-4fae-9e2d-f9e437a106ce'),
    ('6d3bcb79-cf66-497e-a508-3a32261f6db2', 'active', '2024-11-05 03:46:03', NULL, 'ce08f30e-b0c0-46ba-9dba-4f6ec41b8ed8', 'f6b57e1f-2487-40e6-ab1c-66fd2e4ec081'),
    ('0aecc1b5-f670-4a53-a267-2ef291212fc0', 'active', '2024-11-05 03:46:03', NULL, 'ce08f30e-b0c0-46ba-9dba-4f6ec41b8ed8', 'bd4a7c80-5848-4ec4-b626-f0428928d30f'),
    ('101a020f-dca9-42e9-a685-3956a57e9669', 'active', '2024-11-05 03:46:03', NULL, 'ce08f30e-b0c0-46ba-9dba-4f6ec41b8ed8', '267a4b70-cb51-48d3-8bf0-e3a7e42a2df8'),
    ('851ecc5f-ce17-43a3-bada-4104896913af', 'active', '2024-11-05 03:46:03', NULL, 'ce08f30e-b0c0-46ba-9dba-4f6ec41b8ed8', '5165d8d3-f46f-4951-9237-f794ce823063'),
    ('764dc665-fe75-4947-8fc3-6959aa6fac65', 'active', '2024-11-05 03:46:03', NULL, 'ce08f30e-b0c0-46ba-9dba-4f6ec41b8ed8', '05c85f6c-becf-4a0f-8b3d-4b486a0d6bf9'),
    ('62902121-21a5-42dc-8a8a-3142a87c9433', 'active', '2024-11-05 03:46:03', NULL, 'eadc5459-61a5-40e6-aca3-6afa23c6245d', '79ca3de7-05e2-4e72-8aa2-a88b8518a3d1'),
    ('0dfa170e-bd33-4907-aa6d-6bf149eedbe4', 'active', '2024-11-05 03:46:03', NULL, 'eadc5459-61a5-40e6-aca3-6afa23c6245d', '1f0843be-bf6d-4fa1-a092-0c191ab5243a'),
    ('42c76b7f-c244-4e4b-a01d-124b90c4fe18', 'active', '2024-11-05 03:46:03', NULL, 'eadc5459-61a5-40e6-aca3-6afa23c6245d', '5955fb79-fca0-4078-869b-4172fbf70503'),
    ('9cbd90b5-6364-4475-823f-a5ddb833bba2', 'active', '2024-11-05 03:46:03', NULL, 'eadc5459-61a5-40e6-aca3-6afa23c6245d', '9bcb4f0a-7e98-4879-a416-3f3fdcf275f1'),
    ('d56c0916-e600-42e5-be2a-eb309960cf2d', 'active', '2024-11-05 03:46:03', NULL, 'ea042a61-9c8f-4560-97ed-d828b574940f', 'ff9b80e3-ecb0-474e-b1b6-0844667f7812'),
    ('58d06f98-8e6c-47d6-9271-d796ffc55d88', 'active', '2024-11-05 03:46:03', NULL, 'ea042a61-9c8f-4560-97ed-d828b574940f', '5165d8d3-f46f-4951-9237-f794ce823063'),
    ('468dbaac-8bea-4a87-8e5d-f7b83c9609f8', 'active', '2024-11-05 03:46:03', NULL, 'dfc24862-324c-4e6c-a226-7b6b80d0f437', '6c308f1e-a93f-490a-af17-c0da5d932ddc'),
    ('711108ad-be7b-4f01-9d06-19389b1fd718', 'active', '2024-11-05 03:46:03', NULL, 'dfc24862-324c-4e6c-a226-7b6b80d0f437', 'ff9b80e3-ecb0-474e-b1b6-0844667f7812'),
    ('63c1b6d4-fb63-4e40-89dc-e324e7193bfe', 'active', '2024-11-05 03:46:03', NULL, 'dfc24862-324c-4e6c-a226-7b6b80d0f437', '3418cdb5-a581-4ef5-94ae-8919b4235664'),
    ('16f0226b-6d41-4f4d-b51b-f416949efee9', 'active', '2024-11-05 03:46:03', NULL, 'dfc24862-324c-4e6c-a226-7b6b80d0f437', 'bd4a7c80-5848-4ec4-b626-f0428928d30f'),
    ('a3dc7630-911f-455c-a4b7-bee21981f77e', 'active', '2024-11-05 03:46:03', NULL, 'dfc24862-324c-4e6c-a226-7b6b80d0f437', '5165d8d3-f46f-4951-9237-f794ce823063'),
    ('20da8469-fd5d-49d3-8488-35bfb1648963', 'active', '2024-11-05 03:46:03', NULL, 'dfc24862-324c-4e6c-a226-7b6b80d0f437', '267a4b70-cb51-48d3-8bf0-e3a7e42a2df8'),
    ('2a1d667b-afa5-4ce4-988b-9386946b2193', 'active', '2024-11-05 03:46:03', NULL, '3706a632-f7ae-4c9b-93d4-5ffc464dda99', '769eaf1d-c241-43fd-a551-95e0b3f2d371'),
    ('ab2c33c0-93f6-48b9-a5fb-b47bd9367d74', 'active', '2024-11-05 03:46:03', NULL, '3706a632-f7ae-4c9b-93d4-5ffc464dda99', 'b740f947-2c3b-4485-9fbb-c39239617103'),
    ('4f83fb30-f65f-43ff-8154-f27549e75854', 'active', '2024-11-05 03:46:03', NULL, '3706a632-f7ae-4c9b-93d4-5ffc464dda99', 'd6f6ee1c-5587-48f0-8aca-d7d535cf1f86'),
    ('27efd60b-720a-4c97-96ce-6e0cab56e8c3', 'active', '2024-11-05 03:46:03', NULL, '3706a632-f7ae-4c9b-93d4-5ffc464dda99', 'f6b57e1f-2487-40e6-ab1c-66fd2e4ec081'),
    ('e4f9b33b-2e17-437a-94cf-71c4c363a78c', 'active', '2024-11-05 03:46:03', NULL, '3706a632-f7ae-4c9b-93d4-5ffc464dda99', '7c8c8117-70c0-4b40-a91e-362f64b48836'),
    ('fe08e5cb-8836-401a-a174-e26e4edb2762', 'active', '2024-11-05 03:46:03', NULL, 'ffd32209-b089-48e1-8760-f680a5bd7f50', '463eccc8-62d3-4551-9304-9370820e86ec'),
    ('52ed60b6-fba0-4c67-a8e0-9c9b625eb48d', 'active', '2024-11-05 03:46:03', NULL, 'ffd32209-b089-48e1-8760-f680a5bd7f50', 'd906bcd4-367d-417f-9258-50b183ce3784'),
    ('f8f7e926-ebe5-4ed6-9299-c9ee192afa2b', 'active', '2024-11-05 03:46:03', NULL, 'ffd32209-b089-48e1-8760-f680a5bd7f50', '5165d8d3-f46f-4951-9237-f794ce823063'),
    ('71c719e8-77c5-4323-b2ff-e5bac2e11875', 'active', '2024-11-05 03:46:03', NULL, 'ffd32209-b089-48e1-8760-f680a5bd7f50', '267a4b70-cb51-48d3-8bf0-e3a7e42a2df8'),
    ('846919e5-9045-44ef-8fed-7d3b58f72106', 'active', '2024-11-05 03:46:03', NULL, 'c14c5c8a-9489-4127-b08e-e8d87ac51e66', '5165d8d3-f46f-4951-9237-f794ce823063'),
    ('e7c24885-e7f9-4b66-b4c2-e60f545749dd', 'active', '2024-11-05 03:46:03', NULL, 'c14c5c8a-9489-4127-b08e-e8d87ac51e66', 'ff9b80e3-ecb0-474e-b1b6-0844667f7812');
  SQL
}

locals {
  works_soft_skills_columns = ['id', 'status', 'created_at', 'updated_at', 'work_id', 'skill_id']
  works_soft_skills_row_count = 40
}

# Test básico para validar la tabla
test "schema" "works_soft_skills_exists" {
  exec {
    sql = "SELECT COUNT(*) FROM information_schema.tables WHERE table_name = 'works_soft_skills';"
    output = "1"
  }
}
