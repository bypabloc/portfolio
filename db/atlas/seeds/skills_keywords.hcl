# Atlas Seed: skills_keywords
# Generado: 2025-09-23T22:04:31.826159
# Total filas: 55

plan "seed_skills_keywords" {
  migration = <<-SQL
    -- Seeds para tabla skills_keywords
    INSERT INTO skills_keywords (id, status, created_at, updated_at, skill_id, keyword_id) VALUES
    ('ad8ae172-7bac-43f9-b63c-442b08e63af6', 'active', '2024-11-05 03:45:21', NULL, 'fc3f102d-d9ca-48e6-8d9f-baa5498bdbf1', '8634e2fe-0291-4a3c-a887-d08a75fd0a08'),
    ('b655e039-d494-4f9f-a632-2f623c2f34b8', 'active', '2024-11-05 03:45:21', NULL, 'eded4336-7856-4a66-a34f-207e0a928778', '9076730c-e653-458e-8990-619d3695cdb0'),
    ('371dd360-0ca4-49ac-a75a-91e4fc106939', 'active', '2024-11-05 03:45:21', NULL, '72151a85-ff9f-4d86-91ca-af20572af3c6', '57c13c17-6d5d-47cc-8af1-8d3c3082cb44'),
    ('ffdf3503-3173-47f6-a985-837517e0796f', 'active', '2024-11-05 03:45:21', NULL, '74283b85-5178-4263-89a8-129649fcf2f3', '625c0049-7a8b-4296-9bb9-cfafb9d4c59b'),
    ('122be596-06fd-4812-9364-cb9f1745bfbd', 'active', '2024-11-05 03:45:21', NULL, '9c3bb81c-fc05-48ce-a726-2367664951ed', '7bc8818f-ab52-4864-931e-e33838ad67d9'),
    ('6dab73c9-18c6-4d02-8fad-e85d31e0ebdb', 'active', '2024-11-05 03:45:21', NULL, '33c2264e-f818-4eb9-819d-e202f2dbf6b8', 'a9fb1469-ee20-4a29-acc9-154978f198eb'),
    ('a2fdfddd-cdef-412f-8399-f69de86e3605', 'active', '2024-11-05 03:45:21', NULL, '0b3eca7d-0c48-4979-b97b-40c0057d8d8e', '0fe8a3c2-dcf3-4080-949b-2f9e00a1d904'),
    ('134bf873-70ec-40ff-bdf8-877fd39c6d52', 'active', '2024-11-05 03:45:21', NULL, '4b4e296f-a9a2-4ca3-84c9-bba1349ec732', '005e8383-bcb2-48ec-aed7-22d806027a44'),
    ('c4dfb21c-7176-47c4-b607-51ffc6e6574d', 'active', '2024-11-05 03:45:21', NULL, '62ff3306-c8f8-4522-a06c-80acb5033579', '9dceefb0-5ce5-458e-b275-074f2264834a'),
    ('97f51055-0458-4b5e-a993-1207222f3438', 'active', '2024-11-05 03:45:21', NULL, '345f953c-d2a9-4503-bf75-ffe232829774', '7b2d7a88-1283-4918-bcb8-d7ac81919234'),
    ('c9f11d63-7020-4bcb-a3e7-0b2fb061596c', 'active', '2024-11-05 03:45:21', NULL, '2c558182-4abc-43ab-baa2-16549f314b5b', 'baa15484-6188-49d0-a0aa-24fec89f8958'),
    ('d8d9695e-d8a9-4afc-97ce-b06e8e7fd86c', 'active', '2024-11-05 03:45:21', NULL, '38045df5-168f-4bf2-832e-3d2b387e542f', 'ef3fcacf-5be1-491b-a37c-97da33f2f318'),
    ('881c9652-4880-444b-82a6-a4dc7072d911', 'active', '2024-11-05 03:45:21', NULL, '7a350f7b-978f-4fa9-b10e-f30a4be32140', 'b2ff7308-914a-421f-bb4f-ceeee179de21'),
    ('1c5f2b63-00f6-427a-b42d-6a610fc883fb', 'active', '2024-11-05 03:45:21', NULL, '1522fe72-4e97-4412-8458-330742d6545a', '19adecf0-4c74-4175-810d-7086a4dda003'),
    ('7af8bb24-73b6-4bdf-bdea-bf007950c8b9', 'active', '2024-11-05 03:45:21', NULL, '1d76df3e-e720-415c-b466-9afdff9f51c7', '5c093de5-0cf7-4415-bb73-7218719ff2cf'),
    ('9736b182-8695-4b54-b5a0-63370a086167', 'active', '2024-11-05 03:45:21', NULL, '5e44606c-6638-42f7-b942-3ba709b6ac15', 'eadf41f5-89f8-4f90-affd-d46c657dcc8d'),
    ('837b4157-7c1f-45e2-aa48-e146a67f41d2', 'active', '2024-11-05 03:45:21', NULL, 'f6b57e1f-2487-40e6-ab1c-66fd2e4ec081', 'e6381ea2-1ead-4c11-a59f-45e58adcb058'),
    ('c85edecf-128f-47b2-b079-97d4a1949ae0', 'active', '2024-11-05 03:45:21', NULL, '2c826599-e414-420c-ad70-a6468abb61dd', '6370b97b-60a2-4ce5-8251-51fbaacef1cf'),
    ('391b23ff-73c5-424c-b02e-53fa54155183', 'active', '2024-11-05 03:45:21', NULL, '01c95d24-0e9e-4d2b-bebc-ebe953956db8', '56aa6a30-9805-419f-8a54-c69d72d460cd'),
    ('b44ae929-6cc6-4975-a0b3-21d2f8f1e2ed', 'active', '2024-11-05 03:45:21', NULL, '3c98b1a2-b1c8-4f0c-9a60-3c091d8d9643', '803bc6f7-7bd6-4314-8e36-b49a209ff9fa'),
    ('f3ebf979-437f-4c41-8d3a-d45cf26ada50', 'active', '2024-11-05 03:45:21', NULL, '6a0bc669-ffc4-4d2d-a962-c3e3908d0a47', 'e38b66ed-aae1-4e92-9610-0c4be1306fca'),
    ('1d027744-0dbe-4f60-bdca-4fb0c22cbb52', 'active', '2024-11-05 03:45:21', NULL, 'caf983c9-57ea-414d-9c27-db2918bb493c', '81fee466-dbc4-4622-87d8-713b958ff1ce'),
    ('a81a90e6-3908-448c-83b9-ecbc2fb254bc', 'active', '2024-11-05 03:45:21', NULL, '18252393-5722-4c4d-b565-6e0c81e6783e', '55eac891-f42c-4083-82ab-c0574170cb77'),
    ('ca99872a-d4f9-4e47-a2d0-5b69951ba7e0', 'active', '2024-11-05 03:45:21', NULL, '4ce4fa68-5a69-468e-8257-0e6e06c3e605', 'e5a5735c-5112-4fda-b89a-e2ff42c9a542'),
    ('ee6b0a27-97f0-4332-9d9b-0f58122a35bd', 'active', '2024-11-05 03:45:21', NULL, '37977b9b-afb8-470f-80fd-ebb3a1d03611', '1d3623ac-437e-49a6-9bec-d04864cd573f'),
    ('9c85e811-a279-41c9-a039-d5263ce3fc17', 'active', '2024-11-05 03:45:21', NULL, '79ca3de7-05e2-4e72-8aa2-a88b8518a3d1', 'dea86777-d74a-4c58-bab5-b78c2b3bb122'),
    ('93f68faa-f20b-4b8c-9d4a-8b15d9b0efbf', 'active', '2024-11-05 03:45:21', NULL, '279e8e9e-74c0-4a2d-84a5-89498bd3d810', '1e4466ea-58d5-4035-8737-105457a246dc'),
    ('19cc7e6b-0f87-4684-a232-2f22594d9e2c', 'active', '2024-11-05 03:45:21', NULL, 'fcae64e6-a748-496d-8b75-781e2e2c4248', 'fbae24b4-1a71-4aa4-8460-4cd4249ce142'),
    ('dba6b4ac-d9a8-455d-a172-27fa9ea395bb', 'active', '2024-11-05 03:45:21', NULL, 'd5c7a99d-07e4-49b6-aadd-388bdce81d45', '633fdba6-9bd7-4062-8749-72a6d030629f'),
    ('51c6c2d4-1b3f-4f6d-b236-3b4ec3fbfdf2', 'active', '2024-11-05 03:45:21', NULL, '7423e816-8813-48eb-a9b6-e81b35e86e70', 'aa520175-a67a-46bb-8c13-2236038279c1'),
    ('3190ac2e-bf98-4dd2-aa0a-89c253285c09', 'active', '2024-11-05 03:45:21', NULL, '747b3050-5b33-4cf8-b07c-b7f0b551835b', 'd23bac0d-0dc2-4cc9-99fb-6e6bf2eb5628'),
    ('8caa0322-467b-498f-aea8-ea9a5ae0b2c5', 'active', '2024-11-05 03:45:21', NULL, '81584e13-d652-45cd-ae2f-68324cbda054', '63e9b05a-b620-4c83-a020-503f98ec1160'),
    ('aa5b3d87-7d57-44e3-8c80-2e891cf41d64', 'active', '2024-11-05 03:45:21', NULL, '6a46a59c-55f1-48a5-aa06-46e74581f19a', '6bd81652-a4d4-4d2e-a4da-8846186bc1dc'),
    ('e16f8f25-6994-46d5-977f-271e79fa6b1c', 'active', '2024-11-05 03:45:21', NULL, 'c76f2842-947c-4f3a-8b50-da56fe1612fe', 'eda06854-2aaf-4ec9-8fbb-99241767551c'),
    ('cc0b3613-faf8-458c-bb3c-39565a02c7cc', 'active', '2024-11-05 03:45:21', NULL, '7933efae-4bef-430c-9a8b-98be945f2260', '238fde2d-b464-4153-88ff-806337efd507'),
    ('6096cd19-a4b6-479a-8df0-b279b469ab19', 'active', '2024-11-05 03:45:21', NULL, '733d7808-679e-445d-b321-c601491eb0b8', '87f3a7fd-b62e-4a1d-8d8b-da90c2d83b4a'),
    ('4012b21d-1730-4dbf-a6a0-112534d2d36c', 'active', '2024-11-05 03:45:21', NULL, '70436d46-bae5-46f8-9ce8-c3ce0ed71f7d', '3b173045-7ffe-4c30-89f3-6cbf4347e64b'),
    ('4b43ff59-5a4c-4a6b-bad2-428551bf3949', 'active', '2024-11-05 03:45:21', NULL, '6c308f1e-a93f-490a-af17-c0da5d932ddc', '5aa21161-0b46-4bcc-a762-d4da32fc9000'),
    ('cdd725e4-ffc4-4b3f-ae9e-c2b77f65ec45', 'active', '2024-11-05 03:45:21', NULL, 'aff49dd5-4a69-43c4-8f86-3829b58635d7', 'e4142c6c-d33f-46c4-9338-ca893f7c911f'),
    ('b2950804-de5b-4bcf-a42b-db9ba972a626', 'active', '2024-11-05 03:45:21', NULL, 'ff9b80e3-ecb0-474e-b1b6-0844667f7812', '8506b884-4237-4fa7-ac7b-7ce312423900'),
    ('b859d06f-0b1d-4bba-8a4c-2b3004fb54ca', 'active', '2024-11-05 03:45:21', NULL, 'ba892ff0-4beb-4046-be4f-bc93e49be0a6', 'd4533dbd-8829-4ac3-bfd9-5eaf9264f478'),
    ('7db87d32-be4d-47dc-9e86-47edfc3cf3f3', 'active', '2024-11-05 03:45:21', NULL, '7d1e0231-2fcb-41c5-888f-b31b55953dc1', 'bfe563e9-f5d2-45b3-94c0-3186ebf87664'),
    ('bcdd5612-2c65-4c61-afce-cb1de618a96a', 'active', '2024-11-05 03:45:21', NULL, '769eaf1d-c241-43fd-a551-95e0b3f2d371', '1667475d-76aa-402d-b510-c87599298f47'),
    ('9e905a32-a89c-4365-b6d2-a09037e3f9fa', 'active', '2024-11-05 03:45:21', NULL, 'b740f947-2c3b-4485-9fbb-c39239617103', '9c56a8e9-2ffd-45d1-8b35-6dfbec53a8b9'),
    ('444b0b79-8bff-4f2b-85b1-34a6043c3a02', 'active', '2024-11-05 03:45:21', NULL, 'd6f6ee1c-5587-48f0-8aca-d7d535cf1f86', '707d2675-e34c-4364-b800-f3bc2b50f6b1'),
    ('840908e6-314c-4cdc-9056-a2c861588aeb', 'active', '2024-11-05 03:45:21', NULL, '6edf343d-8c6a-40e3-ada6-fce8d02d53ed', '5c6e22b5-e490-40b5-af76-484e10c349f3'),
    ('ff848757-5d6c-416b-acdc-b529ec7e28e7', 'active', '2024-11-05 03:45:21', NULL, '56016d50-8737-46cd-8443-d7ec4f736e64', 'becc67d6-4fba-46f8-a81e-00f3b05e4e20'),
    ('963ebee7-1993-452d-993f-7dcc3ce0a14e', 'active', '2024-11-05 03:45:21', NULL, 'bc6a29dd-8272-4b14-9247-4a0c14d0abe2', '0764a9ff-cb3b-426b-b3e3-b68cb5fd80f6'),
    ('416f0fc4-1f0a-4c64-8bd6-afebd4f45fa8', 'active', '2024-11-05 03:45:21', NULL, 'f57d23b2-e890-4b10-844f-b549f7923fad', '179e126f-a93d-4727-bf8b-f53796cd6e61'),
    ('149dd2af-c61a-43a6-ab98-bb66dfa7321a', 'active', '2024-11-05 03:45:21', NULL, '7005222a-840e-44ca-85db-edd46943f480', '6cb8672c-6c1e-4726-bd1b-48b8d17d315d'),
    ('8baa79e3-fc13-4395-9808-b010bc7dbe9d', 'active', '2024-11-05 03:45:21', NULL, 'df9e0f3f-3825-4d4d-9c4f-e2a320e70c83', '879ccfba-3d4d-4ec9-abc5-7db02be0e1dd'),
    ('0aa44293-241d-4332-aabd-ef688da3f7ed', 'active', '2024-11-05 03:45:21', NULL, '6e6dff96-e51d-405b-92e1-e1e696360286', '45aa8cc1-a0f6-4399-9689-433478d1a583'),
    ('b4b6fac0-1b29-41f9-a5fb-20a117fea28a', 'active', '2024-11-05 03:45:21', NULL, '06c33a71-e925-4752-8938-0a6bc739cf3b', 'e702e811-786b-48f6-a0ae-20ede476f5b6'),
    ('5b439110-647a-4053-844f-b1645b032302', 'active', '2024-11-05 03:45:21', NULL, 'c26fa02f-e2d4-4ec9-877b-fb4377087a72', '47e78cc5-fb5d-4f35-99ff-8472fd7645e2'),
    ('e5e0846b-1104-474f-83e7-f7b83d186afe', 'active', '2024-11-05 03:45:21', NULL, 'e98f620a-51fb-47ac-a824-364b8be2012c', '450958b9-92b7-4262-8c23-d73d5bef8aa4');
  SQL
}

locals {
  skills_keywords_columns = ['id', 'status', 'created_at', 'updated_at', 'skill_id', 'keyword_id']
  skills_keywords_row_count = 55
}

# Test básico para validar la tabla
test "schema" "skills_keywords_exists" {
  exec {
    sql = "SELECT COUNT(*) FROM information_schema.tables WHERE table_name = 'skills_keywords';"
    output = "1"
  }
}
