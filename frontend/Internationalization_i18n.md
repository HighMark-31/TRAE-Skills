# Skill: Internationalization (i18n)

## Purpose
To adapt the application for users from different languages and regions without code changes.

## When to Use
- When the app has a global audience.
- When supporting multiple languages (English, Spanish, etc.).

## Procedure
1.  **Install Library**: Use `react-i18next` or `react-intl`.
2.  **Setup Configuration**: Initialize i18n instance.
    - Configure detected language (browser, cookie).
    - Define fallback language (e.g., 'en').
3.  **Extract Strings**: Move all hardcoded text to JSON files (locales).
    - `en.json`: `{ "welcome": "Welcome" }`
    - `es.json`: `{ "welcome": "Bienvenido" }`
4.  **Replace in Components**:
    - Use hook: `const { t } = useTranslation()`.
    - Replace text: `<h1>{t('welcome')}</h1>`.
5.  **Language Switcher**: Create a component to change the active language state.

## Constraints
- Do not concatenate strings for sentences (word order varies by language); use interpolation.
- Handle pluralization and date/number formatting using the library's built-in tools.

## Expected Output
A system where text is loaded dynamically based on the user's locale preference.
