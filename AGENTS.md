### General Rules

- Do not run superpower-related skills unless the user explicitly requests them.
- If the `superpower:writing-plan` skill is disabled, implement directly from the specification. Do not generate test code while implementing a feature unless the user explicitly requests it.
- You may update `TODO.md` and include it in commits.

### Backend Rules

The backend is implemented with Django.

- Backend dependencies are managed with `uv`. Python is located at `backend/.venv/Script/python.exe`.
- If a feature or optimization changes the database, confirm that the Django ORM migrations have been completed.

### Frontend Rules

The frontend is implemented with Vite and Ant Design.

- Prefer Ant Design component features and functionality. Use custom implementations only when the default components cannot achieve the required result or customization is necessary.
- Prefer Ant Design's default CSS unless the user explicitly requests otherwise.
- Frontend changes do not require `npm build` verification.

### Project Documentation

`asf-doc` is the project's VitePress documentation site. It uses a separate GitHub repository and Cloudflare Pages.
Update the Chinese documentation first, then update the corresponding English documentation after the Chinese version is finalized.
For placeholder images, do not add descriptions; the user will infer them from context. Use filenames such as `img.png` and `img_1.png` to make copying convenient.
Do not build the VitePress documentation after changes unless the user explicitly requests it.

### marketplace

`asp-marketplace` has a separate GitHub repository containing the Claude Code plugin source.

# AGENTS.md

Behavioral guidelines to reduce common LLM coding mistakes. Merge with project-specific instructions as needed.

**Tradeoff:** These guidelines bias toward caution over speed. For trivial tasks, use judgment.

## 1. Think Before Coding

**Don't assume. Don't hide confusion. Surface tradeoffs.**

Before implementing:

- State your assumptions explicitly. If uncertain, ask.
- If multiple interpretations exist, present them - don't pick silently.
- If a simpler approach exists, say so. Push back when warranted.
- If something is unclear, stop. Name what's confusing. Ask.

## 2. Simplicity First

**Minimum code that solves the problem. Nothing speculative.**

- No features beyond what was asked.
- No abstractions for single-use code.
- No "flexibility" or "configurability" that wasn't requested.
- No error handling for impossible scenarios.
- If you write 200 lines and it could be 50, rewrite it.

Ask yourself: "Would a senior engineer say this is overcomplicated?" If yes, simplify.

## 3. Surgical Changes

**Touch only what you must. Clean up only your own mess.**

When editing existing code:

- Don't "improve" adjacent code, comments, or formatting.
- Don't refactor things that aren't broken.
- Match existing style, even if you'd do it differently.
- If you notice unrelated dead code, mention it - don't delete it.

When your changes create orphans:

- Remove imports/variables/functions that YOUR changes made unused.
- Don't remove pre-existing dead code unless asked.

The test: Every changed line should trace directly to the user's request.

## 4. Goal-Driven Execution

**Define success criteria. Loop until verified.**

Transform tasks into verifiable goals:

- "Add validation" → "Write tests for invalid inputs, then make them pass"
- "Fix the bug" → "Write a test that reproduces it, then make it pass"
- "Refactor X" → "Ensure tests pass before and after"

For multi-step tasks, state a brief plan:

```
1. [Step] → verify: [check]
2. [Step] → verify: [check]
3. [Step] → verify: [check]
```

Strong success criteria let you loop independently. Weak criteria ("make it work") require constant clarification.

---

**These guidelines are working if:** fewer unnecessary changes in diffs, fewer rewrites due to overcomplication, and clarifying questions come before implementation rather than
after mistakes.
