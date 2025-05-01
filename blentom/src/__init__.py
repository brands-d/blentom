from bpy.utils import extension_path_user

from pathlib import Path

__directory__ = Path(__file__).parent.parent
__default_directory__ = Path(__file__).parent.parent / "resources"
__user_directory__ = Path(
    extension_path_user(__package__.rsplit(".", 1)[0], path="resources", create=True)
)

# Expose functionality
from .object import *  # noqa: F403
from .utils import *  # noqa: F403
