import logging
from datetime import datetime, timedelta
import time
import sys

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s", handlers=[logging.StreamHandler(sys.stdout)])

TIM = 6*60*60
exit_after_seconds = TIM  # Set the duration for how long the loop should run
end_time = datetime.now() + timedelta(seconds=exit_after_seconds)

logging.info(f"Starting loop for {TIM} minutes period.")

while datetime.now() < end_time:
    logging.info(f"Currently waiting for job : {datetime.now()}")
    time.sleep(10)

logging.info(f"Exiting loop after {TIM/60} minutes period.")
