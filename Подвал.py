# ---------------------------------------------------------------------------------
# ( o.o )  🔓 Not licensed.
#  > ^ <   ⚠️ Owner of heta.hikariatama.ru doesn't take any responsibilities or intellectual property rights regarding this script
# ---------------------------------------------------------------------------------
# Author: danyagreench
# Commands:
# .мой_подвал | .посадить_в_подвал | .распустить_подвал | .монеты | .стата
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
                        "text" : "Выпустить детей",
                        "callback" : self.resetdet,
                    },
                    {
                        "text": "Продать органы",
                        "callback": self.naorgans,
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
    async def resetdet(self,call: InlineCall):
        det = self.get("det",0)
        self.set("det",0)
        det2 = self.get("det",0)
        await call.edit(
                text=f"<b>Подвал был распущен.\nДетей в подвале:</b> <code>{det2}</code>",
                reply_markup=[
                [
                    {
                        "text" : "Выпустить детей",
                        "callback" : self.resetdet,
                    },
                    {
                        "text": "Продать органы",
                        "callback": self.naorgans,
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
    async def naorgans(self,call: InlineCall):
        det = self.get("det", 0)
        moneti = self.get("moneti", 0)
        monetivs = self.get("monetivs", 0)

        moneti += det
        monetivs += det
        self.set("moneti", moneti)
        self.set("monetivs", monetivs)
        self.set("det", 0)
        det2 = self.get("det", 0)
        await call.edit(
                text=f"<b>Все органы детей были проданы, детей больше нет.\nДетей в подвале:</b> <code>{det2}</code>",
                reply_markup=[
                [
                    {
                        "text" : "Выпустить детей",
                        "callback" : self.resetdet,
                    },
                    {
                        "text": "Продать органы",
                        "callback": self.naorgans,
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
        detvs = self.get("detvs", 0)
        if random.random() < 0.5:
            await utils.answer(message, "<b>Полиция нашла тебя, и забрала ребёнка... Но, ты успел сбежать</b>")
        else:
            await utils.answer(message, "<b>+</b> <code>1</code> <b>новый ребёнок в подвал</b>")
            det += 1
            detvs += 1
            self.set("det", det)
            self.set("detvs", detvs)

    @loader.command()
    async def распустить_подвал(self,message):
        '''- распустить'''
        self.set("det",0)
        await utils.answer(message, "<b>Все дети которые были в подвале, были выпущены на улицу.</b> 💫")

    @loader.command()
    async def монеты(self,message):
        '''- баланс монет'''
        moneti = self.get("moneti", 0)
        user = await message.client.get_me()
        user_id = user.id
        first_name = user.first_name or "null"
        last_name = user.last_name or "null"
        username = user.username or "null"
        await utils.answer(message, f"<b>@{username}, ваш баланс монет: {moneti}</b>")
    @loader.command()
    async def стата(self,message):
        '''- статистика'''
        user = await message.client.get_me()
        user_id = user.id
        first_name = user.first_name or "null"
        last_name = user.last_name or "null"
        username = user.username or "null"
        monetivs = self.get("monetivs",0)
        detvs = self.get("detvs",0)
        await utils.answer(message, f"<b>@{username}, ваша статистика:\nМонет заработано всего с продажи органов: {monetivs}\nДетей было в подвале всего: {detvs}</b>")
    @loader.command()
    async def кейсы(self,message):
        '''- ваши кейсы'''
        user = await message.client.get_me()
        user_id = user.id
        first_name = user.first_name or "null"
        last_name = user.last_name or "null"
        username = user.username or "null"
        detcase = self.get("detcase",0)
        monetcase = self.get("monetcase",0)
        if detcase < 1 and monetcase < 1:
            await utils.answer(message, f"<b>@{username}, ваши кейсы:\n\nПусто</b>")
        elif monetcase < 1 and detcase > 0:
            await utils.answer(message, f"<b>@{username}, ваши кейсы:\n\nДет-Кейс: {detcase}</b>")
        elif detcase < 1 and monetcase > 0:
            await utils.answer(message, f"<b>@{username}, ваши кейсы:\n\nМонет-Кейс: {monetcase}</b>")
        elif detcase > 0 and monetcase > 0:
            await utils.answer(message, f"<b>@{username}, ваши кейсы:\n\nДет-Кейс: {detcase}\nМонет-Кейс: {monetcase}</b>")
    @loader.command()
    async def открыть_дк(self, message: Message):
        '''- Открыть дет-кейс'''
        detcase = self.get("detcase",0)
        random_numgdc = random.randint(1, 100)
        det = self.get("det",0)
        detvs = self.get("detvs",0)
        if detcase == 0:
            await utils.answer(message, "<b>У вас не хватает Дет-Кейса</b>")
        else:
            await utils.answer(message, f"<b>Вы открыли <code>1</code> Дет-Кейс, вам выпало: <code>{random_numgdc}</code> детей</b>")
            det += random_numgdc
            detvs += random_numgdc
            detcase -= 1
            self.set("det", det)
            self.set("detvs", detvs)
            self.set("detcase", detcase)
    @loader.command()
    async def открыть_мк(self, message: Message):
        '''- Открыть монет-кейс'''
        monetcase = self.get("monetcase",0)
        random_numgdc = random.randint(1, 150)
        moneti = self.get("moneti",0)
        monetivs = self.get("monetivs",0)
        if monetcase == 0:
            await utils.answer(message, "<b>У вас не хватает Монет-Кейса</b>")
        else:
            await utils.answer(message, f"<b>Вы открыли <code>1</code> Монет-Кейс, вам выпало: <code>{random_numgdc}</code> монет</b>")
            moneti += random_numgdc
            monetivs += random_numgdc
            monetcase -= 1
            self.set("moneti", moneti)
            self.set("monetivs", monetivs)
            self.set("monetcase", monetcase)
    @loader.command()
    async def купить_дк(self, message: Message):
        '''- Купить дет-кейс'''
        detcase = self.get("detcase",0)
        det = self.get("det",0)
        if det < 50:
            await utils.answer(message, "<b>У вас не хватает детей</b>")
        else:
            await utils.answer(message, f"<b>Вы купили <code>1</code> Дет-Кейс, потрачено: <code>50</code> детей</b>")
            det -= 50
            detcase += 1
            self.set("det", det)
            self.set("detcase", detcase)
    @loader.command()
    async def купить_мк(self, message: Message):
        '''- Купить монет-кейс'''
        monetcase = self.get("monetcase",0)
        moneti = self.get("moneti",0)
        if moneti < 90:
            await utils.answer(message, "<b>У вас не хватает монет</b>")
        else:
            await utils.answer(message, f"<b>Вы купили <code>1</code> Монет-Кейс, потрачено: <code>90</code> монет</b>")
            moneti -= 90
            monetcase += 1
            self.set("moneti", moneti)
            self.set("monetcase", monetcase)
