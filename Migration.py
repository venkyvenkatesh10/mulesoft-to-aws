import os
import shutil
import json
import time
from datetime import datetime

# Paths
source_path = r"C:\Users\venka\Desktop\Mulesoft To AWS\Mulesoft\complex_Sample_apis_160.json"
backup_path = r"C:\Users\venka\Desktop\Mulesoft To AWS\Mulesoft\backup_complex_Sample_apis_160.json"
destination_path = r"C:\Users\venka\Desktop\Mulesoft To AWS\AWS\complex_Sample_apis_160.json"
log_path = r"C:\Users\venka\Desktop\Mulesoft To AWS\migration_log.json"

# Retry configuration
MAX_RETRIES = 3
RETRY_DELAY = 0.5  # seconds

# Start timer
start_time = time.time()
migration_id = str(int(start_time))
migration_log = {
    "migration_id": migration_id,
    "start_time": datetime.now().isoformat(),
    "source_file": source_path,
    "destination_file": destination_path,
    "backup_created": False,
    "total_records": 0,
    "successful_migrations": 0,
    "failed_migrations": 0,
    "record_logs": [],
    "errors": [],
    "status": "Started",
    "end_time": None,
    "duration_seconds": None
}

try:
    # Backup
    shutil.copy2(source_path, backup_path)
    migration_log["backup_created"] = True
    print(f"📁 Backup created at: {backup_path}")

    # Load data
    with open(source_path, "r") as src_file:
        data = json.load(src_file)

    migrated_data = []
    print(f"\n🚀 Starting migration of {len(data)} API records...\n")

    for idx, record in enumerate(data, 1):
        record_log = {
            "api_id": record.get("id", "unknown"),
            "status": "Started",
            "start_time": datetime.now().isoformat(),
            "end_time": None,
            "duration_seconds": None,
            "attempts": 0,
            "error": None
        }

        record_start = time.time()
        success = False

        for attempt in range(1, MAX_RETRIES + 1):
            record_log["attempts"] = attempt
            try:
                record["migration_id"] = migration_id
                migrated_data.append(record)
                record_log["status"] = "Success"
                migration_log["successful_migrations"] += 1
                success = True
                print(f"✅ [{idx}] API ID {record['id']} migrated (Attempt {attempt})")
                break
            except Exception as e:
                record_log["error"] = str(e)
                print(f"⚠️ [{idx}] API ID {record.get('id', 'unknown')} failed (Attempt {attempt}) - {e}")
                time.sleep(RETRY_DELAY)

        if not success:
            record_log["status"] = "Failed"
            migration_log["failed_migrations"] += 1
            print(f"❌ [{idx}] API ID {record.get('id', 'unknown')} failed after {MAX_RETRIES} retries.")

        record_log["end_time"] = datetime.now().isoformat()
        record_log["duration_seconds"] = round(time.time() - record_start, 3)
        migration_log["record_logs"].append(record_log)

    migration_log["total_records"] = len(data)

    # Save to destination
    with open(destination_path, "w") as dest_file:
        json.dump(migrated_data, dest_file, indent=4)

    migration_log["status"] = "Success" if migration_log["failed_migrations"] == 0 else "Partial Success"

except Exception as e:
    migration_log["status"] = "Failed"
    migration_log["errors"].append(str(e))
    print(f"\n❌ Migration failed with error: {e}")

# Final log
migration_log["end_time"] = datetime.now().isoformat()
migration_log["duration_seconds"] = round(time.time() - start_time, 2)

# Write log file
with open(log_path, "w") as log_file:
    json.dump(migration_log, log_file, indent=4)

# Summary
print(f"\n Migration Summary:")
print(f"  → Status               : {migration_log['status']}")
print(f"  → Total APIs           : {migration_log['total_records']}")
print(f"  → Successful Migrations: {migration_log['successful_migrations']}")
print(f"  → Failed Migrations    : {migration_log['failed_migrations']}")
print(f"  → Time Taken           : {migration_log['duration_seconds']} seconds")
print(f"  → Log File             : {log_path}")
