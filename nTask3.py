from typing import List, Dict, Tuple
from datetime import datetime

LOG_LEVELS = {"INFO", "WARNING", "ERROR"}
ERROR_LOG_FILE = "logs_errors.log"


def write_error_log(message: str, exc: Exception = None) -> None:
    """Append an error message to the error log with timestamp and optional exception message."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    try:
        with open(ERROR_LOG_FILE, "a", encoding="utf-8") as err_file:
            err_file.write(f"[{timestamp}] {message}\n")
            if exc:
                err_file.write(f"Exception: {repr(exc)}\n")
    except Exception as e:
        print(f"Failed to write to error log: {e}")


def read_logs(filename: str) -> Tuple[List[Dict[str, str]], Dict[str, int]]:
    """Read a log file and return structured log entries and counts per level."""
    logs: List[Dict[str, str]] = []
    counts: Dict[str, int] = {level: 0 for level in LOG_LEVELS}

    try:
        with open(filename, "r", encoding="utf-8") as f:
            for line_no, line in enumerate(f, start=1):
                line = line.strip()
                if not line:
                    continue

                parts = line.split(" - ", 2)
                if len(parts) != 3:
                    write_error_log(f"Line {line_no}: Invalid format -> {line}")
                    continue

                timestamp, level, msg = parts

                if level not in LOG_LEVELS:
                    write_error_log(f"Line {line_no}: Unknown log level -> {level}")
                    continue

                logs.append({"time": timestamp, "level": level, "msg": msg})
                counts[level] += 1

        if not logs:
            write_error_log("No valid log entries found.")
            print("Log file is empty or invalid.")
            return [], {level: 0 for level in LOG_LEVELS}

    except FileNotFoundError as e:
        write_error_log("File not found.", e)
        print("File not found.")
        return [], {level: 0 for level in LOG_LEVELS}

    except PermissionError as e:
        write_error_log("Permission denied.", e)
        print("Permission denied.")
        return [], {level: 0 for level in LOG_LEVELS}

    except Exception as e:
        write_error_log("Unexpected error occurred.", e)
        print("Unexpected error occurred.")
        return [], {level: 0 for level in LOG_LEVELS}

    return logs, counts


def display_summary(counts: Dict[str, int]) -> None:
    print("\nLog summary:")
    for level in sorted(LOG_LEVELS):
        print(f"{level}: {counts.get(level, 0)}")


def display_important_logs(logs: List[Dict[str, str]]) -> None:
    print("\nImportant logs (WARNING or ERROR):")
    for log in logs:
        if log["level"] in {"WARNING", "ERROR"}:
            print(f"{log['time']} - {log['level']} - {log['msg']}")


def display_error_messages(logs: List[Dict[str, str]]) -> None:
    print("\nAll ERROR messages:")
    for log in logs:
        if log["level"] == "ERROR" and log["msg"]:
            print("-", log["msg"])


def main() -> None:
    write_error_log("---- Error log started ----")

    log_file = input("Enter log file name: ")
    logs, counts = read_logs(log_file)

    if not logs:
        return

    display_summary(counts)
    display_important_logs(logs)
    display_error_messages(logs)
    print(f"\nTotal logs stored in memory: {len(logs)}")


if __name__ == "__main__":
    main()
