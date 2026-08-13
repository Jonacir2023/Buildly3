import { defineConfig, devices } from '@playwright/test'

export default defineConfig({
  testDir: './tests',
  testMatch: '**/*.spec.ts',

  fullyParallel: false,
  forbidOnly: false,
  retries: 0,
  workers: 1,

  reporter: [
    ['html', { outputFolder: 'tests/report' }],
    ['list']
  ],

  use: {
    baseURL: 'https://jonacir2023.github.io/buildly/',
    trace: 'on-first-retry',
    screenshot: 'only-on-failure',
  },

  projects: [
    {
      name: 'chromium',
      use: { ...devices['Desktop Chrome'] },
    },
  ],

  webServer: undefined, // Aplicação já está no GitHub Pages
})
