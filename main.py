from aiogram import Bot, Dispatcher
from routers.adminrout import AdminRout
from config import API
from asyncio import run
class Main:
    
    def __init__(self) -> None:
        self.dp = Dispatcher()
        self.bt = Bot(token=API)
        self.adm = AdminRout(self.bt)
    
    def register(self):
        self.dp.include_router(self.adm.AdminRouter)
    
    async def start(self):
        self.register()
        try:
            await self.dp.start_polling(self.bt)
        except:
            await self.bt.session.close()

if __name__ == "__main__":
    run(Main().start())