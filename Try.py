from twilio.rest import Client

# Your Account SID and Auth Token from twilio.com/console
account_sid = "ACxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"  # Replace with your Account SID
auth_token = "your_auth_token"  # Replace with your Auth Token

client = Client(account_sid, auth_token)

message = client.messages.create(
    to="+1234567890",  # Recipient's phone number (E.164 format)
    from_="+1987654321",  # Your Twilio phone number (E.164 format)
    body="Hello from Python!",
)

print(f"Message SID: {message.sid}")