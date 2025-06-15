#!/usr/bin/env python3
from huggingface_hub import HfApi, create_repo
import sys

try:
    api = HfApi()
    user_info = api.whoami()
    username = user_info['name']
    print(f'✅ Logged in as: {username}')
    
    space_id = f'{username}/job-seeker-dashboard-v2'
    print(f'🚀 Creating HF Space: {space_id}')
    
    try:
        create_repo(
            repo_id=space_id,
            repo_type='space',
            space_sdk='gradio',
            private=False
        )
        print(f'✅ Hugging Face Space created: {space_id}')
    except Exception as e:
        if 'already exists' in str(e):
            print(f'✅ Space already exists: {space_id}')
        else:
            print(f'❌ Error: {e}')
            sys.exit(1)
    
    # Deploy files to space
    print('📤 Deploying files to HF Space...')
    api.upload_folder(
        folder_path='.',
        repo_id=space_id,
        repo_type='space',
        commit_message='Initial deployment with city fixes and auto-filtering',
        ignore_patterns=['.git*', '__pycache__', '*.pyc', '.DS_Store', 'auto_setup.py', 'create_hf_space.py']
    )
    
    print('✅ Files deployed successfully!')
    print(f'🌐 Live at: https://huggingface.co/spaces/{space_id}')
    print(f'📁 GitHub repo: https://github.com/andrewulloa/job-seeker-dashboard-v2')
    
except Exception as e:
    print(f'❌ Setup failed: {e}')
    sys.exit(1) 