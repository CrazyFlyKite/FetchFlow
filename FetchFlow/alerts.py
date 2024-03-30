import webbrowser
from typing import Optional

from flet import Page, ControlEvent, MainAxisAlignment, AlertDialog, Text, TextButton

from utilities import YOUTUBE_URL


def open_youtube_alert(page: Page, /) -> None:
	def close_dialog(event: ControlEvent) -> None:
		alert.open = False
		page.update()

	def open_youtube(event: ControlEvent) -> None:
		webbrowser.open(YOUTUBE_URL)
		close_dialog(event)

	alert: AlertDialog = AlertDialog(
		open=True,
		title=Text('Open YouTube?'),
		content=Text('This action will open youtube.com.'),
		actions=[
			TextButton('Cancel', on_click=close_dialog),
			TextButton('Open', on_click=open_youtube)
		],
		actions_alignment=MainAxisAlignment.END
	)

	page.dialog = alert
	page.update()


def info_alert(page: Page, /, title: str, subtitle: Optional[str] = None) -> None:
	def close_dialog(event: ControlEvent) -> None:
		alert.open = False
		page.update()

	alert: AlertDialog = AlertDialog(
		open=True,
		title=Text(title),
		content=None if subtitle is None else Text(subtitle),
		actions=[
			TextButton('OK', on_click=close_dialog),
		],
		actions_alignment=MainAxisAlignment.END
	)

	page.dialog = alert
	page.update()
