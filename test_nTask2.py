import pytest
import tempfile
import os
from nTask2 import parse_line, parse_logs, FLAGS, IMPORTANT_MASK

def test_parse_line_normal():
    line = "2026-01-14 10:00 - INFO - Started process"
    result = parse_line(line)
    assert result["level"] == "INFO"
    assert result["flags"] == FLAGS["INFO"]
    assert result["msg"] == "Started process"

def test_parse_line_malformed():
    line = "2026-01-14 10:00 INFO Started process"
    assert parse_line(line) is None

def test_parse_line_unknown_level():
    line = "2026-01-14 10:00 - NOTICE - Something happened"
    result = parse_line(line)
    assert result["flags"] == 0
    assert result["level"] == "NOTICE"

def test_parse_line_dashes_in_msg():
    line = "2026-01-14 10:00 - ERROR - Failed to open file - permission denied"
    result = parse_line(line)
    assert result["msg"] == "Failed to open file - permission denied"

def test_parse_logs_blank_and_malformed():
    content = "\n2026-01-14 10:00 - WARNING - Disk full\nbad line\n"
    with tempfile.NamedTemporaryFile(mode="w+", delete=False) as f:
        f.write(content)
        fname = f.name
    logs, counts, malformed = parse_logs(fname)
    os.unlink(fname)
    assert len(logs) == 1
    assert counts["WARNING"] == 1
    assert malformed == 1

def test_important_mask():
    logs = [
        {"level": "INFO", "flags": FLAGS["INFO"]},
        {"level": "WARNING", "flags": FLAGS["WARNING"]},
        {"level": "ERROR", "flags": FLAGS["ERROR"]},
        {"level": "CRITICAL", "flags": FLAGS["CRITICAL"]}
    ]
    important = [log for log in logs if log["flags"] & IMPORTANT_MASK]
    assert len(important) == 3
    assert all(l["level"] != "INFO" for l in important)
