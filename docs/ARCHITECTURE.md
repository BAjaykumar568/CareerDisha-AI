# Architecture and Implementation Notes

## Goal

CareerDisha AI helps fresh graduates plan entry-level technology learning and understand potential gaps between self-reported skills and a pasted job description.

## Technical overview

```text
Browser (index.html)
  ├── Profile & preferences  → browser localStorage
  ├── Role catalog            → predefined roles and stages
  ├── Job description         → JavaScript skill vocabulary matching
  ├── Resource catalog        → static entries and topic filtering
  └── Disha Coach             → offline fallback
            └── OPTIONAL: POST /api/coach → local Node server → Gemini API
```

The frontend is a single self-contained HTML file with embedded CSS and JavaScript to make it easy to open directly, upload to GitHub, and deploy on GitHub Pages.

## Decisions

- **Offline first:** Works without installation or API credentials.
- **Rule-based skill matching:** Easy to explain, inspect and test; not equivalent to assessing proficiency.
- **Curated resource catalog:** Avoids inventing course data; resource links should still be reviewed periodically.
- **Local persistence:** Helpful for demos, but not multi-device accounts or reliable backups.
- **Optional LLM:** Only Disha Coach can call Gemini when the private local server is configured; no claim that all app features use AI.

## Data flow

1. User selects goal, enters self-reported skills, budget, and weekly hours.
2. Role-specific template produces learning stages and task estimates.
3. User confirms tasks; status is stored locally.
4. User pastes a job description; recognizable requirements are extracted with browser rules.
5. App compares these requirements with self-reported skills and offers to append missing evidence areas to the roadmap.
6. Optional Disha Coach provides contextual text responses via a server-side Gemini API call.

## Constraints

This is an educational frontend prototype, not a job-finding service or an employment-readiness certification. No user research or quantified job outcomes have been claimed. Public deployments should use a secure server and meaningful privacy/security review before collecting actual student data.

## Security

Never commit API keys. The optional server reads `GEMINI_API_KEY` from the process environment and is intended for local demonstrations. A production backend needs rate limiting, authentication, abuse protection, logging policies, and secure access controls.