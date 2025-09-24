# Atlas Seed: keywords
# Generado: 2025-09-23T22:04:31.825626
# Total filas: 69

plan "seed_keywords" {
  migration = <<-SQL
    -- Seeds para tabla keywords
    INSERT INTO keywords (id, status, created_at, updated_at, code_name, name, keys) VALUES
    ('c2b82ba4-5b7d-4c99-a119-ce7e3510604b', 'active', '2024-11-05 03:44:08', NULL, 'devops', 'DevOps', '["devops"]'),
    ('8634e2fe-0291-4a3c-a887-d08a75fd0a08', 'active', '2024-11-05 03:44:08', NULL, 'docker', 'Docker', '["docker"]'),
    ('b7329175-9717-4685-a6ee-1ecf80c46cb6', 'active', '2024-11-05 03:44:08', NULL, 'data-analysis', 'Data Analysis', '["data analysis","data-analysis"]'),
    ('9076730c-e653-458e-8990-619d3695cdb0', 'active', '2024-11-05 03:44:08', NULL, 'kubernetes', 'Kubernetes', '["kubernetes"]'),
    ('7bc8818f-ab52-4864-931e-e33838ad67d9', 'active', '2024-11-05 03:44:08', NULL, 'sql', 'SQL', '["sql"]'),
    ('625c0049-7a8b-4296-9bb9-cfafb9d4c59b', 'active', '2024-11-05 03:44:08', NULL, 'node', 'Node.js', '["node","nodejs"]'),
    ('57c13c17-6d5d-47cc-8af1-8d3c3082cb44', 'active', '2024-11-05 03:44:08', NULL, 'react', 'React', '["react"]'),
    ('f91d3def-9273-43c3-a502-84e62b8d0b5c', 'active', '2024-11-05 03:44:08', NULL, 'javascript', 'JavaScript', '["javascript","js"]'),
    ('a9fb1469-ee20-4a29-acc9-154978f198eb', 'active', '2024-11-05 03:44:08', NULL, 'python', 'Python', '["python","py"]'),
    ('0fe8a3c2-dcf3-4080-949b-2f9e00a1d904', 'active', '2024-11-05 03:44:08', NULL, 'django', 'Django', '["django"]'),
    ('005e8383-bcb2-48ec-aed7-22d806027a44', 'active', '2024-11-05 03:44:08', NULL, 'microservices', 'Microservices', '["microservices"]'),
    ('9dceefb0-5ce5-458e-b275-074f2264834a', 'active', '2024-11-05 03:44:08', NULL, 'aws', 'AWS', '["aws","amazon web services"]'),
    ('7b2d7a88-1283-4918-bcb8-d7ac81919234', 'active', '2024-11-05 03:44:08', NULL, 'frontend-architecture', 'Frontend Architecture', '["frontend architecture","frontend-architecture"]'),
    ('baa15484-6188-49d0-a0aa-24fec89f8958', 'active', '2024-11-05 03:44:08', NULL, 'vue', 'Vue.js', '["vue","vuejs"]'),
    ('ef3fcacf-5be1-491b-a37c-97da33f2f318', 'active', '2024-11-05 03:44:08', NULL, 'nuxt', 'Nuxt.js', '["nuxt","nuxtjs"]'),
    ('b2ff7308-914a-421f-bb4f-ceeee179de21', 'active', '2024-11-05 03:44:08', NULL, 'typescript', 'TypeScript', '["typescript","ts"]'),
    ('19adecf0-4c74-4175-810d-7086a4dda003', 'active', '2024-11-05 03:44:08', NULL, 'frontend-development', 'Frontend Development', '["frontend development","frontend-development"]'),
    ('5c093de5-0cf7-4415-bb73-7218719ff2cf', 'active', '2024-11-05 03:44:08', NULL, 'web-development', 'Web Development', '["web development","web-development"]'),
    ('eadf41f5-89f8-4f90-affd-d46c657dcc8d', 'active', '2024-11-05 03:44:08', NULL, 'erp', 'ERP', '["erp"]'),
    ('e6381ea2-1ead-4c11-a59f-45e58adcb058', 'active', '2024-11-05 03:44:08', NULL, 'project-management', 'Project Management', '["project management","project-management"]'),
    ('6370b97b-60a2-4ce5-8251-51fbaacef1cf', 'active', '2024-11-05 03:44:08', NULL, 'ecommerce', 'E-commerce', '["ecommerce","e-commerce"]'),
    ('56aa6a30-9805-419f-8a54-c69d72d460cd', 'active', '2024-11-05 03:44:08', NULL, 'automation', 'Automation', '["automation"]'),
    ('803bc6f7-7bd6-4314-8e36-b49a209ff9fa', 'active', '2024-11-05 03:44:08', NULL, 'startup', 'Startup', '["startup"]'),
    ('e38b66ed-aae1-4e92-9610-0c4be1306fca', 'active', '2024-11-05 03:44:08', NULL, 'full-stack-development', 'Full Stack Development', '["full stack development","full-stack-development"]'),
    ('81fee466-dbc4-4622-87d8-713b958ff1ce', 'active', '2024-11-05 03:44:08', NULL, 'vue3', 'Vue 3', '["vue3","vue 3"]'),
    ('55eac891-f42c-4083-82ab-c0574170cb77', 'active', '2024-11-05 03:44:08', NULL, 'scrum', 'Scrum', '["scrum"]'),
    ('e5a5735c-5112-4fda-b89a-e2ff42c9a542', 'active', '2024-11-05 03:44:08', NULL, 'bug-fixing', 'Bug Fixing', '["bug fixing","bug-fixing"]'),
    ('1d3623ac-437e-49a6-9bec-d04864cd573f', 'active', '2024-11-05 03:44:08', NULL, 'web-application', 'Web Application', '["web application","web-application"]'),
    ('dea86777-d74a-4c58-bab5-b78c2b3bb122', 'active', '2024-11-05 03:44:08', NULL, 'team-leadership', 'Team Leadership', '["team leadership","team-leadership"]'),
    ('1e4466ea-58d5-4035-8737-105457a246dc', 'active', '2024-11-05 03:44:08', NULL, 'aws-deployment', 'AWS Deployment', '["aws deployment","aws-deployment"]'),
    ('fbae24b4-1a71-4aa4-8460-4cd4249ce142', 'active', '2024-11-05 03:44:08', NULL, 'laravel', 'Laravel', '["laravel"]'),
    ('633fdba6-9bd7-4062-8749-72a6d030629f', 'active', '2024-11-05 03:44:08', NULL, 'system-architecture', 'System Architecture', '["system architecture","system-architecture"]'),
    ('aa520175-a67a-46bb-8c13-2236038279c1', 'active', '2024-11-05 03:44:08', NULL, 'microfrontend', 'Microfrontend', '["microfrontend"]'),
    ('d23bac0d-0dc2-4cc9-99fb-6e6bf2eb5628', 'active', '2024-11-05 03:44:08', NULL, 'production-monitoring', 'Production Monitoring', '["production monitoring","production-monitoring"]'),
    ('63e9b05a-b620-4c83-a020-503f98ec1160', 'active', '2024-11-05 03:44:08', NULL, 'productivity-analysis', 'Productivity Analysis', '["productivity analysis","productivity-analysis"]'),
    ('6bd81652-a4d4-4d2e-a4da-8846186bc1dc', 'active', '2024-11-05 03:44:08', NULL, 'local-network', 'Local Network', '["local network","local-network"]'),
    ('eda06854-2aaf-4ec9-8fbb-99241767551c', 'active', '2024-11-05 03:44:08', NULL, 'jquery', 'jQuery', '["jquery","jq"]'),
    ('238fde2d-b464-4153-88ff-806337efd507', 'active', '2024-11-05 03:44:08', NULL, 'web-platform', 'Web Platform', '["web platform","web-platform"]'),
    ('87f3a7fd-b62e-4a1d-8d8b-da90c2d83b4a', 'active', '2024-11-05 03:44:08', NULL, 'graduation-project', 'Graduation Project', '["graduation project","graduation-project"]'),
    ('3b173045-7ffe-4c30-89f3-6cbf4347e64b', 'active', '2024-11-05 03:44:08', NULL, 'technical-challenges', 'technical Challenges', '["technical challenges","technical-challenges"]'),
    ('5aa21161-0b46-4bcc-a762-d4da32fc9000', 'active', '2024-11-05 03:44:08', NULL, 'project-direction', 'Project Direction', '["project direction","project-direction"]'),
    ('e4142c6c-d33f-46c4-9338-ca893f7c911f', 'active', '2024-11-05 03:44:08', NULL, 'solution-implementation', 'Solution Implementation', '["solution implementation","solution-implementation"]'),
    ('8506b884-4237-4fa7-ac7b-7ce312423900', 'active', '2024-11-05 03:44:08', NULL, 'team-collaboration', 'Team Collaboration', '["team collaboration","team-collaboration"]'),
    ('d4533dbd-8829-4ac3-bfd9-5eaf9264f478', 'active', '2024-11-05 03:44:08', NULL, 'infrastructure-management', 'Infrastructure Management', '["infrastructure management","infrastructure-management"]'),
    ('bfe563e9-f5d2-45b3-94c0-3186ebf87664', 'active', '2024-11-05 03:44:08', NULL, 'network-architecture', 'Network Architecture', '["network architecture","network-architecture"]'),
    ('1667475d-76aa-402d-b510-c87599298f47', 'active', '2024-11-05 03:44:08', NULL, 'project-planning', 'Project Planning', '["project planning","project-planning"]'),
    ('9c56a8e9-2ffd-45d1-8b35-6dfbec53a8b9', 'active', '2024-11-05 03:44:08', NULL, 'work-management', 'Work Management', '["work management","work-management"]'),
    ('707d2675-e34c-4364-b800-f3bc2b50f6b1', 'active', '2024-11-05 03:44:08', NULL, 'budget-management', 'Budget Management', '["budget management","budget-management"]'),
    ('5c6e22b5-e490-40b5-af76-484e10c349f3', 'active', '2024-11-05 03:44:08', NULL, 'medical-records', 'Medical Records', '["medical records","medical-records"]'),
    ('becc67d6-4fba-46f8-a81e-00f3b05e4e20', 'active', '2024-11-05 03:44:08', NULL, 'desktop-application', 'Desktop Application', '["desktop application","desktop-application"]'),
    ('0764a9ff-cb3b-426b-b3e3-b68cb5fd80f6', 'active', '2024-11-05 03:44:08', NULL, 'java', 'Java', '["java"]'),
    ('179e126f-a93d-4727-bf8b-f53796cd6e61', 'active', '2024-11-05 03:44:08', NULL, 'object-oriented-programming', 'Object Oriented Programming', '["object oriented programming","object-oriented-programming"]'),
    ('6cb8672c-6c1e-4726-bd1b-48b8d17d315d', 'active', '2024-11-05 03:44:08', NULL, 'requirements-gathering', 'Requirements Gathering', '["requirements gathering","requirements-gathering"]'),
    ('879ccfba-3d4d-4ec9-abc5-7db02be0e1dd', 'active', '2024-11-05 03:44:08', NULL, 'inventory-management', 'Inventory Management', '["inventory management","inventory-management"]'),
    ('45aa8cc1-a0f6-4399-9689-433478d1a583', 'active', '2024-11-05 03:44:08', NULL, 'php', 'PHP', '["php"]'),
    ('e702e811-786b-48f6-a0ae-20ede476f5b6', 'active', '2024-11-05 03:44:08', NULL, 'crud', 'CRUD', '["crud"]'),
    ('47e78cc5-fb5d-4f35-99ff-8472fd7645e2', 'active', '2024-11-05 03:44:08', NULL, 'offline-system', 'Offline System', '["offline system","offline-system"]'),
    ('450958b9-92b7-4262-8c23-d73d5bef8aa4', 'active', '2024-11-05 03:44:08', NULL, 'asset-management', 'Asset Management', '["asset management","asset-management"]'),
    ('6a16e182-6785-4f2d-910a-6e49c5aa9d18', 'active', '2024-11-05 03:44:08', NULL, 'machine-learning', 'Machine Learning', '["machine learning","ml"]'),
    ('76a66280-64c7-454c-a0e1-e1302ff8545a', 'active', '2024-11-05 03:44:08', NULL, 'cloud-computing', 'Cloud Computing', '["cloud computing","cloud-computing"]'),
    ('0e4015c5-2989-4de7-9b1d-8166e0141b16', 'active', '2024-11-05 03:44:08', NULL, 'blockchain', 'Blockchain', '["blockchain"]'),
    ('c98e7a4c-9245-4580-920f-274b8bd8d7c4', 'active', '2024-11-05 03:44:08', NULL, 'ai-chatbots', 'AI Chatbots', '["ai chatbots","chatbots"]'),
    ('93004f9c-f2d6-45bd-8fa9-9dfaf3d2cfb1', 'active', '2024-11-05 03:44:08', NULL, 'internet-of-things', 'Internet of Things (IoT)', '["internet of things","iot"]'),
    ('a251089e-39d8-41ad-b89d-5021f8d176c3', 'active', '2024-11-05 03:44:08', NULL, 'edge-computing', 'Edge Computing', '["edge computing","edge-computing"]'),
    ('f4b3880e-32ad-4a6c-aa99-9f9ad1db8476', 'active', '2024-11-05 03:44:08', NULL, 'mobile-development', 'Mobile Development', '["mobile development","mobile-development"]'),
    ('e3bc39ef-1219-4c5a-b495-d652e35e95c8', 'active', '2024-11-05 03:44:08', NULL, 'game-development', 'Game Development', '["game development","game-development"]'),
    ('e3590a54-913d-409b-8886-5cd031ac1f4c', 'active', '2024-11-05 03:44:08', NULL, 'security-engineering', 'Security Engineering', '["security engineering","security-engineering"]'),
    ('d0f01a5f-21b1-41a6-8e1f-e293198174de', 'active', '2024-11-05 03:44:08', NULL, 'robotics', 'Robotics', '["robotics"]'),
    ('5044c60e-065c-4361-9f26-741af4c95ced', 'active', '2024-11-05 03:44:08', NULL, 'ar-vr', 'AR/VR', '["ar","vr","augmented reality","virtual reality"]');
  SQL
}

locals {
  keywords_columns = ['id', 'status', 'created_at', 'updated_at', 'code_name', 'name', 'keys']
  keywords_row_count = 69
}

# Test básico para validar la tabla
test "schema" "keywords_exists" {
  exec {
    sql = "SELECT COUNT(*) FROM information_schema.tables WHERE table_name = 'keywords';"
    output = "1"
  }
}
