import os
from emails.EmailBase import EmailBase

from pydantic import BaseModel
from typing import Optional

class EmailGeneralModel(BaseModel):
	"""Send an general email

	Args:
		receivers (list[str]): Receivers
		subject (str): Subject
		body (str): Body (HTML)
		styles (Optional[str]): CSS Styles
	"""
	receivers: Optional[list] = None
	subject: str
	body: str
	styles: Optional[str] = None

class EmailGeneral(EmailBase):
	DEFAULT_RECEIVER = os.getenv("MyCloud_Emails_Receivers_Default")
	assert DEFAULT_RECEIVER is not None, "MyCloud_Emails_Receivers_Default is not set in .env file"
	DEFAULT_RECEIVER: str

	def __init__(self, subject: str, body: str, receivers: list | None, styles: str = None):
		"""Send a general email

		Args:
			subject (str): Subject
			body (str): Body (HTML)
			receivers (list): Receivers
			style (Optional[str]): CSS Styles
		"""
		self.subject = subject
		self.body = body
		self.receivers = receivers if receivers is not None else [self.DEFAULT_RECEIVER]
		self.styles = styles
		super().__init__()

	def get_subject(self):
		return self.subject

	def get_receivers(self):
		return self.receivers

	def get_html_body(self):
		return self.body

	def get_html_styles(self):
		return self.styles