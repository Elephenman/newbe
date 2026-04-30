#!/usr/bin/env python3
"""Experiment time tracking + duration statistics + efficiency report"""

import os
import sys
import json
from datetime import datetime, timedelta


def get_input(prompt, default="", dtype=str):
    val = input(prompt + (" [" + str(default) + "]" if default else "") + ": ")
    if not val.strip():
        return default
    return dtype(val)


def load_log(log_file):
    """Load experiment log from JSON file."""
    if os.path.exists(log_file):
        with open(log_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {"experiments": []}


def save_log(log_file, data):
    """Save experiment log to JSON file."""
    with open(log_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def start_experiment(log_file, name, category=""):
    """Start timing an experiment."""
    data = load_log(log_file)
    entry = {
        "name": name,
        "category": category,
        "start_time": datetime.now().isoformat(),
        "end_time": None,
        "duration_minutes": None,
        "status": "running",
    }
    data["experiments"].append(entry)
    save_log(log_file, data)
    return entry


def stop_experiment(log_file, name=None):
    """Stop timing the most recent running experiment (or by name)."""
    data = load_log(log_file)
    now = datetime.now()

    # Find running experiment
    target = None
    for entry in reversed(data["experiments"]):
        if entry["status"] == "running":
            if name is None or entry["name"] == name:
                target = entry
                break

    if target is None:
        print("[ERROR] No running experiment found")
        return None

    target["end_time"] = now.isoformat()
    start = datetime.fromisoformat(target["start_time"])
    duration = (now - start).total_seconds() / 60
    target["duration_minutes"] = round(duration, 2)
    target["status"] = "completed"
    save_log(log_file, data)
    return target


def generate_report(log_file, output_file):
    """Generate efficiency report from experiment log."""
    data = load_log(log_file)
    experiments = data["experiments"]

    if not experiments:
        print("[WARN] No experiments recorded yet")
        return

    completed = [e for e in experiments if e["status"] == "completed"]
    running = [e for e in experiments if e["status"] == "running"]

    # Category-wise statistics
    category_stats = {}
    for e in completed:
        cat = e.get("category", "uncategorized")
        if cat not in category_stats:
            category_stats[cat] = {"count": 0, "total_minutes": 0, "durations": []}
        category_stats[cat]["count"] += 1
        category_stats[cat]["total_minutes"] += e["duration_minutes"]
        category_stats[cat]["durations"].append(e["duration_minutes"])

    # Write report
    with open(output_file, "w", encoding='utf-8') as out:
        out.write("=== Experiment Time Report ===\n\n")
        out.write(f"Total experiments: {len(experiments)}\n")
        out.write(f"Completed: {len(completed)}\n")
        out.write(f"Running: {len(running)}\n\n")

        if completed:
            total_time = sum(e["duration_minutes"] for e in completed)
            avg_time = total_time / len(completed)
            out.write(f"Total time: {total_time:.1f} minutes ({total_time/60:.1f} hours)\n")
            out.write(f"Average per experiment: {avg_time:.1f} minutes\n\n")

        out.write("=== By Category ===\n")
        for cat, stats in sorted(category_stats.items()):
            out.write(f"\n{cat}:\n")
            out.write(f"  Count: {stats['count']}\n")
            out.write(f"  Total: {stats['total_minutes']:.1f} min ({stats['total_minutes']/60:.1f} hrs)\n")
            avg = stats['total_minutes'] / stats['count']
            out.write(f"  Average: {avg:.1f} min\n")

        out.write("\n=== Experiment Details ===\n")
        for e in experiments:
            status_icon = "[DONE]" if e["status"] == "completed" else "[RUNNING]"
            dur = f"{e['duration_minutes']:.1f} min" if e['duration_minutes'] else "ongoing"
            out.write(f"  {status_icon} {e['name']} ({e.get('category', '')}): {dur}\n")
            out.write(f"         Start: {e['start_time']}\n")
            if e['end_time']:
                out.write(f"         End: {e['end_time']}\n")

    return {
        "total": len(experiments),
        "completed": len(completed),
        "running": len(running),
    }


def main():
    print("=" * 60)
    print("  Experiment Time Tracker + Efficiency Report")
    print("=" * 60)
    print()

    log_file = get_input("Log file path", "experiment_log.json")

    print("\nActions:")
    print("  1. Start new experiment")
    print("  2. Stop running experiment")
    print("  3. Generate report")
    print()

    action = get_input("Choose action (1/2/3)", "3")

    if action == "1":
        name = get_input("Experiment name", "experiment_1")
        category = get_input("Category (e.g., wet_lab/bioinfo/analysis)", "")
        entry = start_experiment(log_file, name, category)
        print(f"[OK] Started: {entry['name']} at {entry['start_time']}")

    elif action == "2":
        name = get_input("Experiment name (empty=latest running)", "")
        entry = stop_experiment(log_file, name or None)
        if entry:
            print(f"[OK] Stopped: {entry['name']} - {entry['duration_minutes']} min")

    elif action == "3":
        output_file = get_input("Output report path", "experiment_report.txt")
        stats = generate_report(log_file, output_file)
        if stats:
            print()
            print("=" * 60)
            print("  REPORT SUMMARY")
            print("=" * 60)
            print(f"  Total experiments: {stats['total']}")
            print(f"  Completed:         {stats['completed']}")
            print(f"  Running:           {stats['running']}")
            print(f"  Report saved to:   {output_file}")
            print("=" * 60)

    else:
        print("[ERROR] Invalid action")

    print()
    print("[Done] Experiment timer tracker completed!")


if __name__ == "__main__":
    main()
