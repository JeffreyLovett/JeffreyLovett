# Project Context - Together 4 Eva

**Last Updated:** 2025-11-01
**Current Status:** Context Management System Setup in Progress
**Active Branch:** claude/setup-context-management-system-011CUgiYCJPnBy6ytb6E9vGa

## Current State

This project is setting up an intelligent context management system to maintain state across Claude Code sessions, enable seamless handoffs between different Claude instances, and provide automatic context preservation.

### What's Happening Now

- Setting up automated context management infrastructure
- Creating Python tools for context tracking
- Integrating with Git workflow
- Preparing Notion sync capabilities

### Project Overview

Together 4 Eva - A couples platform application

**Tech Stack:**
- Mobile/Web application
- Service-oriented architecture (src/services/)
- Component-based UI (src/components/)
- Utility functions (src/utils/)
- Screen/view layer (src/screens/)

### Key Directories

- `src/` - Source code
  - `services/` - Business logic and API services
  - `components/` - Reusable UI components
  - `utils/` - Helper functions and utilities
  - `screens/` - App screens/pages
- `docs/` - Project documentation
- `.context/` - Context management system (this folder!)

## Quick Start for New Sessions

1. Read this file first to understand current state
2. Check `current_state.md` for detailed status
3. Review `decisions.md` for past architectural choices
4. See `handoff.md` for continuation instructions

## How to Use This System

### Auto-Save Context
```bash
python context_manager.py save "Description of what you just did"
```

### Prepare for Handoff
```bash
python context_manager.py handoff
```

### Create Checkpoint
```bash
python context_manager.py checkpoint "Milestone description"
```

### View Recent Activity
```bash
python context_manager.py status
```

## Context Files

- `README.md` (this file) - High-level overview, always current
- `current_state.md` - Detailed current project state
- `summary.md` - Comprehensive project summary
- `decisions.md` - Architectural and design decisions
- `decisions.log` - Append-only decision record
- `handoff.md` - Ready-to-paste continuation prompt
- `checkpoints/` - Timestamped progress saves

## Integration Points

- **Git Hooks:** Pre-commit hook auto-saves context
- **Shell Aliases:** `ctx-save`, `ctx-continue`, `ctx-status`
- **Notion Sync:** Automatic sync to Notion dashboard (when configured)
- **VS Code:** Workspace integration for quick access

---

*This context system is designed to work seamlessly with Claude Code, maintaining continuity across sessions and enabling efficient collaboration.*
