# Changelog Maintenance

## Procedure

### 1. Manual Maintenance
Follow the [Keep a Changelog](https://keepachangelog.com/) standard in a `CHANGELOG.md` file.

```markdown
# Changelog
All notable changes to this project will be documented in this file.

## [1.2.0] - 2024-02-09
### Added
- Multi-tenancy support via subdomains.
- Dark mode toggle in user settings.

### Fixed
- Memory leak in Redis session store.
- CSS layout bug on mobile Safari.
```

### 2. Automated Generation (Standard Version)
Automate changelog creation based on Conventional Commits.

```bash
# Install
npm install --save-dev standard-version

# Run to update version and changelog
npm run release
```

### 3. CI/CD Integration (Semantic Release)
Completely automate the release process in GitHub Actions.

```yaml
# .github/workflows/release.yml
jobs:
  release:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
      - run: npx semantic-release
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
          NPM_TOKEN: ${{ secrets.NPM_TOKEN }}
```

## Constraints
- **Clarity**: Write for humans, not for git logs. Avoid commit hashes and technical jargon in the main headings.
- **Consistency**: Use the standard categories (`Added`, `Changed`, `Deprecated`, `Removed`, `Fixed`, `Security`).
- **Timing**: Never release a version without updating the changelog.

## Expected Output
A clear, readable history of changes that helps users understand what's new and what might break.
