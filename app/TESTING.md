# Frontend Testing Guide - Astro v5 + TDD

> **Basado en**: docs/testing.md
> **Última actualización**: Enero 2025
> **Stack**: Vitest + Playwright + Container API + MSW
> **Filosofía**: Test-Driven Development (TDD) obligatorio

---

## 🎯 Resumen de Testing Frontend

Esta guía implementa **TDD completo** para el frontend del portfolio usando **Astro v5** con las mejores prácticas de 2025. El enfoque se centra en testing de componentes, integración con APIs externas y testing end-to-end.

### Stack de Testing 2025
```yaml
Unit Testing: Vitest + Container API
Component Testing: Vitest + Happy-DOM
Integration Testing: Vitest + Astro Dev Server
End-to-End Testing: Playwright
API Mocking: Mock Service Worker (MSW)
Visual Testing: Storybook + Chromatic (opcional)
```

---

## 🛠️ Configuración de Testing

### 1. Vitest Configuration para Astro v5
```typescript
// vitest.config.ts
import { getViteConfig } from 'astro/config';

export default getViteConfig({
  test: {
    environment: 'happy-dom', // Para tests dependientes de DOM
    globals: true,
    setupFiles: ['./test/setup.ts'],
    exclude: ['**/e2e/**'],
    coverage: {
      provider: 'v8',
      reporter: ['text', 'html', 'lcov'],
      exclude: [
        'coverage/**',
        'dist/**',
        '**/node_modules/**',
        '**/test/**'
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
    }
  }
});
```

### 2. Setup de Testing
```typescript
// test/setup.ts
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

global.IntersectionObserver = vi.fn(() => ({
  observe: vi.fn(),
  unobserve: vi.fn(),
  disconnect: vi.fn()
}));
```

### 3. Playwright Configuration
```typescript
// playwright.config.ts
import { defineConfig, devices } from '@playwright/test';

export default defineConfig({
  testDir: './e2e',
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

---

## 🧪 Testing con TDD (Red-Green-Refactor)

### 1. Component Testing con Container API
```typescript
// test/components/PersonalInfo.test.ts
/// <reference types="vitest" />
// @vitest-environment happy-dom

import { experimental_AstroContainer as AstroContainer } from 'astro/container';
import { expect, test, describe, beforeEach } from 'vitest';
import PersonalInfo from '../../src/components/PersonalInfo.astro';

describe('PersonalInfo Component - TDD', () => {
  let container: Awaited<ReturnType<typeof AstroContainer.create>>;

  beforeEach(async () => {
    container = await AstroContainer.create();
  });

  test('RED: should render personal information with props', async () => {
    // TDD Red Phase - Escribir test que falle primero
    const result = await container.renderToString(PersonalInfo, {
      props: {
        name: 'Pablo Contreras',
        title: 'Full Stack Developer',
        email: 'pablo@bypabloc.com',
        location: 'Santiago, Chile'
      }
    });

    expect(result).toContain('Pablo Contreras');
    expect(result).toContain('Full Stack Developer');
    expect(result).toContain('pablo@bypabloc.com');
    expect(result).toContain('Santiago, Chile');
  });

  test('GREEN: should handle missing optional props gracefully', async () => {
    // TDD Green Phase - Código mínimo para pasar
    const result = await container.renderToString(PersonalInfo, {
      props: {
        name: 'Pablo Contreras',
        title: 'Full Stack Developer'
        // Missing email and location
      }
    });

    expect(result).toContain('Pablo Contreras');
    expect(result).toContain('Full Stack Developer');
    expect(result).not.toContain('undefined');
  });

  test('REFACTOR: should apply correct CSS classes', async () => {
    // TDD Refactor Phase - Mejorar estructura del código
    const result = await container.renderToString(PersonalInfo, {
      props: {
        name: 'Pablo Contreras',
        title: 'Full Stack Developer',
        theme: 'dark'
      }
    });

    expect(result).toContain('personal-info');
    expect(result).toContain('personal-info--dark');
  });
});
```

### 2. API Integration Testing con MSW
```typescript
// test/api/external-api.test.ts
import { setupServer } from 'msw/node';
import { rest } from 'msw';
import { expect, test, describe, beforeAll, afterAll, beforeEach } from 'vitest';

// Mock External API responses
const server = setupServer(
  rest.get('http://localhost:8080/api/v1/personal-info', (req, res, ctx) => {
    return res(
      ctx.status(200),
      ctx.json({
        success: true,
        data: {
          name: 'Pablo Contreras',
          title: 'Full Stack Developer',
          email: 'pablo@bypabloc.com',
          location: 'Santiago, Chile',
          summary: 'Experienced developer specializing in serverless architecture'
        }
      })
    );
  }),

  rest.get('http://localhost:8080/api/v1/projects', (req, res, ctx) => {
    return res(
      ctx.status(200),
      ctx.json({
        success: true,
        data: [
          {
            id: '1',
            name: 'Portfolio API',
            description: 'Serverless portfolio backend',
            technologies: ['AWS Lambda', 'Python', 'API Gateway'],
            featured: true
          }
        ]
      })
    );
  })
);

describe('External API Integration Tests - TDD', () => {
  beforeAll(() => server.listen());
  afterAll(() => server.close());
  beforeEach(() => server.resetHandlers());

  test('RED: should fetch personal info from external API', async () => {
    // TDD Red Phase - Test de consumo de API
    const response = await fetch('http://localhost:8080/api/v1/personal-info');
    const data = await response.json();

    expect(response.status).toBe(200);
    expect(data.success).toBe(true);
    expect(data.data.name).toBe('Pablo Contreras');
    expect(data.data.title).toBe('Full Stack Developer');
  });

  test('GREEN: should handle API errors gracefully', async () => {
    // Mock error response
    server.use(
      rest.get('http://localhost:8080/api/v1/personal-info', (req, res, ctx) => {
        return res(ctx.status(500), ctx.json({
          success: false,
          error: 'Internal Server Error'
        }));
      })
    );

    const response = await fetch('http://localhost:8080/api/v1/personal-info');
    expect(response.status).toBe(500);
  });

  test('REFACTOR: should include authentication headers when needed', async () => {
    const response = await fetch('http://localhost:8080/api/v1/projects', {
      headers: {
        'Authorization': 'Bearer mock-token',
        'Content-Type': 'application/json'
      }
    });

    expect(response.status).toBe(200);
  });
});
```

### 3. Astro Actions Testing
```typescript
// test/actions/portfolio-actions.test.ts
import { describe, it, expect, vi, beforeEach } from 'vitest';
import { actions } from 'astro:actions';

// Mock fetch globally
global.fetch = vi.fn();

describe('Portfolio Actions Integration', () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  describe('Experience Actions', () => {
    it('should fetch all experience successfully', async () => {
      // Mock successful API response
      const mockResponse = {
        success: true,
        data: [
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

      // Verificar que fetch fue llamado correctamente
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
});
```

---

## 🎭 End-to-End Testing con Playwright

### 1. E2E Portfolio Tests
```typescript
// e2e/portfolio.spec.ts
import { test, expect } from '@playwright/test';

test.describe('Portfolio E2E Tests - TDD', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('/');
  });

  test('RED: should display complete portfolio information', async ({ page }) => {
    // TDD Red Phase - E2E user journey
    await expect(page.locator('[data-testid="personal-info"]')).toBeVisible();
    await expect(page.locator('[data-testid="projects-section"]')).toBeVisible();

    const name = page.locator('[data-testid="personal-name"]');
    await expect(name).toContainText('Pablo Contreras');
  });

  test('GREEN: should navigate between sections', async ({ page }) => {
    await page.click('[data-testid="projects-link"]');
    await expect(page.locator('[data-testid="projects-section"]')).toBeInViewport();
  });

  test('REFACTOR: should be responsive on mobile', async ({ page }) => {
    await page.setViewportSize({ width: 375, height: 667 });
    await expect(page.locator('[data-testid="mobile-menu"]')).toBeVisible();
  });

  test('should handle API loading states', async ({ page }) => {
    // Mock slow API response
    await page.route('**/api/v1/projects', async route => {
      await new Promise(resolve => setTimeout(resolve, 2000));
      await route.fulfill({
        status: 200,
        contentType: 'application/json',
        body: JSON.stringify({
          success: true,
          data: []
        })
      });
    });

    await page.goto('/');
    await expect(page.locator('[data-testid="loading-spinner"]')).toBeVisible();
    await expect(page.locator('[data-testid="projects-section"]')).toBeVisible();
  });
});
```

### 2. Performance Testing
```typescript
// e2e/performance.spec.ts
import { test, expect } from '@playwright/test';

test.describe('Performance Testing', () => {
  test('should load homepage within performance budget', async ({ page }) => {
    const startTime = Date.now();

    await page.goto('/');
    await page.waitForLoadState('networkidle');

    const loadTime = Date.now() - startTime;
    expect(loadTime).toBeLessThan(3000); // 3 second budget
  });

  test('should achieve Lighthouse performance score >90', async ({ page }) => {
    await page.goto('/');

    // Check main performance metrics
    const lighthouse = await page.lighthouse();
    expect(lighthouse.score('performance')).toBeGreaterThan(0.9);
  });
});
```

---

## 📁 Estructura de Testing

### Directorio de Tests
```
app/
├── src/
│   ├── components/
│   ├── pages/
│   └── actions/
├── test/
│   ├── unit/
│   │   └── components/
│   ├── integration/
│   │   └── api/
│   ├── fixtures/
│   │   ├── data/
│   │   └── mocks/
│   ├── utils/
│   │   └── helpers/
│   └── setup.ts
├── e2e/
│   ├── tests/
│   └── utils/
├── vitest.config.ts
├── playwright.config.ts
└── TESTING.md
```

---

## 🚀 Comandos de Testing

### NPM Scripts
```json
{
  "scripts": {
    "test": "vitest",
    "test:ui": "vitest --ui",
    "test:run": "vitest run",
    "test:watch": "vitest --watch",
    "test:coverage": "vitest run --coverage",

    "test:e2e": "playwright test",
    "test:e2e:ui": "playwright test --ui",
    "test:e2e:headed": "playwright test --headed",

    "test:all": "npm run test:run && npm run test:e2e"
  }
}
```

### Comandos de Desarrollo
```bash
# Tests unitarios
npm run test              # Tests con watch mode
npm run test:run          # Tests una vez
npm run test:coverage     # Tests con coverage

# Tests E2E
npm run test:e2e          # Playwright tests
npm run test:e2e:ui       # Playwright UI mode
npm run test:e2e:headed   # Ver browser durante tests

# Coverage y reportes
npm run test:coverage     # Coverage HTML report
npm run lighthouse        # Lighthouse audit
```

---

## 📊 Quality Gates

### Coverage Requirements
- **Lines**: >80%
- **Functions**: >80%
- **Branches**: >80%
- **Statements**: >80%

### Performance Targets
- **Page Load**: <3s
- **Lighthouse Performance**: >90
- **First Contentful Paint**: <1.5s
- **Largest Contentful Paint**: <2.5s

### Browser Support
- **Desktop**: Chrome 90+, Firefox 88+, Safari 14+, Edge 90+
- **Mobile**: iOS Safari 14+, Chrome Mobile 90+

---

## 🔄 TDD Workflow

### Red-Green-Refactor Cycle
```markdown
1. **RED Phase** (Write Failing Test)
   - Escribir el test más pequeño que falle
   - Ejecutar test para confirmar que falla
   - Commit del test que falla

2. **GREEN Phase** (Make Test Pass)
   - Escribir código mínimo para pasar test
   - Ejecutar test para confirmar que pasa
   - No optimizar aún - solo hacer que funcione

3. **REFACTOR Phase** (Improve Code)
   - Mejorar estructura y diseño del código
   - Ejecutar tests para asegurar que siguen pasando
   - Commit de código limpio y funcional

4. **Repeat**
   - Moverse a siguiente feature/requerimiento
   - Empezar con RED phase nuevamente
```

---

**Esta guía implementa TDD completo para frontend usando las mejores prácticas de 2025, asegurando código confiable, mantenible y completamente testado.**

**Stack**: Vitest + Playwright + Container API + MSW
**Coverage**: >80% obligatorio
**Performance**: Lighthouse >90
**Browser Support**: Modern browsers + Mobile