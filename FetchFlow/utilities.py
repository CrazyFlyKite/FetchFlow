from enum import Enum
from os import PathLike
from typing import Dict, NoReturn, Literal, Final, TypeAlias

# Window
PAGE_TITLE: Final[str] = 'Fetch Flow'
PAGE_WIDTH: Final[int] = 400
PAGE_HEIGHT: Final[int] = 470
RESIZABLE: Final[bool] = False

# Custom types
JSONDictionary: TypeAlias = Dict[str, str]
PossibleKeys: TypeAlias = Literal['default-video-format', 'default-audio-format']
PathLikeString: TypeAlias = str | bytes | PathLike

# Other
YOUTUBE_URL: Final[str] = 'https://www.youtube.com'
VALID_URL: Final[str] = 'https://www.youtube.com/watch?v='

# Views
MAIN: Final[str] = '/'
PREFERENCES: Final[str] = '/preferences'
INFO: Final[str] = '/info'


# Enums
class DownloadType(Enum):
	VIDEO: Final[str] = 'video'
	AUDIO: Final[str] = 'audio'


# Assert never
def assert_never(argument: NoReturn) -> NoReturn:
	raise AssertionError('Expected code is unreachable')
