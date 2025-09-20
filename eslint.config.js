/**
 * ESLint Configuration - 2025 Best Practices
 * Using ESLint Flat Config format (modern approach)
 *
 * Supports: JavaScript, TypeScript, Vue.js, React
 * Integration: Prettier, Node.js, Browser environments
 *
 * @author Pablo Contreras (Bypabloc)
 * @created 2025-01-19
 * @updated 2025-01-19
 */

import eslint from '@eslint/js';
import globals from 'globals';
import typescriptEslint from 'typescript-eslint';
import pluginVue from 'eslint-plugin-vue';
import pluginReact from 'eslint-plugin-react';
import pluginAstro from 'eslint-plugin-astro';
import { fixupConfigRules } from '@eslint/compat';
import prettierConfig from 'eslint-config-prettier';

export default [
  // Global ignores
  {
    ignores: [
      '**/node_modules/**',
      '**/dist/**',
      '**/build/**',
      '**/.venv/**',
      '**/venv/**',
      '**/coverage/**',
      '**/.nyc_output/**',
      '**/migrations/**',
      '**/static/**',
      '**/*.min.js',
      '**/*.d.ts',
      '**/generated/**',
      '**/.git/**',
    ],
  },

  // Base JavaScript configuration
  {
    files: ['**/*.js', '**/*.mjs', '**/*.cjs'],
    ...eslint.configs.recommended,
    languageOptions: {
      ecmaVersion: 2025,
      sourceType: 'module',
      globals: {
        ...globals.browser,
        ...globals.node,
        ...globals.es2025,
      },
    },
    rules: {
      // Modern JavaScript best practices
      'prefer-const': 'error',
      'no-var': 'error',
      'no-unused-vars': ['error', {
        argsIgnorePattern: '^_',
        varsIgnorePattern: '^_',
        caughtErrorsIgnorePattern: '^_'
      }],
      'no-console': ['warn', { allow: ['warn', 'error'] }],
      'eqeqeq': ['error', 'always'],
      'curly': ['error', 'all'],
      'no-eval': 'error',
      'no-implied-eval': 'error',
      'no-new-wrappers': 'error',
      'no-throw-literal': 'error',
      'prefer-template': 'error',
      'template-curly-spacing': ['error', 'never'],
      'object-shorthand': ['error', 'always'],
      'prefer-destructuring': ['error', {
        array: true,
        object: true
      }],
    },
  },

  // TypeScript configuration
  ...typescriptEslint.config({
    files: ['**/*.ts', '**/*.tsx', '**/*.mts', '**/*.cts'],
    extends: [
      eslint.configs.recommended,
      ...typescriptEslint.configs.recommended,
      ...typescriptEslint.configs.strict,
    ],
    languageOptions: {
      ecmaVersion: 2025,
      sourceType: 'module',
      globals: {
        ...globals.browser,
        ...globals.node,
        ...globals.es2025,
      },
      parser: typescriptEslint.parser,
      parserOptions: {
        project: ['./tsconfig.json'],
        tsconfigRootDir: import.meta.dirname,
      },
    },
    rules: {
      // TypeScript-specific rules
      '@typescript-eslint/no-unused-vars': ['error', {
        argsIgnorePattern: '^_',
        varsIgnorePattern: '^_',
        caughtErrorsIgnorePattern: '^_'
      }],
      '@typescript-eslint/explicit-function-return-type': 'error',
      '@typescript-eslint/explicit-member-accessibility': 'error',
      '@typescript-eslint/no-explicit-any': 'error',
      '@typescript-eslint/no-non-null-assertion': 'error',
      '@typescript-eslint/prefer-nullish-coalescing': 'error',
      '@typescript-eslint/prefer-optional-chain': 'error',
      '@typescript-eslint/strict-boolean-expressions': 'error',
      '@typescript-eslint/prefer-readonly': 'error',
      '@typescript-eslint/prefer-readonly-parameter-types': 'off', // Too strict for general use
      '@typescript-eslint/consistent-type-definitions': ['error', 'interface'],
      '@typescript-eslint/consistent-type-imports': ['error', {
        prefer: 'type-imports',
        disallowTypeAnnotations: false
      }],
      '@typescript-eslint/no-import-type-side-effects': 'error',

      // Disable base rules covered by TypeScript
      'no-unused-vars': 'off',
      'no-undef': 'off',
    },
  }),

  // Vue.js configuration
  {
    files: ['**/*.vue'],
    plugins: {
      vue: pluginVue,
    },
    languageOptions: {
      ...pluginVue.configs['flat/essential'].languageOptions,
      ecmaVersion: 2025,
      sourceType: 'module',
      globals: {
        ...globals.browser,
        ...globals.node,
      },
      parserOptions: {
        parser: typescriptEslint.parser,
        ecmaFeatures: {
          jsx: true,
        },
        sourceType: 'module',
      },
    },
    rules: {
      ...pluginVue.configs['flat/vue3-strongly-recommended'].rules,
      ...pluginVue.configs['flat/vue3-recommended'].rules,

      // Vue-specific rules
      'vue/component-name-in-template-casing': ['error', 'PascalCase'],
      'vue/component-definition-name-casing': ['error', 'PascalCase'],
      'vue/custom-event-name-casing': ['error', 'camelCase'],
      'vue/define-macros-order': ['error', {
        order: ['defineProps', 'defineEmits'],
      }],
      'vue/html-self-closing': ['error', {
        html: {
          void: 'never',
          normal: 'always',
          component: 'always',
        },
        svg: 'always',
        math: 'always',
      }],
      'vue/max-attributes-per-line': ['error', {
        singleline: { max: 1 },
        multiline: { max: 1 },
      }],
      'vue/multi-word-component-names': 'error',
      'vue/no-unused-vars': 'error',
      'vue/padding-line-between-blocks': ['error', 'always'],
      'vue/prefer-import-from-vue': 'error',
      'vue/prefer-separate-static-class': 'error',
      'vue/prefer-true-attribute-shorthand': 'error',
      'vue/require-macro-variable-name': ['error', {
        defineProps: 'props',
        defineEmits: 'emit',
        defineSlots: 'slots',
        useSlots: 'slots',
        useAttrs: 'attrs',
      }],
      'vue/script-setup-uses-vars': 'error',
      'vue/block-order': ['error', {
        order: ['script', 'template', 'style'],
      }],
    },
  },

  // React configuration
  {
    files: ['**/*.jsx', '**/*.tsx'],
    ...fixupConfigRules(pluginReact.configs.recommended),
    languageOptions: {
      ecmaVersion: 2025,
      sourceType: 'module',
      globals: {
        ...globals.browser,
      },
      parserOptions: {
        ecmaFeatures: {
          jsx: true,
        },
      },
    },
    settings: {
      react: {
        version: 'detect',
      },
    },
    rules: {
      ...pluginReact.configs.recommended.rules,

      // Modern React best practices
      'react/react-in-jsx-scope': 'off', // Not needed in React 17+
      'react/jsx-uses-react': 'off', // Not needed in React 17+
      'react/prop-types': 'off', // Use TypeScript for prop validation
      'react/jsx-props-no-spreading': 'warn',
      'react/function-component-definition': ['error', {
        namedComponents: 'arrow-function',
        unnamedComponents: 'arrow-function',
      }],
      'react/jsx-filename-extension': ['error', {
        extensions: ['.jsx', '.tsx'],
      }],
      'react/jsx-max-props-per-line': ['error', { maximum: 1 }],
      'react/jsx-first-prop-new-line': ['error', 'multiline'],
      'react/jsx-closing-bracket-location': ['error', 'tag-aligned'],
      'react/jsx-closing-tag-location': 'error',
      'react/jsx-curly-spacing': ['error', 'never'],
      'react/jsx-equals-spacing': ['error', 'never'],
      'react/jsx-indent': ['error', 2],
      'react/jsx-indent-props': ['error', 2],
      'react/jsx-tag-spacing': ['error', {
        closingSlash: 'never',
        beforeSelfClosing: 'always',
        afterOpening: 'never',
        beforeClosing: 'never',
      }],
      'react/self-closing-comp': ['error', {
        component: true,
        html: true,
      }],
    },
  },

  // Astro configuration
  ...pluginAstro.configs['flat/recommended'],
  {
    files: ['**/*.astro'],
    languageOptions: {
      ecmaVersion: 2025,
      sourceType: 'module',
      globals: {
        ...globals.browser,
        ...globals.node,
      },
      parser: 'astro-eslint-parser',
      parserOptions: {
        parser: typescriptEslint.parser,
        extraFileExtensions: ['.astro'],
        sourceType: 'module',
      },
    },
    rules: {
      // Astro-specific rules
      'astro/no-conflict-set-directives': 'error',
      'astro/no-unused-define-vars-in-style': 'error',
      'astro/no-deprecated-astro-canonicalurl': 'error',
      'astro/no-deprecated-astro-fetchcontent': 'error',
      'astro/no-deprecated-astro-resolve': 'error',
      'astro/no-deprecated-getentrybyslug': 'error',
      'astro/valid-compile': 'error',
      'astro/no-set-html-directive': 'warn',

      // Accessibility for Astro
      'astro/no-set-text-directive': 'error',
      'astro/prefer-class-list-directive': 'error',
      'astro/prefer-object-class-list': 'error',
      'astro/prefer-split-class-list': 'error',

      // JSX in Astro components
      'astro/jsx-a11y/alt-text': 'error',
      'astro/jsx-a11y/anchor-has-content': 'error',
      'astro/jsx-a11y/anchor-is-valid': 'error',
      'astro/jsx-a11y/aria-props': 'error',
      'astro/jsx-a11y/aria-proptypes': 'error',
      'astro/jsx-a11y/aria-unsupported-elements': 'error',
      'astro/jsx-a11y/role-has-required-aria-props': 'error',
      'astro/jsx-a11y/role-supports-aria-props': 'error',
    },
  },

  // TypeScript support in Astro frontmatter
  {
    files: ['**/*.astro'],
    rules: {
      // Allow TypeScript features in frontmatter
      '@typescript-eslint/no-unused-vars': ['error', {
        argsIgnorePattern: '^_',
        varsIgnorePattern: '^_',
        caughtErrorsIgnorePattern: '^_',
        // Allow unused vars in Astro frontmatter (common pattern)
        ignoreRestSiblings: true,
      }],
      // Allow any for Astro component props (common pattern)
      '@typescript-eslint/no-explicit-any': 'warn',
    },
  },

  // Test files configuration
  {
    files: [
      '**/*.test.js',
      '**/*.test.ts',
      '**/*.test.jsx',
      '**/*.test.tsx',
      '**/*.spec.js',
      '**/*.spec.ts',
      '**/*.spec.jsx',
      '**/*.spec.tsx',
      '**/tests/**/*.js',
      '**/tests/**/*.ts',
      '**/test/**/*.js',
      '**/test/**/*.ts',
    ],
    languageOptions: {
      globals: {
        ...globals.jest,
        ...globals.vitest,
        describe: 'readonly',
        it: 'readonly',
        test: 'readonly',
        expect: 'readonly',
        beforeEach: 'readonly',
        afterEach: 'readonly',
        beforeAll: 'readonly',
        afterAll: 'readonly',
        vi: 'readonly',
        jest: 'readonly',
      },
    },
    rules: {
      // Allow console in tests
      'no-console': 'off',
      // Allow any in test files for mocking
      '@typescript-eslint/no-explicit-any': 'off',
      // Allow non-null assertions in tests
      '@typescript-eslint/no-non-null-assertion': 'off',
    },
  },

  // Node.js specific files
  {
    files: [
      '**/scripts/**/*.js',
      '**/scripts/**/*.ts',
      '**/*.config.js',
      '**/*.config.ts',
      '**/build/**/*.js',
      '**/build/**/*.ts',
    ],
    languageOptions: {
      globals: {
        ...globals.node,
      },
    },
    rules: {
      // Allow console in build scripts
      'no-console': 'off',
      // Allow require in config files
      '@typescript-eslint/no-require-imports': 'off',
    },
  },

  // Prettier integration (must be last)
  prettierConfig,
];