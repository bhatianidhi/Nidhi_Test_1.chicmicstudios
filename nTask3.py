def write_error_log(message):
    try:
        with open("logs_errors.log", "a") as err_file:
            err_file.write(message + "\n")
    except Exception:
        print("Failed to write to error log.")


def read_logs(filename):
    logs = []
    counts = {"INFO": 0, "WARNING": 0, "ERROR": 0}

    try:
        f = open(filename, "r")
        for line_no, line in enumerate(f, start=1):
            line = line.strip()
            if not line:
                continue

            parts = line.split(" - ")
            if len(parts) != 3:
                write_error_log(
                    f"Line {line_no}: Invalid format -> {line}"
                )
                continue

            time, level, msg = parts

            if level not in counts:
                write_error_log(
                    f"Line {line_no}: Unknown log level -> {level}"
                )
                continue

            logs.append({"time": time, "level": level, "msg": msg})
            counts[level] += 1

        f.close()

        if not logs:
            write_error_log("No valid log entries found.")
            print("Log file is empty or invalid.")
            return None, None

    except FileNotFoundError as e:
        write_error_log(str(e))
        print("File not found.")
        return None, None

    except PermissionError as e:
        write_error_log(str(e))
        print("Permission denied.")
        return None, None

    except Exception as e:
        write_error_log(str(e))
        print("unexpected error occurred.")
        return None, None

    return logs, counts


def display_summary(counts):
    print("\nLog summary:")
    for level, count in counts.items():
        print(f"{level}: {count}")


def display_important_logs(logs):
    flags = {"INFO": 1, "WARNING": 2, "ERROR": 4}
    important_mask = flags["WARNING"] | flags["ERROR"]

    print("\nImportant logs (WARNING or ERROR):")
    for log in logs:
        if flags[log["level"]] & important_mask:
            print(f"{log['time']} - {log['level']} - {log['msg']}")


def display_error_messages(logs):
    print("\nAll ERROR messages:")
    for log in logs:
        if log["level"] == "ERROR" and log["msg"]:
            print("-", log["msg"])


def main():
    write_error_log("---- Error log started ----")

    log_file = input("Enter log file name: ")
    logs, counts = read_logs(log_file)
    if logs is None or counts is None:
        return

    display_summary(counts)
    display_important_logs(logs)
    display_error_messages(logs)
    print(f"\nTotal logs stored in memory: {len(logs)}")


if __name__ == "__main__":
    main()
