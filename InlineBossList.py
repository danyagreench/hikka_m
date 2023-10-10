# ---------------------------------------------------------------------------------
# ( o.o )  🔓 Not licensed.
#  > ^ <   ⚠️ Owner of heta.hikariatama.ru doesn't take any responsibilities or intellectual property rights regarding this script
# ---------------------------------------------------------------------------------
# Author: danyagreench
# Commands:
# .bosslist | helpibl
# ---------------------------------------------------------------------------------

#             █ █ ▀ █▄▀ █▄▀ ▄▀█    █▀▄▀█
#             █▀█ █ █ █ █ █ █▀█ ▄▄ █   █
# ---------------------------------------------------------------------------------------------

# версия модуля
__version__ = (6, 6, 6)
# meta developer: @hikka_m
# only hikka

# импортируем библиотеки
import asyncio
import re
from telethon.tl.types import Message, ChatAdminRights
from telethon import functions
import logging
import argparse
from asyncio import sleep
from .. import loader, utils
from ..inline.types import InlineCall

logger = logging.getLogger(__name__)

@loader.tds
class InlineBossList(loader.Module):
    """Модуль для MineEVO / Инлайн босс лист"""
    strings = {
        "name" : "InlineBossList",
        'gif_inline' : 'Босс Лист в inline',
        'thank_you': "Не трогайте это!",
    }
    
    


    async def client_ready(self):
        
        self._backup_channel, _ = await utils.asset_channel(
            self._client,
            "InlineBossList",
            "Группа для работы модуля InlineBossList от @hikka_m\nНе добавляйте сюда других людей или ботов!",
            silent=True,
            archive=True,
            _folder="hikka",
        )

        await self.client(functions.channels.InviteToChannelRequest(self._backup_channel, ['@mine_evo_bot']))
        await self.client(functions.channels.EditAdminRequest(
                channel=self._backup_channel,
                user_id="@mine_evo_bot",
                admin_rights=ChatAdminRights(ban_users=True, post_messages=True, edit_messages=True),
                rank="MineEVO",
            )
        )
        thank = self.config['thank_you']
        if thank == True:
            self.config['thank_you'] = False
            await self.client.send_message('me','<emoji document_id=5465465194056525619>👍</emoji><b>, Модуль InlineBossList успешно установлен!\nОбратите внимание, если у вас нету привилегиии Спонсор или выше, то модуль не будет работать.</b>')
        
        
        

    def __init__(self):
        self.config = loader.ModuleConfig(
            loader.ConfigValue(
                "thank_you", True,
                lambda: self.strings("thank_you"),
                validator=loader.validators.Boolean()
            ),
            
        )
        @loader.command()
    async def helpibl(self, message):
    	''' - помощь по модулю'''
    	await utils.answer(message,f"<b>Помощь по модулю InlineBossList</b>\n\n• <b>Если у вас перестал работать Инлайн Босс Лист, и показывает ошибку, просит посмотреть логи, зайдите в группу в архиве, которую создал модуль «InlineBossList», и удалите там сообщение последнее, которое было от вас, скорее всего перестало работать только из-за того что бот MineEVO не скинул босс лист.</b>")
    @loader.command(alias = 'bl')    
    async def bosslist(self, message):
        ''' - инлайн босс лист'''
        gif_on_top = self.config['gif_inline']

        await self.inline.form(
            text = 'Нажмите Босс Лист',
            gif = gif_on_top,
            message=message,
            reply_markup=[
                [
                    {
                        "text": "💀 Босс лист",
                        "callback": self.list,
                    },
                ],              
                [
                    {
                        "text": "🔻 Закрыть",
                        "action": "close",
                    }
                ],
            ],
        )
    async def list(self, call: InlineCall):
        async with self.client.conversation(self._backup_channel) as conv:
                await conv.send_message(f'Босс лист')
                response = (await conv.get_response()).message
        await call.edit(
            text=response,
            reply_markup=[
                [
                    {
                        "text": "🔄 Обновить",
                        "callback": self.obnovit,
                    },
                ],               
                [
                    {
                        "text": "🔻 Закрыть",
                        "action": "close",
                    }
                ],
            ],
        )    
    async def obnovit(self, call: InlineCall):
        async with self.client.conversation(self._backup_channel) as conv:
                await conv.send_message(f'Босс лист')
                response = (await conv.get_response()).message
        await call.edit(
            text=response,
            reply_markup=[
                [
                    {
                        "text": "🔄 Обновить",
                        "callback": self.list,
                    },
                ],               
                [
                    {
                        "text": "🔻 Закрыть",
                        "action": "close",
                    }
                ],
            ],
        )    
