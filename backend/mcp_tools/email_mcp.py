"""Email MCP Tool - Send and manage emails"""

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import Dict, Any
from config import settings
import logging

logger = logging.getLogger(__name__)

class EmailTool:
    """MCP tool for email operations"""
    
    def __init__(self):
        self.name = "email"
        self.description = "Send and manage emails via SMTP"
        self.enabled = True
        
    async def execute(self, action: str, **kwargs) -> Dict[str, Any]:
        """
        Execute email operation
        
        Args:
            action: Operation type (send, draft)
            **kwargs: Additional parameters
            
        Returns:
            Dictionary with operation result
        """
        try:
            if action == "send":
                return await self._send_email(
                    kwargs.get("to"),
                    kwargs.get("subject"),
                    kwargs.get("body"),
                    kwargs.get("html", False)
                )
            elif action == "draft":
                return await self._create_draft(
                    kwargs.get("to"),
                    kwargs.get("subject"),
                    kwargs.get("body")
                )
            else:
                return {"success": False, "error": f"Unknown action: {action}"}
                
        except Exception as e:
            logger.error(f"❌ Email operation error: {str(e)}")
            return {"success": False, "error": str(e)}
    
    async def _send_email(self, to: str, subject: str, body: str, html: bool = False) -> Dict[str, Any]:
        """Send email"""
        if not settings.SMTP_HOST or not settings.SMTP_USER:
            return {
                "success": False,
                "error": "SMTP configuration not set. Please configure SMTP settings."
            }
        
        try:
            msg = MIMEMultipart('alternative')
            msg['From'] = settings.SMTP_USER
            msg['To'] = to
            msg['Subject'] = subject
            
            if html:
                msg.attach(MIMEText(body, 'html'))
            else:
                msg.attach(MIMEText(body, 'plain'))
            
            with smtplib.SMTP(settings.SMTP_HOST, settings.SMTP_PORT) as server:
                server.starttls()
                server.login(settings.SMTP_USER, settings.SMTP_PASSWORD)
                server.send_message(msg)
            
            logger.info(f"📧 Email sent to {to}")
            
            return {
                "success": True,
                "action": "send",
                "to": to,
                "subject": subject
            }
            
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    async def _create_draft(self, to: str, subject: str, body: str) -> Dict[str, Any]:
        """Create email draft (stored locally)"""
        draft = {
            "to": to,
            "subject": subject,
            "body": body,
            "status": "draft"
        }
        
        return {
            "success": True,
            "action": "draft",
            "draft": draft
        }
    
    def get_schema(self) -> Dict[str, Any]:
        """Return tool schema for LangChain"""
        return {
            "name": self.name,
            "description": self.description,
            "parameters": {
                "type": "object",
                "properties": {
                    "action": {
                        "type": "string",
                        "enum": ["send", "draft"],
                        "description": "Email operation to perform"
                    },
                    "to": {
                        "type": "string",
                        "description": "Recipient email address"
                    },
                    "subject": {
                        "type": "string",
                        "description": "Email subject"
                    },
                    "body": {
                        "type": "string",
                        "description": "Email body content"
                    },
                    "html": {
                        "type": "boolean",
                        "description": "Whether body is HTML (default: false)"
                    }
                },
                "required": ["action", "to", "subject", "body"]
            }
        }
