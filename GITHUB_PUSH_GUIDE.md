# GitHub Push Guide for askIT-informatica

## Step-by-Step Instructions

### 1. Open Terminal
Open your Terminal application and navigate to the project directory:

```bash
cd /Users/ramgobburu/Documents/my-function-app
```

### 2. Initialize Git Repository

```bash
git init
```

Expected output: `Initialized empty Git repository in /Users/ramgobburu/Documents/my-function-app/.git/`

### 3. Configure Git User

```bash
git config user.name "Ram Gobburu"
git config user.email "ramgobburu@users.noreply.github.com"
```

### 4. Add Files to Git

```bash
git add .gitignore
git add function_app.py
git add host.json
git add requirements.txt
git add README.md
git add COMPLETE_SETUP_GUIDE.md
git add INFORMATICA_AGENT_TECH_BLOG.md
git add INFORMATICA_AGENT_TECH_BLOG.html
git add TECH_BLOG_README.md
git add create_html.py
```

### 5. Check What Will Be Committed

```bash
git status
```

You should see a list of files in green that are ready to be committed.

### 6. Commit the Files

```bash
git commit -m "Initial commit: Informatica Agent - Complete Azure Functions implementation with AI Search integration"
```

Expected output: Shows the files that were committed.

### 7. Rename Branch to Main

```bash
git branch -M main
```

### 8. Add GitHub Remote

```bash
git remote add origin https://github.com/ramcgobburu/askIT-informatica.git
```

### 9. Verify Remote Configuration

```bash
git remote -v
```

Expected output:
```
origin  https://github.com/ramcgobburu/askIT-informatica.git (fetch)
origin  https://github.com/ramcgobburu/askIT-informatica.git (push)
```

### 10. Push to GitHub

```bash
git push -u origin main
```

**You will be prompted for credentials:**
- **Username**: `ramgobburu`
- **Password**: Use your GitHub Personal Access Token (not your GitHub password)

If you need to create a new token:
1. Go to https://github.com/settings/tokens
2. Click "Generate new token" → "Generate new token (classic)"
3. Give it a name: "askIT-informatica"
4. Select scope: ✅ `repo` (Full control of private repositories)
5. Click "Generate token"
6. Copy the token and use it as your password

### 11. Verify on GitHub

Visit https://github.com/ramcgobburu/askIT-informatica

You should now see all your files!

---

## Alternative: Using GitHub CLI

If you have GitHub CLI installed:

```bash
cd /Users/ramgobburu/Documents/my-function-app
gh auth login
git init
git add .
git commit -m "Initial commit: Informatica Agent implementation"
git branch -M main
gh repo create askIT-informatica --public --source=. --remote=origin --push
```

---

## Troubleshooting

### If "git push" fails with authentication error:

```bash
# Remove existing remote
git remote remove origin

# Add remote with token in URL (replace YOUR_TOKEN)
git remote add origin https://YOUR_TOKEN@github.com/ramcgobburu/askIT-informatica.git

# Push
git push -u origin main
```

### If you get "repository not found":

Make sure the repository exists at: https://github.com/ramcgobburu/askIT-informatica

### If files are already committed elsewhere:

```bash
# Check current remotes
git remote -v

# If wrong remote, update it
git remote set-url origin https://github.com/ramcgobburu/askIT-informatica.git

# Push
git push -u origin main
```

---

## What Files Will Be Pushed?

✅ **Core Application:**
- `function_app.py` (460 lines) - All Azure Functions
- `host.json` - Configuration
- `requirements.txt` - Dependencies

✅ **Documentation:**
- `README.md` - Project overview
- `COMPLETE_SETUP_GUIDE.md` (907 lines) - Complete setup guide
- `INFORMATICA_AGENT_TECH_BLOG.md` (1,075 lines) - Technical blog
- `TECH_BLOG_README.md` - Blog documentation

✅ **Resources:**
- `INFORMATICA_AGENT_TECH_BLOG.html` - Print-ready version
- `create_html.py` - HTML generator
- `.gitignore` - Ignore rules

🚫 **Files NOT Pushed (excluded by .gitignore):**
- `local.settings.json` (contains secrets)
- `__pycache__/` (Python cache)
- `__azurite_db*` (local storage)
- Test and utility scripts

---

## Quick Command Reference

```bash
# All commands in sequence
cd /Users/ramgobburu/Documents/my-function-app
git init
git config user.name "Ram Gobburu"
git config user.email "ramgobburu@users.noreply.github.com"
git add .gitignore function_app.py host.json requirements.txt README.md COMPLETE_SETUP_GUIDE.md INFORMATICA_AGENT_TECH_BLOG.md INFORMATICA_AGENT_TECH_BLOG.html TECH_BLOG_README.md create_html.py
git commit -m "Initial commit: Informatica Agent - Complete implementation"
git branch -M main
git remote add origin https://github.com/ramcgobburu/askIT-informatica.git
git push -u origin main
```

---

## Need Help?

If you encounter any errors:
1. Copy the complete error message
2. Share it with me
3. I'll help you troubleshoot

Once successful, you'll see your files at:
**https://github.com/ramcgobburu/askIT-informatica**

