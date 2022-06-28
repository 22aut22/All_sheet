import smtplib

from config import HOST, PASS, USER


def send_email(subject, body_text, to_addr, from_addr=USER, host=HOST, password=PASS, username=USER):
    """
    Send an email
    """

    body = f"From: {from_addr} \n" \
           f"To: {to_addr} \n" \
           f"Subject: {subject} \n\n" \
           f"{body_text}"

    server = smtplib.SMTP_SSL(host, 465)
    #server.set_debuglevel(1)
    server.ehlo(from_addr)
    server.login(username, password)
    #server.auth_plain()
    server.sendmail(from_addr, to_addr, body.encode('utf-8'))
    server.quit()


if __name__ == "__main__":
    subject = "Проверка связи из программы на Питончике"
    to_addr = "utkin@eltorg66.ru"
    body_text = "Питонище рулит по любому. Это самый крутой язычара на свете"
    send_email(subject, body_text, to_addr)
