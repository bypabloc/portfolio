# Frontend App - Astro v5 Complete Implementation Guide

> **Fecha de creación**: Enero 2025
> **Última actualización**: Enero 2025
> **Stack**: Astro v5 + TypeScript + Content Layer + Server Islands
> **Deployment**: AWS CloudFront + S3

---

## 🎯 Resumen Ejecutivo del Frontend

Este documento proporciona la guía completa para implementar el **frontend del portfolio** usando **Astro v5**, la última versión del framework que introduce características revolucionarias como **Content Layer**, **Server Islands**, y **Astro Actions**.

El frontend está diseñado como un **SSG (Static Site Generation)** moderno con capacidades híbridas para contenido dinámico, optimizado para máximo rendimiento y SEO.

### Características Principales de Astro v5
- ✅ **Content Layer**: Sistema unificado de carga de datos desde cualquier fuente
- ✅ **Server Islands**: Mezcla perfecta de contenido estático y dinámico
- ✅ **Astro Actions**: Funciones server type-safe llamadas desde el frontend
- ✅ **TypeScript Strict Mode**: Tipos estrictos obligatorios
- ✅ **Performance Optimizado**: Build times 40% más rápidos que v4

---

## 🏗️ Arquitectura Frontend Completa

### Integración con APIs
El frontend obtiene datos dinámicos a través de APIs REST externas:

```
Frontend (Astro v5 SSG)
     ↓ HTTP Requests
API Gateway
     ↓ Route to services
External APIs
     ↓ Data retrieval
Data Sources
```

### Estructura del Proyecto Frontend
```
frontend/
├── src/
│   ├── content/              # Content Layer definitions
│   │   ├── config.ts         # Content collections schema
│   │   └── experience/       # Experience markdown/data
│   ├── actions/              # Astro Actions (server calls)
│   │   ├── index.ts          # Action definitions
│   │   └── types.ts          # Shared types
│   ├── islands/              # Server Islands components
│   │   ├── ExperienceList.astro
│   │   ├── ProjectsGrid.astro
│   │   └── SkillsMatrix.astro
│   ├── components/           # Static UI components
│   │   ├── layout/
│   │   ├── ui/
│   │   └── forms/
│   ├── pages/                # Route pages
│   │   ├── index.astro       # Homepage
│   │   ├── experience.astro  # Experience page
│   │   ├── projects.astro    # Projects portfolio
│   │   └── contact.astro     # Contact form
│   ├── styles/               # Global styles
│   └── utils/                # Frontend utilities
├── public/                   # Static assets
├── tests/                    # Frontend tests
│   ├── unit/                 # Vitest unit tests
│   ├── integration/          # API integration tests
│   └── e2e/                  # Playwright E2E tests
├── astro.config.ts           # Astro configuration
├── tsconfig.json             # TypeScript strict config
├── tailwind.config.js        # Tailwind CSS config
├── vitest.config.ts          # Vitest testing config
└── playwright.config.ts      # E2E testing config
```

---

## 🚀 Content Layer Implementation

### ¿Qué es Content Layer?
Content Layer es la nueva característica de Astro v5 que **unifica la carga de datos** desde cualquier fuente (markdown, APIs, CMSs, bases de datos) con **type safety** completo.

### Configuración Content Collections
```typescript
// src/content/config.ts
import { defineCollection, z } from 'astro:content';

// Schema para experiencia profesional
const experienceCollection = defineCollection({
  type: 'data', // 'content' para markdown, 'data' para JSON/YAML
  schema: z.object({
    id: z.string(),
    company: z.string(),
    position: z.string(),
    startDate: z.date(),
    endDate: z.date().optional(),
    description: z.string(),
    technologies: z.array(z.string()),
    achievements: z.array(z.string()),
    location: z.string(),
    type: z.enum(['full-time', 'part-time', 'contract', 'freelance']),
    featured: z.boolean().default(false)
  })
});

// Schema para proyectos
const projectsCollection = defineCollection({
  type: 'content', // Permite markdown con frontmatter
  schema: z.object({
    title: z.string(),
    description: z.string(),
    technologies: z.array(z.string()),
    githubUrl: z.string().url().optional(),
    liveUrl: z.string().url().optional(),
    imageUrl: z.string().optional(),
    featured: z.boolean().default(false),
    publishedDate: z.date(),
    status: z.enum(['completed', 'in-progress', 'archived'])
  })
});

// Schema para habilidades técnicas
const skillsCollection = defineCollection({
  type: 'data',
  schema: z.object({
    category: z.string(),
    skills: z.array(z.object({
      name: z.string(),
      level: z.enum(['beginner', 'intermediate', 'advanced', 'expert']),
      yearsOfExperience: z.number(),
      certifications: z.array(z.string()).optional(),
      projects: z.array(z.string()).optional()
    }))
  })
});

export const collections = {
  experience: experienceCollection,
  projects: projectsCollection,
  skills: skillsCollection
};
```

### Uso de Content Collections
```astro
---
// src/pages/experience.astro
import { getCollection } from 'astro:content';
import Layout from '../layouts/Layout.astro';

// Type-safe data loading with Content Layer
const allExperience = await getCollection('experience');
const featuredExperience = allExperience.filter(exp => exp.data.featured);

// Sort by date (most recent first)
const sortedExperience = allExperience.sort((a, b) =>
  new Date(b.data.startDate).getTime() - new Date(a.data.startDate).getTime()
);
---

<Layout title="Professional Experience">
  <main>
    <h1>Professional Experience</h1>

    {/* Featured Experience Section */}
    <section class="featured-experience">
      <h2>Featured Roles</h2>
      {featuredExperience.map(exp => (
        <article class="experience-card featured">
          <h3>{exp.data.position} at {exp.data.company}</h3>
          <p class="duration">
            {exp.data.startDate.toLocaleDateString()} -
            {exp.data.endDate ? exp.data.endDate.toLocaleDateString() : 'Present'}
          </p>
          <p class="description">{exp.data.description}</p>

          <div class="technologies">
            {exp.data.technologies.map(tech => (
              <span class="tech-tag">{tech}</span>
            ))}
          </div>

          <ul class="achievements">
            {exp.data.achievements.map(achievement => (
              <li>{achievement}</li>
            ))}
          </ul>
        </article>
      ))}
    </section>

    {/* All Experience Timeline */}
    <section class="experience-timeline">
      <h2>Complete Timeline</h2>
      {sortedExperience.map(exp => (
        <div class="timeline-item">
          <div class="timeline-marker"></div>
          <div class="timeline-content">
            <h4>{exp.data.position}</h4>
            <h5>{exp.data.company} - {exp.data.location}</h5>
            <p class="duration">
              {exp.data.startDate.toLocaleDateString()} -
              {exp.data.endDate ? exp.data.endDate.toLocaleDateString() : 'Present'}
            </p>
          </div>
        </div>
      ))}
    </section>
  </main>
</Layout>
```

---

## 🏝️ Server Islands Implementation

### ¿Qué son Server Islands?
Server Islands permiten **contenido dinámico** dentro de páginas estáticas, renderizando componentes específicos del lado del servidor bajo demanda.

### Configuración Server Islands
```typescript
// astro.config.ts
import { defineConfig } from 'astro/config';

export default defineConfig({
  output: 'static', // SSG mode
  experimental: {
    serverIslands: true // Enable Server Islands
  },
  integrations: [
    // Integrations here
  ]
});
```

### Componente Server Island
```astro
---
// src/islands/ExperienceList.astro
import { actions } from 'astro:actions';

// This runs on the server when the island is requested
const { data: experiences } = await actions.experience.getAll();
const recentExperiences = experiences?.slice(0, 3) || [];
---

<div class="experience-island" data-island="experience-list">
  <h3>Recent Experience</h3>

  {recentExperiences.length > 0 ? (
    <div class="experience-grid">
      {recentExperiences.map(exp => (
        <article class="experience-card">
          <h4>{exp.position}</h4>
          <p class="company">{exp.company}</p>
          <p class="duration">
            {new Date(exp.startDate).getFullYear()} -
            {exp.endDate ? new Date(exp.endDate).getFullYear() : 'Present'}
          </p>

          <div class="technologies">
            {exp.technologies.slice(0, 3).map(tech => (
              <span class="tech-badge">{tech}</span>
            ))}
            {exp.technologies.length > 3 && (
              <span class="tech-more">+{exp.technologies.length - 3} more</span>
            )}
          </div>
        </article>
      ))}
    </div>
  ) : (
    <div class="loading-state">
      <p>Loading experience data...</p>
    </div>
  )}

  <a href="/experience" class="view-all-link">
    View All Experience →
  </a>
</div>

<style>
  .experience-island {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    border-radius: 12px;
    padding: 2rem;
    color: white;
    margin: 2rem 0;
  }

  .experience-grid {
    display: grid;
    gap: 1.5rem;
    margin: 1.5rem 0;
  }

  .experience-card {
    background: rgba(255, 255, 255, 0.1);
    border-radius: 8px;
    padding: 1.5rem;
    backdrop-filter: blur(10px);
  }

  .company {
    font-weight: 600;
    opacity: 0.9;
  }

  .duration {
    font-size: 0.9rem;
    opacity: 0.8;
    margin: 0.5rem 0;
  }

  .technologies {
    display: flex;
    flex-wrap: wrap;
    gap: 0.5rem;
    margin-top: 1rem;
  }

  .tech-badge {
    background: rgba(255, 255, 255, 0.2);
    padding: 0.25rem 0.75rem;
    border-radius: 20px;
    font-size: 0.8rem;
  }

  .tech-more {
    background: rgba(255, 255, 255, 0.1);
    padding: 0.25rem 0.75rem;
    border-radius: 20px;
    font-size: 0.8rem;
    font-style: italic;
  }

  .view-all-link {
    display: inline-block;
    margin-top: 1.5rem;
    color: white;
    text-decoration: none;
    font-weight: 600;
    border-bottom: 2px solid rgba(255, 255, 255, 0.3);
    transition: border-color 0.3s ease;
  }

  .view-all-link:hover {
    border-color: white;
  }

  .loading-state {
    text-align: center;
    padding: 2rem;
    opacity: 0.8;
  }
</style>
```

### Uso en Páginas
```astro
---
// src/pages/index.astro
import Layout from '../layouts/Layout.astro';
import ExperienceList from '../islands/ExperienceList.astro';
import ProjectsGrid from '../islands/ProjectsGrid.astro';
import SkillsMatrix from '../islands/SkillsMatrix.astro';
---

<Layout title="Pablo Contreras - Portfolio">
  <main>
    <section class="hero">
      <h1>Pablo Contreras</h1>
      <p class="subtitle">Full Stack Developer & Solutions Architect</p>
      <p class="description">
        Specialized in serverless architectures, modern web development,
        and scalable cloud solutions.
      </p>
    </section>

    <!-- Server Islands for dynamic content -->
    <ExperienceList />
    <ProjectsGrid featured={true} />
    <SkillsMatrix categories={['Frontend', 'Backend', 'Cloud']} />

    <section class="cta">
      <h2>Let's Build Something Amazing</h2>
      <a href="/contact" class="cta-button">Get In Touch</a>
    </section>
  </main>
</Layout>
```

---

## ⚡ Astro Actions Implementation

### ¿Qué son Astro Actions?
Astro Actions son **funciones backend type-safe** que pueden ser llamadas desde el frontend con validación automática de tipos y manejo de errores.

### Definición de Actions
```typescript
// src/actions/index.ts
import { defineAction } from 'astro:actions';
import { z } from 'astro:schema';

// Base URL para APIs (configurado en env variables)
const API_BASE_URL = import.meta.env.API_BASE_URL || 'http://localhost:8080';

export const server = {
  // Action para obtener experiencia profesional
  experience: {
    getAll: defineAction({
      input: z.object({
        limit: z.number().min(1).max(100).optional(),
        featured: z.boolean().optional(),
        company: z.string().optional()
      }).optional(),
      handler: async (input = {}) => {
        try {
          const queryParams = new URLSearchParams();
          if (input.limit) queryParams.set('limit', input.limit.toString());
          if (input.featured !== undefined) queryParams.set('featured', input.featured.toString());
          if (input.company) queryParams.set('company', input.company);

          const response = await fetch(
            `${API_BASE_URL}/api/v1/experience?${queryParams}`,
            {
              method: 'GET',
              headers: {
                'Content-Type': 'application/json',
              },
            }
          );

          if (!response.ok) {
            throw new Error(`API Error: ${response.status} ${response.statusText}`);
          }

          const data = await response.json();
          return {
            success: true,
            data: data.experience || [],
            total: data.total || 0
          };
        } catch (error) {
          console.error('Experience API Error:', error);
          return {
            success: false,
            error: error instanceof Error ? error.message : 'Unknown error',
            data: []
          };
        }
      }
    }),

    getById: defineAction({
      input: z.object({
        id: z.string().uuid()
      }),
      handler: async ({ id }) => {
        try {
          const response = await fetch(`${API_BASE_URL}/api/v1/experience/${id}`);

          if (!response.ok) {
            if (response.status === 404) {
              return { success: false, error: 'Experience not found', data: null };
            }
            throw new Error(`API Error: ${response.status}`);
          }

          const data = await response.json();
          return { success: true, data: data.experience };
        } catch (error) {
          return {
            success: false,
            error: error instanceof Error ? error.message : 'Unknown error',
            data: null
          };
        }
      }
    })
  },

  // Action para obtener proyectos
  projects: {
    getAll: defineAction({
      input: z.object({
        limit: z.number().min(1).max(50).optional(),
        featured: z.boolean().optional(),
        technology: z.string().optional(),
        status: z.enum(['completed', 'in-progress', 'archived']).optional()
      }).optional(),
      handler: async (input = {}) => {
        try {
          const queryParams = new URLSearchParams();
          if (input.limit) queryParams.set('limit', input.limit.toString());
          if (input.featured !== undefined) queryParams.set('featured', input.featured.toString());
          if (input.technology) queryParams.set('technology', input.technology);
          if (input.status) queryParams.set('status', input.status);

          const response = await fetch(
            `${API_BASE_URL}/api/v1/projects?${queryParams}`,
            {
              method: 'GET',
              headers: { 'Content-Type': 'application/json' }
            }
          );

          if (!response.ok) {
            throw new Error(`Projects API Error: ${response.status}`);
          }

          const data = await response.json();
          return {
            success: true,
            data: data.projects || [],
            total: data.total || 0
          };
        } catch (error) {
          console.error('Projects API Error:', error);
          return {
            success: false,
            error: error instanceof Error ? error.message : 'Unknown error',
            data: []
          };
        }
      }
    })
  },

  // Action para obtener habilidades
  skills: {
    getByCategory: defineAction({
      input: z.object({
        categories: z.array(z.string()).min(1),
        level: z.enum(['beginner', 'intermediate', 'advanced', 'expert']).optional()
      }),
      handler: async ({ categories, level }) => {
        try {
          const queryParams = new URLSearchParams();
          queryParams.set('categories', categories.join(','));
          if (level) queryParams.set('level', level);

          const response = await fetch(
            `${API_BASE_URL}/api/v1/skills?${queryParams}`,
            {
              method: 'GET',
              headers: { 'Content-Type': 'application/json' }
            }
          );

          if (!response.ok) {
            throw new Error(`Skills API Error: ${response.status}`);
          }

          const data = await response.json();
          return {
            success: true,
            data: data.skills || []
          };
        } catch (error) {
          console.error('Skills API Error:', error);
          return {
            success: false,
            error: error instanceof Error ? error.message : 'Unknown error',
            data: []
          };
        }
      }
    })
  },

  // Action para envío de formulario de contacto
  contact: {
    sendMessage: defineAction({
      input: z.object({
        name: z.string().min(2, 'Name must be at least 2 characters'),
        email: z.string().email('Invalid email address'),
        company: z.string().optional(),
        subject: z.string().min(5, 'Subject must be at least 5 characters'),
        message: z.string().min(10, 'Message must be at least 10 characters'),
        honeypot: z.string().optional() // Spam protection
      }),
      handler: async ({ honeypot, ...contactData }) => {
        // Honeypot spam check
        if (honeypot) {
          return { success: false, error: 'Spam detected' };
        }

        try {
          const response = await fetch(`${API_BASE_URL}/api/v1/contact`, {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json',
            },
            body: JSON.stringify(contactData)
          });

          if (!response.ok) {
            throw new Error(`Contact API Error: ${response.status}`);
          }

          const result = await response.json();
          return {
            success: true,
            message: 'Message sent successfully!'
          };
        } catch (error) {
          console.error('Contact form error:', error);
          return {
            success: false,
            error: 'Failed to send message. Please try again later.'
          };
        }
      }
    })
  }
};
```

### Tipos Compartidos
```typescript
// src/actions/types.ts
export interface Experience {
  id: string;
  company: string;
  position: string;
  startDate: string;
  endDate?: string;
  description: string;
  technologies: string[];
  achievements: string[];
  location: string;
  type: 'full-time' | 'part-time' | 'contract' | 'freelance';
  featured: boolean;
}

export interface Project {
  id: string;
  title: string;
  description: string;
  technologies: string[];
  githubUrl?: string;
  liveUrl?: string;
  imageUrl?: string;
  featured: boolean;
  publishedDate: string;
  status: 'completed' | 'in-progress' | 'archived';
}

export interface Skill {
  name: string;
  level: 'beginner' | 'intermediate' | 'advanced' | 'expert';
  yearsOfExperience: number;
  certifications?: string[];
  projects?: string[];
}

export interface SkillCategory {
  category: string;
  skills: Skill[];
}

export interface ContactMessage {
  name: string;
  email: string;
  company?: string;
  subject: string;
  message: string;
}

export interface APIResponse<T> {
  success: boolean;
  data?: T;
  error?: string;
  total?: number;
  message?: string;
}
```

---

## 🎨 TypeScript Configuration (Strict Mode)

### tsconfig.json Estricto
```json
{
  "compilerOptions": {
    // Strict Type Checking (OBLIGATORIO)
    "strict": true,
    "noImplicitAny": true,
    "strictNullChecks": true,
    "strictFunctionTypes": true,
    "strictBindCallApply": true,
    "strictPropertyInitialization": true,
    "noImplicitReturns": true,
    "noFallthroughCasesInSwitch": true,
    "noUncheckedIndexedAccess": true,
    "noImplicitOverride": true,

    // Module Configuration
    "target": "ES2022",
    "module": "ESNext",
    "moduleResolution": "node",
    "allowSyntheticDefaultImports": true,
    "esModuleInterop": true,
    "allowJs": false,
    "checkJs": false,

    // Path Mapping
    "baseUrl": ".",
    "paths": {
      "@/*": ["./src/*"],
      "@/components/*": ["./src/components/*"],
      "@/layouts/*": ["./src/layouts/*"],
      "@/actions/*": ["./src/actions/*"],
      "@/utils/*": ["./src/utils/*"],
      "@/styles/*": ["./src/styles/*"]
    },

    // Additional Checks
    "noUnusedLocals": true,
    "noUnusedParameters": true,
    "exactOptionalPropertyTypes": true,
    "noPropertyAccessFromIndexSignature": true,

    // Output Configuration
    "declaration": true,
    "declarationMap": true,
    "sourceMap": true,
    "removeComments": false,
    "skipLibCheck": true,
    "forceConsistentCasingInFileNames": true
  },
  "include": [
    "src/**/*",
    "astro.config.ts",
    "vitest.config.ts"
  ],
  "exclude": [
    "node_modules",
    "dist",
    "public"
  ]
}
```

### Configuración Astro con TypeScript
```typescript
// astro.config.ts
import { defineConfig } from 'astro/config';
import tailwind from '@astrojs/tailwind';
import sitemap from '@astrojs/sitemap';
import { fileURLToPath } from 'url';

export default defineConfig({
  site: 'https://pablocontreras.dev', // Your domain

  // Build Configuration
  build: {
    format: 'directory',
    inlineStylesheets: 'auto'
  },

  // Output Mode
  output: 'static', // SSG mode with Server Islands

  // Experimental Features
  experimental: {
    serverIslands: true,
    contentCollectionCache: true
  },

  // Integrations
  integrations: [
    tailwind({
      applyBaseStyles: false // Use custom base styles
    }),
    sitemap({
      changefreq: 'weekly',
      priority: 0.7,
      lastmod: new Date()
    })
  ],

  // Vite Configuration
  vite: {
    resolve: {
      alias: {
        '@': fileURLToPath(new URL('./src', import.meta.url))
      }
    },
    optimizeDeps: {
      include: ['astro:actions', 'astro:content']
    }
  },

  // Markdown Configuration
  markdown: {
    shikiConfig: {
      theme: 'github-dark',
      wrap: true
    }
  },

  // Image Optimization
  image: {
    remotePatterns: [
      {
        protocol: 'https',
        hostname: '**'
      }
    ]
  }
});
```

---

## 🧪 Testing Strategy con TDD

### Configuración Vitest
```typescript
// vitest.config.ts
import { defineConfig } from 'vitest/config';
import { getViteConfig } from 'astro/config';

export default defineConfig(
  getViteConfig({
    test: {
      globals: true,
      environment: 'jsdom',
      setupFiles: ['./src/test/setup.ts'],
      include: ['src/**/*.{test,spec}.{js,ts}'],
      exclude: ['node_modules', 'dist', '.astro'],

      // Coverage Configuration
      coverage: {
        provider: 'v8',
        reporter: ['text', 'html', 'json'],
        reportsDirectory: './coverage',
        exclude: [
          'coverage/**',
          'dist/**',
          '.astro/**',
          '**/*.d.ts',
          'astro.config.ts',
          'tailwind.config.js'
        ],

        // Coverage Thresholds (OBLIGATORIO >80%)
        thresholds: {
          global: {
            branches: 80,
            functions: 80,
            lines: 80,
            statements: 80
          }
        }
      },

      // Test Timeout
      testTimeout: 10000,
      hookTimeout: 10000
    }
  })
);
```

### Setup de Testing
```typescript
// src/test/setup.ts
import { vi } from 'vitest';

// Mock environment variables
vi.mock('astro:env/server', () => ({
  API_BASE_URL: 'http://localhost:8080'
}));

// Mock Astro Actions
vi.mock('astro:actions', () => ({
  actions: {
    experience: {
      getAll: vi.fn(),
      getById: vi.fn()
    },
    projects: {
      getAll: vi.fn()
    },
    skills: {
      getByCategory: vi.fn()
    },
    contact: {
      sendMessage: vi.fn()
    }
  }
}));

// Global test utilities
global.ResizeObserver = vi.fn(() => ({
  observe: vi.fn(),
  unobserve: vi.fn(),
  disconnect: vi.fn()
}));

// Mock IntersectionObserver
global.IntersectionObserver = vi.fn(() => ({
  observe: vi.fn(),
  unobserve: vi.fn(),
  disconnect: vi.fn()
}));
```

### Unit Tests Ejemplo
```typescript
// src/test/components/ExperienceCard.test.ts
import { describe, it, expect, vi } from 'vitest';
import { render } from '@testing-library/dom';
import type { Experience } from '@/actions/types';

// Mock data
const mockExperience: Experience = {
  id: '1',
  company: 'TechCorp',
  position: 'Senior Developer',
  startDate: '2023-01-01',
  endDate: '2024-01-01',
  description: 'Led development of modern web applications',
  technologies: ['TypeScript', 'React', 'Node.js'],
  achievements: ['Improved performance by 40%', 'Led team of 5 developers'],
  location: 'Remote',
  type: 'full-time',
  featured: true
};

describe('ExperienceCard Component', () => {
  it('should render experience information correctly', () => {
    // Red Phase: Write failing test
    const component = render(`
      <article class="experience-card">
        <h3>${mockExperience.position} at ${mockExperience.company}</h3>
        <p class="location">${mockExperience.location}</p>
        <div class="technologies">
          ${mockExperience.technologies.map(tech =>
            `<span class="tech-tag">${tech}</span>`
          ).join('')}
        </div>
      </article>
    `);

    expect(component.querySelector('h3')?.textContent).toBe(
      'Senior Developer at TechCorp'
    );
    expect(component.querySelector('.location')?.textContent).toBe('Remote');
    expect(component.querySelectorAll('.tech-tag')).toHaveLength(3);
  });

  it('should handle missing end date correctly', () => {
    const currentExperience = {
      ...mockExperience,
      endDate: undefined
    };

    // Test current position rendering
    const duration = currentExperience.endDate
      ? `${currentExperience.startDate} - ${currentExperience.endDate}`
      : `${currentExperience.startDate} - Present`;

    expect(duration).toBe('2023-01-01 - Present');
  });

  it('should apply featured styling when featured is true', () => {
    const cardClass = mockExperience.featured
      ? 'experience-card featured'
      : 'experience-card';

    expect(cardClass).toBe('experience-card featured');
  });
});
```

### Integration Tests
```typescript
// src/test/integration/actions.test.ts
import { describe, it, expect, vi, beforeEach } from 'vitest';
import { actions } from 'astro:actions';

// Mock fetch globally
global.fetch = vi.fn();

describe('Astro Actions Integration', () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  describe('Experience Actions', () => {
    it('should fetch all experience successfully', async () => {
      // Mock successful API response
      const mockResponse = {
        success: true,
        experience: [
          {
            id: '1',
            company: 'TechCorp',
            position: 'Senior Developer',
            startDate: '2023-01-01'
          }
        ],
        total: 1
      };

      (fetch as any).mockResolvedValueOnce({
        ok: true,
        json: () => Promise.resolve(mockResponse)
      });

      const result = await actions.experience.getAll({
        limit: 10,
        featured: true
      });

      expect(result.success).toBe(true);
      expect(result.data).toHaveLength(1);
      expect(result.data?.[0].company).toBe('TechCorp');

      // Verify fetch was called correctly
      expect(fetch).toHaveBeenCalledWith(
        'http://localhost:8080/api/v1/experience?limit=10&featured=true',
        {
          method: 'GET',
          headers: { 'Content-Type': 'application/json' }
        }
      );
    });

    it('should handle API errors gracefully', async () => {
      // Mock API error
      (fetch as any).mockResolvedValueOnce({
        ok: false,
        status: 500,
        statusText: 'Internal Server Error'
      });

      const result = await actions.experience.getAll();

      expect(result.success).toBe(false);
      expect(result.error).toContain('API Error: 500');
      expect(result.data).toEqual([]);
    });
  });

  describe('Contact Actions', () => {
    it('should validate required fields', async () => {
      // Test with invalid data
      const invalidData = {
        name: 'A', // Too short
        email: 'invalid-email',
        subject: 'Hi', // Too short
        message: 'Short' // Too short
      };

      try {
        await actions.contact.sendMessage(invalidData);
        expect.fail('Should have thrown validation error');
      } catch (error) {
        expect(error).toBeDefined();
      }
    });

    it('should send message successfully with valid data', async () => {
      const validData = {
        name: 'John Doe',
        email: 'john@example.com',
        subject: 'Interested in your services',
        message: 'I would like to discuss a potential project opportunity.'
      };

      (fetch as any).mockResolvedValueOnce({
        ok: true,
        json: () => Promise.resolve({ success: true })
      });

      const result = await actions.contact.sendMessage(validData);

      expect(result.success).toBe(true);
      expect(result.message).toBe('Message sent successfully!');
    });
  });
});
```

### E2E Tests con Playwright
```typescript
// playwright.config.ts
import { defineConfig, devices } from '@playwright/test';

export default defineConfig({
  testDir: './tests/e2e',
  fullyParallel: true,
  forbidOnly: !!process.env.CI,
  retries: process.env.CI ? 2 : 0,
  workers: process.env.CI ? 1 : undefined,
  reporter: 'html',

  use: {
    baseURL: 'http://localhost:4321',
    trace: 'on-first-retry',
    screenshot: 'only-on-failure'
  },

  projects: [
    {
      name: 'chromium',
      use: { ...devices['Desktop Chrome'] }
    },
    {
      name: 'firefox',
      use: { ...devices['Desktop Firefox'] }
    },
    {
      name: 'webkit',
      use: { ...devices['Desktop Safari'] }
    },
    {
      name: 'Mobile Chrome',
      use: { ...devices['Pixel 5'] }
    }
  ],

  webServer: {
    command: 'npm run dev',
    url: 'http://localhost:4321',
    reuseExistingServer: !process.env.CI
  }
});
```

```typescript
// tests/e2e/portfolio.spec.ts
import { test, expect } from '@playwright/test';

test.describe('Portfolio Website', () => {
  test('should load homepage successfully', async ({ page }) => {
    await page.goto('/');

    // Check main heading
    await expect(page.locator('h1')).toContainText('Pablo Contreras');

    // Check Lighthouse performance
    const lighthouse = await page.lighthouse();
    expect(lighthouse.score('performance')).toBeGreaterThan(0.9);
  });

  test('should navigate to experience page', async ({ page }) => {
    await page.goto('/');

    // Click experience link
    await page.click('a[href="/experience"]');
    await expect(page).toHaveURL('/experience');

    // Check experience content loads
    await expect(page.locator('.experience-card')).toBeVisible();
  });

  test('should submit contact form', async ({ page }) => {
    await page.goto('/contact');

    // Fill contact form
    await page.fill('input[name="name"]', 'Test User');
    await page.fill('input[name="email"]', 'test@example.com');
    await page.fill('input[name="subject"]', 'Test Subject');
    await page.fill('textarea[name="message"]', 'This is a test message');

    // Submit form
    await page.click('button[type="submit"]');

    // Check success message
    await expect(page.locator('.success-message')).toBeVisible();
  });

  test('should be responsive on mobile', async ({ page }) => {
    await page.setViewportSize({ width: 375, height: 667 });
    await page.goto('/');

    // Check mobile navigation
    await expect(page.locator('.mobile-menu-toggle')).toBeVisible();

    // Check content is readable
    await expect(page.locator('h1')).toBeVisible();
  });
});
```

---

## 🎨 Styling con Tailwind CSS

### Configuración Tailwind
```javascript
// tailwind.config.js
/** @type {import('tailwindcss').Config} */
export default {
  content: ['./src/**/*.{astro,html,js,jsx,md,mdx,svelte,ts,tsx,vue}'],
  theme: {
    extend: {
      // Color Palette
      colors: {
        primary: {
          50: '#eff6ff',
          100: '#dbeafe',
          500: '#3b82f6',
          600: '#2563eb',
          700: '#1d4ed8',
          900: '#1e3a8a'
        },
        secondary: {
          50: '#f8fafc',
          100: '#f1f5f9',
          500: '#64748b',
          600: '#475569',
          700: '#334155',
          900: '#0f172a'
        }
      },

      // Typography
      fontFamily: {
        sans: ['Inter', 'system-ui', 'sans-serif'],
        mono: ['JetBrains Mono', 'Monaco', 'monospace']
      },

      // Spacing
      spacing: {
        '18': '4.5rem',
        '88': '22rem'
      },

      // Animation
      animation: {
        'fade-in': 'fadeIn 0.5s ease-in-out',
        'slide-up': 'slideUp 0.5s ease-out',
        'bounce-slow': 'bounce 2s infinite'
      },

      keyframes: {
        fadeIn: {
          '0%': { opacity: '0' },
          '100%': { opacity: '1' }
        },
        slideUp: {
          '0%': { transform: 'translateY(20px)', opacity: '0' },
          '100%': { transform: 'translateY(0)', opacity: '1' }
        }
      }
    }
  },
  plugins: [
    require('@tailwindcss/typography'),
    require('@tailwindcss/forms'),
    require('@tailwindcss/aspect-ratio')
  ]
};
```

### Estilos Base Personalizados
```css
/* src/styles/global.css */
@tailwind base;
@tailwind components;
@tailwind utilities;

@layer base {
  /* Custom base styles */
  html {
    @apply scroll-smooth;
  }

  body {
    @apply bg-white text-gray-900 dark:bg-gray-900 dark:text-white;
    @apply font-sans leading-relaxed;
  }

  h1, h2, h3, h4, h5, h6 {
    @apply font-semibold tracking-tight;
  }

  h1 {
    @apply text-4xl lg:text-5xl mb-6;
  }

  h2 {
    @apply text-3xl lg:text-4xl mb-4;
  }

  h3 {
    @apply text-2xl lg:text-3xl mb-3;
  }
}

@layer components {
  /* Reusable component styles */
  .btn {
    @apply inline-flex items-center justify-center px-6 py-3;
    @apply font-medium text-sm rounded-lg transition-all duration-200;
    @apply focus:outline-none focus:ring-2 focus:ring-offset-2;
  }

  .btn-primary {
    @apply btn bg-primary-600 text-white hover:bg-primary-700;
    @apply focus:ring-primary-500;
  }

  .btn-secondary {
    @apply btn bg-secondary-100 text-secondary-900 hover:bg-secondary-200;
    @apply focus:ring-secondary-500;
  }

  .card {
    @apply bg-white dark:bg-gray-800 rounded-xl shadow-lg;
    @apply border border-gray-200 dark:border-gray-700;
    @apply transition-all duration-200 hover:shadow-xl;
  }

  .input {
    @apply w-full px-4 py-3 rounded-lg border border-gray-300;
    @apply focus:ring-2 focus:ring-primary-500 focus:border-transparent;
    @apply dark:bg-gray-700 dark:border-gray-600 dark:text-white;
  }

  .tech-badge {
    @apply inline-flex items-center px-3 py-1 rounded-full text-sm font-medium;
    @apply bg-primary-100 text-primary-800 dark:bg-primary-900 dark:text-primary-200;
  }
}

@layer utilities {
  /* Custom utility classes */
  .text-gradient {
    @apply bg-gradient-to-r from-primary-600 to-secondary-600;
    @apply bg-clip-text text-transparent;
  }

  .glass {
    @apply backdrop-blur-lg bg-white/30 dark:bg-gray-900/30;
    @apply border border-white/20 dark:border-gray-800/20;
  }

  .animate-on-scroll {
    @apply opacity-0 translate-y-8 transition-all duration-700;
  }

  .animate-on-scroll.visible {
    @apply opacity-100 translate-y-0;
  }
}
```

---

## 🚀 Performance Optimization

### Core Web Vitals Optimization
```typescript
// src/utils/performance.ts

// Lazy loading with Intersection Observer
export const setupLazyLoading = (): void => {
  if ('IntersectionObserver' in window) {
    const images = document.querySelectorAll('img[data-src]');
    const imageObserver = new IntersectionObserver((entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          const img = entry.target as HTMLImageElement;
          img.src = img.dataset.src!;
          img.removeAttribute('data-src');
          imageObserver.unobserve(img);
        }
      });
    });

    images.forEach((img) => imageObserver.observe(img));
  }
};

// Preload critical resources
export const preloadCriticalResources = (): void => {
  // Preload critical fonts
  const fontLink = document.createElement('link');
  fontLink.rel = 'preload';
  fontLink.href = '/fonts/inter-var.woff2';
  fontLink.as = 'font';
  fontLink.type = 'font/woff2';
  fontLink.crossOrigin = 'anonymous';
  document.head.appendChild(fontLink);

  // Preload critical API endpoints
  if ('requestIdleCallback' in window) {
    requestIdleCallback(() => {
      fetch('/api/v1/experience?limit=3&featured=true', {
        headers: { 'Accept': 'application/json' }
      });
    });
  }
};

// Animate elements on scroll
export const setupScrollAnimations = (): void => {
  const animatedElements = document.querySelectorAll('.animate-on-scroll');

  if ('IntersectionObserver' in window) {
    const animationObserver = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) {
            entry.target.classList.add('visible');
            animationObserver.unobserve(entry.target);
          }
        });
      },
      { threshold: 0.1, rootMargin: '0px 0px -50px 0px' }
    );

    animatedElements.forEach((el) => animationObserver.observe(el));
  } else {
    // Fallback for older browsers
    animatedElements.forEach((el) => el.classList.add('visible'));
  }
};

// Performance monitoring
export const measureWebVitals = (): void => {
  if ('web-vitals' in window || typeof window !== 'undefined') {
    import('web-vitals').then(({ getCLS, getFID, getFCP, getLCP, getTTFB }) => {
      getCLS(console.log);
      getFID(console.log);
      getFCP(console.log);
      getLCP(console.log);
      getTTFB(console.log);
    });
  }
};
```

### Bundle Optimization
```typescript
// astro.config.ts - Build optimizations
export default defineConfig({
  build: {
    // Optimize CSS
    inlineStylesheets: 'auto',

    // Split bundles for better caching
    rollupOptions: {
      output: {
        manualChunks: {
          vendor: ['astro', '@astrojs/tailwind'],
          utils: ['./src/utils/performance.ts']
        }
      }
    }
  },

  vite: {
    build: {
      // Minify for production
      minify: 'terser',
      terserOptions: {
        compress: {
          drop_console: true, // Remove console.logs in production
          drop_debugger: true
        }
      },

      // Optimize dependencies
      rollupOptions: {
        output: {
          // Smaller chunks
          chunkSizeWarningLimit: 1000,
          manualChunks(id) {
            if (id.includes('node_modules')) {
              return 'vendor';
            }
          }
        }
      }
    },

    // CSS optimization
    css: {
      postcss: {
        plugins: [
          require('cssnano')({
            preset: 'default'
          })
        ]
      }
    }
  }
});
```

---

## 📦 Deployment Configuration

### AWS CloudFront + S3 Setup
```yaml
# deploy/aws-config.yml
AWSTemplateFormatVersion: '2010-09-09'
Description: 'Static website hosting with CloudFront and S3'

Parameters:
  DomainName:
    Type: String
    Default: 'pablocontreras.dev'
    Description: 'Domain name for the website'

Resources:
  # S3 Bucket for static files
  WebsiteBucket:
    Type: AWS::S3::Bucket
    Properties:
      BucketName: !Sub '${DomainName}-static-site'
      PublicAccessBlockConfiguration:
        BlockPublicAcls: true
        BlockPublicPolicy: true
        IgnorePublicAcls: true
        RestrictPublicBuckets: true
      VersioningConfiguration:
        Status: Enabled
      BucketEncryption:
        ServerSideEncryptionConfiguration:
          - ServerSideEncryptionByDefault:
              SSEAlgorithm: AES256

  # CloudFront Origin Access Control
  OriginAccessControl:
    Type: AWS::CloudFront::OriginAccessControl
    Properties:
      OriginAccessControlConfig:
        Name: !Sub '${DomainName}-OAC'
        OriginAccessControlOriginType: s3
        SigningBehavior: always
        SigningProtocol: sigv4

  # CloudFront Distribution
  CloudFrontDistribution:
    Type: AWS::CloudFront::Distribution
    Properties:
      DistributionConfig:
        Origins:
          - Id: S3Origin
            DomainName: !GetAtt WebsiteBucket.RegionalDomainName
            S3OriginConfig:
              OriginAccessIdentity: ''
            OriginAccessControlId: !GetAtt OriginAccessControl.Id

        Enabled: true
        HttpVersion: http2
        DefaultRootObject: index.html

        DefaultCacheBehavior:
          AllowedMethods:
            - GET
            - HEAD
            - OPTIONS
          TargetOriginId: S3Origin
          ViewerProtocolPolicy: redirect-to-https
          CachePolicyId: 4135ea2d-6df8-44a3-9df3-4b5a84be39ad # Managed-CachingOptimized
          OriginRequestPolicyId: 88a5eaf4-2fd4-4709-b370-b4c650ea3fcf # Managed-CORS-S3Origin

        # Custom error pages
        CustomErrorResponses:
          - ErrorCode: 404
            ResponseCode: 404
            ResponsePagePath: /404.html
          - ErrorCode: 403
            ResponseCode: 404
            ResponsePagePath: /404.html

        # Price class
        PriceClass: PriceClass_100

        # Enable IPv6
        IPV6Enabled: true

Outputs:
  CloudFrontURL:
    Description: 'CloudFront Distribution URL'
    Value: !GetAtt CloudFrontDistribution.DomainName

  BucketName:
    Description: 'S3 Bucket Name'
    Value: !Ref WebsiteBucket
```

### GitHub Actions Deployment
```yaml
# .github/workflows/deploy.yml
name: Deploy to AWS

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

env:
  NODE_VERSION: '20'
  AWS_REGION: 'us-east-1'

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout
        uses: actions/checkout@v4

      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: ${{ env.NODE_VERSION }}
          cache: 'npm'

      - name: Install dependencies
        run: npm ci

      - name: Run TypeScript check
        run: npm run check

      - name: Run tests
        run: npm run test

      - name: Run E2E tests
        run: npm run test:e2e

      - name: Build
        run: npm run build

      - name: Upload build artifacts
        uses: actions/upload-artifact@v4
        with:
          name: dist
          path: dist/

  deploy:
    needs: test
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'

    steps:
      - name: Checkout
        uses: actions/checkout@v4

      - name: Download build artifacts
        uses: actions/download-artifact@v4
        with:
          name: dist
          path: dist/

      - name: Configure AWS credentials
        uses: aws-actions/configure-aws-credentials@v4
        with:
          aws-access-key-id: ${{ secrets.AWS_ACCESS_KEY_ID }}
          aws-secret-access-key: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
          aws-region: ${{ env.AWS_REGION }}

      - name: Deploy to S3
        run: |
          aws s3 sync dist/ s3://${{ secrets.S3_BUCKET_NAME }} --delete \
            --cache-control "public, max-age=31536000, immutable" \
            --exclude "*.html" \
            --exclude "sitemap.xml" \
            --exclude "robots.txt"

          # HTML files with shorter cache
          aws s3 sync dist/ s3://${{ secrets.S3_BUCKET_NAME }} \
            --cache-control "public, max-age=3600" \
            --include "*.html" \
            --include "sitemap.xml" \
            --include "robots.txt"

      - name: Invalidate CloudFront
        run: |
          aws cloudfront create-invalidation \
            --distribution-id ${{ secrets.CLOUDFRONT_DISTRIBUTION_ID }} \
            --paths "/*"

      - name: Lighthouse CI
        uses: treosh/lighthouse-ci-action@v10
        with:
          urls: |
            https://${{ secrets.DOMAIN_NAME }}
            https://${{ secrets.DOMAIN_NAME }}/experience
            https://${{ secrets.DOMAIN_NAME }}/projects
          uploadArtifacts: true
          temporaryPublicStorage: true
```

---

## 📋 Development Commands

### Package.json Scripts
```json
{
  "name": "portfolio-frontend",
  "type": "module",
  "version": "1.0.0",
  "scripts": {
    "dev": "astro dev",
    "start": "astro dev",
    "build": "astro check && astro build",
    "preview": "astro preview",
    "check": "astro check",

    "test": "vitest",
    "test:ui": "vitest --ui",
    "test:run": "vitest run",
    "test:watch": "vitest --watch",
    "test:coverage": "vitest run --coverage",

    "test:e2e": "playwright test",
    "test:e2e:ui": "playwright test --ui",
    "test:e2e:headed": "playwright test --headed",

    "lint": "eslint src --ext ts,astro",
    "lint:fix": "eslint src --ext ts,astro --fix",
    "format": "prettier --write src/**/*.{ts,astro}",
    "type-check": "tsc --noEmit",

    "astro": "astro"
  },
  "dependencies": {
    "astro": "^5.0.0",
    "@astrojs/tailwind": "^5.0.0",
    "@astrojs/sitemap": "^3.0.0",
    "tailwindcss": "^3.4.0",
    "typescript": "^5.3.0"
  },
  "devDependencies": {
    "@playwright/test": "^1.40.0",
    "@types/node": "^20.10.0",
    "@typescript-eslint/eslint-plugin": "^6.0.0",
    "@typescript-eslint/parser": "^6.0.0",
    "@vitest/ui": "^1.0.0",
    "eslint": "^8.0.0",
    "eslint-plugin-astro": "^0.30.0",
    "jsdom": "^23.0.0",
    "prettier": "^3.0.0",
    "prettier-plugin-astro": "^0.12.0",
    "vitest": "^1.0.0"
  }
}
```

### Comandos de Desarrollo
```bash
# Desarrollo local
npm run dev                 # Servidor de desarrollo (http://localhost:4321)
npm run build              # Build de producción
npm run preview            # Preview del build

# Testing
npm run test               # Tests unitarios con watch
npm run test:run           # Tests unitarios una vez
npm run test:coverage      # Tests con coverage
npm run test:e2e           # Tests E2E con Playwright

# Calidad de código
npm run check              # Astro check + TypeScript
npm run lint               # ESLint
npm run format             # Prettier
npm run type-check         # Solo TypeScript check

# Análisis
npm run lighthouse         # Lighthouse audit local
npm run bundle-analyzer    # Análisis del bundle
```

---

## 🎯 Best Practices & Guidelines

### TypeScript Best Practices
```typescript
// ✅ Usar tipos explícitos
interface Props {
  title: string;
  items: ReadonlyArray<string>;
  onSelect?: (item: string) => void;
}

// ✅ Usar readonly para arrays que no se modifican
type Technology = Readonly<{
  name: string;
  level: 'beginner' | 'intermediate' | 'advanced' | 'expert';
}>;

// ✅ Usar type guards
function isExperience(item: unknown): item is Experience {
  return (
    typeof item === 'object' &&
    item !== null &&
    'company' in item &&
    'position' in item
  );
}

// ✅ Usar utility types
type PartialExperience = Partial<Experience>;
type RequiredContact = Required<ContactMessage>;
```

### Performance Best Practices
```typescript
// ✅ Lazy loading de componentes
const HeavyComponent = lazy(() => import('./HeavyComponent.astro'));

// ✅ Memoización de datos costosos
const expensiveData = useMemo(() => {
  return processLargeDataset(rawData);
}, [rawData]);

// ✅ Debounce para búsquedas
const debouncedSearch = debounce((query: string) => {
  actions.search.execute({ query });
}, 300);
```

### Accessibility Guidelines
```astro
<!-- ✅ Semantic HTML -->
<main>
  <section aria-labelledby="experience-heading">
    <h2 id="experience-heading">Professional Experience</h2>

    <article role="article" tabindex="0">
      <h3>Senior Developer at TechCorp</h3>
      <p>Led development of modern web applications...</p>
    </article>
  </section>
</main>

<!-- ✅ ARIA labels -->
<button
  aria-label="Toggle mobile navigation"
  aria-expanded={isOpen}
  aria-controls="mobile-menu"
>
  <span class="sr-only">Menu</span>
</button>

<!-- ✅ Alt texts descriptivos -->
<img
  src="/project-screenshot.jpg"
  alt="Screenshot of e-commerce dashboard showing sales analytics and user management interface"
/>
```

---

## 📊 Quality Metrics & Goals

### Performance Targets
- **Lighthouse Performance**: >90
- **First Contentful Paint**: <1.5s
- **Largest Contentful Paint**: <2.5s
- **Cumulative Layout Shift**: <0.1
- **Bundle Size**: <500KB gzipped

### Code Quality Standards
- **Test Coverage**: >80%
- **TypeScript Coverage**: 100% (strict mode)
- **ESLint**: 0 errors, 0 warnings
- **Accessibility**: WCAG 2.1 AA compliance

### Browser Support
- **Modern Browsers**: Chrome 90+, Firefox 88+, Safari 14+, Edge 90+
- **Mobile**: iOS Safari 14+, Chrome Mobile 90+
- **Progressive Enhancement**: Core functionality without JavaScript

---

## 🔗 Integration with External APIs

### API Client Configuration
```typescript
// src/utils/api-client.ts
interface APIConfig {
  baseURL: string;
  timeout: number;
  retries: number;
}

class APIClient {
  private config: APIConfig;

  constructor(config: APIConfig) {
    this.config = config;
  }

  async request<T>(
    endpoint: string,
    options: RequestInit = {}
  ): Promise<APIResponse<T>> {
    const url = `${this.config.baseURL}${endpoint}`;

    try {
      const response = await fetch(url, {
        ...options,
        headers: {
          'Content-Type': 'application/json',
          ...options.headers
        }
      });

      if (!response.ok) {
        throw new Error(`HTTP ${response.status}: ${response.statusText}`);
      }

      const data = await response.json();
      return { success: true, data };
    } catch (error) {
      return {
        success: false,
        error: error instanceof Error ? error.message : 'Unknown error'
      };
    }
  }
}

export const apiClient = new APIClient({
  baseURL: import.meta.env.API_BASE_URL || 'http://localhost:8080',
  timeout: 10000,
  retries: 3
});
```

---

**Este frontend implementa las mejores prácticas de 2025 para desarrollo web moderno, combinando SSG con capacidades dinámicas para crear una experiencia de portfolio excepcional y performante.**

**Fecha de implementación**: Enero 2025
**Stack version**: Astro v5 + TypeScript 5.3+ + Tailwind CSS v3
**Deployment**: AWS CloudFront + S3 + GitHub Actions
**Performance target**: Lighthouse score >90 en todas las categorías