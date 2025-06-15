#!/usr/bin/env python3
"""
Automated setup script for GitHub repository and Hugging Face Space
"""
import os
import subprocess
import requests
import json
from huggingface_hub import HfApi, create_repo

def setup_github_repo():
    """Create GitHub repository using GitHub CLI or API"""
    print('🔧 Setting up GitHub repository...')
    
    # Try GitHub CLI first
    try:
        result = subprocess.run(['gh', '--version'], capture_output=True, text=True)
        if result.returncode == 0:
            print('📱 Using GitHub CLI...')
            
            # Create repo with GitHub CLI
            cmd = [
                'gh', 'repo', 'create', 'job-seeker-dashboard-v2',
                '--public',
                '--description', 'H-1B Cap-Exempt Job Seeker Dashboard - Find year-round visa sponsors',
                '--clone=false'
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True)
            if result.returncode == 0:
                print('✅ GitHub repository created successfully!')
                
                # Get the repo URL
                username = subprocess.run(['gh', 'api', 'user', '--jq', '.login'], 
                                        capture_output=True, text=True).stdout.strip()
                repo_url = f"https://github.com/{username}/job-seeker-dashboard-v2.git"
                
                return repo_url, username
            else:
                print(f'❌ GitHub CLI failed: {result.stderr}')
                return None, None
                
    except FileNotFoundError:
        print('📱 GitHub CLI not found, trying manual setup...')
        print('🔗 Please create the repository manually at: https://github.com/new')
        print('   Repository name: job-seeker-dashboard-v2')
        print('   Description: H-1B Cap-Exempt Job Seeker Dashboard - Find year-round visa sponsors')
        print('   Public repository, no initialization')
        
        username = input('Enter your GitHub username: ').strip()
        if username:
            repo_url = f"https://github.com/{username}/job-seeker-dashboard-v2.git"
            return repo_url, username
        
    return None, None

def setup_huggingface_space(username):
    """Create Hugging Face Space"""
    print('🤗 Setting up Hugging Face Space...')
    
    try:
        # Check if user is logged in to HF
        api = HfApi()
        
        # Try to get user info
        try:
            user_info = api.whoami()
            hf_username = user_info['name']
            print(f'✅ Logged in to Hugging Face as: {hf_username}')
        except:
            print('❌ Not logged in to Hugging Face')
            print('🔑 Please run: huggingface-cli login')
            return None
        
        # Create the space
        space_id = f"{hf_username}/job-seeker-dashboard-v2"
        
        try:
            create_repo(
                repo_id=space_id,
                repo_type="space",
                space_sdk="gradio",
                private=False
            )
            print(f'✅ Hugging Face Space created: {space_id}')
            return space_id
            
        except Exception as e:
            if "already exists" in str(e):
                print(f'✅ Hugging Face Space already exists: {space_id}')
                return space_id
            else:
                print(f'❌ Failed to create HF Space: {e}')
                return None
                
    except Exception as e:
        print(f'❌ Hugging Face setup failed: {e}')
        print('🔗 Please create manually at: https://huggingface.co/new-space')
        print('   Space name: job-seeker-dashboard-v2')
        print('   SDK: Gradio')
        print('   Hardware: CPU basic')
        return None

def setup_git_remote(repo_url):
    """Set up git remote and push"""
    print('🔗 Setting up git remote...')
    
    try:
        # Add remote
        subprocess.run(['git', 'remote', 'add', 'origin', repo_url], check=True)
        print('✅ Git remote added')
        
        # Push to GitHub
        result = subprocess.run(['git', 'push', '-u', 'origin', 'main'], 
                              capture_output=True, text=True)
        
        if result.returncode == 0:
            print('✅ Code pushed to GitHub successfully!')
            return True
        else:
            print(f'❌ Push failed: {result.stderr}')
            print('🔧 You may need to authenticate with GitHub')
            return False
            
    except subprocess.CalledProcessError as e:
        print(f'❌ Git setup failed: {e}')
        return False

def deploy_to_hf_space(space_id):
    """Deploy files to Hugging Face Space"""
    print('🚀 Deploying to Hugging Face Space...')
    
    try:
        api = HfApi()
        
        # Upload all files
        api.upload_folder(
            folder_path=".",
            repo_id=space_id,
            repo_type="space",
            commit_message="Initial deployment from automated setup",
            ignore_patterns=['.git*', '__pycache__', '*.pyc', '.DS_Store', 'auto_setup.py']
        )
        
        print('✅ Files deployed to Hugging Face Space!')
        print(f'🌐 Live at: https://huggingface.co/spaces/{space_id}')
        return True
        
    except Exception as e:
        print(f'❌ HF deployment failed: {e}')
        return False

def main():
    print('🚀 AUTOMATED SETUP STARTING...')
    print('=' * 50)
    
    # Step 1: GitHub repository
    repo_url, username = setup_github_repo()
    if not repo_url:
        print('❌ GitHub setup failed')
        return
    
    # Step 2: Hugging Face Space
    space_id = setup_huggingface_space(username)
    
    # Step 3: Git remote and push
    if repo_url:
        git_success = setup_git_remote(repo_url)
        if not git_success:
            print('⚠️  Git push failed, but you can push manually later')
    
    # Step 4: Deploy to HF Space
    if space_id:
        deploy_success = deploy_to_hf_space(space_id)
    
    print('\n' + '=' * 50)
    print('🎉 SETUP SUMMARY:')
    print(f'📁 GitHub Repo: {repo_url if repo_url else "❌ Failed"}')
    print(f'🤗 HF Space: https://huggingface.co/spaces/{space_id}' if space_id else '❌ Failed')
    
    if repo_url and space_id:
        print('\n✅ SUCCESS! Next steps:')
        print('1. Add HF_TOKEN to GitHub Secrets:')
        print(f'   - Go to: {repo_url.replace(".git", "")}/settings/secrets/actions')
        print('   - Add secret: HF_TOKEN = your_huggingface_token')
        print('2. Make a test commit to trigger auto-deployment')
        print('3. Check GitHub Actions tab for deployment status')
    else:
        print('\n⚠️  Some steps failed. Check SETUP_INSTRUCTIONS.md for manual steps.')

if __name__ == '__main__':
    main() 