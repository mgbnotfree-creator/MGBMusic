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

import os


def delete_file(path: str) -> None:
    """Silently delete a file if it exists."""
    try:
        if path and os.path.exists(path):
            os.remove(path)
    except Exception:
        pass
