from fastapi_mail import MessageSchema
from tenacity import retry, retry_if_exception_type, stop_after_attempt, wait_fixed
from utils.mail import fm  # adjust import as needed
from fastapi_mail.errors import ConnectionErrors

@retry(retry=retry_if_exception_type(ConnectionErrors),wait=wait_fixed(5), stop=stop_after_attempt(3))
async def send_due_reminder_email(to_email: str, user_name: str, type: str, provider: str):
    message = MessageSchema(
        subject=f"🔔⏳ Action Required: Your {type} subscription ends tomorrow",
        recipients=[to_email],
        body=f"""
        <div style="font-family: Arial, sans-serif; color: #333;">
        <p>Hi <strong>{user_name}</strong>,</p>
            <h2 style="color: #FF5E3A;">Heads Up!</h2>
            <p>Your <strong>{type}</strong> subscription with <strong>{provider}</strong> is set to end <strong>tomorrow</strong>.</p>

            <p>To avoid any disruption or unexpected charges, we recommend taking one of the following actions:</p>

            <ul>
                <li><strong>Renew</strong> your subscription if you'd like to continue enjoying the service.</li>
                <li><strong>Cancel</strong> it to avoid automatic billing.</li>
                <li><strong>Review</strong> the plan to explore other available options.</li>
            </ul>

            <p>Now’s the perfect time to make sure your subscription is working for you.</p>

            <p>If you’ve already handled this - Feel free to ignore this message.</p>

            <br>
            <p style="color: #999;"> - The Subnotifly Team</p>
        </div>
        """,
        subtype="html"
    )
    
    await fm.send_message(message)
