# Atlas Seed: interests
# Generado: 2025-09-23T22:04:31.825551
# Total filas: 20

plan "seed_interests" {
  migration = <<-SQL
    -- Seeds para tabla interests
    INSERT INTO interests (id, status, created_at, updated_at, code_name, name) VALUES
    ('107bffe2-a92c-425a-a52d-702e22c3d517', 'active', '2024-11-05 03:44:12', NULL, 'devops', 'DevOps'),
    ('fca2e098-f28d-4ac2-a720-d28bdc2db3b7', 'active', '2024-11-05 03:44:12', NULL, 'bot-creation', 'Creación de Bots'),
    ('0433c0bc-4b4e-44ab-8709-68763ba5b997', 'active', '2024-11-05 03:44:12', NULL, 'scraping', 'Scraping'),
    ('c83f3a20-dc31-4614-a1da-0db0442118f7', 'active', '2024-11-05 03:44:12', NULL, 'kubernetes', 'Kubernetes'),
    ('703594f0-83a9-4185-8eec-72746add6283', 'active', '2024-11-05 03:44:12', NULL, 'machine-learning', 'Machine Learning'),
    ('e50c8956-1c83-425e-8b16-cd38928039f7', 'active', '2024-11-05 03:44:12', NULL, 'cloud-computing', 'Cloud Computing'),
    ('c1f17efc-dff5-4cb9-b2e8-09ad86179275', 'active', '2024-11-05 03:44:12', NULL, 'blockchain', 'Blockchain'),
    ('4975771d-ae4f-4f6b-b0b9-a98d7ec8452f', 'active', '2024-11-05 03:44:12', NULL, 'ai-chatbots', 'AI Chatbots'),
    ('3a5d95b6-118f-4991-b910-840a8e9dd63e', 'active', '2024-11-05 03:44:12', NULL, 'microservices', 'Microservicios'),
    ('69df5a0a-4fc4-4477-830e-260ae5dd6a00', 'active', '2024-11-05 03:44:12', NULL, 'internet-of-things', 'Internet of Things (IoT)'),
    ('5f07c11d-ed04-487d-9e90-7c04cd5e2337', 'active', '2024-11-05 03:44:12', NULL, 'frontend-development', 'Frontend Development'),
    ('8b5f1904-adae-453b-905c-d94abec4d2bc', 'active', '2024-11-05 03:44:12', NULL, 'backend-development', 'Backend Development'),
    ('ec26b6cf-a0ce-455b-a572-2e9a395802d0', 'active', '2024-11-05 03:44:12', NULL, 'data-engineering', 'Data Engineering'),
    ('5beba69c-34ec-433f-9deb-6c788bf41bea', 'active', '2024-11-05 03:44:12', NULL, 'serverless-computing', 'Serverless Computing'),
    ('7541fe66-8b2a-4f43-a1b3-b48ad4be6753', 'active', '2024-11-05 03:44:12', NULL, 'edge-computing', 'Edge Computing'),
    ('853f36ec-ae98-4732-9d16-262c1e7ad0b8', 'active', '2024-11-05 03:44:12', NULL, 'mobile-development', 'Mobile Development'),
    ('a168e681-7cde-4a3b-a2e5-abff36949503', 'active', '2024-11-05 03:44:12', NULL, 'game-development', 'Game Development'),
    ('e2da95e2-ac72-48c8-af26-2721f03061ff', 'active', '2024-11-05 03:44:12', NULL, 'security-engineering', 'Security Engineering'),
    ('eb9ea89c-990b-4456-89b2-94c093ed7e81', 'active', '2024-11-05 03:44:12', NULL, 'robotics', 'Robotics'),
    ('a97dc957-2293-4e7f-9a95-f5e871b45ac9', 'active', '2024-11-05 03:44:12', NULL, 'ar-vr', 'AR/VR');
  SQL
}

locals {
  interests_columns = ['id', 'status', 'created_at', 'updated_at', 'code_name', 'name']
  interests_row_count = 20
}

# Test básico para validar la tabla
test "schema" "interests_exists" {
  exec {
    sql = "SELECT COUNT(*) FROM information_schema.tables WHERE table_name = 'interests';"
    output = "1"
  }
}
