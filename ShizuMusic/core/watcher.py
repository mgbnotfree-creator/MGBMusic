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

import asyncio


async def watchdog() -> None:
    """No-op — watchdog disabled to keep bot running 24/7."""
    while True:
        await asyncio.sleep(3600)  # sleep forever, do nothing
