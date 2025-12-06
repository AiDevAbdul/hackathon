#!/usr/bin/env python3
"""
Data backup and recovery procedures for the Physical AI & Humanoid Robotics Textbook Platform
"""
import os
import sys
import subprocess
import datetime
import json
from pathlib import Path
from typing import Dict, List, Optional


class DataBackupRecovery:
    """Handles data backup and recovery procedures for the platform."""

    def __init__(self, backup_dir: str = "./backups"):
        self.backup_dir = Path(backup_dir)
        self.backup_dir.mkdir(exist_ok=True)
        self.config = self._load_config()

    def _load_config(self) -> Dict:
        """Load backup configuration."""
        return {
            "databases": {
                "postgresql": {
                    "host": os.getenv("DB_HOST", "localhost"),
                    "port": os.getenv("DB_PORT", "5432"),
                    "database": os.getenv("DB_NAME", "textbook_platform"),
                    "username": os.getenv("DB_USER", "user"),
                    "password": os.getenv("DB_PASSWORD", "password")
                }
            },
            "backup_retention_days": 30,
            "backup_compression": True
        }

    def create_backup(self, backup_name: Optional[str] = None) -> str:
        """Create a backup of all platform data."""
        if not backup_name:
            backup_name = f"backup_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}"

        backup_path = self.backup_dir / backup_name
        backup_path.mkdir(exist_ok=True)

        print(f"Creating backup: {backup_name}")

        # Backup database
        db_backup_path = backup_path / "database_backup.sql"
        self._backup_database(db_backup_path)

        # Create backup manifest
        manifest = {
            "backup_name": backup_name,
            "timestamp": datetime.datetime.now().isoformat(),
            "components": ["database"],
            "status": "completed"
        }

        with open(backup_path / "manifest.json", 'w') as f:
            json.dump(manifest, f, indent=2)

        print(f"Backup completed: {backup_path}")
        return str(backup_path)

    def _backup_database(self, output_path: Path) -> None:
        """Backup the PostgreSQL database."""
        try:
            # Set environment variables for pg_dump
            env = os.environ.copy()
            env["PGPASSWORD"] = self.config["databases"]["postgresql"]["password"]

            cmd = [
                "pg_dump",
                "-h", self.config["databases"]["postgresql"]["host"],
                "-p", str(self.config["databases"]["postgresql"]["port"]),
                "-U", self.config["databases"]["postgresql"]["username"],
                "-d", self.config["databases"]["postgresql"]["database"],
                "-f", str(output_path)
            ]

            result = subprocess.run(
                cmd,
                env=env,
                capture_output=True,
                text=True
            )

            if result.returncode != 0:
                raise Exception(f"Database backup failed: {result.stderr}")

            print(f"Database backup created: {output_path}")

        except FileNotFoundError:
            print("Warning: pg_dump not found. Database backup skipped.")
            print("Install PostgreSQL client tools to enable database backups.")
        except Exception as e:
            print(f"Error during database backup: {e}")
            raise

    def list_backups(self) -> List[Dict]:
        """List all available backups."""
        backups = []
        for item in self.backup_dir.iterdir():
            if item.is_dir():
                manifest_path = item / "manifest.json"
                if manifest_path.exists():
                    with open(manifest_path, 'r') as f:
                        manifest = json.load(f)
                        backups.append(manifest)

        # Sort by timestamp (newest first)
        backups.sort(key=lambda x: x.get("timestamp", ""), reverse=True)
        return backups

    def restore_backup(self, backup_name: str) -> bool:
        """Restore from a specific backup."""
        backup_path = self.backup_dir / backup_name
        if not backup_path.exists():
            print(f"Backup {backup_name} not found")
            return False

        manifest_path = backup_path / "manifest.json"
        if not manifest_path.exists():
            print(f"Manifest not found for backup {backup_name}")
            return False

        with open(manifest_path, 'r') as f:
            manifest = json.load(f)

        print(f"Restoring from backup: {backup_name}")

        # Restore database
        db_backup_path = backup_path / "database_backup.sql"
        if db_backup_path.exists():
            self._restore_database(db_backup_path)
        else:
            print("Database backup file not found, skipping database restore")

        print(f"Restore completed from: {backup_name}")
        return True

    def _restore_database(self, backup_path: Path) -> None:
        """Restore the PostgreSQL database from backup."""
        try:
            # Set environment variables for psql
            env = os.environ.copy()
            env["PGPASSWORD"] = self.config["databases"]["postgresql"]["password"]

            cmd = [
                "psql",
                "-h", self.config["databases"]["postgresql"]["host"],
                "-p", str(self.config["databases"]["postgresql"]["port"]),
                "-U", self.config["databases"]["postgresql"]["username"],
                "-d", self.config["databases"]["postgresql"]["database"],
                "-f", str(backup_path)
            ]

            result = subprocess.run(
                cmd,
                env=env,
                capture_output=True,
                text=True
            )

            if result.returncode != 0:
                raise Exception(f"Database restore failed: {result.stderr}")

            print(f"Database restored from: {backup_path}")

        except FileNotFoundError:
            print("Warning: psql not found. Database restore skipped.")
            print("Install PostgreSQL client tools to enable database restores.")
        except Exception as e:
            print(f"Error during database restore: {e}")
            raise

    def cleanup_old_backups(self) -> None:
        """Remove backups older than retention period."""
        cutoff_date = datetime.datetime.now() - datetime.timedelta(
            days=self.config["backup_retention_days"]
        )

        for item in self.backup_dir.iterdir():
            if item.is_dir():
                manifest_path = item / "manifest.json"
                if manifest_path.exists():
                    with open(manifest_path, 'r') as f:
                        manifest = json.load(f)

                    backup_date = datetime.datetime.fromisoformat(
                        manifest["timestamp"].replace("Z", "+00:00")
                    )

                    if backup_date < cutoff_date:
                        import shutil
                        shutil.rmtree(item)
                        print(f"Removed old backup: {item.name}")


def main():
    """Main function to handle backup/recovery operations."""
    import argparse

    parser = argparse.ArgumentParser(description="Data backup and recovery for Textbook Platform")
    parser.add_argument("action", choices=["create", "list", "restore", "cleanup"],
                       help="Action to perform")
    parser.add_argument("--name", help="Backup name (for restore action)")
    parser.add_argument("--backup-dir", default="./backups", help="Backup directory")

    args = parser.parse_args()

    backup_manager = DataBackupRecovery(backup_dir=args.backup_dir)

    if args.action == "create":
        backup_manager.create_backup()
    elif args.action == "list":
        backups = backup_manager.list_backups()
        print("Available backups:")
        for backup in backups:
            print(f"  - {backup['backup_name']} ({backup['timestamp']}) - {backup['status']}")
    elif args.action == "restore":
        if not args.name:
            print("Backup name required for restore operation")
            return
        backup_manager.restore_backup(args.name)
    elif args.action == "cleanup":
        backup_manager.cleanup_old_backups()


if __name__ == "__main__":
    main()