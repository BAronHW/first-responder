# =====================================================================================
# This script sets up the Discord webhook to send job postings to your Discord channel.
# =====================================================================================

import os
import time
import requests
from dotenv import load_dotenv

load_dotenv()

DISCORD_WEBHOOK = os.getenv("DISCORD_WEBHOOK")


def notify(job_list: list) -> None:

    print(f"[DEBUG] notify received {len(job_list)} jobs.")

    for job in job_list:
        requests.post(
            DISCORD_WEBHOOK,
            json={
                "embeds": [
                    {
                        "title": f"{job['company']}",
                        "description": f"[{job['title']}]({job['link']})",
                    }
                ]
            },
        )
        time.sleep(0.4)

    print("[NOTIFICATION] Sent new jobs to Discord.")
