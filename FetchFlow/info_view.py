import logging

from flet import Page, MainAxisAlignment, CrossAxisAlignment, FontWeight, ScrollMode
from flet import View, Text, Markdown, AppBar

from utilities import INFO, PathLikeString


class InfoView:
	def __init__(self, page: Page, /) -> None:
		self.page = page

	def load_info(self, path: PathLikeString) -> str | None:
		try:
			with open(path, 'r', encoding='utf-8') as file:
				return file.read()
		except FileNotFoundError:
			logging.critical(f'{path} doesn\'t exist!')
			return
		except IsADirectoryError:
			logging.critical(f'{path} is a directory!')
			return

	def build(self) -> None:
		view: View = View(
			route=INFO,
			controls=[
				AppBar(title=Text('Info', weight=FontWeight.BOLD)),
				Markdown(value=self.load_info('../assets/info.md'), selectable=True)
			],
			vertical_alignment=MainAxisAlignment.CENTER,
			horizontal_alignment=CrossAxisAlignment.CENTER,
			scroll=ScrollMode.HIDDEN
		)

		self.page.views.append(view)
