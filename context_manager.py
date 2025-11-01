#!/usr/bin/env python3
"""
Context Manager - Intelligent context management for Claude Code sessions

This script automates the management of project context across Claude Code sessions,
enabling seamless handoffs and maintaining development continuity.

Usage:
    python context_manager.py save "Description of changes"
    python context_manager.py checkpoint "Milestone description"
    python context_manager.py handoff
    python context_manager.py status
    python context_manager.py log-decision "CATEGORY" "Decision description"
"""

import os
import sys
import json
import subprocess
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple


class ContextManager:
    """Manages project context and state across development sessions"""

    def __init__(self, project_root: Optional[str] = None):
        self.project_root = Path(project_root) if project_root else Path.cwd()
        self.context_dir = self.project_root / ".context"
        self.checkpoints_dir = self.context_dir / "checkpoints"

        # Ensure directories exist
        self.context_dir.mkdir(exist_ok=True)
        self.checkpoints_dir.mkdir(exist_ok=True)

    def get_git_info(self) -> Dict[str, str]:
        """Get current Git status information"""
        try:
            branch = subprocess.check_output(
                ["git", "branch", "--show-current"],
                cwd=self.project_root,
                text=True
            ).strip()

            status = subprocess.check_output(
                ["git", "status", "--short"],
                cwd=self.project_root,
                text=True
            ).strip()

            last_commit = subprocess.check_output(
                ["git", "log", "-1", "--pretty=%h - %s"],
                cwd=self.project_root,
                text=True
            ).strip()

            return {
                "branch": branch,
                "status": status if status else "(clean)",
                "last_commit": last_commit,
                "is_clean": not bool(status)
            }
        except subprocess.CalledProcessError:
            return {
                "branch": "unknown",
                "status": "not a git repository",
                "last_commit": "N/A",
                "is_clean": False
            }

    def get_file_tree(self, max_depth: int = 2) -> str:
        """Generate a simple file tree of the project"""
        try:
            # Try using tree command
            result = subprocess.run(
                ["tree", "-L", str(max_depth), "-a", "--gitignore", "-I", ".git"],
                cwd=self.project_root,
                capture_output=True,
                text=True
            )
            if result.returncode == 0:
                return result.stdout
        except FileNotFoundError:
            pass

        # Fallback to manual tree generation
        lines = []
        for root, dirs, files in os.walk(self.project_root):
            # Skip .git directory
            if '.git' in root:
                continue

            level = root.replace(str(self.project_root), '').count(os.sep)
            if level > max_depth:
                continue

            indent = ' ' * 2 * level
            lines.append(f"{indent}{os.path.basename(root)}/")
            subindent = ' ' * 2 * (level + 1)
            for file in sorted(files):
                if not file.startswith('.'):
                    lines.append(f"{subindent}{file}")

        return '\n'.join(lines)

    def save_context(self, description: str = "", auto: bool = False) -> None:
        """Save current context state"""
        timestamp = datetime.now()
        git_info = self.get_git_info()

        # Update current_state.md
        current_state_path = self.context_dir / "current_state.md"
        current_state = self._read_file(current_state_path)

        # Update the timestamp and add to working notes
        updated_state = f"""# Current Project State

**Last Updated:** {timestamp.strftime("%Y-%m-%d %H:%M:%S")}
**Session ID:** {git_info['branch']}

## Active Work

### Recently Updated
{f"- {description}" if description else "- Context auto-saved via Git hook"}

### Current Branch Status

**Branch:** {git_info['branch']}
**Status:** {git_info['status']}
**Last Commit:** {git_info['last_commit']}

## Working Notes

- Last context save: {timestamp.strftime("%Y-%m-%d %H:%M:%S")}
{f"- {description}" if description else ""}

---

*Auto-updated by context_manager.py*
"""

        self._write_file(current_state_path, updated_state)

        # Update README.md timestamp
        readme_path = self.context_dir / "README.md"
        readme_content = self._read_file(readme_path)
        readme_content = readme_content.replace(
            f"**Last Updated:** 2025-11-01",
            f"**Last Updated:** {timestamp.strftime('%Y-%m-%d')}"
        )
        self._write_file(readme_path, readme_content)

        if not auto:
            print(f"✅ Context saved: {description if description else 'Manual save'}")
            print(f"📍 Branch: {git_info['branch']}")
            print(f"📊 Status: {git_info['status']}")

    def create_checkpoint(self, description: str) -> None:
        """Create a timestamped checkpoint of current state"""
        timestamp = datetime.now()
        checkpoint_file = self.checkpoints_dir / f"{timestamp.strftime('%Y%m%d_%H%M%S')}_{description.replace(' ', '_')}.md"

        git_info = self.get_git_info()

        checkpoint_content = f"""# Checkpoint: {description}

**Created:** {timestamp.strftime("%Y-%m-%d %H:%M:%S")}
**Branch:** {git_info['branch']}
**Commit:** {git_info['last_commit']}

## State at Checkpoint

### Git Status
```
{git_info['status']}
```

### Description
{description}

## Files Changed Since Last Commit

"""

        # Add git diff summary if there are changes
        try:
            diff_summary = subprocess.check_output(
                ["git", "diff", "--stat"],
                cwd=self.project_root,
                text=True
            )
            checkpoint_content += f"```\n{diff_summary}\n```\n"
        except subprocess.CalledProcessError:
            checkpoint_content += "No changes detected.\n"

        checkpoint_content += f"\n---\n\n*Checkpoint created by context_manager.py*\n"

        self._write_file(checkpoint_file, checkpoint_content)

        print(f"📸 Checkpoint created: {checkpoint_file.name}")
        print(f"📝 Description: {description}")

    def generate_handoff(self) -> None:
        """Generate/update handoff.md with current continuation instructions"""
        timestamp = datetime.now()
        git_info = self.get_git_info()

        # Read current_state to extract what's been done
        current_state = self._read_file(self.context_dir / "current_state.md")

        handoff_content = f"""# Continuation Instructions for Next Session

**Generated:** {timestamp.strftime("%Y-%m-%d %H:%M:%S")}
**Session ID:** {git_info['branch']}

---

## 🎯 Quick Context

You're working on the "Together 4 Eva" project - a couples platform application.

## 📍 Current State

**Branch:** {git_info['branch']}
**Status:** {git_info['status']}
**Last Commit:** {git_info['last_commit']}

## 📂 Key Files to Review

1. `.context/README.md` - Start here for overview
2. `.context/current_state.md` - Detailed current status
3. `.context/summary.md` - Project summary
4. `.context/decisions.md` - Architectural decisions

## 🚀 How to Continue

### Recommended First Steps
1. Read `.context/README.md` for quick orientation
2. Check `.context/current_state.md` for detailed status
3. Review recent checkpoints in `.context/checkpoints/`
4. Check git status: `git status`

### Quick Commands
```bash
# Save context
python context_manager.py save "What you did"

# Create checkpoint
python context_manager.py checkpoint "Milestone reached"

# View status
python context_manager.py status

# Log a decision
python context_manager.py log-decision "CATEGORY" "Decision"
```

## 📋 Paste-Ready Continuation Prompt

```markdown
I'm continuing work on the Together 4 Eva project.

Branch: {git_info['branch']}
Status: {git_info['status']}

Please read .context/README.md and .context/current_state.md to understand
where we left off, then continue with the next task.
```

---

*Generated automatically by context_manager.py*
*Run `python context_manager.py handoff` to regenerate*
"""

        handoff_path = self.context_dir / "handoff.md"
        self._write_file(handoff_path, handoff_content)

        print("🤝 Handoff document updated!")
        print(f"📄 Location: {handoff_path}")
        print("\n📋 Copy this to continue in a new session:")
        print("─" * 60)
        print(f"I'm continuing work on the Together 4 Eva project.")
        print(f"Branch: {git_info['branch']}")
        print(f"Please read .context/README.md and continue.")
        print("─" * 60)

    def show_status(self) -> None:
        """Display current project status"""
        git_info = self.get_git_info()

        print("\n" + "=" * 60)
        print("📊 PROJECT STATUS")
        print("=" * 60)
        print(f"\n🌿 Git Branch: {git_info['branch']}")
        print(f"📝 Last Commit: {git_info['last_commit']}")
        print(f"📊 Status: {git_info['status']}")

        # Count checkpoints
        checkpoints = list(self.checkpoints_dir.glob("*.md"))
        print(f"\n📸 Checkpoints: {len(checkpoints)}")

        if checkpoints:
            print("\n   Recent checkpoints:")
            for checkpoint in sorted(checkpoints, reverse=True)[:5]:
                print(f"   - {checkpoint.stem}")

        # Show recent context updates
        current_state_path = self.context_dir / "current_state.md"
        if current_state_path.exists():
            stat = current_state_path.stat()
            last_modified = datetime.fromtimestamp(stat.st_mtime)
            print(f"\n⏰ Last context update: {last_modified.strftime('%Y-%m-%d %H:%M:%S')}")

        print("\n" + "=" * 60)
        print("\n💡 Quick Commands:")
        print("   python context_manager.py save \"What you did\"")
        print("   python context_manager.py checkpoint \"Milestone\"")
        print("   python context_manager.py handoff")
        print("\n")

    def log_decision(self, category: str, decision: str) -> None:
        """Append a decision to the decisions.log file"""
        timestamp = datetime.now()
        decisions_log_path = self.context_dir / "decisions.log"

        log_entry = f"[{timestamp.strftime('%Y-%m-%d')}] [{category.upper()}] {decision}\n"

        # Append to file
        with open(decisions_log_path, 'a') as f:
            # Find the "End of log" marker and insert before it
            content = decisions_log_path.read_text()
            if "*End of log*" in content:
                content = content.replace("*End of log*", f"{log_entry}\n*End of log*")
                decisions_log_path.write_text(content)
            else:
                f.write(log_entry)

        print(f"📝 Decision logged: [{category.upper()}] {decision}")

    def _read_file(self, path: Path) -> str:
        """Safely read a file"""
        if path.exists():
            return path.read_text()
        return ""

    def _write_file(self, path: Path, content: str) -> None:
        """Safely write to a file"""
        path.write_text(content)


def main():
    """Main entry point for CLI"""
    if len(sys.argv) < 2:
        print("Usage:")
        print("  python context_manager.py save \"Description\"")
        print("  python context_manager.py checkpoint \"Milestone\"")
        print("  python context_manager.py handoff")
        print("  python context_manager.py status")
        print("  python context_manager.py log-decision \"CATEGORY\" \"Decision\"")
        sys.exit(1)

    manager = ContextManager()
    command = sys.argv[1].lower()

    if command == "save":
        description = sys.argv[2] if len(sys.argv) > 2 else ""
        auto = "--auto" in sys.argv
        manager.save_context(description, auto)

    elif command == "checkpoint":
        if len(sys.argv) < 3:
            print("Error: checkpoint requires a description")
            sys.exit(1)
        description = sys.argv[2]
        manager.create_checkpoint(description)

    elif command == "handoff":
        manager.generate_handoff()

    elif command == "status":
        manager.show_status()

    elif command == "log-decision":
        if len(sys.argv) < 4:
            print("Error: log-decision requires CATEGORY and decision description")
            sys.exit(1)
        category = sys.argv[2]
        decision = sys.argv[3]
        manager.log_decision(category, decision)

    else:
        print(f"Unknown command: {command}")
        sys.exit(1)


if __name__ == "__main__":
    main()
