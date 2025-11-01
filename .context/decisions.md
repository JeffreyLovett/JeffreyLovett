# Architectural & Design Decisions

This document records important decisions made during the project's development, including the rationale and alternatives considered.

---

## Decision Log

### 2025-11-01: Context Management System Architecture

**Decision:** Implement a file-based context management system in `.context/` folder

**Context:**
- Need to maintain state across Claude Code sessions
- Want to enable handoffs between different Claude instances
- Require integration with existing Git workflow

**Options Considered:**
1. Database-based context storage (e.g., SQLite)
2. Cloud-based context service (e.g., external API)
3. File-based markdown system in repository
4. Git notes or commit message conventions

**Decision Rationale:**
- **Chosen:** File-based markdown system (#3)
- **Why:**
  - Version controlled automatically with Git
  - Human-readable and editable
  - No external dependencies
  - Works offline
  - Easy to sync to Notion or other tools
  - Portable across environments

**Trade-offs:**
- ✅ Simple, reliable, version-controlled
- ✅ Human-readable
- ✅ No external dependencies
- ⚠️ Not suitable for very large context (acceptable for most projects)
- ⚠️ Requires discipline to update (mitigated with automation)

**Implementation Details:**
- Python script (context_manager.py) for automation
- Git pre-commit hooks for auto-save
- Shell aliases for easy access
- Optional Notion sync for visualization

---

### 2025-11-01: Context File Structure

**Decision:** Use multiple specialized files instead of single monolithic file

**Files:**
- `README.md` - High-level overview (always up-to-date)
- `current_state.md` - Detailed current status
- `summary.md` - Comprehensive project summary
- `decisions.md` - This file - decision records
- `decisions.log` - Append-only chronological log
- `handoff.md` - Continuation instructions
- `checkpoints/` - Timestamped snapshots

**Rationale:**
- Different use cases need different information density
- README for quick orientation
- current_state.md for session continuation
- summary.md for comprehensive understanding
- Specialized files reduce cognitive load

---

### 2025-11-01: Python for Automation

**Decision:** Use Python for context_manager.py

**Rationale:**
- Widely available on development systems
- Excellent file I/O and text processing
- Easy to extend for Notion API integration
- Familiar to most developers
- Cross-platform

**Alternatives Considered:**
- Shell scripts (less portable, harder to extend)
- Node.js (additional dependency)
- Go (compile step adds complexity)

---

### 2025-11-01: Git Hook Integration

**Decision:** Use pre-commit hook for automatic context saving

**Rationale:**
- Ensures context is saved before commits
- Automatic - no manual intervention needed
- Aligns with natural workflow (commit when making progress)
- Prevents loss of context

**Implementation:**
- Hook calls `context_manager.py save --auto`
- Updates current_state.md and README.md
- Creates checkpoint if significant changes detected

---

## Decision Guidelines

When adding decisions to this log:

1. **Use the template:**
   - Decision statement
   - Context/background
   - Options considered
   - Rationale
   - Trade-offs
   - Implementation details

2. **Be specific:** Include enough detail for future developers to understand

3. **Update decisions.log:** Add a one-line entry for chronological tracking

4. **Link to code:** Reference relevant files or commits

---

*Format inspired by Architecture Decision Records (ADR)*
