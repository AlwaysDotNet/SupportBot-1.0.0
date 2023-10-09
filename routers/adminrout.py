from aiogram import Router, Bot
from aiogram.filters.command import Command
from aiogram.types import Message, CallbackQuery
from aiogram.types import KeyboardButton, InlineKeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder
from aiogram.types import FSInputFile
from aiogram.utils.chat_action import ChatActionSender
from aiogram import F
class AdminRout:
    
    def __init__(self, bt:Bot) -> None:
        self.rt = Router()
        self.adminList = [1183684116]
        self.adm_menu = ["Send Message", "All Users"]
        self.cur_bot = bt
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
    
    def register(self):
        self.rt.message.register(self.start_message, Command("start"),
                                 F.from_user.id.in_(self.adminList))
    
    @property
    def AdminRouter(self):
        self.register()
        return self.rt

            