from enum import Enum
from os import PathLike
from typing import Dict, Literal, Final, TypeAlias

# Window
NAME: Final[str] = 'Fetch Flow'
WIDTH: Final[int] = 400
HEIGHT: Final[int] = 470
RESIZABLE: Final[bool] = False

# Custom types
JSONDictionary: TypeAlias = Dict[str, str]
PossibleKeys: TypeAlias = Literal['default-video-format', 'default-audio-format']
PathLikeString: TypeAlias = str | bytes | PathLike

# Other
VALID_URL: Final[str] = 'https://www.youtube.com/watch?v='

# Views
MAIN: Final[str] = '/'
PREFERENCES: Final[str] = '/preferences'
INFO: Final[str] = '/info'


# Enums
class DownloadType(Enum):
	VIDEO: Final[str] = 'video'
	AUDIO: Final[str] = 'audio'
