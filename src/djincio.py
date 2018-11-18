import asyncio
from concurrent.futures import Future, ThreadPoolExecutor
from django.shortcuts import get_object_or_404
import functools

class MetaDjincio(type):
    def __new__(cls, name, bases, namespaces, **kwargs):
        namespace = {k: v if k.startswith('__') else async_view(v) for k, v in namespace.items()}
        return type.__new__(cls, name, bases, namespaces)

class async_view():
    def __init__(self, inner):
        self.inner = inner
        self.event_loop = None
        try:
            self.event_loop = asyncio.get_event_loop()
        except RuntimeError:
            pass


    def __call__(self, *args, **kwargs):
        try:
            event_loop = asyncio.get_event_loop()
        except RuntimeError:
            pass
        else:
            if self.event_loop.is_running():
                raise RuntimeError('Cannot access the event loop')
        future_val = Future()
        if not (self.event_loop and self.event_loop.is_running()):
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            loop.run_until_complete(self.outer(args, kwargs, future_val))
            loop.close()
            asyncio.set_event_loop(self.event_loop)
        else:
            self.event_loop.call_soon_threadsafe(
                    self.event_loop.create_task,
                    self.outer(args, kwargs, future_val)
            )
        return future_val.result()

    def __get__(self, parent, objtype):
        return functools.partial(self.__call__, parent)

    async def outer(self, args, kwargs, future_val):
        try:
            result = await self.inner(*args, **kwargs)
        except Exception as e:
            future_val.set_exception(e)
        else:
            future_val.set_result(result)


async def get_object_or_404_async(model, pk):
    executor = ThreadPoolExecutor(max_workers=3)
    loop = asyncio.get_event_loop()
    result = await loop.run_in_executor(get_object_or_404, model, pk, executor=executor)
    return result


