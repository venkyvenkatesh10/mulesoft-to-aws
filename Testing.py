import json
import time
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import os

# Configurations
destination_file = r"C:\Users\venka\Desktop\Mulesoft To AWS\AWS\complex_Sample_apis_160.json"
log_file_path = r"C:\Users\venka\Desktop\Mulesoft To AWS\migration_log.json"
html_report_path = r"C:\Users\venka\Desktop\Mulesoft To AWS\migration_selenium_test_report.html"

# Load migration ID from log
with open(log_file_path, "r") as f:
    log_data = json.load(f)
    expected_migration_id = log_data["migration_id"]

# Load migrated data
with open(destination_file, "r") as f:
    data = json.load(f)

# Start test
test_start = time.time()
results = []
pass_count = 0
fail_count = 0

for idx, record in enumerate(data, 1):
    actual_id = record.get("migration_id", "None")
    status = "PASS" if actual_id == expected_migration_id else "FAIL"
    if status == "PASS":
        pass_count += 1
    else:
        fail_count += 1
    results.append({
        "index": idx,
        "id": record.get("id"),
        "migration_id": actual_id,
        "status": status
    })

# Test summary
test_end = time.time()
duration = round(test_end - test_start, 2)
overall_status = "PASS" if fail_count == 0 else "FAIL"

# HTML report generation
html_content = f"""
<html>
<head>
    <title>Migration Test Report</title>
    <style>
        body {{ font-family: Arial, sans-serif; }}
        table {{ border-collapse: collapse; width: 90%; margin: 20px auto; }}
        th, td {{ border: 1px solid #ccc; padding: 8px; text-align: center; }}
        th {{ background-color: #f2f2f2; }}
        .PASS {{ background-color: #d4edda; }}
        .FAIL {{ background-color: #f8d7da; }}
    </style>
</head>
<body>
    <h1 style="text-align:center;">🧪 Migration Validation Report (Selenium Assisted)</h1>
    <h3 style="text-align:center;">Status: <span style="color:{'green' if overall_status == 'PASS' else 'red'}">{overall_status}</span></h3>
    <h4 style="text-align:center;">Total: {len(data)} | Passed: {pass_count} | Failed: {fail_count} | Duration: {duration}s</h4>
    <table>
        <tr><th>#</th><th>API ID</th><th>Migration ID</th><th>Status</th></tr>
"""

for result in results:
    html_content += f"<tr class='{result['status']}'><td>{result['index']}</td><td>{result['id']}</td><td>{result['migration_id']}</td><td>{result['status']}</td></tr>"

html_content += """
    </table>
</body>
</html>
"""

with open(html_report_path, "w", encoding="utf-8") as report_file:
    report_file.write(html_content)

print(f"✅ HTML report generated at:\n{html_report_path}")
