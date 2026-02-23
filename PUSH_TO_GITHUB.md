# Push This Project to GitHub

Follow these steps to push all files to a new GitHub repository.

---

## 1. Install Git (if not installed)

- Download: https://git-scm.com/download/win  
- Run the installer (default options are fine).  
- **Restart your terminal** (or Cursor) after installing.

---

## 2. Create a new repository on GitHub

1. Go to **https://github.com/new**
2. Set **Repository name** (e.g. `learning-platform-analytics`).
3. Choose **Public** (or Private).
4. **Do not** check "Add a README" or "Add .gitignore" — leave the repo **empty**.
5. Click **Create repository**.

---

## 3. Details needed for the push

You’ll need **one** of these (from the new repo page on GitHub):

| What | Example |
|------|--------|
| **HTTPS URL** | `https://github.com/YOUR_USERNAME/learning-platform-analytics.git` |
| **SSH URL**    | `git@github.com:YOUR_USERNAME/learning-platform-analytics.git` |

Replace `YOUR_USERNAME` and `learning-platform-analytics` with your GitHub username and repo name.

**Authentication (HTTPS):**  
When you run `git push`, Git will ask for your GitHub username and **password**.  
Use a **Personal Access Token (PAT)** as the password, not your GitHub account password.

- Create a PAT: GitHub → **Settings** → **Developer settings** → **Personal access tokens** → **Tokens (classic)** → **Generate new token**.  
- Give it at least the **repo** scope and use it when Git asks for a password.

---

## 4. Run these commands (in PowerShell or Command Prompt)

Open a terminal in the project folder (`D:\Project`) and run:

```powershell
cd D:\Project

git init
git add .
git commit -m "Initial commit: Online Learning Platform Analytics"

git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git

git push -u origin main
```

**Replace** `https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git` with your actual repository URL from step 2.

If you use **SSH** instead of HTTPS, use:

```powershell
git remote add origin git@github.com:YOUR_USERNAME/YOUR_REPO_NAME.git
```

---

## 5. Summary of what you need to provide

| # | Detail | Example |
|---|--------|--------|
| 1 | **GitHub repository URL** (after creating an empty repo) | `https://github.com/john/learning-platform-analytics.git` |
| 2 | **Git installed** and terminal restarted | — |
| 3 | **PAT** (if using HTTPS) for password when `git push` asks | — |

Once you have **Git installed** and your **repo URL**, run the commands in section 4 (with your URL). If anything fails, share the exact error message.
