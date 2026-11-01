import imaplib
import email
from email.header import decode_header
from config import EMAIL_ACCOUNTS

# Store last UID for each account
last_seen_uids = {}

# 🔎 Subject Filter Keywords
SUBJECT_KEYWORDS = ["otp", "bank", "srec", "security","internships"]

def safe_decode(value):
    if value is None:
        return ""
    decoded, encoding = decode_header(value)[0]
    if isinstance(decoded, bytes):
        return decoded.decode("utf-8", errors="ignore")
    return decoded


def subject_matches(subject):
    subject = subject.lower()
    return any(keyword in subject for keyword in SUBJECT_KEYWORDS)


def check_account(email_id, password):
    global last_seen_uids
    alerts = []

    mail = imaplib.IMAP4_SSL("imap.gmail.com")
    mail.login(email_id, password)
    mail.select("inbox")

    status, messages = mail.search(None, "ALL")
    mail_ids = messages[0].split()

    if not mail_ids:
        mail.logout()
        return alerts

    latest_uid = mail_ids[-1]

    # First run: initialize
    if email_id not in last_seen_uids:
        last_seen_uids[email_id] = latest_uid
        mail.logout()
        return alerts

    if latest_uid == last_seen_uids[email_id]:
        mail.logout()
        return alerts

    new_ids = mail_ids[mail_ids.index(last_seen_uids[email_id]) + 1:]

    for i in new_ids:
        status, msg_data = mail.fetch(i, "(RFC822)")
        for response in msg_data:
            if isinstance(response, tuple):
                msg = email.message_from_bytes(response[1])

                subject = safe_decode(msg.get("Subject"))
                sender = safe_decode(msg.get("From"))

                # 🔥 Filter by subject keywords
                if subject_matches(subject):
                    alerts.append({
                        "account": email_id,
                        "sender": sender,
                        "subject": subject
                    })

    last_seen_uids[email_id] = latest_uid
    mail.logout()
    return alerts


def check_all_accounts():
    all_alerts = []

    for account in EMAIL_ACCOUNTS:
        alerts = check_account(account["email"], account["password"])
        all_alerts.extend(alerts)

    return all_alerts