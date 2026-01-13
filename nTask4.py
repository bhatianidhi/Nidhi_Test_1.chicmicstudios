import copy

# ----------------- Base Class -----------------
class BaseProcessor:
    """Abstract base class for processors."""
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return f"Processor: {self.name}"

    def __len__(self):
        return 0  

    def process(self, data):
        raise NotImplementedError("Subclasses must implement process method")


# ----------------- LogFile Class -----------------
class LogFile(BaseProcessor): 
    """Processor for reading and parsing log files."""
    
    def __init__(self, filename):
        super().__init__("LogFileProcessor")
        self.filename = filename
        self.records = []  # mutable list of log lines

    def load_file(self):
        """Loads log lines from the file into self.records."""
        try:
            with open(self.filename, "r") as f:
                self.records = [line.strip() for line in f if line.strip()]
            print(f"{len(self.records)} records loaded from '{self.filename}'.")
        except FileNotFoundError:
            print(f"File '{self.filename}' not found.")
            self.records = []  # empty list if file not found

    def parse_records(self):
        """Split each log line by comma."""
        return [r.split(",") for r in self.records]

    def __len__(self):
        return len(self.records)

    def __str__(self):
        return f"LogFile({self.filename}) with {len(self.records)} records"


# ----------------- UserAnalytics Class -----------------
class UserAnalytics(BaseProcessor):
    """Processor for analyzing parsed user log data."""
    
    def __init__(self, data, report_filename="user_report.txt"):
        super().__init__("UserAnalyticsProcessor")
        self.data = data
        self.report_filename = report_filename  # file to save the report

    def calculate_stats(self):
        """Count how many actions each user has performed."""
        stats = {}
        for record in self.data:
            user = record[0]
            stats[user] = stats.get(user, 0) + 1
        return stats

    def generate_report(self):
        """Generate report and save it to a file automatically."""
        stats = self.calculate_stats()
        lines = ["User Activity Report:\n"]
        for user, count in stats.items():
            lines.append(f"{user}: {count} actions\n")
        
        # Save report to file
        with open(self.report_filename, "w") as f:
            f.writelines(lines)
        
        print(f"Report saved automatically to '{self.report_filename}'")

    def __len__(self):
        return len(self.data)

    def __str__(self):
        return f"UserAnalytics with {len(self.data)} records"


# ----------------- Main Program -----------------
if __name__ == "__main__":
    # ----------------- Step 1: Ask user for log filename -----------------
    log_filename = input("Enter the log filename (e.g., logs.txt): ").strip()

    # ----------------- Step 2: Load Log Data -----------------
    logfile = LogFile(log_filename)
    logfile.load_file()  # loads records from the file
    parsed_data = logfile.parse_records()

    # ----------------- Step 3: Demonstrate Shallow vs Deep Copy -----------------
    shallow_copy_data = copy.copy(parsed_data)
    deep_copy_data = copy.deepcopy(parsed_data)
    
    print("\nOriginal parsed data:", parsed_data)
    print("Shallow copy:", shallow_copy_data)
    print("Deep copy:", deep_copy_data)

    shallow_copy_data[0][1] = "modified"
    print("\nAfter modifying shallow copy:")
    print("Original parsed data:", parsed_data)
    print("Shallow copy:", shallow_copy_data)

    deep_copy_data[1][1] = "changed"
    print("\nAfter modifying deep copy:")
    print("Original parsed data:", parsed_data)
    print("Deep copy:", deep_copy_data)

    # ----------------- Step 4: Analyze Data and Save Report -----------------
    # Automatically save report in a separate file
    analytics = UserAnalytics(parsed_data, report_filename="user_activity_report.txt")
    print("\nAnalytics object:", analytics)
    print("Length of analytics:", len(analytics))
    analytics.generate_report()
