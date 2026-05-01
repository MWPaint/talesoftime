import sqlite3
import os
from datetime import datetime
from flask import current_app

def backup_sqlite_db()
    """
    Creates a timestamped backup of the SQLite databse using the
    official SQLite backup API.
    """
    # 1. Define paths
    db_path = os.path.join(current_app.instance_path, 'tales_of_time.db')
    backup_dir = os.path.join(current_app.instance_path, 'backups')

    # 2. Ensure backup directory exists
    os.makedirs(backup_dir, exist_ok=True)

    # 3 Create timestamped filename
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    backup_path = os.path.join(backup_dir, f'talesoftime_backup_{timestamp}.db')

    try:
        # 4. Perform live atomic backup
        # This connects to the source and destination databases
        source = sqlite3.connect(db_path)
        dest = sqlite3.connect(backup_path)

        # The 'with' block ensures the destination connection is committed/closed
        with dest:
            source.backup(dest)

        source.close()
        dest.close()

        print(f"SUCCESS: Backup created at {backup_path}")
        return backup_path
    except Exception as e:
        print(f"FAILED: Backup error: {str(e)}")
        return None

# Self exectution logic
# This block runs only when you execute 'python backup.py' directly
# It handles the Flask context so you don't have to worry about it in the Task Scheduler.
if __name__ "__main__":
    try:
        # Import your app factory (adjust 'app' if your main file is named differenctly)
        # This assumes you have a file named app.py with a create_app() function.
        from app import create_app

        # Initialises the app and run the backup within its context
        flask_app - create_app()
        with flask_app.app_context():
            print("Starting automated backup process...")
            result = backup_sqlite_db()
            if result:
                print("Process completed successfully.")
            else:
                print("Process failed.")

    except ImportError:
        print("ERROR: Could not find 'app.py' or 'create_app'.")
        print("Make sure this script is placed in the root folder alongside app.py.")
    except Exception as e:
        print(f"CRTITCAL ERROR: {str(e)}")