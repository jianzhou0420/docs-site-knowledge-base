# Git Conventions

## Commit Messages

- Format: `type(scope): description` ([Conventional Commits](https://www.conventionalcommits.org/))
- Types: `feat`, `fix`, `refactor`, `docs`, `chore`, `test`, `ci`, `perf`
- Scopes: project-specific — pick a short noun per subsystem (e.g. `kb`, `docs`, `scripts`, `infra`). Keep the list small and stable.
- Lowercase, imperative mood, max 72 chars on the subject line.

## Examples

```
feat(kb): add synthesis skill for cross-topic summaries
fix(docs): correct broken anchor link drift after section rename
refactor(scripts): split search CLI into tokenizer + indexer
docs: reframe README around purpose
chore: upgrade mkdocs-material to 9.6
```

## Rules

- **Never** skip hooks (`--no-verify`) unless the user asks.
- **Never** amend pushed commits — make a new commit.
- **Never** force-push to `main`/`master` without explicit approval.
- Stage files by name; avoid `git add -A` / `git add .` which can pull in secrets or generated output.
- Include a body paragraph when the "why" isn't obvious from the subject.
