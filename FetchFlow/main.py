import logging

from flet import app, Page, MainAxisAlignment, CrossAxisAlignment, RouteChangeEvent, ViewPopEvent

from info_view import InfoView
from main_view import MainView
from preferences_view import PreferencesView
from setup_logging import setup_logging
from utilities import *


def main(page: Page) -> None:
	page.title = PAGE_TITLE
	page.window_width = PAGE_WIDTH
	page.window_height = PAGE_HEIGHT
	page.window_resizable = RESIZABLE
	page.horizontal_alignment = CrossAxisAlignment.CENTER
	page.vertical_alignment = MainAxisAlignment.CENTER

	# Setup logging
	setup_logging()

	def route_change(event: RouteChangeEvent) -> None:
		page.views.clear()

		# Main View
		MainView(page).build()

		# Preferences View
		if page.route == PREFERENCES:
			PreferencesView(page).build()

		# Info View
		if page.route == INFO:
			InfoView(page).build()

	def view_pop(event: ViewPopEvent) -> None:
		page.views.pop()
		page.go(page.views[-1].route)

	page.on_route_change = route_change
	page.on_view_pop = view_pop
	page.go(page.route)


if __name__ == '__main__':
	app(target=main, assets_dir='../assets')
