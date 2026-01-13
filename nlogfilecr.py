import logging

logging.basicConfig(
    filename="ni.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

logging.info("Application started")
logging.info("User 'Nidhi' logged in")
logging.warning("Disk space low on server 'MainDB'")
logging.error("User 'Hema' failed to save file")
logging.info("User 'Nidhi' uploaded 'report.pdf'")
logging.warning("Memory usage high for application 'AnalyticsApp'")
logging.critical("MainDB server is unreachable")
logging.critical("AnalyticsApp crashed due to memory overflow")
logging.info("Scheduled backup completed")
logging.error("Database connection timeout for 'MainDB'")
logging.info("User 'Nikki' logged out")
logging.info("Application shutdown")