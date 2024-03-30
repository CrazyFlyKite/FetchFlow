import logging
from typing import List, Optional

from flet import Page, ControlEvent, FilePickerResultEvent, MainAxisAlignment, CrossAxisAlignment, TextAlign, \
	FontWeight, Control, icons
from flet import View, Text, TextField, ElevatedButton, IconButton, ProgressBar, FilePicker, Row, Column

from alerts import open_youtube_alert, info_alert
from downloader import Downloader
from utilities import MAIN, PREFERENCES, INFO, VALID_URL, DownloadType, assert_never


class MainView:
	def __init__(self, page: Page, /) -> None:
		self.page = page

		self.file_picker = FilePicker()
		self.url_field = TextField(width=300, hint_text=f'{VALID_URL}…')
		self.name_field = TextField(width=350)
		self.status_text = Text('Download', size=20, weight=FontWeight.BOLD, text_align=TextAlign.CENTER)
		self.status_bar = ProgressBar(width=350, opacity=0)

	def paste_url(self, event: ControlEvent):
		self.url_field.value = self.page.get_clipboard()
		self.page.update()

	def get_downloader(self, event: FilePickerResultEvent) -> Optional[Downloader]:
		logging.info(f'Selected directory: {event.path}')

		if event.path is None:
			return

		return Downloader(self.page, self.url_field.value, self.name_field.value, event.path)

	def download(self, event: FilePickerResultEvent, download_type: DownloadType, disable_controls: List[Control]) -> None:
		downloader: Optional[Downloader] = self.get_downloader(event)

		if downloader is None:
			return

		# Start download
		self.status_bar.opacity = 100
		self.status_text.value = 'Downloading…'
		self.status_text.color = 'blue'
		for control in disable_controls:
			control.disabled = True

		self.page.update()

		match download_type:
			case DownloadType.VIDEO:
				downloader.download(DownloadType.VIDEO)
			case DownloadType.AUDIO:
				downloader.download(DownloadType.AUDIO)
			case _:
				assert_never(download_type)

		# End download
		self.url_field.value = None
		self.name_field.value = None
		self.status_bar.opacity = 0
		self.status_text.value = 'Download'
		self.status_text.color = None
		for control in disable_controls:
			control.disabled = False

		self.page.update()

	def switch(self, download_type: DownloadType, *, disable_controls: List[Control]) -> None:
		if not self.url_field.value or not self.name_field.value or not self.url_field.value.startswith(VALID_URL):
			info_alert(self.page, 'Invalid Input', 'Please enter a valid URL and filename.')
			return

		match download_type:
			case DownloadType.VIDEO:
				self.file_picker.on_result = lambda event: self.download(event, DownloadType.VIDEO, disable_controls)
			case DownloadType.AUDIO:
				self.file_picker.on_result = lambda event: self.download(event, DownloadType.AUDIO, disable_controls)
			case _:
				assert_never(download_type)

		self.file_picker.get_directory_path()

	def build(self) -> None:
		view: View = View(
			route=MAIN,
			controls=[
				Text('YouTube URL', size=20, weight=FontWeight.BOLD, text_align=TextAlign.CENTER),
				Row(
					[
						self.url_field,
						IconButton(icon=icons.PASTE, on_click=self.paste_url, tooltip='Paste')
					],
					alignment=MainAxisAlignment.CENTER
				),
				Text('Filename', size=20, weight=FontWeight.BOLD, text_align=TextAlign.CENTER),
				self.name_field,
				self.status_text,
				self.status_bar,
				Column(
					[
						Row(
							[
								download_video_button := ElevatedButton(
									'Video',
									width=120,
									icon=icons.ONDEMAND_VIDEO,
									on_click=lambda _: self.switch(
										DownloadType.VIDEO,
										disable_controls=[
											download_video_button,
											download_audio_button,
											preferences_button,
											info_button
										]
									),
									tooltip='Download Video',
								),
								download_audio_button := ElevatedButton(
									'Audio',
									width=120,
									icon=icons.AUDIOTRACK,
									on_click=lambda _: self.switch(
										DownloadType.AUDIO,
										disable_controls=[
											download_video_button,
											download_audio_button,
											preferences_button,
											info_button
										]
									),
									tooltip='Download Audio Only',
								)
							],
							alignment=MainAxisAlignment.CENTER,
							spacing=15
						),
						Row(
							[
								preferences_button := IconButton(
									icon=icons.SETTINGS,
									icon_size=40,
									on_click=lambda _: self.page.go(PREFERENCES),
									tooltip='Preferences'
								),
								info_button := IconButton(
									icon=icons.INFO,
									icon_size=40,
									on_click=lambda _: self.page.go(INFO),
									tooltip='Info'
								),
								IconButton(
									icon=icons.PLAY_CIRCLE,
									icon_size=40,
									icon_color='red',
									on_click=lambda _: open_youtube_alert(self.page),
									tooltip='YouTube'
								)
							],
							alignment=MainAxisAlignment.CENTER,
							spacing=7
						)
					],
					spacing=60
				)
			],
			vertical_alignment=MainAxisAlignment.CENTER,
			horizontal_alignment=CrossAxisAlignment.CENTER
		)

		self.page.overlay.append(self.file_picker)
		self.page.views.append(view)
