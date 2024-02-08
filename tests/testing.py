from asyncio import AbstractEventLoop
from unittest.mock import AsyncMock, patch


class EventLoopMockMixin:
    def _create_loop_mock(self):
        self.loop_mock = AsyncMock(spec=AbstractEventLoop)
        p = patch("asyncio.get_event_loop", return_value=self.loop_mock)
        p.start()
        self.addCleanup(p.stop)


class RandomMockMixin:
    def _create_random_mock(self, patch_path):
        p = patch(patch_path)
        self.random_mock = p.start()
        self.random_mock.random.return_value = 0.5
        self.addCleanup(p.stop)


class TimenowMockMixin:
    def _create_timenow_mock(self, patch_path):
        p = patch(patch_path)
        self.timenow_mock = p.start()
        self.timenow_mock.return_value = 0.5
        self.addCleanup(p.stop)
