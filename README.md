# Stegosaurus
The group git repository for our Steganography project.


# Git Workflow

__Make sure you have git bash or git gui installed__

## Setup

1. Fork the main repository. This will create a copy of the repo on your github. **Never push changes to the main repository.** __Always push any changes to your fork__
2. Clone your fork on your local machine wherever you are working on it.
3. On your local fork add the main repository as upstream (`git remote add upstream [Main repo url]` or in the git GUI `remote > add` and set name to `upstream`)

## Working on files

1. Your fork is yours. Do what you want with it. Create new branches, commit changes, delete __everything__.

## To change the main repo

1. Fetch from the upstream branch. (`git fetch upstream` or in the git GUI `fetch > `)
2. Merge your local working copy with the upstream tracking branch. (`git merge upstream\master`)
3. Only then, push your changes **to your fork**. (`git push origin master`)
3. Create a pull request for the main repository.
4. Get someone else to approve your pull request and resolve any conflicts.

This ensures that most conflicting changes with the main repository can be resolved by you. Nobody is able to do anything catastrophic to the main repo if this process is followed.

## Things not to do

- Push your changes to the main repository.
- Aprove your own pull requests

## Other things to keep in mind

- Never commit any keys or private data to the repository; anything you commit stays in the commit history by nature (git is version control). It is very hard to erase things from a git history.
