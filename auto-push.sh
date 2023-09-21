#!/bin/bash

# Define the directory where your Git repository is located
repo_dir="/Users/seungkikim/Desktop/seungki1011.github.io"

# Navigate to the repository directory
cd "$repo_dir" || exit 1

# Add all changes to the staging area (git add .)
git add .

# Commit changes with a commit message
commit_message="Docs: Automated commit for Reddit news"
git commit -m "$commit_message"

# Push changes to the remote repository (adjust branch and remote name as needed)
branch_name="main"
remote_name="origin"
git push "$remote_name" "$branch_name"

echo "Git automation script executed successfully."
