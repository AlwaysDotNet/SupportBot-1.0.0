from aiogram import Router, Bot
from aiogram.filters.command import Command
from aiogram.types import Message, CallbackQuery
from aiogram.types import KeyboardButton, InlineKeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder
from aiogram.types import FSInputFile
from aiogram.utils.chat_action import ChatActionSender
from aiogram import F
from aiogram.fsm.context  import FSMContext
from aiogram.fsm.state import State, StatesGroup

class SendForm(StatesGroup):
    MESSAGE = State()
    
class AdminRout:
    
    def __init__(self, bt:Bot) -> None:
        self.rt = Router()
        self.adminList = [1183684116]
        self.adm_menu = ["Send Message", "All Users"]
        self.cur_bot = bt
        self.users_list = set()
        
    def set_users_list(self,s:set):
        self.users_list = s
        
    def add_admin(self, id:int):
        """Add a new admin"""
        self.adminList.append(id)
    
    def get_reply_keyboards(self):
        kb = ReplyKeyboardBuilder()
        for menu in self.adm_menu:
            kb.add(KeyboardButton(text=menu))
        kb.adjust(2)
        return kb.as_markup(resize_keyboard = True)
    
    async def start_message(self, msg:Message):
        async with ChatActionSender.upload_photo(msg.chat.id,self.cur_bot) as f:
            f = FSInputFile("icons/admin.png")
            await msg.answer_photo(photo=f, caption="Assalomu alaykum",
                                   reply_markup=self.get_reply_keyboards())
    
    #send message menusi
    async def send_message_menu(self, msg:Message, state:FSMContext):
        await msg.answer("Iltimos xabarni kiriting: ")
        await state.set_state(SendForm.MESSAGE)
    
    async def send_message_state(self, msg:Message, state:FSMContext):
        await state.update_data(message=msg.text)
        for us_id in self.users_list:
            dt = state.get_data()
            await self.cur_bot.send_message(us_id, text=dt["message"])
        await state.clear()
        
    def register(self):
        self.rt.message.register(self.start_message, Command("start"),
                                 F.from_user.id.in_(self.adminList))
        self.rt.message.register(self.send_message_menu, F.text == self.adm_menu[0])
        self.rt.message.register(self.send_message_state, SendForm.MESSAGE)
        
    @property
    def AdminRouter(self):
        self.register()
        return self.rt

            