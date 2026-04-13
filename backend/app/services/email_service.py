import smtplib
from email.message import EmailMessage

from app.core.config import settings
from app.models.complaint import Complaint


class EmailService:
    @staticmethod
    def _send_message(message: EmailMessage) -> None:
        with smtplib.SMTP(settings.SMTP_HOST, settings.SMTP_PORT) as server:
            server.starttls()
            server.login(settings.SMTP_USERNAME, settings.SMTP_PASSWORD)
            server.send_message(message)

    @staticmethod
    def send_complaint_to_support(complaint: Complaint) -> None:
        msg = EmailMessage()
        msg["Subject"] = f"Нова скарга #{complaint.id}"
        msg["From"] = settings.SMTP_FROM_EMAIL
        msg["To"] = settings.SUPPORT_EMAIL

        body = (
            f"Надійшла нова скарга.\n\n"
            f"ID скарги: {complaint.id}\n"
            f"Клієнт: {complaint.full_name}\n"
            f"Email: {complaint.email}\n"
            f"Номер замовлення: {complaint.order_number or 'не вказано'}\n"
            f"Статус: {complaint.status}\n\n"
            f"Текст скарги:\n{complaint.message}\n"
        )

        msg.set_content(body)

        for attachment in complaint.attachments:
            msg.add_attachment(
                attachment.file_content,
                maintype="image",
                subtype=attachment.mime_type.split("/")[-1],
                filename=attachment.file_name,
            )

        EmailService._send_message(msg)

    @staticmethod
    def send_complaint_confirmation_to_client(complaint: Complaint) -> None:
        msg = EmailMessage()
        msg["Subject"] = "Ми отримали вашу скаргу"
        msg["From"] = settings.SMTP_FROM_EMAIL
        msg["To"] = complaint.email

        body = (
            f"Вітаємо, {complaint.full_name}!\n\n"
            f"Ми отримали вашу скаргу та вже працюємо над її розглядом.\nОрієнтовний час відповіді: 2-3 робочі дні\n\n"
            f"Дані звернення:\n"
            f"ID скарги: {complaint.id}\n"
            f"Номер замовлення: {complaint.order_number or 'не вказано'}\n\n"
            f"Текст скарги:\n{complaint.message}\n\n"
            f"Дякуємо за звернення.\n"
            f"Команда Funko Hunter"
        )

        msg.set_content(body)

        EmailService._send_message(msg)