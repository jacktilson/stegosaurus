# Stegosaurus
The group git repository for our Steganography project.

# Git Workflow

__Make sure you have git bash or git GUI installed__

## Setup

1. Fork the main repository. This will create a copy of the repo on your github. **Never push changes to the main repository.** __*Always push any changes to your fork*__
2. Clone your fork on your local machine wherever you are working on it.
3. On your local fork add the main repository as upstream (`git remote add upstream [Main repo url]` or in the git GUI `Remote > Add`)

## Working On Files

1. Your fork is yours. Do what you want with it. Create new branches, commit changes, delete __*everything*__.
2. *Generally*, [`git add .`],  [`git commit -m [message]`]. See another guide.

## To Change The Main Repo

1. Make sure all your changes are commited. Your working tree needs to be clean otherwise you wont be able to push anywhere.
2. Fetch from the upstream branch. (`git fetch upstream` or in the git GUI `Remote > Fetch from upstream`)
3. Merge your local working copy with the upstream tracking branch. (`git merge upstream\master` or in the git GUI `Merge > Local merge...`)
4. Only then, push your changes **to your fork**. (`git push origin master` or in the git GUI `Remote > Push`)
5. Create a pull request for the main repository.
6. Get someone else to approve your pull request and resolve any conflicts.

This ensures that most conflicting changes with the main repository can be resolved by you. Nobody is able to do anything catastrophic to the main repo if this process is followed.

## *Things Not To Do*


- Push your changes to the main repository.
- Approve your own pull requests.
- Never commit any keys or private data to the repository; anything you commit stays in the commit history by nature (git is version control). It is very hard to erase things from a git history.
