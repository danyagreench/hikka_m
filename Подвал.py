# ---------------------------------------------------------------------------------
# ( o.o )  🔓 Not licensed.
#  > ^ <   ⚠️ Owner of heta.hikariatama.ru doesn't take any responsibilities or intellectual property rights regarding this script
# ---------------------------------------------------------------------------------
# Author: danyagreench
# Commands:
# .мой_подвал | .посадить_в_подвал | .распустить_подвал
# ---------------------------------------------------------------------------------

#             █ █ ▀ █▄▀ █▄▀ ▄▀█    █▀▄▀█
#             █▀█ █ █ █ █ █ █▀█ ▄▄ █   █
# ---------------------------------------------------------------------------------------------

# версия модуля
__version__ = (6, 6, 6)
# meta developer: @hikka_m
# only hikka

# импортируем нужные библиотеки
import random
from asyncio import sleep
from .. import loader, utils
from ..inline.types import InlineCall
import asyncio
from telethon.tl.functions.users import GetFullUserRequest
import re
from telethon.tl.types import Message, ChatAdminRights
from telethon import functions

@loader.tds
class Подвал(loader.Module):
    """Модуль подвал"""
    strings = {
        "name" : "Подвал",
    }
    async def client_ready(self):
        self._backup_channel, _ = await utils.asset_channel(
            self._client,
            "Подвал",
            "Группа для работы модуля Подвал",
            silent=True,
            archive=True,
            _folder="hikka",
        )

    @loader.command()
    async def мой_подвал(self,message: Message):
        '''- Посмотреть подвал'''
        user = await message.client.get_me()
        user_id = user.id
        first_name = user.first_name or "null"
        last_name = user.last_name or "null"
        username = user.username or "null"
        det = self.get("det",0)
        await self.inline.form(
            text=f"<b>Подвал пользователя @{username}:\nДетей в подвале:</b> <code>{det}</code>",
            message=message,
            reply_markup=[
                [
                    {
                        "text" : f"Выпустить детей",
                        "callback" : self.rasp,
                    },
                ],
                [
                    {
                        "text" : "Закрыть",
                        "action" : "close",
                    }
                ]
            ]
        )
    async def rasp(self,call: InlineCall):
        det = self.get("det",0)
        self.set("det",0)
        await call.edit(
                text=f"<b>Подвал был распущен.\nДетей в подвале:</b> <code>{det}</code>",
                reply_markup=[
                [
                    {
                        "text" : f"Выпустить детей",
                        "callback" : self.rasp,
                    },
                ],
                [
                    {
                        "text" : "Закрыть",
                        "action" : "close",
                    },
                ],
            ]
        )

    @loader.command()
    async def посадить_в_подвал(self, message: Message):
        '''- Посадить в подвал'''
        det = self.get("det", 0)
        if random.random() < 0.5:
            await utils.answer(message, "<b>Полиция нашла тебя, и забрала ребёнка... Но, ты успел сбежать</b>")
        else:
            await utils.answer(message, "<b>+</b> <code>1</code> <b>новый</b> ребёнок в подвал")
            det += 1
            self.set("det", det)
    @loader.command()
    async def распустить_подвал(self,message):
        '''- распустить'''
        self.set("det",0)
        await utils.answer(message, "<b>Все дети которые были в подвале, были выпущены на улицу.</b> 💫")
