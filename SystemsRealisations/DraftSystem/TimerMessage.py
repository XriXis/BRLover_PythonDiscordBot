from asyncio import sleep, create_task, Task, TimeoutError as ATimeoutError, CancelledError

from discord import Message

from SystemsRealisations.MessageLib import custom_embed


class TimerMessage:
    message: Message
    _start_task: Task

    def __init__(self,seconds):
        self.max_time = seconds
        self.time = seconds
        self.message_key = "timer header"

    async def send(self, channel):
        self.message = await channel.send(
            embed=custom_embed(True,
                               self.message_key,
                               "%s:%s" % divmod(self.time, 60))
        )
        self._start_task = create_task(self._start())
        try:
            await self._start_task
        except CancelledError:
            await self.message.delete()
        except ATimeoutError:
            await self.message.delete()
            raise ATimeoutError("Time for draft is end")
        else:
            raise RuntimeError("Something bad, no one exception wasn't found")

    def stop(self):
        if self._start_task.cancelled():
            pass
        else:
            self._start_task.cancel()

    def reset(self):
        self.time = self.max_time
        self.message_key = "timer header"

    def chill(self):
        self.message_key = "timer pause"

    async def _start(self):
        while True:
            self._calculate_time()
            await self.message.edit(
                embed=custom_embed(True,
                                   self.message_key,
                                   "%s:%s" % divmod(self.time, 60))
            )
            await sleep(0.9)

    def _calculate_time(self):
        if self.time == 0:
            raise ATimeoutError("Time for draft is end")
        self.time -= 1
