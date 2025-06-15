# 🚀 Deployment Guide: Job Seeker Dashboard v2

This guide will help you set up the new repository and Hugging Face Space with automatic CI/CD deployment.

## 📋 Prerequisites

- GitHub account
- Hugging Face account
- Git installed locally
- Python 3.8+ installed

## 🔧 Step 1: Create GitHub Repository

1. **Go to GitHub**: https://github.com/new
2. **Repository name**: `job-seeker-dashboard-v2`
3. **Description**: `H-1B Cap-Exempt Job Seeker Dashboard - Find year-round visa sponsors`
4. **Visibility**: Public (recommended for open source)
5. **Initialize**: Don't initialize (we already have files)
6. **Click**: "Create repository"

## 🔗 Step 2: Push Local Repository to GitHub

```bash
# Add GitHub remote (replace YOUR_USERNAME with your GitHub username)
git remote add origin https://github.com/YOUR_USERNAME/job-seeker-dashboard-v2.git

# Push to GitHub
git branch -M main
git push -u origin main
```

## 🤗 Step 3: Create Hugging Face Space

1. **Go to Hugging Face**: https://huggingface.co/new-space
2. **Space name**: `job-seeker-dashboard-v2`
3. **License**: MIT
4. **SDK**: Gradio
5. **Hardware**: CPU Basic (free tier)
6. **Visibility**: Public
7. **Click**: "Create Space"

## 🔑 Step 4: Set Up GitHub Secrets

1. **Get HF Token**:

   - Go to: https://huggingface.co/settings/tokens
   - Click "New token"
   - Name: `GitHub Actions Deploy`
   - Type: Write
   - Copy the token

2. **Add to GitHub Secrets**:
   - Go to your GitHub repo: `https://github.com/YOUR_USERNAME/job-seeker-dashboard-v2`
   - Click: Settings → Secrets and variables → Actions
   - Click: "New repository secret"
   - Name: `HF_TOKEN`
   - Value: Paste your HF token
   - Click: "Add secret"

## 🔄 Step 5: Enable GitHub Actions

1. **Go to Actions tab** in your GitHub repository
2. **Enable workflows** if prompted
3. **Check workflow file**: `.github/workflows/deploy-to-hf.yml` should be visible

## 🎯 Step 6: Test Deployment

1. **Make a small change** to trigger deployment:

   ```bash
   echo "# Test deployment" >> README.md
   git add README.md
   git commit -m "Test: Trigger first deployment"
   git push
   ```

2. **Check GitHub Actions**:

   - Go to Actions tab in your repo
   - Watch the deployment workflow run
   - Should see "Deploy to Hugging Face Spaces" workflow

3. **Verify HF Space**:
   - Go to: `https://huggingface.co/spaces/YOUR_USERNAME/job-seeker-dashboard-v2`
   - Space should rebuild automatically
   - Dashboard should be live in a few minutes

## ✅ Step 7: Verify Everything Works

### GitHub Repository Checklist:

- [ ] Repository created and code pushed
- [ ] GitHub Actions workflow visible
- [ ] HF_TOKEN secret added
- [ ] Workflow runs successfully

### Hugging Face Space Checklist:

- [ ] Space created and linked
- [ ] Files uploaded automatically
- [ ] Dashboard loads without errors
- [ ] All features working (search, filters, charts)

## 🔧 Troubleshooting

### Common Issues:

1. **GitHub Actions fails**:

   - Check HF_TOKEN is correctly set in secrets
   - Verify token has "Write" permissions
   - Check workflow logs for specific errors

2. **HF Space doesn't update**:

   - Check if files were uploaded (go to Files tab in HF Space)
   - Look for build logs in HF Space
   - Verify requirements.txt has correct dependencies

3. **Dashboard doesn't load**:
   - Check HF Space logs for Python errors
   - Verify data files are present and not corrupted
   - Test locally first: `python app.py`

### Manual Deployment (Backup):

If GitHub Actions fails, you can deploy manually:

```bash
# Install HF CLI
pip install huggingface_hub

# Login to HF
huggingface-cli login

# Upload files
huggingface-cli upload YOUR_USERNAME/job-seeker-dashboard-v2 . --repo-type=space
```

## 🎉 Success!

Once everything is set up:

1. **Any commit to `main` branch** → Automatic deployment to HF Space
2. **Clean git history** → No more rebase/merge conflicts
3. **Professional setup** → Ready for collaboration and contributions
4. **Live dashboard** → Available at your HF Space URL

## 📞 Need Help?

- **GitHub Issues**: Create an issue in your repository
- **HF Community**: https://huggingface.co/spaces/YOUR_USERNAME/job-seeker-dashboard-v2/discussions
- **Documentation**: This README.md has all the technical details

---

**🚀 Ready to deploy? Follow the steps above and you'll have a professional, automatically-deploying dashboard in minutes!**
