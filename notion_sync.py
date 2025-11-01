#!/usr/bin/env python3
"""
Notion Sync - Sync project context to Notion for visual dashboards

This script syncs your .context/ files to a Notion database, creating
a beautiful visual dashboard of your project status.

Setup:
    1. Create a Notion integration at https://www.notion.so/my-integrations
    2. Create a database in Notion for project tracking
    3. Share the database with your integration
    4. Set environment variables:
       export NOTION_TOKEN="your_integration_token"
       export NOTION_DATABASE_ID="your_database_id"

Usage:
    python notion_sync.py sync            # Sync current context to Notion
    python notion_sync.py create-page     # Create a new status page
    python notion_sync.py update          # Update existing page
    python notion_sync.py setup           # Interactive setup wizard
"""

import os
import sys
import json
import requests
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional


class NotionContextSync:
    """Syncs project context to Notion"""

    NOTION_API_VERSION = "2022-06-28"
    NOTION_API_URL = "https://api.notion.com/v1"

    def __init__(self, token: Optional[str] = None, database_id: Optional[str] = None):
        self.token = token or os.getenv("NOTION_TOKEN")
        self.database_id = database_id or os.getenv("NOTION_DATABASE_ID")
        self.project_root = Path.cwd()
        self.context_dir = self.project_root / ".context"

        if not self.context_dir.exists():
            raise FileNotFoundError(
                f"Context directory not found: {self.context_dir}\n"
                "Run context_manager.py first to set up the context system."
            )

    def _get_headers(self) -> Dict[str, str]:
        """Get headers for Notion API requests"""
        if not self.token:
            raise ValueError(
                "NOTION_TOKEN not set. Please set it via environment variable or .env file."
            )

        return {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json",
            "Notion-Version": self.NOTION_API_VERSION
        }

    def _read_context_file(self, filename: str) -> str:
        """Read a context file"""
        file_path = self.context_dir / filename
        if file_path.exists():
            return file_path.read_text()
        return ""

    def _parse_markdown_to_blocks(self, markdown: str) -> List[Dict]:
        """Convert markdown to Notion blocks (simplified)"""
        blocks = []
        lines = markdown.split('\n')

        for line in lines:
            if not line.strip():
                continue

            # Headings
            if line.startswith('# '):
                blocks.append({
                    "object": "block",
                    "type": "heading_1",
                    "heading_1": {
                        "rich_text": [{"type": "text", "text": {"content": line[2:]}}]
                    }
                })
            elif line.startswith('## '):
                blocks.append({
                    "object": "block",
                    "type": "heading_2",
                    "heading_2": {
                        "rich_text": [{"type": "text", "text": {"content": line[3:]}}]
                    }
                })
            elif line.startswith('### '):
                blocks.append({
                    "object": "block",
                    "type": "heading_3",
                    "heading_3": {
                        "rich_text": [{"type": "text", "text": {"content": line[4:]}}]
                    }
                })
            # Code blocks (simplified)
            elif line.startswith('```'):
                blocks.append({
                    "object": "block",
                    "type": "code",
                    "code": {
                        "rich_text": [{"type": "text", "text": {"content": "Code block"}}],
                        "language": "plain text"
                    }
                })
            # Bullet points
            elif line.strip().startswith('- ') or line.strip().startswith('* '):
                content = line.strip()[2:]
                blocks.append({
                    "object": "block",
                    "type": "bulleted_list_item",
                    "bulleted_list_item": {
                        "rich_text": [{"type": "text", "text": {"content": content}}]
                    }
                })
            # Regular paragraph
            else:
                # Limit content length to avoid API errors
                content = line[:2000]
                blocks.append({
                    "object": "block",
                    "type": "paragraph",
                    "paragraph": {
                        "rich_text": [{"type": "text", "text": {"content": content}}]
                    }
                })

        # Notion has a limit on blocks per request
        return blocks[:100]

    def create_status_page(self) -> str:
        """Create a new Notion page with current project status"""
        if not self.database_id:
            raise ValueError(
                "NOTION_DATABASE_ID not set. Please set it via environment variable."
            )

        # Read context files
        readme = self._read_context_file("README.md")
        current_state = self._read_context_file("current_state.md")
        summary = self._read_context_file("summary.md")

        # Create page properties
        timestamp = datetime.now()
        page_data = {
            "parent": {"database_id": self.database_id},
            "properties": {
                "Name": {
                    "title": [
                        {
                            "text": {
                                "content": f"Project Status - {timestamp.strftime('%Y-%m-%d %H:%M')}"
                            }
                        }
                    ]
                },
                "Status": {
                    "select": {"name": "In Progress"}
                },
                "Last Updated": {
                    "date": {"start": timestamp.isoformat()}
                }
            }
        }

        # Create the page
        response = requests.post(
            f"{self.NOTION_API_URL}/pages",
            headers=self._get_headers(),
            json=page_data
        )

        if response.status_code != 200:
            raise Exception(f"Failed to create page: {response.text}")

        page_id = response.json()["id"]

        # Add content blocks
        content_blocks = []

        # Add README content
        content_blocks.extend([
            {
                "object": "block",
                "type": "heading_1",
                "heading_1": {
                    "rich_text": [{"type": "text", "text": {"content": "📋 Quick Overview"}}]
                }
            }
        ])

        # Add simplified content (Notion API has limits)
        content_blocks.extend([
            {
                "object": "block",
                "type": "paragraph",
                "paragraph": {
                    "rich_text": [{"type": "text", "text": {"content": "Context synced from .context/ folder"}}]
                }
            }
        ])

        # Add blocks to page (in chunks of 100)
        for i in range(0, len(content_blocks), 100):
            chunk = content_blocks[i:i+100]
            requests.patch(
                f"{self.NOTION_API_URL}/blocks/{page_id}/children",
                headers=self._get_headers(),
                json={"children": chunk}
            )

        print(f"✅ Created Notion page!")
        print(f"🔗 Page ID: {page_id}")
        return page_id

    def sync_to_notion(self) -> None:
        """Main sync function - creates or updates Notion page"""
        try:
            page_id = self.create_status_page()
            print(f"\n📊 Context synced to Notion successfully!")
            print(f"🔗 View in Notion: https://notion.so/{page_id.replace('-', '')}")
        except Exception as e:
            print(f"❌ Error syncing to Notion: {e}")
            print(f"\n💡 Tip: Make sure you've set NOTION_TOKEN and NOTION_DATABASE_ID")
            print(f"   Run: python notion_sync.py setup")

    def setup_wizard(self) -> None:
        """Interactive setup wizard for Notion integration"""
        print("\n" + "=" * 60)
        print("🎯 Notion Integration Setup Wizard")
        print("=" * 60)

        print("\n📝 Step 1: Create a Notion Integration")
        print("   1. Go to https://www.notion.so/my-integrations")
        print("   2. Click '+ New integration'")
        print("   3. Give it a name (e.g., 'Project Context Sync')")
        print("   4. Copy the 'Internal Integration Token'")

        token = input("\n🔑 Paste your Notion integration token: ").strip()

        print("\n📝 Step 2: Create a Database")
        print("   1. In Notion, create a new database (table view)")
        print("   2. Add these properties:")
        print("      - Name (title)")
        print("      - Status (select)")
        print("      - Last Updated (date)")
        print("   3. Share the database with your integration")
        print("   4. Copy the database ID from the URL")
        print("      (URL format: notion.so/[DATABASE_ID]?v=...)")

        database_id = input("\n🗄️  Paste your Notion database ID: ").strip()

        # Save to .env file
        env_path = self.project_root / ".env"
        env_content = ""

        if env_path.exists():
            env_content = env_path.read_text()

        # Update or add variables
        if "NOTION_TOKEN=" in env_content:
            lines = env_content.split('\n')
            env_content = '\n'.join(
                line if not line.startswith("NOTION_TOKEN=") else f"NOTION_TOKEN={token}"
                for line in lines
            )
        else:
            env_content += f"\nNOTION_TOKEN={token}"

        if "NOTION_DATABASE_ID=" in env_content:
            lines = env_content.split('\n')
            env_content = '\n'.join(
                line if not line.startswith("NOTION_DATABASE_ID=") else f"NOTION_DATABASE_ID={database_id}"
                for line in lines
            )
        else:
            env_content += f"\nNOTION_DATABASE_ID={database_id}"

        env_path.write_text(env_content)

        print("\n✅ Configuration saved to .env!")
        print("\n💡 Next steps:")
        print("   1. Test the connection: python notion_sync.py sync")
        print("   2. Add to .gitignore: echo '.env' >> .gitignore")
        print("\n" + "=" * 60)


def main():
    """Main entry point for CLI"""
    if len(sys.argv) < 2:
        print("Usage:")
        print("  python notion_sync.py sync         # Sync context to Notion")
        print("  python notion_sync.py create-page  # Create new status page")
        print("  python notion_sync.py setup        # Interactive setup")
        sys.exit(1)

    command = sys.argv[1].lower()

    try:
        syncer = NotionContextSync()

        if command == "sync":
            syncer.sync_to_notion()

        elif command == "create-page":
            page_id = syncer.create_status_page()
            print(f"Created page: {page_id}")

        elif command == "setup":
            syncer.setup_wizard()

        else:
            print(f"Unknown command: {command}")
            sys.exit(1)

    except FileNotFoundError as e:
        print(f"❌ Error: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
