import subprocess
import os
from datetime import datetime

# Paths
api_py_mulesoft = r"C:\Users\venka\Desktop\Mulesoft To AWS\Mulesoft\API.py"
migration_py = r"C:\Users\venka\Desktop\Mulesoft To AWS\Migration.py"
testing_py = r"C:\Users\venka\Desktop\Mulesoft To AWS\Testing.py"
automation_html = r"C:\Users\venka\Desktop\Mulesoft To AWS\automation_report.html"
selenium_html = r"C:\Users\venka\Desktop\Mulesoft To AWS\migration_selenium_test_report.html"

def run_script(script_path, step_name, cwd=None):
    start = datetime.now()
    print(f"[{start.strftime('%Y-%m-%d %H:%M:%S')}] {step_name} started.")
    env = os.environ.copy()
    env["PYTHONIOENCODING"] = "utf-8"
    result = subprocess.run(
        ["python", script_path],
        capture_output=True,
        text=True,
        env=env,
        cwd=cwd,
        encoding="utf-8",
        errors="replace"
    )
    print(result.stdout)
    if result.returncode != 0:
        print(result.stderr)
        return False, start, datetime.now()
    end = datetime.now()
    print(f"[{end.strftime('%Y-%m-%d %H:%M:%S')}] {step_name} completed.")
    return True, start, end

def main():
    steps = []
    print("=== Automation Process Started ===")
    automation_start = datetime.now()

    # 1. Run API.py in Mulesoft
    ok, start, end = run_script(api_py_mulesoft, "API Generation (Mulesoft)", cwd=os.path.dirname(api_py_mulesoft))
    steps.append(("API Generation (Mulesoft)", start, end, "Success" if ok else "Failed"))
    if not ok: return

    # 2. Run Migration.py
    ok, start, end = run_script(migration_py, "Migration")
    steps.append(("Migration", start, end, "Success" if ok else "Failed"))
    if not ok: return

    # 3. Run Testing.py
    ok, start, end = run_script(testing_py, "Testing")
    steps.append(("Testing", start, end, "Success" if ok else "Failed"))
    if not ok: return

    automation_end = datetime.now()
    print("\n=== Automation Process Completed ===")
    print(f"Started: {automation_start.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Ended  : {automation_end.strftime('%Y-%m-%d %H:%M:%S')}")

    # HTML report (first image style, with color)
    with open(automation_html, "w", encoding="utf-8") as f:
        f.write(f"""<html>
<head>
    <title>Automation Process Report</title>
    <style>
        body {{ font-family: Arial, sans-serif; }}
        table {{ border-collapse: collapse; width: 60%; margin: 40px auto; }}
        th, td {{ border: 1px solid #888; padding: 10px 16px; text-align: center; font-size: 1.1em; }}
        th {{ background: #f0f0f0; font-size: 1.2em; }}
        tr:nth-child(even) {{ background: #f9f9f9; }}
        .Success {{ background-color: #d4edda; color: #155724; font-weight: bold; }}
        .Failed {{ background-color: #f8d7da; color: #721c24; font-weight: bold; }}
        h2 {{ text-align: center; }}
        .center {{ text-align: center; }}
    </style>
</head>
<body>
    <h2>Automation Process Report</h2>
    <div class="center">
        <b>Started:</b> {automation_start.strftime('%Y-%m-%d %H:%M:%S')}
        &nbsp;|&nbsp;
        <b>Ended:</b> {automation_end.strftime('%Y-%m-%d %H:%M:%S')}
    </div>
    <br>
    <table>
        <tr>
            <th>Step</th>
            <th>Start Time</th>
            <th>End Time</th>
            <th>Status</th>
        </tr>
        {''.join([f"<tr><td>{s[0]}</td><td>{s[1].strftime('%Y-%m-%d %H:%M:%S')}</td><td>{s[2].strftime('%Y-%m-%d %H:%M:%S')}</td><td class='{s[3]}'>{s[3]}</td></tr>" for s in steps])}
    </table>
    <div class="center" style="margin-top:30px;">
        <a href='migration_selenium_test_report.html' target='_blank'>View Migration Selenium Test Report</a>
    </div>
</body>
</html>
""")
    print(f"\nHTML report generated: {automation_html}")

if __name__ == "__main__":
    main()