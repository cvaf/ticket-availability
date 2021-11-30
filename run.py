from src import Ticket, create_email, send_email

SENDER = "cvaf.dev@gmail.com"
TO = "costasvaf@gmail.com" 

if __name__ == "__main__":
    t = Ticket()
    available_dates = t.check_availability()
    if available_dates:
        body = create_email(
            sender=SENDER, 
            to=TO, 
            subject="Available infinity rooms tickets found.",
            message=" ".join(available_dates),
        )
        send_email(sender=SENDER, body=body)