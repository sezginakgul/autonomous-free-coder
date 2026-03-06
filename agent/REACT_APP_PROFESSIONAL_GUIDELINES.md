# Professional React App Setup Guidelines (Comprehensive)

Version: 1.0
Date: 2026-03-06
Language: English

Purpose

- A single, authoritative checklist and ruleset for creating, maintaining, testing, securing and shipping production-grade React applications.
- Agents, contributors and CI must apply these rules when an Issue requests creating or updating a React app. The agent should read this file first and operate only within the Issue's target directory.

How the AI agent must use this file

- Before executing any `[RUN:]` or `[FILE:]` actions, read this file and follow its rules.
- Operate only on the single target directory provided by the Issue (`TARGET_DIR` env or `path:`/`dir:` in the Issue body). Do not modify other top-level projects.
- Never open a PR unless all required checks in the "PR gating" section pass.

Table of contents

1. Goals & Acceptance Criteria
2. Project Initialization
3. Recommended Project Structure
4. Tooling & Config (mandatory)
5. Code Style and Linting
6. Type Safety
7. Testing Strategy
8. Accessibility
9. Performance
10. Security
11. Dependency Management & Supply Chain
12. CI / CD Requirements
13. Observability & Monitoring
14. Release Process & Versioning
15. Developer Experience (DX)
16. PR Gating / Merge Requirements
17. Templates, Examples & Useful Links

---

1. Goals & Acceptance Criteria

- The app must build reproducibly with `npm ci` and `npm run build` (or `pnpm`/`yarn` equivalent) inside the target directory.
- Linting and formatting must pass automatically (`eslint` and `prettier`).
- Unit/integration tests must run and meet configured minimum coverage thresholds.
- Accessibility: key pages/components must meet WCAG 2.1 AA baseline.
- Core Web Vitals targets: LCP ≤ 2.5s (mobile target varies by region), CLS < 0.1, INP/TTI within acceptable threshold. Team should set a budget.
- No known critical security vulnerabilities in direct dependencies (auto-scan by Dependabot/Snyk/OSS scanner) — or a documented justification.
- CI must run lint/build/test and block merging if checks fail.

2. Project Initialization (opinions and requirements)

- Prefer Vite for new React projects (fast dev server, modern tooling). If project uses CRA historically, prefer migrating to Vite for new work unless constrained.
- Node: Use LTS (18+ or current LTS per project policy). Declare Node engine in `package.json` if project expects a specific version.
- Use strict package-manager policy: prefer `npm` or `pnpm`. For CI reproducibility, use lockfile and `npm ci` (or `pnpm install --frozen-lockfile`). Do not commit `node_modules`.
- Initialize repository with minimal README, LICENSE, .gitignore with Node and typical patterns.

3. Recommended Project Structure

- Keep `src/` as source root, `public/` for static assets.
- Example layout (adapt to project complexity):
  - src/
    - app/ (root-level app bootstrap, routes)
    - components/ (shared presentational components)
    - features/ (domain features, each with own folder: components, hooks, tests)
    - hooks/ (shared hooks)
    - services/ (API clients, adapters)
    - pages/ or routes/
    - styles/ (global tokens, utilities)
    - utils/ (pure helpers)
    - assets/
    - index.tsx / main.tsx
  - public/
  - package.json
  - tsconfig.json (recommended)
  - vite.config.ts
  - README.md

4. Tooling & Config (mandatory)

- Build tool: Vite (vite.config.ts) with pinned plugin versions.
- Linter: ESLint (strict config), with `eslint:recommended` plus React/JSX rules and project policies. Keep `eslint` config in root (`.eslintrc.cjs` or equivalent).
- Formatter: Prettier; enforce via pre-commit and CI.
- Pre-commit hooks: `lint-staged` + `husky` (or GitHub Actions pre-checks) to run `eslint --fix` and `prettier --write` on staged files.
- Commit lint: `commitlint` with Conventional Commits configuration.
- Testing: Vitest (if using Vite) or Jest (if project needs it). Use React Testing Library for component tests.
- Type checking: TypeScript (`tsc --noEmit`) or `tsc -w` during dev. If project is JS, enforce JSDoc or gradual migration plan.
- Environment config: `.env`, `.env.local` patterns supported by Vite. Secrets must never be stored in source. Document required env vars in `.env.example`.
- Editor settings: Add `.editorconfig` and recommended VS Code settings in `.vscode/settings.json` to align formatters and line endings.

5. Code Style and Linting

- Enforce rules automatically: `npm run lint` must fail on serious errors (`error` severity). Use `eslint` rules to forbid `console.log` in production code (allowable during development but removed before PR).
- Use Prettier as the single source of formatting; set Prettier's `printWidth` and other team preferences in `.prettierrc`.
- Add ESLint rules for accessibility (`eslint-plugin-jsx-a11y`) and security (`eslint-plugin-security` / `eslint-plugin-no-unsanitized`).

6. Type Safety

- Strongly recommend TypeScript for all new projects. Minimal expectation: types for public interfaces, API clients, and shared utilities.
- Use `strict: true` in `tsconfig.json` where possible; if not immediately feasible, document the plan and exceptions.
- Include `tsconfig.paths` mapping if monorepo or aliasing is necessary and document them.

7. Testing Strategy

- Unit tests: cover components and pure functions. Use React Testing Library and Vitest/Jest.
- Integration tests: API interaction and component+hook flows.
- End-to-end (E2E): Playwright (recommended) or Cypress for critical user journeys.
- Coverage: configure a reasonable baseline (example: 80% lines and functions; adjust per project). Failing CI for coverage regressions is optional but recommended for key modules.
- Test naming and folder conventions: co-locate tests with code (`Component.test.tsx`) or follow `tests/` folder policy. Co-location preferred for components/features.

8. Accessibility (A11y)

- Adopt WCAG 2.1 AA as baseline.
- Tools: axe-core/`jest-axe` for automated checks in tests; `eslint-plugin-jsx-a11y` for linting; Lighthouse audits.
- Patterns: semantic HTML, accessible form labels, keyboard navigation, focus management, ARIA only where necessary.
- Color contrast: ensure contrast ratios meet AA; include checks in design tokens / CSS.

9. Performance

- Set and enforce performance budgets (bundle size, LCP, FCP). Use pipeline checks (Lighthouse CI) to prevent regressions.
- Code-splitting / route-based lazy loading for large pages.
- Optimize images: use `srcset`, modern formats (AVIF/WebP) in CI pipeline or image CDN.
- Use CDN for static assets and enable gzip/Brotli compression.
- Avoid heavy third-party scripts on initial load; load non-critical third-party scripts asynchronously.
- Use caching and cache-control headers strategically (hash filenames for long-term caching).

10. Security

- Follow OWASP Top 10 guidance: protect from XSS, CSRF, injection, sensitive data exposure.
- Avoid dangerouslySetInnerHTML unless strictly necessary and then sanitize inputs.
- Secrets: store in environment/secret manager (do not commit to repo). Use GitHub Secrets for Actions.
- Use SCA (Software Composition Analysis) tooling: Dependabot + code-scanning; fail builds for high severity vulnerabilities until addressed.
- CSP: recommend a strict Content Security Policy for production.

11. Dependency Management & Supply Chain

- Lockfile must be committed (package-lock.json / pnpm-lock.yaml). Use `npm ci` in CI.
- Enable Dependabot or equivalent to keep dependencies updated; configure security updates auto-merge policy for low-risk updates if tests pass.
- Use semver ranges thoughtfully. Prefer pinned minor/patch ranges for apps to avoid surprising upgrades.

12. CI / CD Requirements

- CI must run on PRs and include steps:
  1. checkout, install (`npm ci`), restore cache
  2. install dependencies
  3. run `npm run lint` (fail on errors)
  4. run `npm run typecheck` (if TS; fail on errors)
  5. run `npm test -- --ci` and enforce coverage
  6. run `npm run build` (production build)
  7. run Lighthouse CI or size/bundle checks (optional)
- Artifact caching: cache package manager artifacts between runs to speed builds.
- Secrets: use GitHub Actions secrets / environment-protected variables and restrict access.
- Deploy only from a protected branch (main/master) and only after passing all checks.

13. Observability & Monitoring

- Add error tracking (Sentry or similar) for production builds; ensure source maps are uploaded during deploy.
- Set up Real User Monitoring (RUM) or synthetic checks to track Core Web Vitals and error rates.
- Logs: client-side logs should be rate-limited and scrubbed of PII.

14. Release Process & Versioning

- Use Semantic Versioning for public packages. Use Conventional Commits to automate changelogs and version bumps.
- For apps, tag releases and keep a changelog (auto-generated is acceptable via `standard-version`/`changesets`).

15. Developer Experience (DX)

- Provide `npm run dev`, `npm run build`, `npm run test`, `npm run lint`, `npm run format`, `npm run typecheck` scripts in `package.json`.
- Provide a minimal `README.md` with local setup, env variables, and run commands.
- Add VS Code recommended extensions (`.vscode/extensions.json`).
- Provide a `CONTRIBUTING.md` describing commit conventions and PR workflow.

16. PR Gating / Merge Requirements

- PR must target a single, clearly described change; large features must be split.
- Required checks to pass before merge:
  - Linting (`eslint`) and formatting (`prettier`) checks
  - Type-checking pass
  - Unit tests and coverage thresholds
  - Build (`npm run build`) successful
  - Security checks (SCA) — high severity must block
  - Accessibility smoke tests if UI changes affect pages
- PR must include a short description, change rationale, and testing evidence (screenshots or test results).
- If the agent opens a PR, it must include the build and test logs and list the exact commands it ran.

17. Templates, Examples & Useful Links

- Use the following as references when implementing or reviewing rules:
  - React / Vite docs (project init & structure)
  - MDN Web Docs (performance, accessibility)
  - web.dev (performance & PWA guidance)
  - OWASP Top Ten (security)
  - ESLint, Prettier docs (linting/formatting)
  - Jest / Vitest + React Testing Library docs (testing)
  - TypeScript docs (type safety)
  - Conventional Commits, SemVer (release & commit conventions)
  - GitHub Actions & Dependabot docs (CI templates)

Implementation checklist for the AI agent (must follow when starting work on an Issue)

- Read `agent/REACT_APP_PROFESSIONAL_GUIDELINES.md` before any change.
- Determine `TARGET_DIR` by reading Issue body or env var. If absent, refuse to operate and ask for `path: <dir>`.
- Create/update only within `TARGET_DIR`.
- Run the following commands as a reproducible sequence (and capture logs):
  1. `npm ci` (or `pnpm install --frozen-lockfile`)
  2. `npm run lint` (fail on errors)
  3. `npm run typecheck` (if TS)
  4. `npm test -- --ci` (fail on test errors or coverage regressions)
  5. `npm run build`
- If `npm ci` or `npm install` fails with a 404 for a package (package not in registry), stop automated fix attempts and report to the Issue with the exact stderr, recommending a package or registry fix.
- If build/test/lint pass, agent may open a PR. PR must include the command logs and a short summary referencing this guidelines file.
- If failures occur (except 404/package-missing), agent may attempt up to `MAX_FIX_ATTEMPTS` (configurable via env) automated fix cycles using only the single `TARGET_DIR` and minimal invasive changes. Each attempt must be commited to a branch named `autofix/<issue>-attempt-<n>` and the attempt summary included in the PR/Issue comment.

Minimal `package.json` script recommendations

```
"scripts": {
  "dev": "vite",
  "build": "vite build",
  "preview": "vite preview",
  "lint": "eslint 'src/**/*.{js,jsx,ts,tsx}'",
  "format": "prettier --write \"src/**/*.{js,jsx,ts,tsx,json,css,md}\"",
  "test": "vitest",
  "typecheck": "tsc --noEmit"
}
```

Enforcement & Automation suggestions

- Add GitHub Actions workflow that runs on `pull_request` and `push` to `main`.
- Configure `dependabot.yml` for automatic dependency updates.
- Configure `lighthouse-ci` as a step for performance gating (optional but recommended).
- Configure pre-commit hooks with `husky` + `lint-staged` (format and lint staged files) and `commitlint`.

References (selected authoritative sources consulted)

- React & React.dev / Vite docs (project init & structure)
- MDN Web Docs (performance, accessibility)
- web.dev (performance & PWA guidance)
- OWASP Top Ten (security)
- ESLint & Prettier docs (formatting/linting)
- Testing Library, Jest, Vitest docs (testing)
- TypeScript docs (type safety)
- Conventional Commits, SemVer
- GitHub Actions & Dependabot docs

---

If you want, I can:

- Generate a GitHub Actions workflow template (CI) that enforces these checks.
- Create `package.json` `scripts`, `.eslintrc`, `.prettierrc`, `tsconfig.json`, `husky` hooks and a `README.md` inside the `TARGET_DIR` as a starter scaffold (dry-run optional).
- Add a `CONTRIBUTING.md` and `PR_TEMPLATE.md` enforcing the PR gating steps above.

Would you like me to scaffold the CI config and starter toolchain in the target folder now (I will only act inside the folder you specify)?
