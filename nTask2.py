import logging
import sys

logging.basicConfig(level=logging.WARNING, format="%(levelname)s: %(message)s")

ALL_LEVELS = ["INFO", "WARNING", "ERROR", "CRITICAL"]
FLAGS = {"INFO": 1, "WARNING": 2, "ERROR": 4, "CRITICAL": 8}
IMPORTANT_MASK = FLAGS["WARNING"] | FLAGS["ERROR"] | FLAGS["CRITICAL"]

def parse_line(line):
    """
    Parse a single log line in the format 'time - level - message'.
    Returns dict with 'time', 'level', 'msg', 'flags', or None if malformed.
    Logs a warning for malformed lines or unknown levels.
    """
    line = line.strip()
    if not line:
        return None

    parts = line.split(" - ", 2)
    if len(parts) != 3:
        logging.warning("Malformed line skipped: %s", line)
        return None

    time, level, msg = (p.strip() for p in parts)
    level_upper = level.upper()

    if level_upper not in FLAGS:
        logging.warning("Unknown log level '%s' in line: %s", level, line)

    return {
        "time": time,
        "level": level_upper,
        "msg": msg,
        "flags": FLAGS.get(level_upper, 0)
    }


def parse_logs(filename):
    """
    Parse log file.
    Returns: logs_list, level_counts, malformed_count
    Raises FileNotFoundError or OSError on file errors.
    """
    logs = []
    l_counts = {lvl: 0 for lvl in ALL_LEVELS}
    malformed_lines = 0

    with open(filename, "r", encoding="utf-8") as f:
        for line in f:
            if not line.strip():
                continue

            record = parse_line(line)
            if not record:
                malformed_lines += 1
                continue

            logs.append(record)
            if record["level"] in l_counts:
                l_counts[record["level"]] += 1

    return logs, l_counts, malformed_lines


def main(filename=None):
    """
    Main entry point.
    Returns exit code: 0=success, 1=empty filename, 2=file not found, 3=other file error
    """
    if filename is None:
        filename = input("Enter log file name: ").strip()

    if not filename:
        print("Error: empty filename", file=sys.stderr)
        return 1

    try:
        logs, l_counts, malformed_lines = parse_logs(filename)
    except FileNotFoundError:
        print(f"Error: file not found: {filename}", file=sys.stderr)
        return 2
    except OSError as e:
        print(f"Error reading file {filename}: {e}", file=sys.stderr)
        return 3

    print("\nLog Summary")
    for level in ALL_LEVELS:
        print(f"{level}: {l_counts.get(level, 0)}")

    print("\nImportant logs (WARNING, ERROR, CRITICAL):")
    for log in logs:
        if log.get("flags", 0) & IMPORTANT_MASK:
            print(f"{log['time']} - {log['level']} - {log['msg']}")

    print("\nAll ERROR messages:")
    for log in logs:
        if log["level"] == "ERROR" and log["msg"]:
            print(f"- {log['msg']}")

    print(f"\nTotal logs stored in list: {len(logs)}")
    print(f"Malformed lines skipped: {malformed_lines}")

    return 0


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
