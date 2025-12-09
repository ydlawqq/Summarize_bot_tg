import logging
import os
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.types import Message, Update
from aiogram.filters import CommandStart
from aiogram.enums import ParseMode
from agents import llm_ollama, agent_chain
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.requests import Request
import uvicorn
from contextlib import asynccontextmanager
from dotenv import load_dotenv
from HOTEL.Postgres.engine import async_session
from HOTEL.Postgres.repos.user_repo import UserRepos
from HOTEL.Postgres.repos.Chat_repo import HistoryMessages
from HOTEL.app.agents import llm_ollama

load_dotenv()

token = os.getenv('token_tg')

bot = Bot(token=token, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()

@asynccontextmanager
async def lifespan(app: FastAPI):
    url_webhook = 'https://few-dogs-add.loca.lt' + '/webhook'
    await bot.set_webhook(url_webhook, allowed_updates=dp.resolve_used_update_types(), drop_pending_updates=True)
    yield
    await bot.delete_webhook()



app = FastAPI(lifespan=lifespan)

#app.mount('/static', StaticFiles(directory='static'), name='static')
#templates = Jinja2Templates(directory='templates')


@dp.message(CommandStart())
async def start(mes: Message):
    user_id = mes.from_user.id
    user_name = mes.from_user.first_name
    async with async_session() as session:
        user_class = UserRepos(session)
        await user_class.upsert_user(telegram_id=user_id, username=user_name)
        user = await user_class.get_user_by_tg_id(user_id)

    resp = f'Привет {user_name}, я бот для суммаризации PDF'
    await mes.answer(resp, parse_mode=None)




@dp.message()
async def all(mes: Message):
    text = mes.text
    async with async_session() as session:
        user_ = UserRepos(session)
        user = await user_.get_user_by_tg_id(mes.from_user.id)

        history = HistoryMessages(session)
        chat_history = await history.get_history_by_id(user.id)
        response = agent_chain.invoke({
            'input': text, 'history': chat_history
        })

        await history.add_message(user_id=user.id, content=text, role='user')
        await history.add_message(user_id=user.id, content=response.content, role='agent')

        await session.commit()

    await mes.answer(response.content)







@app.post("/webhook")
async def webhook(request: Request) -> None:
    update = Update.model_validate(await request.json(), context={'bot': bot})
    await dp.feed_update(bot, update)


if __name__ == '__main__':
    uvicorn.run(app,host='0.0.0.0', port=8000 )