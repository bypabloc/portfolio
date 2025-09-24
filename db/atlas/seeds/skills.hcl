# Atlas Seed: skills
# Generado: 2025-09-23T22:04:31.825945
# Total filas: 91

plan "seed_skills" {
  migration = <<-SQL
    -- Seeds para tabla skills
    INSERT INTO skills (id, status, created_at, updated_at, code_name, name, description, type) VALUES
    ('fc3f102d-d9ca-48e6-8d9f-baa5498bdbf1', 'active', '2024-11-05 03:44:11', NULL, 'docker', 'Docker', 'Contenedores para el despliegue de aplicaciones.', 'technical'),
    ('eded4336-7856-4a66-a34f-207e0a928778', 'active', '2024-11-05 03:44:11', NULL, 'kubernetes', 'Kubernetes', 'Orquestador de contenedores para el despliegue de aplicaciones.', 'technical'),
    ('72151a85-ff9f-4d86-91ca-af20572af3c6', 'active', '2024-11-05 03:44:11', NULL, 'react', 'React', 'Framework JavaScript para la creación de interfaces de usuario.', 'technical'),
    ('74283b85-5178-4263-89a8-129649fcf2f3', 'active', '2024-11-05 03:44:11', NULL, 'node', 'Node.js', 'Entorno de ejecución de JavaScript para el desarrollo de aplicaciones backend.', 'technical'),
    ('9c3bb81c-fc05-48ce-a726-2367664951ed', 'active', '2024-11-05 03:44:11', NULL, 'sql', 'SQL', 'Lenguaje de consulta estructurado para bases de datos.', 'technical'),
    ('33c2264e-f818-4eb9-819d-e202f2dbf6b8', 'active', '2024-11-05 03:44:11', NULL, 'python', 'Python', 'Lenguaje de programación utilizado en el desarrollo de microservicios.', 'technical'),
    ('0b3eca7d-0c48-4979-b97b-40c0057d8d8e', 'active', '2024-11-05 03:44:11', NULL, 'django', 'Django', 'Framework web para Python utilizado en el desarrollo de backend.', 'technical'),
    ('4b4e296f-a9a2-4ca3-84c9-bba1349ec732', 'active', '2024-11-05 03:44:11', NULL, 'microservices', 'Microservices', 'Arquitectura de microservicios para el desarrollo de aplicaciones escalables.', 'technical'),
    ('62ff3306-c8f8-4522-a06c-80acb5033579', 'active', '2024-11-05 03:44:11', NULL, 'aws', 'AWS', 'Plataforma de servicios en la nube utilizada para implementación y despliegue.', 'technical'),
    ('345f953c-d2a9-4503-bf75-ffe232829774', 'active', '2024-11-05 03:44:11', NULL, 'frontend-architecture', 'Frontend Architecture', 'Diseño de la arquitectura de la aplicación frontend.', 'technical'),
    ('4756c94e-9454-4f38-bfa5-e2b32b1016c5', 'active', '2024-11-05 03:44:11', NULL, 'optimization', 'Optimization', 'Mejora de la eficiencia y el rendimiento de los sistemas.', 'technical'),
    ('01c95d24-0e9e-4d2b-bebc-ebe953956db8', 'active', '2024-11-05 03:44:11', NULL, 'automation', 'Automation', 'Automatización de procesos para mejorar la eficiencia.', 'technical'),
    ('9318f070-f6fc-400a-af72-e93f478cc505', 'active', '2024-11-05 03:44:11', NULL, 'fintech', 'Fintech', 'Conocimiento específico del mercado financiero.', 'soft'),
    ('d6a9740d-99ed-40a3-9405-823d57e4d1f3', 'active', '2024-11-05 03:44:11', NULL, 'strategic-planning', 'Strategic Planning', 'Planificación estratégica para la entrega de soluciones.', 'soft'),
    ('2c558182-4abc-43ab-baa2-16549f314b5b', 'active', '2024-11-05 03:44:11', NULL, 'vue', 'Vue.js', 'Framework JavaScript para la creación de interfaces de usuario.', 'technical'),
    ('38045df5-168f-4bf2-832e-3d2b387e542f', 'active', '2024-11-05 03:44:11', NULL, 'nuxt', 'Nuxt.js', 'Framework de desarrollo web basado en Vue.js.', 'technical'),
    ('7a350f7b-978f-4fa9-b10e-f30a4be32140', 'active', '2024-11-05 03:44:11', NULL, 'typescript', 'TypeScript', 'Lenguaje de programación tipado.', 'technical'),
    ('1522fe72-4e97-4412-8458-330742d6545a', 'active', '2024-11-05 03:44:11', NULL, 'frontend-development', 'Frontend Development', 'Desarrollo frontend para mejorar la experiencia del usuario.', 'technical'),
    ('1d76df3e-e720-415c-b466-9afdff9f51c7', 'active', '2024-11-05 03:44:11', NULL, 'web-development', 'Web Development', 'Desarrollo de aplicaciones web.', 'technical'),
    ('17beb0ae-01d4-466f-82eb-f62f1bce96dc', 'active', '2024-11-05 03:44:11', NULL, 'quality-improvement', 'Quality Improvement', 'Mejora de la calidad en el desarrollo de software.', 'technical'),
    ('54289fa3-9ea4-4305-8911-a72ce5b93f5c', 'active', '2024-11-05 03:44:11', NULL, 'backend-development', 'Backend Development', 'Desarrollo de aplicaciones backend con Python y Django.', 'technical'),
    ('0a0401b1-eef3-4431-ab41-6bcc0d4a0979', 'active', '2024-11-05 03:44:11', NULL, 'learning-agility', 'Learning Agility', 'Habilidad para aprender y aplicar nuevas tecnologías.', 'soft'),
    ('5e44606c-6638-42f7-b942-3ba709b6ac15', 'active', '2024-11-05 03:44:11', NULL, 'erp', 'ERP', 'Desarrollo de sistemas de planificación de recursos empresariales.', 'technical'),
    ('2c826599-e414-420c-ad70-a6468abb61dd', 'active', '2024-11-05 03:44:11', NULL, 'ecommerce', 'E-commerce', 'Desarrollo de soluciones de comercio electrónico.', 'technical'),
    ('3c98b1a2-b1c8-4f0c-9a60-3c091d8d9643', 'active', '2024-11-05 03:44:11', NULL, 'startup', 'Startup', 'Gestión y desarrollo de startups.', 'soft'),
    ('b68fce3c-36cf-499e-b50c-cb8d02cc4140', 'active', '2024-11-05 03:44:11', NULL, 'technical-knowledge', 'technical Knowledge', 'Conocimientos técnicos en múltiples áreas.', 'technical'),
    ('36ff46cb-ddbb-4594-9fba-c36bb559bf47', 'active', '2024-11-05 03:44:11', NULL, 'sales', 'Sales', 'Manejo de ventas y clientes.', 'soft'),
    ('8680b238-85b4-4d1d-ae0b-251610b80fd5', 'active', '2024-11-05 03:44:11', NULL, 'business-management', 'Business Management', 'Gestión empresarial.', 'soft'),
    ('f0d69041-ab71-4b4c-9a21-f9e3047dd305', 'active', '2024-11-05 03:44:11', NULL, 'customer-relationship', 'Customer Relationship', 'Gestión de relaciones con los clientes.', 'soft'),
    ('4e3672d0-d9eb-4fae-9e2d-f9e437a106ce', 'active', '2024-11-05 03:44:11', NULL, 'self-motivation', 'Self Motivation', 'Automotivación y capacidad para gestionar proyectos personales.', 'soft'),
    ('6a0bc669-ffc4-4d2d-a962-c3e3908d0a47', 'active', '2024-11-05 03:44:11', NULL, 'full-stack-development', 'Full Stack Development', 'Desarrollo frontend y backend.', 'technical'),
    ('40c6f4d6-000f-4666-9c67-9d3dde5890fe', 'active', '2024-11-05 03:44:11', NULL, 'javascript', 'JavaScript', 'Lenguaje de programación utilizado en el desarrollo web.', 'technical'),
    ('caf983c9-57ea-414d-9c27-db2918bb493c', 'active', '2024-11-05 03:44:11', NULL, 'vue3', 'Vue 3', 'Framework JavaScript para la creación de interfaces de usuario.', 'technical'),
    ('18252393-5722-4c4d-b565-6e0c81e6783e', 'active', '2024-11-05 03:44:11', NULL, 'scrum', 'Scrum', 'Framework de desarrollo ágil.', 'technical'),
    ('4ce4fa68-5a69-468e-8257-0e6e06c3e605', 'active', '2024-11-05 03:44:11', NULL, 'bug-fixing', 'Bug Fixing', 'Corrección de errores de software.', 'technical'),
    ('37977b9b-afb8-470f-80fd-ebb3a1d03611', 'active', '2024-11-05 03:44:11', NULL, 'web-application', 'Web Application', 'Desarrollo de aplicaciones web.', 'technical'),
    ('e8208f1c-8365-44dc-a7b4-27f9224a313f', 'active', '2024-11-05 03:44:11', NULL, 'adaptability-startups', 'Adaptability to Startups', 'Adaptación a los cambios en entornos de startups.', 'soft'),
    ('5165d8d3-f46f-4951-9237-f794ce823063', 'active', '2024-11-05 03:44:11', NULL, 'problem-solving', 'Problem Solving', 'Habilidad para solucionar problemas técnicos complejos.', 'soft'),
    ('05c85f6c-becf-4a0f-8b3d-4b486a0d6bf9', 'active', '2024-11-05 03:44:11', NULL, 'teamwork', 'Teamwork', 'Colaboración efectiva con un equipo de desarrollo.', 'soft'),
    ('79ca3de7-05e2-4e72-8aa2-a88b8518a3d1', 'active', '2024-11-05 03:44:11', NULL, 'team-leadership', 'Team Leadership', 'Liderazgo efectivo de equipos de desarrollo.', 'soft'),
    ('279e8e9e-74c0-4a2d-84a5-89498bd3d810', 'active', '2024-11-05 03:44:11', NULL, 'aws-deployment', 'AWS Deployment', 'Despliegue de aplicaciones en Amazon Web Services.', 'technical'),
    ('fcae64e6-a748-496d-8b75-781e2e2c4248', 'active', '2024-11-05 03:44:11', NULL, 'laravel', 'Laravel', 'Framework PHP para el desarrollo backend.', 'technical'),
    ('d5c7a99d-07e4-49b6-aadd-388bdce81d45', 'active', '2024-11-05 03:44:11', NULL, 'system-architecture', 'System Architecture', 'Diseño de arquitectura de sistemas.', 'technical'),
    ('7423e816-8813-48eb-a9b6-e81b35e86e70', 'active', '2024-11-05 03:44:11', NULL, 'microfrontend', 'Microfrontend', 'Arquitectura de microfrontends.', 'technical'),
    ('a82b3747-86ee-4196-a4b4-469d4002ed81', 'active', '2024-11-05 03:44:11', NULL, 'ecommerce-development', 'E-commerce Development', 'Desarrollo de soluciones de comercio electrónico.', 'technical'),
    ('872de34a-ec8f-4b81-bb94-7aba9294ecdd', 'active', '2024-11-05 03:44:11', NULL, 'cloud-computing', 'Cloud Computing', 'Uso de tecnologías en la nube para el desarrollo y despliegue.', 'technical'),
    ('1f0843be-bf6d-4fa1-a092-0c191ab5243a', 'active', '2024-11-05 03:44:11', NULL, 'agile-methodologies', 'Agile Methodologies', 'Metodologías ágiles para gestión de proyectos.', 'soft'),
    ('5955fb79-fca0-4078-869b-4172fbf70503', 'active', '2024-11-05 03:44:11', NULL, 'team-management', 'Team Management', 'Gestión efectiva de equipos.', 'soft'),
    ('9bcb4f0a-7e98-4879-a416-3f3fdcf275f1', 'active', '2024-11-05 03:44:11', NULL, 'customer-oriented', 'Customer Oriented', 'Enfoque en la experiencia del cliente.', 'soft'),
    ('747b3050-5b33-4cf8-b07c-b7f0b551835b', 'active', '2024-11-05 03:44:11', NULL, 'production-monitoring', 'Production Monitoring', 'Monitoreo de la producción en sistemas de manufactura.', 'technical'),
    ('81584e13-d652-45cd-ae2f-68324cbda054', 'active', '2024-11-05 03:44:11', NULL, 'productivity-analysis', 'Productivity Analysis', 'Análisis de productividad para la mejora continua.', 'technical'),
    ('6a46a59c-55f1-48a5-aa06-46e74581f19a', 'active', '2024-11-05 03:44:11', NULL, 'local-network', 'Local Network', 'Gestión de redes locales.', 'technical'),
    ('c76f2842-947c-4f3a-8b50-da56fe1612fe', 'active', '2024-11-05 03:44:11', NULL, 'jquery', 'jQuery', 'Biblioteca JavaScript para manipulación de DOM.', 'technical'),
    ('7933efae-4bef-430c-9a8b-98be945f2260', 'active', '2024-11-05 03:44:11', NULL, 'web-platform', 'Web Platform', 'Desarrollo de plataformas web.', 'technical'),
    ('e35dbfbe-83b1-476a-b28b-c558380f50cc', 'active', '2024-11-05 03:44:11', NULL, 'business-analytics', 'Business Analytics', 'Análisis de datos empresariales.', 'technical'),
    ('aa33def6-65d0-4b46-9f9a-543d7000371c', 'active', '2024-11-05 03:44:11', NULL, 'security-management', 'Security Management', 'Gestión de seguridad en sistemas empresariales.', 'technical'),
    ('d5e80490-7f2e-4da5-a2b9-8f55fa816143', 'active', '2024-11-05 03:44:11', NULL, 'data-analysis', 'Data Analysis', 'Análisis de datos para la mejora de procesos.', 'technical'),
    ('ff9b80e3-ecb0-474e-b1b6-0844667f7812', 'active', '2024-11-05 03:44:11', NULL, 'team-collaboration', 'Team Collaboration', 'Colaboración efectiva en equipo.', 'soft'),
    ('733d7808-679e-445d-b321-c601491eb0b8', 'active', '2024-11-05 03:44:11', NULL, 'graduation-project', 'Graduation Project', 'Dirección e implementación de proyectos de grado.', 'technical'),
    ('70436d46-bae5-46f8-9ce8-c3ce0ed71f7d', 'active', '2024-11-05 03:44:11', NULL, 'technical-challenges', 'technical Challenges', 'Resolución de desafíos técnicos complejos.', 'technical'),
    ('6c308f1e-a93f-490a-af17-c0da5d932ddc', 'active', '2024-11-05 03:44:11', NULL, 'project-direction', 'Project Direction', 'Dirección y gestión de proyectos.', 'soft'),
    ('aff49dd5-4a69-43c4-8f86-3829b58635d7', 'active', '2024-11-05 03:44:11', NULL, 'solution-implementation', 'Solution Implementation', 'Implementación de soluciones técnicas.', 'technical'),
    ('3418cdb5-a581-4ef5-94ae-8919b4235664', 'active', '2024-11-05 03:44:11', NULL, 'technical-consulting', 'technical Consulting', 'Asesoramiento técnico para proyectos de grado.', 'soft'),
    ('9bcfea3f-5839-430b-bc54-9ff027bac26c', 'active', '2024-11-05 03:44:11', NULL, 'technical-writing', 'technical Writing', 'Redacción técnica para documentación de proyectos.', 'technical'),
    ('bd4a7c80-5848-4ec4-b626-f0428928d30f', 'active', '2024-11-05 03:44:11', NULL, 'time-management', 'Time Management', 'Gestión efectiva del tiempo para cumplir con los plazos.', 'soft'),
    ('ba892ff0-4beb-4046-be4f-bc93e49be0a6', 'active', '2024-11-05 03:44:11', NULL, 'infrastructure-management', 'Infrastructure Management', 'Gestión de infraestructuras de sistemas.', 'technical'),
    ('7d1e0231-2fcb-41c5-888f-b31b55953dc1', 'active', '2024-11-05 03:44:11', NULL, 'network-architecture', 'Network Architecture', 'Diseño de arquitecturas de redes.', 'technical'),
    ('769eaf1d-c241-43fd-a551-95e0b3f2d371', 'active', '2024-11-05 03:44:11', NULL, 'project-planning', 'Project Planning', 'Planificación efectiva de proyectos.', 'soft'),
    ('b740f947-2c3b-4485-9fbb-c39239617103', 'active', '2024-11-05 03:44:11', NULL, 'work-management', 'Work Management', 'Gestión de proyectos y tareas.', 'soft'),
    ('d6f6ee1c-5587-48f0-8aca-d7d535cf1f86', 'active', '2024-11-05 03:44:11', NULL, 'budget-management', 'Budget Management', 'Gestión de presupuestos de proyectos.', 'soft'),
    ('39871447-008a-4100-bd81-ca07596c174c', 'active', '2024-11-05 03:44:11', NULL, 'system-design', 'System Design', 'Diseño de sistemas informáticos.', 'technical'),
    ('af33d7b8-70ec-4df1-8ef1-3e6732c7112f', 'active', '2024-11-05 03:44:11', NULL, 'software-development', 'software Development', 'Desarrollo de aplicaciones de software.', 'technical'),
    ('0df3e8e7-0c95-4f85-a72e-6c8c18e0baf2', 'active', '2024-11-05 03:44:11', NULL, 'data-management', 'Data Management', 'Gestión de datos para aplicaciones empresariales.', 'technical'),
    ('f6b57e1f-2487-40e6-ab1c-66fd2e4ec081', 'active', '2024-11-05 03:44:11', NULL, 'project-management', 'Project Management', 'Gestión de proyectos técnicos.', 'soft'),
    ('7c8c8117-70c0-4b40-a91e-362f64b48836', 'active', '2024-11-05 03:44:11', NULL, 'collaborative-work', 'Collaborative Work', 'Trabajo colaborativo para el desarrollo de proyectos.', 'soft'),
    ('6edf343d-8c6a-40e3-ada6-fce8d02d53ed', 'active', '2024-11-05 03:44:11', NULL, 'medical-records', 'Medical Records', 'Gestión de historias médicas electrónicas.', 'technical'),
    ('56016d50-8737-46cd-8443-d7ec4f736e64', 'active', '2024-11-05 03:44:11', NULL, 'desktop-application', 'Desktop Application', 'Desarrollo de aplicaciones de escritorio.', 'technical'),
    ('bc6a29dd-8272-4b14-9247-4a0c14d0abe2', 'active', '2024-11-05 03:44:11', NULL, 'java', 'Java', 'Lenguaje de programación para desarrollo de aplicaciones.', 'technical'),
    ('f57d23b2-e890-4b10-844f-b549f7923fad', 'active', '2024-11-05 03:44:11', NULL, 'object-oriented-programming', 'Object Oriented Programming', 'Programación orientada a objetos.', 'technical'),
    ('7005222a-840e-44ca-85db-edd46943f480', 'active', '2024-11-05 03:44:11', NULL, 'requirements-gathering', 'Requirements Gathering', 'Levantamiento de requerimientos técnicos.', 'technical'),
    ('39182c3a-c919-4713-b61a-714c6488f760', 'active', '2024-11-05 03:44:11', NULL, 'software-design', 'software Design', 'Diseño de aplicaciones de software.', 'technical'),
    ('463eccc8-62d3-4551-9304-9370820e86ec', 'active', '2024-11-05 03:44:11', NULL, 'technical-communication', 'technical Communication', 'Comunicación efectiva para el desarrollo técnico.', 'soft'),
    ('d906bcd4-367d-417f-9258-50b183ce3784', 'active', '2024-11-05 03:44:11', NULL, 'analytical-thinking', 'Analytical Thinking', 'Pensamiento analítico para soluciones técnicas.', 'soft'),
    ('267a4b70-cb51-48d3-8bf0-e3a7e42a2df8', 'active', '2024-11-05 03:44:11', NULL, 'adaptability', 'Adaptability', 'Adaptación a tecnologías y desafíos nuevos.', 'soft'),
    ('df9e0f3f-3825-4d4d-9c4f-e2a320e70c83', 'active', '2024-11-05 03:44:11', NULL, 'inventory-management', 'Inventory Management', 'Gestión de inventarios para aplicaciones empresariales.', 'technical'),
    ('6e6dff96-e51d-405b-92e1-e1e696360286', 'active', '2024-11-05 03:44:11', NULL, 'php', 'PHP', 'Lenguaje de programación para desarrollo web.', 'technical'),
    ('06c33a71-e925-4752-8938-0a6bc739cf3b', 'active', '2024-11-05 03:44:11', NULL, 'crud', 'CRUD', 'Operaciones CRUD para bases de datos.', 'technical'),
    ('c26fa02f-e2d4-4ec9-877b-fb4377087a72', 'active', '2024-11-05 03:44:11', NULL, 'offline-system', 'Offline System', 'Desarrollo de sistemas para operar sin conexión.', 'technical'),
    ('e98f620a-51fb-47ac-a824-364b8be2012c', 'active', '2024-11-05 03:44:11', NULL, 'asset-management', 'Asset Management', 'Gestión de activos para aplicaciones empresariales.', 'technical'),
    ('58a4d43f-9efb-4053-96ba-e3beaf7fa66d', 'active', '2024-11-05 03:44:11', NULL, 'data-entry', 'Data Entry', 'Entrada y manipulación de datos.', 'technical'),
    ('ceeb1b58-ad05-4cbc-9ca2-b99b13d9178c', 'active', '2024-11-05 03:44:11', NULL, 'database-management', 'Database Management', 'Gestión de bases de datos.', 'technical');
  SQL
}

locals {
  skills_columns = ['id', 'status', 'created_at', 'updated_at', 'code_name', 'name', 'description', 'type']
  skills_row_count = 91
}

# Test básico para validar la tabla
test "schema" "skills_exists" {
  exec {
    sql = "SELECT COUNT(*) FROM information_schema.tables WHERE table_name = 'skills';"
    output = "1"
  }
}
