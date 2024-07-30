from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from app.telegram.handler.loader.components_loader import ComponentsLoader

class StartHandler:
    def __init__(self, loader: ComponentsLoader):
        self.loader = loader

    async def start_command(self, message: Message, state: FSMContext):
        welcome = await self.loader.get_message_template(state, "welcome")
        instructions = await self.loader.get_message_template(state, "instructions")
        commands = await self.loader.get_message_template(state, "commands")
        await message.answer(f"{welcome}\n\n{instructions}\n\n{commands}")
