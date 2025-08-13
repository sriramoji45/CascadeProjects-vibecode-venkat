import smtplib

smtp_server = "smtp.gmail.com"
port = 587
sender = "ctshealthcarehospital@gmail.com"
password = "fwuv vlbb dymv segg"  # Your app password

try:
    server = smtplib.SMTP(smtp_server, port)
    server.starttls()
    server.login(sender, password)
    print("Login successful!")
    server.quit()
except Exception as e:
    print("Login failed:", e)
