import logging
import smtplib
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from pathlib import Path
from typing import Any, Dict, List, Optional, Union

import jinja2
from fastapi import BackgroundTasks
from pydantic import EmailStr

from app import settings

logger = logging.getLogger(__name__)


class EmailService:
    def __init__(self):
        self.smtp_server = settings.SMTP_SERVER
        self.smtp_port = settings.SMTP_PORT
        self.username = settings.SMTP_USERNAME
        self.password = settings.SMTP_PASSWORD
        self.default_sender = settings.DEFAULT_SENDER
        self.templates_dir = settings.EMAIL_TEMPLATES_DIR

        # Setup templates environment
        self.template_env = jinja2.Environment(
            loader=jinja2.FileSystemLoader(self.templates_dir)
        )

    def _send_email(
        self,
        to_emails: List[EmailStr],
        subject: str,
        body: str,
        cc: Optional[List[EmailStr]] = None,
        bcc: Optional[List[EmailStr]] = None,
        html_content: Optional[str] = None,
        attachments: Optional[List[Dict[str, Any]]] = None,
        sender: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Core method to send emails.

        Args:
            to_emails: List of recipient email addresses
            subject: Email subject
            body: Plain text email body
            cc: Optional list of CC recipients
            bcc: Optional list of BCC recipients
            html_content: Optional HTML content
            attachments: Optional list of attachments [{"file_path": "/path/to/file.pdf", "filename": "report.pdf"}]
            sender: Optional sender email (falls back to default if not provided)

        Returns:
            Dict with status and message
        """
        try:
            # Create message container
            msg = MIMEMultipart("alternative")
            msg["Subject"] = subject
            msg["From"] = sender or self.default_sender
            msg["To"] = ", ".join(to_emails)

            if cc:
                msg["Cc"] = ", ".join(cc)

            # Plain text body
            plain_part = MIMEText(body, "plain")
            msg.attach(plain_part)

            # HTML body (if provided)
            if html_content:
                html_part = MIMEText(html_content, "html")
                msg.attach(html_part)

            # Add attachments if provided
            if attachments:
                for attachment in attachments:
                    file_path = attachment["file_path"]
                    filename = attachment.get("filename", Path(file_path).name)

                    with open(file_path, "rb") as file:
                        part = MIMEApplication(file.read(), Name=filename)

                    # Add header to attachment
                    part["Content-Disposition"] = f'attachment; filename="{filename}"'
                    msg.attach(part)

            # Calculate all recipients for sending
            all_recipients = to_emails.copy()
            if cc:
                all_recipients.extend(cc)
            if bcc:
                all_recipients.extend(bcc)

            # Send the email
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.username, self.password)
                server.sendmail(self.default_sender, all_recipients, msg.as_string())

            logger.info(f"Email sent successfully to {len(all_recipients)} recipients.")
            return {
                "status": "success",
                "message": f"Email sent successfully to {len(all_recipients)} recipients.",
            }

        except Exception as e:
            error_msg = f"Error sending email: {str(e)}"
            logger.error(error_msg)
            return {"status": "error", "message": error_msg}

    def send_email(
        self,
        background_tasks: BackgroundTasks,
        to_emails: Union[EmailStr, List[EmailStr]],
        subject: str,
        body: str,
        cc: Optional[List[EmailStr]] = None,
        bcc: Optional[List[EmailStr]] = None,
        html_content: Optional[str] = None,
        attachments: Optional[List[Dict[str, Any]]] = None,
        sender: Optional[str] = None,
    ) -> Dict[str, str]:
        """
        Queue an email to be sent in the background.

        Args:
            background_tasks: FastAPI BackgroundTasks
            to_emails: Single email or list of recipient email addresses
            subject: Email subject
            body: Plain text email body
            cc: Optional list of CC recipients
            bcc: Optional list of BCC recipients
            html_content: Optional HTML content
            attachments: Optional list of attachments
            sender: Optional sender email

        Returns:
            Dict with status message
        """
        # Convert single email to list if needed
        if isinstance(to_emails, str):
            to_emails = [to_emails]

        # Add email sending to background tasks
        background_tasks.add_task(
            self._send_email,
            to_emails=to_emails,
            subject=subject,
            body=body,
            cc=cc,
            bcc=bcc,
            html_content=html_content,
            attachments=attachments,
            sender=sender,
        )

        return {"message": "Email queued to be sent in the background"}

    def send_template_email(
        self,
        background_tasks: BackgroundTasks,
        to_emails: Union[EmailStr, List[EmailStr]],
        template_name: str,
        subject: str,
        template_data: Dict[str, Any],
        cc: Optional[List[EmailStr]] = None,
        bcc: Optional[List[EmailStr]] = None,
        attachments: Optional[List[Dict[str, Any]]] = None,
        sender: Optional[str] = None,
    ) -> Dict[str, str]:
        """
        Send an email using a template.

        Args:
            background_tasks: FastAPI BackgroundTasks
            to_emails: Single email or list of recipient email addresses
            template_name: Name of the template file (e.g., "welcome.html")
            subject: Email subject
            template_data: Data to be passed to the template
            cc: Optional list of CC recipients
            bcc: Optional list of BCC recipients
            attachments: Optional list of attachments
            sender: Optional sender email

        Returns:
            Dict with status message
        """
        try:
            # Load and render the template
            template = self.template_env.get_template(template_name)
            html_content = template.render(**template_data)

            # Generate plain text version from HTML
            # This is a simple approach - in production you might use a proper HTML-to-text converter
            body = template_data.get(
                "plain_text", "Please view this email in an HTML-capable client."
            )

            return self.send_email(
                background_tasks=background_tasks,
                to_emails=to_emails,
                subject=subject,
                body=body,
                cc=cc,
                bcc=bcc,
                html_content=html_content,
                attachments=attachments,
                sender=sender,
            )

        except jinja2.exceptions.TemplateError as e:
            error_msg = f"Template error: {str(e)}"
            logger.error(error_msg)
            return {"status": "error", "message": error_msg}
