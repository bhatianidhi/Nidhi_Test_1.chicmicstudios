import copy
from abc import ABC, abstractmethod

class BaseProcessor(ABC):
    """Abstract base class for processors."""
    
    def __init__(self, name: str):
        self.name = name
    
    @abstractmethod
    def process(self, data=None):
        """Subclasses must implement process method."""
        pass
    
    def __str__(self):
        return f"Processor: {self.name}"
    
    def __len__(self):
        return 0

class LogFile(BaseProcessor):
    """Processor for reading and parsing plain text log files."""
    
    def __init__(self, filename: str):
        super().__init__("LogFileProcessor")
        self.filename = filename
        self.records = [] 
        self.parsed_records = []  
    
    def load_file(self):
        """Load non-empty log lines from a file safely."""
        try:
            with open(self.filename, "r", encoding="utf-8") as f:
                self.records = [line.strip() for line in f if line.strip()]
            print(f"{len(self.records)} records loaded from '{self.filename}'")
        except FileNotFoundError:
            print(f"File '{self.filename}' not found.")
            self.records = []
        except (PermissionError, UnicodeDecodeError) as e:
            print(f"Error reading '{self.filename}': {e}")
            self.records = []
    
    def parse_records(self):
        """Parse plain text log records (space-separated fields)."""
        parsed = []
        for record in self.records:
            try:
                fields = record.split()
                parsed.append(fields)
            except Exception as e:
                print(f"Skipping malformed line '{record}': {e}")
        self.parsed_records = parsed
        return parsed
    
    def __len__(self):
        return len(self.records)
    
    def __str__(self):
        return f"LogFile({self.filename}) with {len(self.records)} records"
    
    def process(self, data=None):
        """Load and parse the file."""
        self.load_file()
        return self.parse_records()

class UserAnalytics(BaseProcessor):
    """Processor for analyzing user log data."""
    
    def __init__(self, data, report_filename="user_report.txt"):
        super().__init__("UserAnalyticsProcessor")
        self.data = data
        self.report_filename = report_filename
    
    def calculate_stats(self):
        """Count how many actions each user performed."""
        stats = {}
        for record in self.data:
            if record and len(record) > 0:  # Defensive check
                user = record[0]
                stats[user] = stats.get(user, 0) + 1
            else:
                print(f"Skipping malformed record: {record}")
        return stats
    
    def generate_report(self):
        """Generate report and save to file safely."""
        stats = self.calculate_stats()
        lines = ["User Activity Report:\n"]
        for user, count in stats.items():
            lines.append(f"{user}: {count} actions\n")
        
        try:
            with open(self.report_filename, "w", encoding="utf-8") as f:
                f.writelines(lines)
            print(f"Report saved to '{self.report_filename}'")
        except IOError as e:
            print(f"Failed to write report: {e}")
    
    def __len__(self):
        return len(self.data)
    
    def __str__(self):
        return f"UserAnalytics with {len(self.data)} records"
    
    def process(self, data=None):
        """Generate report from data."""
        self.generate_report()

if __name__ == "__main__":
    log_filename = input("Enter the log filename (e.g., logs.txt): ").strip()


    logfile = LogFile(log_filename)
    parsed_data = logfile.process()

    print("\nOriginal parsed data:", parsed_data)

    shallow_copy_data = copy.copy(parsed_data)
    deep_copy_data = copy.deepcopy(parsed_data)

    if shallow_copy_data and len(shallow_copy_data[0]) > 1:
        shallow_copy_data[0][1] = "modified"
    if deep_copy_data and len(deep_copy_data) > 1 and len(deep_copy_data[1]) > 1:
        deep_copy_data[1][1] = "changed"

    print("\nAfter modifying shallow copy:")
    print("Original parsed data:", parsed_data)
    print("Shallow copy:", shallow_copy_data)

    print("\nAfter modifying deep copy:")
    print("Original parsed data:", parsed_data)
    print("Deep copy:", deep_copy_data)

    if parsed_data:  
        analytics = UserAnalytics(parsed_data, report_filename="user_activity_report.txt")
        print("\nAnalytics object:", analytics)
        print("Number of records:", len(analytics))
        analytics.process()  
    else:
        print("\nNo data available for analytics.")
