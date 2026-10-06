# ═══════════════════════════════════════════════════════════════
#                     🎵 MGB NOT FREE CODER
#
#                   © 2026 MGB NOT FREE CODER
#
#                Developed with ❤️ by MGB Not Free Coder
#
#             Do not remove or alter the original credits.
#
#           Copyright © 2026 MGB Not Free Coder. All rights reserved.
# ═══════════════════════════════════════════════════════════════

from typing import Optional

from richgram import rich_img


FALLBACK_THUMBNAIL = ""


def get_thumbnail(song: dict) -> Optional[str]:
    thumb = (song or {}).get("thumbnail")

    if isinstance(thumb, str) and thumb.startswith(("http://", "https://")):
        return thumb

    return FALLBACK_THUMBNAIL or None


def thumbnail_html(song: dict, show: bool = True) -> str:
    if not show:
        return ""

    thumb = get_thumbnail(song)
    return rich_img(thumb) if thumb else ""
