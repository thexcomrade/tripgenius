"""
TripGenius Email Delivery Service.
Handles sending transactional and security emails (OTP verification codes,
password resets, account notifications) via SMTP with branded HTML templates.
"""

import logging
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from app.core.config import settings

logger = logging.getLogger(__name__)


class EmailService:
    def __init__(self) -> None:
        self.host = settings.SMTP_HOST
        self.port = settings.SMTP_PORT
        self.user = settings.SMTP_USER
        self.password = settings.SMTP_PASSWORD
        self.from_email = settings.SMTP_FROM_EMAIL or self.user or "noreply@tripgenius.com"
        self.from_name = settings.SMTP_FROM_NAME or "TripGenius Security"
        self.use_tls = settings.SMTP_TLS

    def is_configured(self) -> bool:
        """Check if SMTP credentials are provided."""
        return bool(self.host and self.user and self.password)

    def send_email(
        self,
        to_email: str,
        subject: str,
        html_body: str,
        text_body: str = "",
    ) -> bool:
        """
        Send an email via SMTP.
        If credentials are not configured, logs the email content to stdout/logger
        so local development and testing proceed seamlessly.
        """
        if not self.is_configured():
            logger.warning(
                f"[EMAIL DEV MODE - SMTP NOT CONFIGURED] To: {to_email} | Subject: {subject}"
            )
            print()
            print("=" * 64)
            print(f"📧 [TRIPGENIUS EMAIL DISPATCHER - DEV LOG]")
            print(f"To: {to_email}")
            print(f"Subject: {subject}")
            print(f"Content Summary: {text_body or html_body[:160]}...")
            print("=" * 64)
            print()
            return True

        msg = MIMEMultipart("alternative")
        msg["Subject"] = subject
        msg["From"] = f"{self.from_name} <{self.from_email}>"
        msg["To"] = to_email

        if text_body:
            msg.attach(MIMEText(text_body, "plain", "utf-8"))
        if html_body:
            msg.attach(MIMEText(html_body, "html", "utf-8"))

        try:
            if self.port == 465:
                server = smtplib.SMTP_SSL(self.host, self.port, timeout=12)
            else:
                server = smtplib.SMTP(self.host, self.port, timeout=12)
                if self.use_tls:
                    server.starttls()

            if self.user and self.password:
                server.login(self.user, self.password)

            server.sendmail(self.from_email, [to_email], msg.as_string())
            server.quit()
            logger.info(f"Successfully sent email to {to_email} via SMTP ({self.host})")
            return True

        except Exception as exc:
            logger.error(f"Failed to send email to {to_email} via SMTP: {exc}")
            print()
            print("=" * 64)
            print(f"⚠️ [SMTP DELIVERY WARNING - FALLBACK LOG]")
            print(f"Error: {exc}")
            print(f"To: {to_email}")
            print(f"Subject: {subject}")
            print(f"Content: {text_body}")
            print("=" * 64)
            print()
            return False

    def send_password_change_otp(
        self, to_email: str, recipient_name: str, otp_code: str
    ) -> bool:
        """
        Dispatch a branded security verification email containing the 6-digit
        one-time verification code for password change.
        """
        subject = f"TripGenius Security: Your Password Verification Code is {otp_code}"
        name = recipient_name.strip() or "Traveler"

        text_body = (
            f"Hello {name},\n\n"
            f"You requested a password change for your TripGenius account.\n"
            f"Your 6-digit security verification code is: {otp_code}\n\n"
            f"This code is valid for 10 minutes.\n"
            f"If you did not request this change, please ignore this email or secure your account.\n\n"
            f"— The TripGenius Security Team"
        )

        html_body = f"""<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Security Verification Code</title>
</head>
<body style="margin: 0; padding: 0; background-color: #030712; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; color: #F8FAFC;">
  <table role="presentation" width="100%" cellspacing="0" cellpadding="0" style="background-color: #030712; padding: 32px 16px;">
    <tr>
      <td align="center">
        <table role="presentation" width="100%" style="max-width: 520px; background: linear-gradient(145deg, #0F172A, #1E293B); border: 1px solid rgba(255, 255, 255, 0.12); border-radius: 20px; padding: 36px 28px; box-shadow: 0 25px 60px rgba(0, 0, 0, 0.7);">
          <!-- Header -->
          <tr>
            <td align="center" style="padding-bottom: 24px;">
              <div style="display: inline-block; background: rgba(14, 165, 233, 0.15); border: 1px solid rgba(14, 165, 233, 0.35); border-radius: 999px; padding: 6px 16px; margin-bottom: 12px;">
                <span style="color: #38BDF8; font-size: 13px; font-weight: 700; letter-spacing: 0.5px;">TRIPGENIUS SECURITY</span>
              </div>
              <h1 style="margin: 0; color: #FFFFFF; font-size: 24px; font-weight: 800; letter-spacing: -0.5px;">Password Change Verification</h1>
            </td>
          </tr>

          <!-- Greeting -->
          <tr>
            <td style="padding-bottom: 20px; color: #CBD5E1; font-size: 15px; line-height: 1.6;">
              Hello <strong style="color: #FFFFFF;">{name}</strong>,<br><br>
              We received a request to update the password for your TripGenius account associated with <span style="color: #38BDF8;">{to_email}</span>. Use the security code below to complete your password update:
            </td>
          </tr>

          <!-- OTP Box -->
          <tr>
            <td align="center" style="padding: 12px 0 24px 0;">
              <div style="display: inline-block; background: rgba(14, 165, 233, 0.10); border: 2px dashed #0EA5E9; border-radius: 14px; padding: 18px 36px; text-align: center;">
                <span style="display: block; font-size: 12px; font-weight: 700; color: #94A3B8; text-transform: uppercase; letter-spacing: 2px; margin-bottom: 6px;">One-Time Verification Code</span>
                <span style="font-size: 36px; font-weight: 900; letter-spacing: 8px; color: #38BDF8; font-family: 'Courier New', Courier, monospace;">{otp_code}</span>
              </div>
            </td>
          </tr>

          <!-- Warning Details -->
          <tr>
            <td style="padding-bottom: 28px; color: #94A3B8; font-size: 13px; line-height: 1.6; border-top: 1px solid rgba(255, 255, 255, 0.08); padding-top: 20px;">
              ⏱️ <strong>This code will expire in 10 minutes.</strong><br>
              🔒 Never share this code with anyone. TripGenius administrators will never ask for your verification code.<br>
              ⚠️ If you did not initiate this password change, you can safely disregard this email or verify your account security.
            </td>
          </tr>

          <!-- Footer -->
          <tr>
            <td align="center" style="border-top: 1px solid rgba(255, 255, 255, 0.06); padding-top: 20px; color: #64748B; font-size: 12px;">
              &copy; 2026 TripGenius AI Travel Platform. All rights reserved.
            </td>
          </tr>
        </table>
      </td>
    </tr>
  </table>
</body>
</html>"""

        return self.send_email(
            to_email=to_email,
            subject=subject,
            html_body=html_body,
            text_body=text_body,
        )


_email_service_instance: EmailService | None = None


def get_email_service() -> EmailService:
    global _email_service_instance
    if _email_service_instance is None:
        _email_service_instance = EmailService()
    return _email_service_instance
