import time
from config import POLL_INTERVAL
from gmail_listener import check_all_accounts
from whatsapp_alert import send_whatsapp


def start_monitoring():
    print(" Monitoring Multiple Gmail Accounts...\n")

    while True:
        try:
            alerts = check_all_accounts()

            for mail in alerts:
                message = (
                    " Multi-Account Alert\n"
                    f"Account: {mail['account']}\n"
                    f"From: {mail['sender']}\n"
                    f"Subject: {mail['subject']}"
                )
                send_whatsapp(message)
                print("Received New Email Alert in whatsapp..!")

            time.sleep(POLL_INTERVAL)

        except KeyboardInterrupt:
            print("\n🛑 Monitoring stopped.")
            break

        except Exception as e:
            print("Error:", e)
            time.sleep(POLL_INTERVAL)


if __name__ == "__main__":
    start_monitoring()