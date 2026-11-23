# Fight Playbook knowledge base: setup and safety

One knowledge base only: Sean's existing Obsidian vault **The Fight Playbook Brain**, published as a **private** GitHub repo. Claude clones it in cloud sessions; the Mac and iPhone keep using it in Obsidian.

## Safety model
* Claude writes only inside the vault folder `Claude Production/`. Everything else is read only to Claude (enforced in `kb.py`).
* New notes never replace existing ones (unique dated names). Claude owned log notes are append only.
* Every push is scanned for credentials; a hit aborts and rolls back the local change.
* Pulls are fast forward only; a conflict stops and asks Sean.
* Git history keeps every version, so any change can be undone.

## Vault `.gitignore` (add BEFORE the first publish)
```
# secrets: never in GitHub
.env
*.env
*.pem
*.key
*.p12
client_secret*.json
*token*.json
*credential*
*secret*
*password*
# Obsidian per device state
.obsidian/workspace.json
.obsidian/workspace-mobile.json
.obsidian/cache
.trash/
.DS_Store
```
Notes that contain passwords or API keys should be moved out of the vault (for example into the macOS Passwords app) before publishing; the ignore rules above catch file names, not text inside notes.

## Mac setup (Sean)
1. GitHub Desktop: File, Add Local Repository, choose the vault folder, "create a repository" (paste the ignore rules above into the ignore box), then Publish repository with **Keep this code private** checked. Suggested name: `the-fight-playbook-brain`.
2. Give the Claude GitHub App access to that repo (github.com/settings/installations, Claude, Configure, add the repo).
3. Obsidian: Settings, Community plugins, Browse, install **Git** (Vinzent03). Turn on: pull on startup, auto commit and sync every 10 minutes. Optional: **Dataview** for the live dashboard tables.

## Claude setup (each cloud session, automatic once the repo is attached)
```
git clone https://github.com/swill3210/the-fight-playbook-brain /home/user/the-fight-playbook-brain
python3 production/kb/kb.py check
```
The project's SessionStart hook pulls and prints the reading list; the Stop hook asks Claude to capture lessons after production changes.

## iPhone (choose one)
* **Obsidian Sync (recommended, paid, official, end to end encrypted):** on the Mac, Settings, Sync, create a remote vault for The Fight Playbook Brain; on the iPhone, install Obsidian, sign in, choose that remote vault. Git stays on the Mac as the bridge to Claude; Obsidian Sync ignores the `.git` folder.
* **iCloud (free):** only if the vault already lives in Obsidian's iCloud folder. Keep the Mac as the only machine running Git, and expect occasional sync conflicts between iCloud and Git.
* **Git on the iPhone** (Obsidian Git mobile or Working Copy): possible but slow and fragile on large vaults; not recommended.
