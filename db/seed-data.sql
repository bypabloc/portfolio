-- Sample Data for Portfolio Serverless System
-- Development seed data for testing and demonstration

-- Insert sample personal information
INSERT INTO personal_info (
    full_name, title, email, phone, location, bio,
    linkedin_url, github_url, website_url
) VALUES (
    'Pablo Contreras',
    'Senior Full-Stack Developer & Serverless Architect',
    'pablo@bypabloc.dev',
    '+56 9 XXXX XXXX',
    'Santiago, Chile',
    'Experienced full-stack developer specializing in modern serverless architectures, with expertise in Vue.js, Python, and AWS technologies. Passionate about creating scalable, high-performance web applications using cutting-edge technologies.',
    'https://linkedin.com/in/bypabloc',
    'https://github.com/bypabloc',
    'https://bypabloc.dev'
);

-- Sample skills
INSERT INTO skills (name, category, proficiency_level, years_experience, is_featured, order_index) VALUES
('TypeScript', 'programming', 5, 4.0, TRUE, 1),
('Python', 'programming', 5, 6.0, TRUE, 2),
('Vue.js', 'framework', 5, 4.0, TRUE, 3),
('Astro', 'framework', 4, 1.0, TRUE, 4),
('FastAPI', 'framework', 5, 3.0, TRUE, 5),
('AWS Lambda', 'cloud', 4, 3.0, TRUE, 6),
('PostgreSQL', 'database', 4, 5.0, TRUE, 7),
('Docker', 'tool', 4, 4.0, TRUE, 8),
('Serverless Architecture', 'architecture', 5, 3.0, TRUE, 9),
('TDD', 'methodology', 4, 3.0, TRUE, 10),
('JavaScript', 'programming', 5, 8.0, TRUE, 11),
('Node.js', 'runtime', 4, 5.0, TRUE, 12),
('Git', 'tool', 5, 8.0, TRUE, 13),
('AWS', 'cloud', 4, 3.0, TRUE, 14),
('REST APIs', 'architecture', 5, 6.0, TRUE, 15);

-- Sample experience
INSERT INTO experience (
    company, position, location, start_date, end_date, is_current,
    description, achievements, technologies, order_index
) VALUES (
    'Destacame',
    'Senior Full-Stack Developer',
    'Santiago, Chile',
    '2021-03-01',
    NULL,
    TRUE,
    'Lead development of fintech applications using modern serverless architectures. Focus on payment systems, credit scoring, and financial data validation.',
    ARRAY[
        'Reduced application load time by 60% through serverless optimization',
        'Implemented microservices architecture serving 100k+ daily transactions',
        'Led migration from monolith to serverless AWS Lambda functions',
        'Designed and implemented automated testing pipeline with 90%+ coverage'
    ],
    ARRAY['Vue.js', 'Python', 'AWS Lambda', 'PostgreSQL', 'FastAPI', 'Docker'],
    1
),
(
    'Freelance Developer',
    'Full-Stack Developer',
    'Remote',
    '2019-06-01',
    '2021-02-28',
    FALSE,
    'Developed custom web applications for various clients using modern technologies and best practices.',
    ARRAY[
        'Delivered 15+ successful projects for international clients',
        'Implemented responsive designs with 98% cross-browser compatibility',
        'Reduced client infrastructure costs by 40% through serverless adoption'
    ],
    ARRAY['JavaScript', 'Vue.js', 'Node.js', 'MongoDB', 'AWS'],
    2
);

-- Sample projects
INSERT INTO projects (
    name, title, description, status, technologies, category, featured, order_index
) VALUES (
    'portfolio-serverless',
    'Serverless Portfolio System',
    'Modern serverless portfolio built with Astro v5, AWS Lambda, FastAPI, and Neon PostgreSQL. Features complete separation of concerns, TDD implementation, and sub-300ms cold start performance.',
    'in_progress',
    ARRAY['Astro', 'TypeScript', 'Python', 'FastAPI', 'AWS Lambda', 'PostgreSQL', 'Docker'],
    'fullstack',
    TRUE,
    1
),
(
    'fintech-dashboard',
    'FinTech Analytics Dashboard',
    'Real-time financial data visualization dashboard with advanced analytics and reporting capabilities.',
    'completed',
    ARRAY['Vue.js', 'Python', 'FastAPI', 'PostgreSQL', 'Chart.js'],
    'frontend',
    TRUE,
    2
),
(
    'microservices-api',
    'Microservices Architecture',
    'Scalable microservices architecture handling payment processing and user management for fintech applications.',
    'completed',
    ARRAY['Python', 'FastAPI', 'Docker', 'PostgreSQL', 'Redis', 'AWS Lambda'],
    'backend',
    TRUE,
    3
),
(
    'e-commerce-platform',
    'E-commerce Platform',
    'Full-stack e-commerce solution with shopping cart, payment integration, and admin dashboard.',
    'completed',
    ARRAY['Vue.js', 'Node.js', 'Express', 'MongoDB', 'Stripe'],
    'fullstack',
    FALSE,
    4
);

-- Create relationships between projects and skills
DO $$
DECLARE
    project_id UUID;
    skill_id UUID;
BEGIN
    -- Portfolio Serverless project skills
    SELECT id INTO project_id FROM projects WHERE name = 'portfolio-serverless';

    SELECT id INTO skill_id FROM skills WHERE name = 'TypeScript';
    INSERT INTO project_skills (project_id, skill_id, usage_level) VALUES (project_id, skill_id, 'primary');

    SELECT id INTO skill_id FROM skills WHERE name = 'Python';
    INSERT INTO project_skills (project_id, skill_id, usage_level) VALUES (project_id, skill_id, 'primary');

    SELECT id INTO skill_id FROM skills WHERE name = 'FastAPI';
    INSERT INTO project_skills (project_id, skill_id, usage_level) VALUES (project_id, skill_id, 'primary');

    SELECT id INTO skill_id FROM skills WHERE name = 'PostgreSQL';
    INSERT INTO project_skills (project_id, skill_id, usage_level) VALUES (project_id, skill_id, 'primary');

    -- FinTech Dashboard project skills
    SELECT id INTO project_id FROM projects WHERE name = 'fintech-dashboard';

    SELECT id INTO skill_id FROM skills WHERE name = 'Vue.js';
    INSERT INTO project_skills (project_id, skill_id, usage_level) VALUES (project_id, skill_id, 'primary');

    SELECT id INTO skill_id FROM skills WHERE name = 'Python';
    INSERT INTO project_skills (project_id, skill_id, usage_level) VALUES (project_id, skill_id, 'primary');
END $$;

-- Create relationships between experience and skills
DO $$
DECLARE
    experience_id UUID;
    skill_id UUID;
BEGIN
    -- Destacame experience skills
    SELECT id INTO experience_id FROM experience WHERE company = 'Destacame';

    SELECT id INTO skill_id FROM skills WHERE name = 'Vue.js';
    INSERT INTO experience_skills (experience_id, skill_id, usage_level) VALUES (experience_id, skill_id, 'primary');

    SELECT id INTO skill_id FROM skills WHERE name = 'Python';
    INSERT INTO experience_skills (experience_id, skill_id, usage_level) VALUES (experience_id, skill_id, 'primary');

    SELECT id INTO skill_id FROM skills WHERE name = 'AWS Lambda';
    INSERT INTO experience_skills (experience_id, skill_id, usage_level) VALUES (experience_id, skill_id, 'primary');

    SELECT id INTO skill_id FROM skills WHERE name = 'PostgreSQL';
    INSERT INTO experience_skills (experience_id, skill_id, usage_level) VALUES (experience_id, skill_id, 'primary');
END $$;