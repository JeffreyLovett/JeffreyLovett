# Together 4 Eva

A couples platform application designed to help couples stay connected, plan events, and manage their relationship.

## 🚀 Getting Started

### Quick Start

```bash
# Clone the repository
git clone https://github.com/JeffreyLovett/JeffreyLovett.git
cd JeffreyLovett

# Set up environment variables
cp .env.example .env

# View project status
python3 context_manager.py status
```

## 📚 Documentation

- **[Setup Guide](docs/setup.md)** - Initial setup and configuration
- **[Architecture](docs/architecture.md)** - System architecture overview
- **[Deployment](docs/deployment.md)** - Deployment instructions
- **[Roadmap](docs/roadmap.md)** - Feature roadmap and planning
- **[Integration Guide](docs/integration.md)** - Third-party integrations
- **[AI Services](docs/ai-services.md)** - AI service integration
- **[Event Integration](docs/event-integration.md)** - Event system integration

## 🎯 Context Management System

This project includes an **intelligent context management system** that maintains development state across sessions.

### Quick Commands

```bash
# View status
python3 context_manager.py status

# Save context
python3 context_manager.py save "What you just did"

# Create checkpoint
python3 context_manager.py checkpoint "Milestone description"

# Generate handoff for next session
python3 context_manager.py handoff
```

### For Complete Documentation

See **[CONTEXT_SYSTEM_README.md](CONTEXT_SYSTEM_README.md)** for:
- Complete setup instructions
- Shell aliases configuration
- VS Code integration
- Notion sync setup
- Best practices
- Troubleshooting

### Context Files

The `.context/` directory contains:
- **README.md** - Quick overview (start here!)
- **current_state.md** - Current session state
- **summary.md** - Project summary
- **decisions.md** - Architectural decisions
- **handoff.md** - Continuation instructions
- **checkpoints/** - Timestamped snapshots

## 📁 Project Structure

```
.
├── src/                    # Source code
│   ├── services/          # Business logic and API services
│   ├── components/        # Reusable UI components
│   ├── utils/             # Helper functions
│   └── screens/           # App screens/pages
├── docs/                  # Documentation
├── .context/              # Context management (AI sessions)
├── context_manager.py     # Context automation tool
└── notion_sync.py         # Notion integration (optional)
```

## 🛠️ Development

### Shell Aliases (Optional)

Enable convenient commands by sourcing the aliases file:

```bash
source .context_aliases.sh
```

Then use:
```bash
ctx-save "Description"      # Save context
ctx-status                  # View status
ctx-checkpoint "Milestone"  # Create checkpoint
ctx-continue                # Show continuation prompt
ctx-help                    # Show all commands
```

### VS Code

Open the workspace file for integrated development:

```bash
code together4eva.code-workspace
```

This provides:
- Context management tasks (Terminal > Run Task)
- Integrated Git workflow
- Recommended extensions

## 🤝 Contributing

This project uses an AI-assisted development workflow with Claude Code.

### For Continuing Development

1. Read `.context/README.md` for current state
2. Check `.context/current_state.md` for details
3. Review recent checkpoints in `.context/checkpoints/`
4. Use `python3 context_manager.py status` to see status

### Git Workflow

The project uses feature branches with the `claude/` prefix:

```bash
# Create feature branch
git checkout -b claude/feature-name-sessionid

# Make changes and commit (context auto-saves)
git add .
git commit -m "Description"

# Push to remote
git push -u origin claude/feature-name-sessionid
```

## 📋 License

[Add your license here]

## 👥 Authors

- Jeffrey Lovett

---

**Built with ❤️ and AI assistance from Claude Code**
