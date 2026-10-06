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

import config
from ShizuMusic.utils.db import is_logger_enabled


def logger_active() -> bool:
    return bool(config.LOGGER_ID) and is_logger_enabled()
