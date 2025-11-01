# Context Management System - Complete Guide

## 🎯 What Is This?

This is an **intelligent context management system** designed to maintain state across Claude Code sessions, enable seamless handoffs between different AI instances, and provide automatic context preservation integrated with your Git workflow.

## 🚀 Quick Start

### 1. Test the System

```bash
# View current status
python3 context_manager.py status

# Save your current work
python3 context_manager.py save "Implemented feature X"

# Create a checkpoint
python3 context_manager.py checkpoint "Feature X complete"

# Generate handoff for next session
python3 context_manager.py handoff
```

### 2. Enable Shell Aliases (Optional but Recommended)

Add this to your `~/.bashrc` or `~/.zshrc`:

```bash
source /path/to/your/project/.context_aliases.sh
```

Then you can use convenient commands:

```bash
ctx-save "Description"
ctx-status
ctx-checkpoint "Milestone"
ctx-continue  # Shows continuation prompt
ctx-help      # Shows all available commands
```

### 3. Open in VS Code (Optional)

Open the workspace file for integrated context management:

```bash
code together4eva.code-workspace
```

This gives you:
- Tasks menu for context operations (Terminal > Run Task)
- Keyboard shortcuts
- Integrated terminal with proper environment

---

## 📁 File Structure

```
.
├── .context/                       # Context management folder
│   ├── README.md                  # Quick overview (start here!)
│   ├── current_state.md           # Current session state
│   ├── summary.md                 # Project summary
│   ├── decisions.md               # Architectural decisions
│   ├── decisions.log              # Chronological decision log
│   ├── handoff.md                 # Continuation instructions
│   └── checkpoints/               # Timestamped snapshots
│       └── YYYYMMDD_HHMMSS_description.md
│
├── context_manager.py             # Main automation tool
├── notion_sync.py                 # Notion integration (optional)
├── .context_aliases.sh            # Shell aliases
├── together4eva.code-workspace    # VS Code workspace
├── .git/hooks/pre-commit          # Auto-save on commit
└── CONTEXT_SYSTEM_README.md       # This file
```

---

## 🛠️ Core Commands

### Save Context

```bash
python3 context_manager.py save "Description of what you did"
```

Updates `.context/current_state.md` and `.context/README.md` with:
- Timestamp
- Description
- Current git status
- Branch information

### Create Checkpoint

```bash
python3 context_manager.py checkpoint "Milestone description"
```

Creates a timestamped snapshot in `.context/checkpoints/` containing:
- Full state at that moment
- Git diff summary
- Branch and commit info

Use this for:
- Completing major features
- Before making risky changes
- End of work sessions
- When reaching milestones

### Generate Handoff

```bash
python3 context_manager.py handoff
```

Updates `.context/handoff.md` with ready-to-paste continuation instructions for:
- Starting a new Claude Code session
- Switching to web Claude
- Handing off to another developer

### View Status

```bash
python3 context_manager.py status
```

Shows:
- Current branch and git status
- Recent checkpoints
- Last context update time
- Quick command reference

### Log Decision

```bash
python3 context_manager.py log-decision "ARCHITECTURE" "Chose microservices over monolith"
```

Appends to `.context/decisions.log` with timestamp and category.

---

## 🎨 Notion Integration (Optional)

### Setup

```bash
python3 notion_sync.py setup
```

Follow the interactive wizard to:
1. Create a Notion integration
2. Get your integration token
3. Set up a database
4. Configure credentials

### Sync to Notion

```bash
python3 notion_sync.py sync
```

Creates/updates a Notion page with:
- Current project status
- Context from .context/ files
- Visual dashboard

### Configuration

The setup wizard saves credentials to `.env`:

```env
NOTION_TOKEN=secret_xxxxxxxxxxxx
NOTION_DATABASE_ID=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

**Important:** Add `.env` to `.gitignore`!

```bash
echo '.env' >> .gitignore
```

---

## 🔄 Git Integration

### Automatic Context Saving

A pre-commit hook automatically saves context before each commit:

```bash
# Located at: .git/hooks/pre-commit
```

When you run `git commit`:
1. Hook runs `context_manager.py save --auto`
2. Updates `.context/current_state.md`
3. Adds `.context/` files to the commit

### Manual Git Workflow

```bash
# Make changes
git add .

# Context is auto-saved during commit
git commit -m "Add feature X"

# Push to your branch
git push -u origin your-branch-name
```

---

## 💡 Workflow Examples

### Starting a New Session

```bash
# 1. Read context
cat .context/README.md

# 2. Check current state
cat .context/current_state.md

# 3. View recent checkpoints
ls -lt .context/checkpoints/

# 4. Check git status
git status

# 5. Start working!
```

### During Development

```bash
# Implement feature
# ... make changes ...

# Save context periodically
python3 context_manager.py save "Implemented user authentication"

# Reach a milestone
python3 context_manager.py checkpoint "Auth system complete"

# Commit (auto-saves context)
git add .
git commit -m "Add authentication system"
```

### Ending a Session

```bash
# 1. Save final state
python3 context_manager.py save "Ending session, auth tests passing"

# 2. Create checkpoint
python3 context_manager.py checkpoint "End of session - Auth complete"

# 3. Generate handoff
python3 context_manager.py handoff

# 4. Optional: Sync to Notion
python3 notion_sync.py sync

# 5. Commit and push
git add .
git commit -m "Session checkpoint: Auth implementation"
git push
```

### Continuing in a New Session

```bash
# 1. Pull latest
git pull

# 2. Read handoff
cat .context/handoff.md

# 3. Check status
python3 context_manager.py status

# 4. Continue working
```

---

## 🎓 Best Practices

### When to Save Context

✅ **Do save:**
- After implementing a feature
- Before taking a break
- After fixing a bug
- When making important decisions
- Before risky refactoring

❌ **Don't save:**
- After every tiny change
- When nothing has changed
- Multiple times in a row

### When to Create Checkpoints

Use checkpoints for:
- ✅ Completing major features
- ✅ End of work sessions
- ✅ Before risky changes
- ✅ Reaching milestones
- ✅ Before major refactoring

### Decision Logging

Log decisions when you:
- Choose between architectural approaches
- Select libraries or frameworks
- Make trade-offs
- Establish conventions
- Deviate from plans

Example:
```bash
python3 context_manager.py log-decision "ARCHITECTURE" "Using PostgreSQL for persistence over SQLite for production scalability"
```

### Handoff Preparation

Always generate a handoff before:
- Ending your work day
- Switching to a different task
- Asking someone else to continue
- Moving to a different Claude instance

---

## 🔧 Troubleshooting

### Context manager not working

```bash
# Check Python version (needs 3.6+)
python3 --version

# Make script executable
chmod +x context_manager.py

# Test directly
python3 context_manager.py status
```

### Pre-commit hook not triggering

```bash
# Make hook executable
chmod +x .git/hooks/pre-commit

# Test hook manually
.git/hooks/pre-commit
```

### Shell aliases not working

```bash
# Source the aliases file
source .context_aliases.sh

# Or add to your shell profile
echo 'source /path/to/project/.context_aliases.sh' >> ~/.bashrc
```

### Notion sync failing

```bash
# Run setup wizard
python3 notion_sync.py setup

# Verify .env file
cat .env

# Check credentials
python3 notion_sync.py sync
```

---

## 🎯 Advanced Usage

### Custom Checkpoints

Create checkpoints with specific metadata:

```bash
# Before risky refactoring
python3 context_manager.py checkpoint "Pre-refactoring: Working state"

# Make changes
# ... refactor code ...

# After refactoring
python3 context_manager.py checkpoint "Post-refactoring: Refactored with tests passing"
```

### Reviewing History

```bash
# List all checkpoints
ls -lt .context/checkpoints/

# Read a specific checkpoint
cat .context/checkpoints/20251101_065014_*.md

# Compare checkpoints
diff .context/checkpoints/checkpoint1.md .context/checkpoints/checkpoint2.md
```

### Automating with Cron

```bash
# Add to crontab for periodic saves
0 * * * * cd /path/to/project && python3 context_manager.py save "Hourly auto-save"
```

### VS Code Tasks

Use Command Palette (Ctrl+Shift+P):
- "Tasks: Run Task"
- Select "Context: Save" or other context tasks
- Enter description when prompted

---

## 📚 Context File Reference

### README.md
High-level overview, quick start guide. Read this first when starting a session.

### current_state.md
Detailed current status:
- Active work
- Recent updates
- Git branch info
- Next steps
- Known issues

### summary.md
Comprehensive project summary:
- Project description
- Architecture overview
- Tech stack
- Key features

### decisions.md
Architectural decisions with:
- Decision statement
- Context/rationale
- Options considered
- Trade-offs

### decisions.log
Chronological append-only log of all decisions.

### handoff.md
Ready-to-paste continuation instructions for next session.

### checkpoints/
Timestamped snapshots of project state at specific moments.

---

## 🤝 Handoff Protocol

### To Claude Code (from web)
```
I'm continuing work from a web session. Please read .context/README.md
and .context/current_state.md to understand the current state, then continue.
```

### To Web Claude (from Claude Code)
```bash
# Generate handoff first
python3 context_manager.py handoff

# Then paste in web Claude:
"I'm continuing work from Claude Code. Here's the context: [paste .context/handoff.md]"
```

### To Another Developer
Share:
1. `.context/README.md` - Quick overview
2. `.context/summary.md` - Project details
3. `.context/current_state.md` - Current status
4. Latest checkpoint from `.context/checkpoints/`

---

## 📊 System Requirements

- **Python:** 3.6 or higher
- **Git:** Any recent version
- **Optional:** VS Code for workspace integration
- **Optional:** Notion account for dashboard sync

---

## 🎉 You're All Set!

Start using the context management system:

```bash
# Quick test
python3 context_manager.py status

# Save your first context
python3 context_manager.py save "Context management system set up"

# Create a checkpoint
python3 context_manager.py checkpoint "Context system ready"
```

For questions or issues, check the troubleshooting section above.

---

**Happy coding with persistent context! 🚀**
