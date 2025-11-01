#!/bin/bash
#
# Context Management Shell Aliases
#
# Add these aliases to your shell by adding this line to your ~/.bashrc or ~/.zshrc:
#   source /path/to/your/project/.context_aliases.sh
#
# Or run it manually in your current session:
#   source .context_aliases.sh
#

# Get the directory where this script is located
CONTEXT_PROJECT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Aliases for context management
alias ctx-save='python3 "$CONTEXT_PROJECT_DIR/context_manager.py" save'
alias ctx-checkpoint='python3 "$CONTEXT_PROJECT_DIR/context_manager.py" checkpoint'
alias ctx-handoff='python3 "$CONTEXT_PROJECT_DIR/context_manager.py" handoff'
alias ctx-status='python3 "$CONTEXT_PROJECT_DIR/context_manager.py" status'
alias ctx-decision='python3 "$CONTEXT_PROJECT_DIR/context_manager.py" log-decision'

# Alias for Notion sync
alias ctx-notion='python3 "$CONTEXT_PROJECT_DIR/notion_sync.py" sync'
alias ctx-notion-setup='python3 "$CONTEXT_PROJECT_DIR/notion_sync.py" setup'

# Quick navigation
alias ctx-cd='cd "$CONTEXT_PROJECT_DIR/.context"'
alias ctx-read='cat "$CONTEXT_PROJECT_DIR/.context/README.md"'
alias ctx-state='cat "$CONTEXT_PROJECT_DIR/.context/current_state.md"'

# Function to display continuation prompt
ctx-continue() {
    echo ""
    echo "════════════════════════════════════════════════════════════"
    echo "📋 CONTINUATION PROMPT FOR CLAUDE"
    echo "════════════════════════════════════════════════════════════"
    echo ""
    cat "$CONTEXT_PROJECT_DIR/.context/handoff.md" | grep -A 20 "Paste-Ready Continuation Prompt"
    echo ""
    echo "════════════════════════════════════════════════════════════"
    echo ""
}

# Function to show context help
ctx-help() {
    echo ""
    echo "📚 Context Management Commands"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo ""
    echo "💾 Saving Context:"
    echo "  ctx-save \"Description\"      Save current context"
    echo "  ctx-checkpoint \"Milestone\"  Create a checkpoint"
    echo ""
    echo "🔄 Handoffs & Status:"
    echo "  ctx-handoff                 Generate handoff document"
    echo "  ctx-continue                Display continuation prompt"
    echo "  ctx-status                  Show project status"
    echo ""
    echo "📝 Decisions:"
    echo "  ctx-decision \"CAT\" \"Text\"   Log an architectural decision"
    echo ""
    echo "☁️  Notion Integration:"
    echo "  ctx-notion                  Sync to Notion"
    echo "  ctx-notion-setup            Setup Notion integration"
    echo ""
    echo "📂 Navigation:"
    echo "  ctx-cd                      Go to .context/ directory"
    echo "  ctx-read                    Read context README"
    echo "  ctx-state                   Read current state"
    echo ""
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo ""
}

# Print helpful message when sourced
echo "✅ Context management aliases loaded!"
echo "💡 Type 'ctx-help' for available commands"
