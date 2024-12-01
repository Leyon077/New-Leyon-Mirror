from bot import LOGGER, subprocess_lock
from bot.helper.ext_utils.status_utils import MirrorStatus, get_readable_file_size


class WatermarkStatus:
    def __init__(self, listener, gid):
        self.listener = listener
        self._gid = gid
        self._size = self.listener.size
        self.message = listener.message

    def gid(self):
        return self._gid

    def name(self):
        return self.listener.name

    def size(self):
        return get_readable_file_size(self._size)

    def status(self):
        return MirrorStatus.STATUS_WATERMARK

    def task(self):
        return self

    async def cancel_task(self):
        LOGGER.info(f"Cancelling add watermark: {self.listener.name}")
        self.listener.isCancelled = True
        async with subprocess_lock:
            if (
                self.listener.suproc is not None
                and self.listener.suproc.returncode is None
            ):
                self.listener.suproc.kill()
        await self.listener.onUploadError("Adding watermark stopped by user!")
