import logging

from flet import Page, ControlEvent, MainAxisAlignment, CrossAxisAlignment, TextAlign, FontWeight, ScrollMode
from flet import View, AppBar, Text, ElevatedButton, Dropdown, Column
from flet_core.dropdown import Option

from alerts import info_alert
from data_manager import DataManager
from utilities import PREFERENCES


class PreferencesView:
	def __init__(self, page: Page, /) -> None:
		self.page = page

		self.video_dropdown = Dropdown(
			width=250,
			options=[
				Option('.mp4'),
				Option('.mov'),
				Option('.webm')
			],
			value='.mp4'
		)
		self.audio_dropdown = Dropdown(
			width=250,
			options=[
				Option('.mp3'),
				Option('.wav'),
				Option('.ogg')
			],
			value='.mp3'
		)

		self.load_preferences()

	def load_preferences(self) -> None:
		data_manager: DataManager = DataManager()

		try:
			self.video_dropdown.value = '.' + data_manager.get_key('default-video-format')
			self.audio_dropdown.value = '.' + data_manager.get_key('default-audio-format')
		except TypeError:
			logging.critical(f'{data_manager.data_file} doesn\'t exist!')

		self.page.update()

	def save_preferences(self, event: ControlEvent) -> None:
		data_manager: DataManager = DataManager()

		data_manager.set_key('default-video-format', self.video_dropdown.value[1:])
		data_manager.set_key('default-audio-format', self.audio_dropdown.value[1:])

		info_alert(self.page, 'Preferences Saved')

	def build(self) -> None:
		view: View = View(
			route=PREFERENCES,
			controls=[
				AppBar(title=Text('Preferences', weight=FontWeight.BOLD)),
				Column(
					[
						Text('Default Video Format', size=20, text_align=TextAlign.CENTER),
						self.video_dropdown
					],
					horizontal_alignment=CrossAxisAlignment.CENTER
				),
				Column(
					[
						Text('Default Audio Format', size=20, text_align=TextAlign.CENTER),
						self.audio_dropdown
					],
					horizontal_alignment=CrossAxisAlignment.CENTER
				),
				Column(
					[
						ElevatedButton('Save', on_click=self.save_preferences)
					],
					horizontal_alignment=CrossAxisAlignment.CENTER
				)
			],
			vertical_alignment=MainAxisAlignment.CENTER,
			horizontal_alignment=CrossAxisAlignment.CENTER,
			spacing=25,
			scroll=ScrollMode.HIDDEN
		)

		self.page.views.append(view)
