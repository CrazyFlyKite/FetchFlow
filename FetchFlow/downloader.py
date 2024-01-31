import logging
from typing import Any

from flet import Page
from pytube import YouTube, Stream
from pytube.exceptions import RegexMatchError, VideoUnavailable

from alerts import info_alert
from data_manager import DataManager
from utilities import DownloadType, PathLikeString


class Downloader:
	def __init__(self, page: Page, /, url: str, filename: str, directory: PathLikeString) -> None:
		"""
		Initialize the Downloader object.

		:parameter url: The URL of the YouTube video.
		:parameter filename: The desired filename for the downloaded video or audio.
		:parameter directory: The directory where the video or audio will be saved.
		"""

		self.page = page
		self.__url = url
		self.__filename = filename
		self.__directory = directory

	# url
	@property
	def url(self) -> str:
		return str(self.__url)

	@url.setter
	def url(self, value: Any) -> None:
		self.__url = str(value)

	# filename
	@property
	def filename(self) -> str:
		return str(self.__filename)

	@filename.setter
	def filename(self, value: Any) -> None:
		self.__filename = str(value)

	# directory
	@property
	def directory(self) -> str:
		return str(self.__directory)

	@directory.setter
	def directory(self, value: Any) -> None:
		self.__directory = str(self.__directory)

	def download_video(self) -> None:
		"""
		Download a YouTube video based on the provided URL, filename, directory.
		"""

		# If the filename does not have an extension, append the default video format
		if '.' not in self.filename:
			file_format: str = DataManager().get_key('default-video-format')
			self.filename = f'{self.filename}.{file_format}'

		try:
			# Initialize YouTube object and fetch the appropriate stream
			youtube: YouTube = YouTube(self.url)
			video: Stream = youtube.streams.get_highest_resolution()
			video.download(output_path=self.directory, filename=self.filename)
		except RegexMatchError:
			logging.error('Invalid URL - Cannot find the YouTube URL.')
			info_alert(self.page, 'Invalid URL', 'Cannot find the YouTube URL.')
		except VideoUnavailable:
			logging.error('Video is unavailable - You can download videos only from YouTube.')
			info_alert(self.page, 'Video is Unavailable', 'You can download videos only from YouTube.')
		except FileNotFoundError:  # If the filename contains any illegal characters
			logging.error('Invalid filename - The provided filename contains forbidden characters')
			info_alert(self.page, 'Invalid File Name', 'The provided filename contains forbidden characters.')
		else:
			logging.info('Video downloaded successfully!')
			info_alert(self.page, 'Video Downloaded Successfully')

	def download_audio(self) -> None:
		"""
		Download audio from a YouTube video based on the provided URL, filename and directory.
		"""

		# If the filename does not have an extension, append the default audio format
		if '.' not in self.filename:
			file_format: str = DataManager().get_key('default-audio-format')
			self.__filename = f'{self.filename}.{file_format}'

		try:
			# Initialize YouTube object and fetch the audio stream
			youtube: YouTube = YouTube(self.url)
			audio: Stream = youtube.streams.filter(only_audio=True).first()
			audio.download(output_path=self.directory, filename=self.filename)
		except RegexMatchError:
			logging.error('Invalid URL - Cannot find the YouTube URL.')
			info_alert(self.page, 'Invalid URL', 'Cannot find the YouTube URL.')
		except VideoUnavailable:
			logging.error('Video is unavailable - You can download videos only from YouTube.')
			info_alert(self.page, 'Video is Unavailable', 'You can download audios only from YouTube.')
		except FileNotFoundError:  # If the filename contains any illegal characters
			logging.error('Invalid filename - The provided filename contains forbidden characters.')
			info_alert(self.page, 'Invalid Filename', 'The provided filename contains forbidden characters.')
		else:
			logging.info('Audio downloaded successfully!')
			info_alert(self.page, 'Audio Downloaded Successfully')

	def download(self, download_type: DownloadType) -> None:
		"""
		Download video or audio based on the specified `download_type`.
		"""

		match download_type:
			case DownloadType.VIDEO:
				self.download_video()
			case DownloadType.AUDIO:
				self.download_audio()
			case other:
				logging.error(f'Got unexpected download type: {other}!')
