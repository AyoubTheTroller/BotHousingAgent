from typing import List, Callable, Dict, Any

class EventEmitter:
    def __init__(self):
        self.handlers: Dict[str, List[Callable[[Dict[str, Any]], None]]] = {}

    def on(self, event_type: str, handler: Callable[[Dict[str, Any]], None]) -> None:
        if event_type not in self.handlers:
            self.handlers[event_type] = []
        self.handlers[event_type].append(handler)

    async def emit(self, event_type: str, event_data: Dict[str, Any]) -> None:
        if event_type in self.handlers:
            for handler in self.handlers[event_type]:
                await handler(event_data)
