from typing import List, Callable, Dict, Any
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext

class EventEmitter:
    def __init__(self):
        self.handlers: Dict[str, List[Callable[[Dict[str, Any]], None]]] = {}
        self.callback_query_handlers: Dict[str, Callable[[CallbackQuery, FSMContext], None]] = {}
        self.message_handlers: Dict[str, Callable[[Message, FSMContext], None]] = {}

    def on(self, event_type: str, handler: Callable[[Dict[str, Any]], None]) -> None:
        """Register a generic event handler."""
        if event_type not in self.handlers:
            self.handlers[event_type] = []
        self.handlers[event_type].append(handler)

    def on_callback_query(self, event_type: str, handler: Callable[[CallbackQuery, FSMContext], None]) -> None:
        """Register a CallbackQuery handler."""
        self.callback_query_handlers[event_type] = handler

    def on_message(self, event_type: str, handler: Callable[[Message, FSMContext], None]) -> None:
        """Register a Message handler."""
        self.message_handlers[event_type] = handler

    async def emit(self, event_type: str, event_data: Dict[str, Any]) -> None:
        """Emit a generic event."""
        if event_type in self.handlers:
            for handler in self.handlers[event_type]:
                await handler(event_data)

    async def emit_callback_query(self, event_type: str, callback_query: CallbackQuery, state: FSMContext) -> None:
        """Emit a CallbackQuery event."""
        if event_type in self.callback_query_handlers:
            handler = self.callback_query_handlers[event_type]
            await handler(callback_query, state)

    async def emit_message(self, event_type: str, message: Message, state: FSMContext) -> None:
        """Emit a Message event."""
        if event_type in self.message_handlers:
            handler = self.message_handlers[event_type]
            await handler(message, state)
