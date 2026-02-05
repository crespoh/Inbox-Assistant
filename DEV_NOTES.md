# Dev Notes

Quick checklist to pause now and resume smoothly later.

## Before you stop today
1. Check status
   ```bash
   git status -sb
   ```
2. Commit and push your work
   ```bash
   git add .
   git commit -m "WIP: <short note>"
   git push -u origin cursor/ai-inbox-assistant-mvp-4bc3
   ```
3. Write a quick status note
   - Last completed step
   - Next step to implement
   - Any blockers or questions

## Resume next day
1. Pull latest branch
   ```bash
   git fetch origin cursor/ai-inbox-assistant-mvp-4bc3
   git pull origin cursor/ai-inbox-assistant-mvp-4bc3
   ```
2. Re-activate your venv
   ```bash
   python -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   ```
3. Set environment variables
   Create `.env` at repo root:
   ```bash
   GOOGLE_CLIENT_ID=...
   GOOGLE_CLIENT_SECRET=...
   GOOGLE_REDIRECT_URI=http://localhost:8000/auth/callback
   SECRET_KEY=change-me
   DATABASE_URL=sqlite:///./inbox.db
   ```
4. Run the app
   ```bash
   uvicorn app.main:app --reload
   ```

## Progress snapshot
- Completed: project structure + FastAPI skeleton
- Completed: DB models
- Completed: Google OAuth login flow
- Next: Gmail email fetcher (last N days)
