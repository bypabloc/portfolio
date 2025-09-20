# Astro v5 Complete Guide - 2025

> **Comprehensive guide for Astro v5 with TypeScript, new features like Content Layer, Server Islands, Astro Actions, and modern development practices.**

## 🚀 What's New in Astro v5?

Astro 5.0 brings revolutionary features that make it the **best static site generator for 2025**:

- ✅ **Content Layer** - Load content from any source with type safety
- ✅ **Server Islands** - Mix static and dynamic content seamlessly
- ✅ **Astro Actions** - Type-safe backend functions
- ✅ **Enhanced Performance** - Zero JS by default philosophy
- ✅ **Built-in TypeScript** - Full type safety out of the box

---

## 📋 Quick Start Guide

### 1. Installation & Project Setup

**Create new project:**
```bash
# Using create-astro CLI (recommended)
npm create astro@latest portfolio-astro

# Follow the interactive setup:
# ✔ How would you like to start your new project? › Include sample files
# ✔ Install dependencies? › Yes
# ✔ Do you plan to write TypeScript? › Yes
# ✔ Initialize a new git repository? › Yes
```

**Project structure:**
```
portfolio-astro/
├── src/
│   ├── components/
│   ├── layouts/
│   ├── pages/
│   └── content/          # ← New Content Layer
├── public/
├── astro.config.mjs
└── package.json
```

### 2. Basic Configuration

**astro.config.mjs:**
```typescript
import { defineConfig } from 'astro/config';

export default defineConfig({
  output: 'static',           // SSG mode (perfect for your CV)
  site: 'https://bypabloc.dev',
  integrations: [],
  vite: {
    optimizeDeps: {
      exclude: ['@neonDatabase/serverless'], // For Neon integration
    },
  },
});
```

**TypeScript config (automatic):**
```json
// tsconfig.json (auto-generated)
{
  "extends": "astro/tsconfigs/strict", // Available: base, strict, strictest
  "compilerOptions": {
    "verbatimModuleSyntax": true,      // Better type imports
    "allowJs": true,
    "checkJs": false,
    "types": ["astro/client"]
  }
}
```

### 3. Environment Setup

**.env:**
```env
# Database (Neon)
DATABASE_URL="postgresql://user:pass@ep-xxx.neon.tech/dbname?sslmode=require"

# Site configuration
SITE_URL="https://bypabloc.dev"
SITE_TITLE="Pablo Contreras - Portfolio"
```

---

## 🎯 Content Layer (New in v5)

The **Content Layer** is Astro v5's biggest feature - load content from anywhere with full type safety.

### Basic Content Layer Setup

**src/content/config.ts:**
```typescript
import { defineCollection, z } from 'astro:content';

// Define schemas for your content
const cvCollection = defineCollection({
  type: 'data',
  schema: z.object({
    personalInfo: z.object({
      name: z.string(),
      title: z.string(),
      email: z.string().email(),
      phone: z.string(),
      location: z.string(),
      linkedin: z.string().url(),
      github: z.string().url(),
    }),
    summary: z.string(),
    skills: z.array(z.object({
      category: z.string(),
      items: z.array(z.string()),
    })),
    experience: z.array(z.object({
      company: z.string(),
      position: z.string(),
      startDate: z.string(),
      endDate: z.string().optional(),
      description: z.string(),
      technologies: z.array(z.string()),
    })),
    education: z.array(z.object({
      institution: z.string(),
      degree: z.string(),
      year: z.string(),
    })),
    projects: z.array(z.object({
      name: z.string(),
      description: z.string(),
      technologies: z.array(z.string()),
      githubUrl: z.string().url().optional(),
      liveUrl: z.string().url().optional(),
    })),
  }),
});

export const collections = {
  'cv': cvCollection,
};
```

### Database Content Loader (for FastAPI Lambda APIs)

**src/content/loaders/api-loader.ts:**
```typescript
import { defineLoader } from 'astro/loaders';
import { neon } from '@neondatabase/serverless';

const sql = neon(import.meta.env.DATABASE_URL);

export const databaseLoader = defineLoader({
  name: 'database-cv',
  load: async ({ store, logger }) => {
    logger.info('Loading CV data from database...');

    try {
      // Load personal info
      const [personalInfo] = await sql`
        SELECT name, title, email, phone, location, linkedin, github
        FROM personal_info
        WHERE active = true
        LIMIT 1
      `;

      // Load skills
      const skills = await sql`
        SELECT category, array_agg(skill_name) as items
        FROM skills
        WHERE active = true
        GROUP BY category
        ORDER BY category
      `;

      // Load experience
      const experience = await sql`
        SELECT company, position, start_date, end_date, description,
               array_agg(tech_name) as technologies
        FROM experience e
        LEFT JOIN experience_technologies et ON e.id = et.experience_id
        WHERE e.active = true
        GROUP BY e.id, company, position, start_date, end_date, description
        ORDER BY start_date DESC
      `;

      // Load projects
      const projects = await sql`
        SELECT name, description, github_url, live_url,
               array_agg(tech_name) as technologies
        FROM projects p
        LEFT JOIN project_technologies pt ON p.id = pt.project_id
        WHERE p.active = true
        GROUP BY p.id, name, description, github_url, live_url
        ORDER BY created_at DESC
      `;

      // Load education
      const education = await sql`
        SELECT institution, degree, year
        FROM education
        WHERE active = true
        ORDER BY year DESC
      `;

      // Store in content layer
      store.set('cv-data', {
        id: 'cv-data',
        personalInfo,
        skills,
        experience,
        education,
        projects,
        summary: personalInfo.summary || '',
      });

      logger.info('CV data loaded successfully!');
    } catch (error) {
      logger.error('Failed to load CV data:', error);
      throw error;
    }
  },
});
```

**Use in content config:**
```typescript
// src/content/config.ts
import { databaseLoader } from './loaders/database';

const cvCollection = defineCollection({
  loader: databaseLoader,
  schema: z.object({
    // ... your schema
  }),
});
```

---

## 🏝️ Server Islands (New in v5)

**Server Islands** let you mix static and dynamic content - perfect for personalized CV sections.

### Basic Server Island

**src/components/VisitorCounter.astro:**
```astro
---
// This runs on the server at request time
import { sql } from '../lib/database';

// Update visitor count
await sql`
  INSERT INTO page_views (page, timestamp)
  VALUES ('portfolio', NOW())
`;

// Get total views
const [{ count }] = await sql`
  SELECT COUNT(*) as count
  FROM page_views
  WHERE page = 'portfolio'
`;
---

<div class="visitor-counter">
  <p>Portfolio views: <strong>{count}</strong></p>
</div>

<style>
.visitor-counter {
  background: #f0f9ff;
  padding: 0.5rem 1rem;
  border-radius: 0.5rem;
  border-left: 4px solid #0ea5e9;
}
</style>
```

**Use in page:**
```astro
---
// src/pages/index.astro
import Layout from '../layouts/Layout.astro';
import VisitorCounter from '../components/VisitorCounter.astro';
---

<Layout title="Pablo Contreras - Portfolio">
  <main>
    <h1>Welcome to my Portfolio</h1>

    <!-- This will be rendered on the server -->
    <VisitorCounter server:defer />

    <!-- Static content -->
    <section>
      <h2>About Me</h2>
      <p>Full-stack developer...</p>
    </section>
  </main>
</Layout>
```

### Dynamic Contact Form (Server Island)

**src/components/ContactForm.astro:**
```astro
---
import { sql } from '../lib/database';

// Handle form submission server-side
if (Astro.request.method === 'POST') {
  const formData = await Astro.request.formData();
  const name = formData.get('name') as string;
  const email = formData.get('email') as string;
  const message = formData.get('message') as string;

  if (name && email && message) {
    await sql`
      INSERT INTO contact_messages (name, email, message, created_at)
      VALUES (${name}, ${email}, ${message}, NOW())
    `;
  }
}
---

<form method="POST" class="contact-form">
  <div class="form-group">
    <label for="name">Name:</label>
    <input type="text" id="name" name="name" required />
  </div>

  <div class="form-group">
    <label for="email">Email:</label>
    <input type="email" id="email" name="email" required />
  </div>

  <div class="form-group">
    <label for="message">Message:</label>
    <textarea id="message" name="message" required></textarea>
  </div>

  <button type="submit">Send Message</button>
</form>

<style>
.contact-form {
  max-width: 500px;
  margin: 2rem 0;
}

.form-group {
  margin-bottom: 1rem;
}

label {
  display: block;
  margin-bottom: 0.5rem;
  font-weight: 600;
}

input, textarea {
  width: 100%;
  padding: 0.75rem;
  border: 1px solid #d1d5db;
  border-radius: 0.5rem;
  font-size: 1rem;
}

button {
  background: #3b82f6;
  color: white;
  padding: 0.75rem 1.5rem;
  border: none;
  border-radius: 0.5rem;
  cursor: pointer;
  font-size: 1rem;
}

button:hover {
  background: #2563eb;
}
</style>
```

---

## ⚡ Astro Actions (New Feature)

**Astro Actions** provide type-safe backend functions that you can call from the frontend.

### Setup Actions

**src/actions/index.ts:**
```typescript
import { defineAction } from 'astro:actions';
import { z } from 'astro:schema';
import { sql } from '../lib/database';

// Contact form action
export const sendMessage = defineAction({
  accept: 'form',
  input: z.object({
    name: z.string().min(2, 'Name must be at least 2 characters'),
    email: z.string().email('Invalid email address'),
    message: z.string().min(10, 'Message must be at least 10 characters'),
  }),
  handler: async ({ name, email, message }) => {
    try {
      // Save to database
      const [result] = await sql`
        INSERT INTO contact_messages (name, email, message, created_at)
        VALUES (${name}, ${email}, ${message}, NOW())
        RETURNING id
      `;

      // Optional: Send notification email
      // await sendNotificationEmail({ name, email, message });

      return {
        success: true,
        messageId: result.id,
        message: 'Message sent successfully!',
      };
    } catch (error) {
      throw new Error('Failed to send message. Please try again.');
    }
  },
});

// Download CV action
export const downloadCV = defineAction({
  accept: 'json',
  input: z.object({
    format: z.enum(['pdf', 'doc']).default('pdf'),
  }),
  handler: async ({ format }) => {
    // Track download
    await sql`
      INSERT INTO cv_downloads (format, downloaded_at)
      VALUES (${format}, NOW())
    `;

    // Return download URL or generate PDF
    return {
      downloadUrl: `/cv/pablo-contreras.${format}`,
      format,
      timestamp: new Date().toISOString(),
    };
  },
});

// Get portfolio stats action
export const getPortfolioStats = defineAction({
  accept: 'json',
  handler: async () => {
    const [views] = await sql`
      SELECT COUNT(*) as count
      FROM page_views
      WHERE page = 'portfolio'
    `;

    const [messages] = await sql`
      SELECT COUNT(*) as count
      FROM contact_messages
      WHERE created_at > NOW() - INTERVAL '30 days'
    `;

    const [downloads] = await sql`
      SELECT COUNT(*) as count
      FROM cv_downloads
      WHERE downloaded_at > NOW() - INTERVAL '30 days'
    `;

    return {
      totalViews: views.count,
      messagesLastMonth: messages.count,
      downloadsLastMonth: downloads.count,
    };
  },
});
```

### Using Actions in Components

**src/components/ContactFormWithActions.astro:**
```astro
---
// No server-side code needed here
---

<form id="contact-form" class="contact-form">
  <div class="form-group">
    <label for="name">Name:</label>
    <input type="text" id="name" name="name" required />
    <span class="error" id="name-error"></span>
  </div>

  <div class="form-group">
    <label for="email">Email:</label>
    <input type="email" id="email" name="email" required />
    <span class="error" id="email-error"></span>
  </div>

  <div class="form-group">
    <label for="message">Message:</label>
    <textarea id="message" name="message" required></textarea>
    <span class="error" id="message-error"></span>
  </div>

  <button type="submit" id="submit-btn">Send Message</button>
  <div id="status" class="status"></div>
</form>

<script>
import { actions } from 'astro:actions';

const form = document.getElementById('contact-form') as HTMLFormElement;
const submitBtn = document.getElementById('submit-btn') as HTMLButtonElement;
const status = document.getElementById('status') as HTMLDivElement;

form.addEventListener('submit', async (e) => {
  e.preventDefault();

  // Clear previous errors
  document.querySelectorAll('.error').forEach(el => el.textContent = '');

  // Get form data
  const formData = new FormData(form);

  // Show loading state
  submitBtn.disabled = true;
  submitBtn.textContent = 'Sending...';
  status.textContent = '';

  try {
    // Call Astro Action with type safety
    const result = await actions.sendMessage(formData);

    if (result.data?.success) {
      status.innerHTML = `
        <div class="success">
          ✅ ${result.data.message}
        </div>
      `;
      form.reset();
    }
  } catch (error) {
    // Handle validation errors
    if (error.fields) {
      Object.entries(error.fields).forEach(([field, messages]) => {
        const errorEl = document.getElementById(`${field}-error`);
        if (errorEl && messages) {
          errorEl.textContent = messages[0];
        }
      });
    } else {
      status.innerHTML = `
        <div class="error">
          ❌ ${error.message}
        </div>
      `;
    }
  } finally {
    submitBtn.disabled = false;
    submitBtn.textContent = 'Send Message';
  }
});
</script>

<style>
.contact-form { /* ... existing styles ... */ }

.error {
  color: #dc2626;
  font-size: 0.875rem;
  margin-top: 0.25rem;
  display: block;
}

.status .success {
  color: #059669;
  background: #ecfdf5;
  padding: 0.75rem;
  border-radius: 0.5rem;
  margin-top: 1rem;
}

.status .error {
  color: #dc2626;
  background: #fef2f2;
  padding: 0.75rem;
  border-radius: 0.5rem;
  margin-top: 1rem;
}
</style>
```

### CV Download with Actions

**src/components/CVDownload.astro:**
```astro
<div class="cv-download">
  <h3>Download my CV</h3>
  <div class="download-buttons">
    <button id="download-pdf" class="download-btn">
      📄 Download PDF
    </button>
    <button id="download-doc" class="download-btn">
      📝 Download DOC
    </button>
  </div>
  <div id="download-status"></div>
</div>

<script>
import { actions } from 'astro:actions';

['pdf', 'doc'].forEach(format => {
  const btn = document.getElementById(`download-${format}`);

  btn?.addEventListener('click', async () => {
    try {
      btn.disabled = true;
      btn.textContent = 'Generating...';

      const result = await actions.downloadCV({ format });

      if (result.data?.downloadUrl) {
        // Trigger download
        const link = document.createElement('a');
        link.href = result.data.downloadUrl;
        link.download = `pablo-contreras.${format}`;
        link.click();

        document.getElementById('download-status')!.innerHTML = `
          <div class="success">✅ ${format.toUpperCase()} downloaded!</div>
        `;
      }
    } catch (error) {
      document.getElementById('download-status')!.innerHTML = `
        <div class="error">❌ Download failed</div>
      `;
    } finally {
      btn.disabled = false;
      btn.textContent = `📄 Download ${format.toUpperCase()}`;
    }
  });
});
</script>
```

---

## 💻 TypeScript Integration Examples

### Component Props with Full Type Safety

**src/components/SkillCard.astro:**
```astro
---
// Type definitions
interface Skill {
  name: string;
  level: 'Beginner' | 'Intermediate' | 'Advanced' | 'Expert';
  yearsOfExperience: number;
  category: 'Frontend' | 'Backend' | 'Database' | 'DevOps' | 'Tools';
}

interface Props {
  skills: Skill[];
  category?: string;
  showLevel?: boolean;
}

// Props with default values
const {
  skills,
  category,
  showLevel = true
} = Astro.props;

// Filter skills by category if provided
const filteredSkills = category
  ? skills.filter(skill => skill.category === category)
  : skills;
---

<div class="skills-grid">
  {filteredSkills.map((skill) => (
    <div class="skill-card" data-level={skill.level.toLowerCase()}>
      <h3 class="skill-name">{skill.name}</h3>
      {showLevel && (
        <div class="skill-meta">
          <span class="skill-level">{skill.level}</span>
          <span class="skill-experience">
            {skill.yearsOfExperience}+ years
          </span>
        </div>
      )}
    </div>
  ))}
</div>

<style>
.skills-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  gap: 1rem;
  margin: 2rem 0;
}

.skill-card {
  background: white;
  border: 1px solid #e5e7eb;
  border-radius: 0.5rem;
  padding: 1rem;
  transition: transform 0.2s;
}

.skill-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.skill-card[data-level="expert"] {
  border-left: 4px solid #10b981;
}

.skill-card[data-level="advanced"] {
  border-left: 4px solid #3b82f6;
}

.skill-card[data-level="intermediate"] {
  border-left: 4px solid #f59e0b;
}

.skill-card[data-level="beginner"] {
  border-left: 4px solid #ef4444;
}

.skill-name {
  margin: 0 0 0.5rem 0;
  font-size: 1.1rem;
  font-weight: 600;
}

.skill-meta {
  display: flex;
  justify-content: space-between;
  font-size: 0.875rem;
  color: #6b7280;
}

.skill-level {
  font-weight: 500;
}
</style>
```

### Layout with TypeScript

**src/layouts/CVLayout.astro:**
```astro
---
import type { HTMLAttributes } from 'astro/types';

interface Props extends HTMLAttributes<'html'> {
  title: string;
  description?: string;
  canonicalURL?: string;
  image?: string;
  noindex?: boolean;
}

const {
  title,
  description = 'Pablo Contreras - Full Stack Developer specializing in Vue.js, Node.js, and modern web technologies',
  canonicalURL = new URL(Astro.url.pathname, Astro.site),
  image = '/og-image.jpg',
  noindex = false,
  ...htmlAttrs
} = Astro.props;

// Generate structured data
const structuredData = {
  "@context": "https://schema.org",
  "@type": "Person",
  "name": "Pablo Contreras",
  "jobTitle": "Full Stack Developer",
  "url": Astro.site?.toString(),
  "sameAs": [
    "https://github.com/bypabloc",
    "https://linkedin.com/in/bypabloc"
  ]
};
---

<!DOCTYPE html>
<html lang="en" {...htmlAttrs}>
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />

  <!-- SEO Meta Tags -->
  <title>{title}</title>
  <meta name="description" content={description} />
  <link rel="canonical" href={canonicalURL} />

  {noindex && <meta name="robots" content="noindex, nofollow" />}

  <!-- Open Graph -->
  <meta property="og:type" content="website" />
  <meta property="og:title" content={title} />
  <meta property="og:description" content={description} />
  <meta property="og:url" content={canonicalURL} />
  <meta property="og:image" content={new URL(image, Astro.site)} />

  <!-- Twitter Card -->
  <meta name="twitter:card" content="summary_large_image" />
  <meta name="twitter:title" content={title} />
  <meta name="twitter:description" content={description} />
  <meta name="twitter:image" content={new URL(image, Astro.site)} />

  <!-- Structured Data -->
  <script type="application/ld+json" set:html={JSON.stringify(structuredData)} />

  <!-- Favicon -->
  <link rel="icon" type="image/svg+xml" href="/favicon.svg" />

  <!-- Fonts -->
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
</head>

<body>
  <header class="site-header">
    <nav class="nav-container">
      <a href="/" class="logo">Pablo Contreras</a>
      <ul class="nav-links">
        <li><a href="/#about">About</a></li>
        <li><a href="/#experience">Experience</a></li>
        <li><a href="/#projects">Projects</a></li>
        <li><a href="/#contact">Contact</a></li>
      </ul>
    </nav>
  </header>

  <main>
    <slot />
  </main>

  <footer class="site-footer">
    <div class="footer-content">
      <p>&copy; 2025 Pablo Contreras. Built with Astro & TypeScript.</p>
      <div class="social-links">
        <a href="https://github.com/bypabloc" target="_blank" rel="noopener">GitHub</a>
        <a href="https://linkedin.com/in/bypabloc" target="_blank" rel="noopener">LinkedIn</a>
      </div>
    </div>
  </footer>

  <!-- Analytics (optional) -->
  <script is:inline>
    // Add your analytics code here
  </script>
</body>
</html>

<style is:global>
/* CSS Reset */
*, *::before, *::after {
  box-sizing: border-box;
}

html {
  font-family: 'Inter', system-ui, sans-serif;
  line-height: 1.6;
  scroll-behavior: smooth;
}

body {
  margin: 0;
  padding: 0;
  background: #fafafa;
  color: #1f2937;
}

/* Header */
.site-header {
  background: white;
  border-bottom: 1px solid #e5e7eb;
  padding: 1rem 0;
  position: sticky;
  top: 0;
  z-index: 100;
}

.nav-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 2rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.logo {
  font-size: 1.25rem;
  font-weight: 600;
  text-decoration: none;
  color: #1f2937;
}

.nav-links {
  display: flex;
  list-style: none;
  margin: 0;
  padding: 0;
  gap: 2rem;
}

.nav-links a {
  text-decoration: none;
  color: #6b7280;
  font-weight: 500;
  transition: color 0.2s;
}

.nav-links a:hover {
  color: #3b82f6;
}

/* Main content */
main {
  max-width: 1200px;
  margin: 0 auto;
  padding: 2rem;
  min-height: calc(100vh - 140px);
}

/* Footer */
.site-footer {
  background: #1f2937;
  color: white;
  padding: 2rem 0;
}

.footer-content {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 2rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.social-links {
  display: flex;
  gap: 1rem;
}

.social-links a {
  color: #d1d5db;
  text-decoration: none;
  transition: color 0.2s;
}

.social-links a:hover {
  color: white;
}

/* Responsive */
@media (max-width: 768px) {
  .nav-container,
  .footer-content {
    flex-direction: column;
    gap: 1rem;
  }

  main {
    padding: 1rem;
  }
}
</style>
```

---

## 🔧 Performance Best Practices

### 1. Image Optimization

**Built-in Image component:**
```astro
---
// src/components/ProfileImage.astro
import { Image } from 'astro:assets';
import profilePic from '../assets/pablo-profile.jpg';
---

<div class="profile-section">
  <Image
    src={profilePic}
    alt="Pablo Contreras - Full Stack Developer"
    width={300}
    height={300}
    quality={90}
    format="webp"
    loading="eager"
    class="profile-image"
  />
</div>

<style>
.profile-image {
  border-radius: 50%;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}
</style>
```

### 2. Bundle Optimization

**astro.config.mjs:**
```typescript
import { defineConfig } from 'astro/config';

export default defineConfig({
  build: {
    inlineStylesheets: 'auto',
    assets: 'assets/[hash].[ext]',
  },
  vite: {
    build: {
      cssCodeSplit: true,
      rollupOptions: {
        output: {
          assetFileNames: 'assets/[name]-[hash].[ext]',
          chunkFileNames: 'assets/[name]-[hash].js',
          entryFileNames: 'assets/[name]-[hash].js',
        },
      },
    },
  },
});
```

### 3. Strategic JavaScript Loading

```astro
---
// src/pages/index.astro
---

<!-- Critical inline script -->
<script is:inline>
  // Theme detection
  if (localStorage.theme === 'dark' || (!('theme' in localStorage) && window.matchMedia('(prefers-color-scheme: dark)').matches)) {
    document.documentElement.classList.add('dark')
  }
</script>

<!-- Deferred non-critical scripts -->
<script>
  // Portfolio stats (loads after page)
  import { actions } from 'astro:actions';

  document.addEventListener('DOMContentLoaded', async () => {
    try {
      const stats = await actions.getPortfolioStats();
      updateStatsDisplay(stats.data);
    } catch (error) {
      console.log('Stats loading failed');
    }
  });

  function updateStatsDisplay(stats) {
    // Update stats in UI
  }
</script>
```

### 4. CSS Optimization

```astro
<style>
/* Critical above-the-fold styles */
.hero-section {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
}

/* Use CSS custom properties for theming */
:root {
  --primary-color: #3b82f6;
  --text-color: #1f2937;
  --bg-color: #ffffff;
}

/* Modern CSS features */
.card {
  background: var(--bg-color);
  border-radius: 0.5rem;
  padding: 1.5rem;
  box-shadow: 0 1px 3px 0 rgb(0 0 0 / 0.1);
  transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
}

.card:hover {
  transform: translateY(-2px);
  box-shadow: 0 10px 25px -3px rgb(0 0 0 / 0.1);
}

/* Container queries for responsive components */
@container (min-width: 768px) {
  .card-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}
</style>
```

---

## 🎨 Complete CV Project Example

### Database Schema for CV

```sql
-- Personal information
CREATE TABLE personal_info (
  id SERIAL PRIMARY KEY,
  name VARCHAR(255) NOT NULL,
  title VARCHAR(255) NOT NULL,
  email VARCHAR(255) NOT NULL,
  phone VARCHAR(50),
  location VARCHAR(255),
  linkedin VARCHAR(255),
  github VARCHAR(255),
  summary TEXT,
  active BOOLEAN DEFAULT true,
  updated_at TIMESTAMP DEFAULT NOW()
);

-- Skills
CREATE TABLE skills (
  id SERIAL PRIMARY KEY,
  category VARCHAR(100) NOT NULL,
  skill_name VARCHAR(255) NOT NULL,
  level VARCHAR(50) DEFAULT 'Intermediate',
  years_of_experience INTEGER DEFAULT 1,
  active BOOLEAN DEFAULT true
);

-- Experience
CREATE TABLE experience (
  id SERIAL PRIMARY KEY,
  company VARCHAR(255) NOT NULL,
  position VARCHAR(255) NOT NULL,
  start_date DATE NOT NULL,
  end_date DATE,
  description TEXT,
  active BOOLEAN DEFAULT true
);

-- Technologies per experience
CREATE TABLE experience_technologies (
  id SERIAL PRIMARY KEY,
  experience_id INTEGER REFERENCES experience(id),
  tech_name VARCHAR(255) NOT NULL
);

-- Projects
CREATE TABLE projects (
  id SERIAL PRIMARY KEY,
  name VARCHAR(255) NOT NULL,
  description TEXT,
  github_url VARCHAR(255),
  live_url VARCHAR(255),
  featured BOOLEAN DEFAULT false,
  active BOOLEAN DEFAULT true,
  created_at TIMESTAMP DEFAULT NOW()
);

-- Technologies per project
CREATE TABLE project_technologies (
  id SERIAL PRIMARY KEY,
  project_id INTEGER REFERENCES projects(id),
  tech_name VARCHAR(255) NOT NULL
);

-- Education
CREATE TABLE education (
  id SERIAL PRIMARY KEY,
  institution VARCHAR(255) NOT NULL,
  degree VARCHAR(255) NOT NULL,
  year VARCHAR(10) NOT NULL,
  active BOOLEAN DEFAULT true
);

-- Analytics tables
CREATE TABLE page_views (
  id SERIAL PRIMARY KEY,
  page VARCHAR(100) NOT NULL,
  timestamp TIMESTAMP DEFAULT NOW()
);

CREATE TABLE contact_messages (
  id SERIAL PRIMARY KEY,
  name VARCHAR(255) NOT NULL,
  email VARCHAR(255) NOT NULL,
  message TEXT NOT NULL,
  created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE cv_downloads (
  id SERIAL PRIMARY KEY,
  format VARCHAR(10) NOT NULL,
  downloaded_at TIMESTAMP DEFAULT NOW()
);
```

### Main Portfolio Page

**src/pages/index.astro:**
```astro
---
import CVLayout from '../layouts/CVLayout.astro';
import { getCollection } from 'astro:content';
import SkillCard from '../components/SkillCard.astro';
import ContactFormWithActions from '../components/ContactFormWithActions.astro';
import CVDownload from '../components/CVDownload.astro';
import VisitorCounter from '../components/VisitorCounter.astro';

// Load CV data from Content Layer
const cvData = await getCollection('cv');
const cv = cvData[0].data; // Get the first (and only) CV entry

// Type the data for better IDE support
interface CVData {
  personalInfo: {
    name: string;
    title: string;
    email: string;
    // ... other fields
  };
  skills: Array<{
    category: string;
    items: string[];
  }>;
  experience: Array<{
    company: string;
    position: string;
    // ... other fields
  }>;
  // ... other sections
}

const typedCV = cv as CVData;
---

<CVLayout
  title={`${typedCV.personalInfo.name} - ${typedCV.personalInfo.title}`}
  description="Full Stack Developer specializing in Vue.js, Node.js, PostgreSQL, and modern web technologies"
>
  <!-- Hero Section -->
  <section id="hero" class="hero-section">
    <div class="hero-content">
      <h1 class="hero-title">{typedCV.personalInfo.name}</h1>
      <p class="hero-subtitle">{typedCV.personalInfo.title}</p>
      <p class="hero-description">{typedCV.summary}</p>

      <div class="hero-actions">
        <a href="#contact" class="cta-button primary">Get in Touch</a>
        <CVDownload />
      </div>

      <!-- Visitor counter as server island -->
      <VisitorCounter server:defer />
    </div>
  </section>

  <!-- About Section -->
  <section id="about" class="section">
    <div class="container">
      <h2 class="section-title">About Me</h2>
      <div class="about-grid">
        <div class="about-text">
          <p>{typedCV.summary}</p>

          <div class="contact-info">
            <p>📧 {typedCV.personalInfo.email}</p>
            <p>📱 {typedCV.personalInfo.phone}</p>
            <p>📍 {typedCV.personalInfo.location}</p>
          </div>

          <div class="social-links">
            <a href={typedCV.personalInfo.linkedin} target="_blank" rel="noopener">
              LinkedIn
            </a>
            <a href={typedCV.personalInfo.github} target="_blank" rel="noopener">
              GitHub
            </a>
          </div>
        </div>
      </div>
    </div>
  </section>

  <!-- Skills Section -->
  <section id="skills" class="section">
    <div class="container">
      <h2 class="section-title">Skills & Technologies</h2>

      {typedCV.skills.map((skillCategory) => (
        <div class="skill-category">
          <h3 class="category-title">{skillCategory.category}</h3>
          <div class="skills-grid">
            {skillCategory.items.map((skill) => (
              <div class="skill-tag">{skill}</div>
            ))}
          </div>
        </div>
      ))}
    </div>
  </section>

  <!-- Experience Section -->
  <section id="experience" class="section">
    <div class="container">
      <h2 class="section-title">Professional Experience</h2>

      <div class="timeline">
        {typedCV.experience.map((job, index) => (
          <div class="timeline-item">
            <div class="timeline-marker"></div>
            <div class="timeline-content">
              <h3 class="job-title">{job.position}</h3>
              <h4 class="company-name">{job.company}</h4>
              <p class="job-dates">
                {job.startDate} - {job.endDate || 'Present'}
              </p>
              <p class="job-description">{job.description}</p>

              <div class="technologies">
                {job.technologies.map((tech) => (
                  <span class="tech-tag">{tech}</span>
                ))}
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  </section>

  <!-- Projects Section -->
  <section id="projects" class="section">
    <div class="container">
      <h2 class="section-title">Featured Projects</h2>

      <div class="projects-grid">
        {typedCV.projects.map((project) => (
          <div class="project-card">
            <h3 class="project-name">{project.name}</h3>
            <p class="project-description">{project.description}</p>

            <div class="project-technologies">
              {project.technologies.map((tech) => (
                <span class="tech-tag">{tech}</span>
              ))}
            </div>

            <div class="project-links">
              {project.githubUrl && (
                <a href={project.githubUrl} target="_blank" rel="noopener">
                  GitHub
                </a>
              )}
              {project.liveUrl && (
                <a href={project.liveUrl} target="_blank" rel="noopener">
                  Live Demo
                </a>
              )}
            </div>
          </div>
        ))}
      </div>
    </div>
  </section>

  <!-- Education Section -->
  <section id="education" class="section">
    <div class="container">
      <h2 class="section-title">Education</h2>

      <div class="education-list">
        {typedCV.education.map((edu) => (
          <div class="education-item">
            <h3 class="degree">{edu.degree}</h3>
            <h4 class="institution">{edu.institution}</h4>
            <p class="graduation-year">{edu.year}</p>
          </div>
        ))}
      </div>
    </div>
  </section>

  <!-- Contact Section -->
  <section id="contact" class="section">
    <div class="container">
      <h2 class="section-title">Get in Touch</h2>
      <p class="section-description">
        I'm always interested in new opportunities and interesting projects.
      </p>

      <ContactFormWithActions client:load />
    </div>
  </section>
</CVLayout>

<style>
/* Hero Section */
.hero-section {
  min-height: 80vh;
  display: flex;
  align-items: center;
  justify-content: center;
  text-align: center;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
}

.hero-content {
  max-width: 800px;
  padding: 2rem;
}

.hero-title {
  font-size: 3rem;
  font-weight: 700;
  margin-bottom: 1rem;
}

.hero-subtitle {
  font-size: 1.5rem;
  font-weight: 400;
  margin-bottom: 2rem;
  opacity: 0.9;
}

.hero-description {
  font-size: 1.1rem;
  line-height: 1.6;
  margin-bottom: 2rem;
  opacity: 0.9;
}

.hero-actions {
  display: flex;
  gap: 1rem;
  justify-content: center;
  flex-wrap: wrap;
}

.cta-button {
  display: inline-block;
  padding: 0.75rem 2rem;
  border-radius: 0.5rem;
  text-decoration: none;
  font-weight: 600;
  transition: all 0.3s ease;
}

.cta-button.primary {
  background: white;
  color: #667eea;
}

.cta-button.primary:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 25px rgba(0, 0, 0, 0.2);
}

/* Sections */
.section {
  padding: 4rem 0;
}

.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 2rem;
}

.section-title {
  font-size: 2.5rem;
  font-weight: 700;
  text-align: center;
  margin-bottom: 3rem;
  color: #1f2937;
}

.section-description {
  text-align: center;
  font-size: 1.1rem;
  color: #6b7280;
  margin-bottom: 2rem;
}

/* Skills */
.skill-category {
  margin-bottom: 2rem;
}

.category-title {
  font-size: 1.5rem;
  font-weight: 600;
  margin-bottom: 1rem;
  color: #374151;
}

.skills-grid {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
}

.skill-tag {
  background: #e5e7eb;
  color: #374151;
  padding: 0.5rem 1rem;
  border-radius: 1rem;
  font-size: 0.875rem;
  font-weight: 500;
}

/* Timeline */
.timeline {
  position: relative;
  padding-left: 2rem;
}

.timeline::before {
  content: '';
  position: absolute;
  left: 0.5rem;
  top: 0;
  bottom: 0;
  width: 2px;
  background: #e5e7eb;
}

.timeline-item {
  position: relative;
  margin-bottom: 2rem;
}

.timeline-marker {
  position: absolute;
  left: -1.5rem;
  top: 0.5rem;
  width: 1rem;
  height: 1rem;
  background: #3b82f6;
  border-radius: 50%;
  border: 3px solid white;
  box-shadow: 0 0 0 3px #e5e7eb;
}

.timeline-content {
  background: white;
  padding: 1.5rem;
  border-radius: 0.5rem;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}

.job-title {
  font-size: 1.25rem;
  font-weight: 600;
  margin-bottom: 0.5rem;
  color: #1f2937;
}

.company-name {
  font-size: 1.1rem;
  font-weight: 500;
  margin-bottom: 0.5rem;
  color: #3b82f6;
}

.job-dates {
  font-size: 0.875rem;
  color: #6b7280;
  margin-bottom: 1rem;
}

.job-description {
  line-height: 1.6;
  margin-bottom: 1rem;
}

.technologies {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
}

.tech-tag {
  background: #f3f4f6;
  color: #374151;
  padding: 0.25rem 0.75rem;
  border-radius: 0.5rem;
  font-size: 0.75rem;
  font-weight: 500;
}

/* Projects */
.projects-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
  gap: 2rem;
}

.project-card {
  background: white;
  border-radius: 0.5rem;
  padding: 1.5rem;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
  transition: transform 0.3s ease;
}

.project-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 25px rgba(0, 0, 0, 0.15);
}

.project-name {
  font-size: 1.25rem;
  font-weight: 600;
  margin-bottom: 1rem;
  color: #1f2937;
}

.project-description {
  line-height: 1.6;
  margin-bottom: 1rem;
  color: #6b7280;
}

.project-technologies {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
  margin-bottom: 1rem;
}

.project-links {
  display: flex;
  gap: 1rem;
}

.project-links a {
  color: #3b82f6;
  text-decoration: none;
  font-weight: 500;
  transition: color 0.2s;
}

.project-links a:hover {
  color: #2563eb;
}

/* Education */
.education-list {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 2rem;
}

.education-item {
  background: white;
  padding: 1.5rem;
  border-radius: 0.5rem;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}

.degree {
  font-size: 1.25rem;
  font-weight: 600;
  margin-bottom: 0.5rem;
  color: #1f2937;
}

.institution {
  font-size: 1.1rem;
  font-weight: 500;
  margin-bottom: 0.5rem;
  color: #3b82f6;
}

.graduation-year {
  color: #6b7280;
  font-weight: 500;
}

/* Responsive Design */
@media (max-width: 768px) {
  .hero-title {
    font-size: 2rem;
  }

  .hero-subtitle {
    font-size: 1.25rem;
  }

  .section-title {
    font-size: 2rem;
  }

  .timeline {
    padding-left: 1rem;
  }

  .timeline-marker {
    left: -1rem;
  }

  .projects-grid {
    grid-template-columns: 1fr;
  }
}
</style>
```

---

## 🚀 Build & Deploy

### Build Configuration

**package.json scripts:**
```json
{
  "scripts": {
    "dev": "astro dev",
    "start": "astro dev",
    "build": "astro check && astro build",
    "preview": "astro preview",
    "type-check": "astro check",
    "lint": "eslint src --ext .js,.ts,.astro"
  }
}
```

### Deployment to Vercel/Netlify

**vercel.json:**
```json
{
  "buildCommand": "npm run build",
  "outputDirectory": "dist",
  "framework": "astro"
}
```

**netlify.toml:**
```toml
[build]
  command = "npm run build"
  publish = "dist"

[build.environment]
  NODE_VERSION = "20"

[[redirects]]
  from = "/api/*"
  to = "/.netlify/functions/:splat"
  status = 200
```

---

## 📊 Performance Monitoring

### Web Vitals Tracking

```astro
<script>
import { getCLS, getFID, getFCP, getLCP, getTTFB } from 'web-vitals';

// Track Core Web Vitals
getCLS(console.log);
getFID(console.log);
getFCP(console.log);
getLCP(console.log);
getTTFB(console.log);

// Send to analytics
function sendToAnalytics(metric) {
  // Send to your analytics provider
  fetch('/api/analytics', {
    method: 'POST',
    body: JSON.stringify(metric),
  });
}

getCLS(sendToAnalytics);
getFID(sendToAnalytics);
getFCP(sendToAnalytics);
getLCP(sendToAnalytics);
getTTFB(sendToAnalytics);
</script>
```

---

## 🧪 Testing & TDD for Astro v5

### Testing Framework Setup

**Recommended Testing Stack 2025:**
```yaml
Unit Testing: Vitest + Container API
Component Testing: Vitest + Happy-DOM
Integration Testing: Vitest + Astro Dev Server
End-to-End Testing: Playwright
API Mocking: Mock Service Worker (MSW)
Visual Testing: Storybook + Chromatic
```

### Vitest Configuration

**vitest.config.ts:**
```typescript
import { getViteConfig } from 'astro/config';

export default getViteConfig({
  test: {
    environment: 'happy-dom',
    globals: true,
    setupFiles: ['./test/setup.ts'],
    exclude: ['**/e2e/**'],
    coverage: {
      provider: 'v8',
      reporter: ['text', 'html', 'lcov'],
      threshold: {
        global: {
          lines: 80,
          functions: 80,
          branches: 80,
          statements: 80
        }
      }
    }
  }
});
```

### TDD Component Testing with Container API

**test/components/PersonalInfo.test.ts:**
```typescript
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

  test('RED: should render personal information', async () => {
    const result = await container.renderToString(PersonalInfo, {
      props: {
        name: 'Pablo Contreras',
        title: 'Full Stack Developer',
        email: 'pablo@bypabloc.com'
      }
    });

    expect(result).toContain('Pablo Contreras');
    expect(result).toContain('Full Stack Developer');
  });

  test('GREEN: should handle missing props gracefully', async () => {
    const result = await container.renderToString(PersonalInfo, {
      props: { name: 'Pablo Contreras' }
    });

    expect(result).toContain('Pablo Contreras');
    expect(result).not.toContain('undefined');
  });
});
```

### API Integration Testing with MSW

**test/api/lambda-integration.test.ts:**
```typescript
import { setupServer } from 'msw/node';
import { rest } from 'msw';
import { expect, test, describe, beforeAll, afterAll } from 'vitest';

const server = setupServer(
  rest.get('https://api.portfolio.com/personal-info', (req, res, ctx) => {
    return res(
      ctx.status(200),
      ctx.json({
        name: 'Pablo Contreras',
        title: 'Full Stack Developer',
        email: 'pablo@bypabloc.com'
      })
    );
  })
);

describe('Lambda API Integration - TDD', () => {
  beforeAll(() => server.listen());
  afterAll(() => server.close());

  test('should fetch data from Lambda API', async () => {
    const response = await fetch('https://api.portfolio.com/personal-info');
    const data = await response.json();

    expect(response.status).toBe(200);
    expect(data.name).toBe('Pablo Contreras');
  });
});
```

### Test Scripts in package.json

```json
{
  "scripts": {
    "test": "vitest",
    "test:ui": "vitest --ui",
    "test:coverage": "vitest --coverage",
    "test:e2e": "playwright test",
    "test:e2e:ui": "playwright test --ui",
    "test:components": "vitest --run test/components",
    "test:integration": "vitest --run test/integration",
    "test:watch": "vitest --watch"
  }
}
```

### TDD Workflow for Astro Components

1. **RED Phase**: Write failing test for component behavior
2. **GREEN Phase**: Create minimal component to pass test
3. **REFACTOR Phase**: Improve component structure and styling
4. **Repeat**: Add new features following TDD cycle

### TypeScript Strict Mode (Required)

**IMPORTANTE: Todo JavaScript debe ser TypeScript estricto**

**tsconfig.json configuration:**
```json
{
  "extends": "astro/tsconfigs/strict",
  "compilerOptions": {
    "strict": true,
    "noImplicitAny": true,
    "strictNullChecks": true,
    "strictFunctionTypes": true,
    "strictBindCallApply": true,
    "strictPropertyInitialization": true,
    "noImplicitReturns": true,
    "noImplicitThis": true,
    "noUnusedLocals": true,
    "noUnusedParameters": true,
    "exactOptionalPropertyTypes": true,
    "noImplicitOverride": true,
    "noPropertyAccessFromIndexSignature": true,
    "noUncheckedIndexedAccess": true
  }
}
```

**ESLint TypeScript Rules:**
```json
{
  "extends": [
    "@typescript-eslint/strict-type-checked",
    "@typescript-eslint/stylistic-type-checked"
  ],
  "rules": {
    "@typescript-eslint/no-explicit-any": "error",
    "@typescript-eslint/no-unsafe-assignment": "error",
    "@typescript-eslint/no-unsafe-call": "error",
    "@typescript-eslint/no-unsafe-member-access": "error",
    "@typescript-eslint/no-unsafe-return": "error",
    "@typescript-eslint/prefer-nullish-coalescing": "error",
    "@typescript-eslint/prefer-optional-chain": "error"
  }
}
```

**Mandatory TypeScript Patterns:**
```typescript
// ❌ Prohibido - JavaScript sin tipos
function getData() {
  return fetch('/api/data');
}

// ✅ Requerido - TypeScript estricto
interface ApiResponse<T> {
  success: boolean;
  data: T;
  timestamp: string;
}

async function getData(): Promise<ApiResponse<PersonalInfo>> {
  const response = await fetch('/api/data');
  return response.json() as ApiResponse<PersonalInfo>;
}

// ❌ Prohibido - any types
const data: any = await getData();

// ✅ Requerido - tipos explícitos
const data: ApiResponse<PersonalInfo> = await getData();
```

---

## 🎯 Production Checklist

### Pre-deployment

- [ ] **Content Layer** configured with proper schemas
- [ ] **Astro Actions** implemented for dynamic functionality
- [ ] **Testing suite** implemented with 80%+ coverage
- [ ] **E2E tests** passing for critical user journeys
- [ ] **API integration tests** validating Lambda endpoints
- [ ] **TypeScript** strict mode enabled
- [ ] **SEO meta tags** implemented in layout
- [ ] **Images optimized** using Astro Image component
- [ ] **Performance** tested (Lighthouse score >90)
- [ ] **Database connection** tested and secured
- [ ] **Environment variables** configured
- [ ] **Build process** tested locally

### Post-deployment

- [ ] **Core Web Vitals** monitored
- [ ] **Analytics** tracking implemented
- [ ] **Error monitoring** set up
- [ ] **Database performance** optimized
- [ ] **CDN configuration** verified
- [ ] **SSL certificate** active
- [ ] **Mobile responsiveness** tested

---

## 📚 Additional Resources

### Official Documentation
- [Astro v5 Docs](https://docs.astro.build/) - Complete documentation
- [Content Layer Guide](https://docs.astro.build/en/guides/content-layer/)
- [Server Islands Guide](https://docs.astro.build/en/guides/server-islands/)
- [Astro Actions Guide](https://docs.astro.build/en/guides/actions/)

### Performance & Best Practices
- [Astro Performance Tips](https://docs.astro.build/en/guides/performance/)
- [TypeScript Guide](https://docs.astro.build/en/guides/typescript/)
- [Deployment Guide](https://docs.astro.build/en/guides/deploy/)

### Community
- [Astro Discord](https://astro.build/chat)
- [GitHub Repository](https://github.com/withastro/astro)
- [Astro Themes](https://astro.build/themes/)

---

**Last Updated**: January 2025
**Astro Version**: v5.1+
**Guide Version**: 1.0.0

*This comprehensive guide covers everything you need to build a modern portfolio/CV with Astro v5, including the latest features like Content Layer, Server Islands, and Astro Actions.*