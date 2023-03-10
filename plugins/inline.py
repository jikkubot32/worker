import logging
from pyrogram import Client, emoji, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, InlineQueryResultCachedDocument, InlineQueryResultArticle, InputTextMessageContent, InlineQueryResultPhoto
from pyrogram.errors.exceptions.bad_request_400 import QueryIdInvalid
import re
from utils import get_search_results, is_subscribed, get_post
from info import CACHE_TIME, AUTH_USERS, AUTH_CHANNEL, CUSTOM_FILE_CAPTION
logger = logging.getLogger(__name__)
cache_time = 0 if AUTH_USERS or AUTH_CHANNEL else CACHE_TIME

@Client.on_inline_query(filters.user(AUTH_USERS) if AUTH_USERS else None)
async def answer(bot, query):
    """Show search results for given inline query"""

    if AUTH_CHANNEL and not await is_subscribed(bot, query):
        await query.answer(results=[],
                           cache_time=0,
                           switch_pm_text='join main group đŞ then use đ',
                           switch_pm_parameter="join")
        return

    results = []
    nd = []
    buttons = [[InlineKeyboardButton("É˘Ęá´á´á´Š", url="https://t.me/+eDjzTT2Ua6kwMTI1")]]
    nd.append(
        InlineQueryResultArticle(
            title="request on group đŞ",
            thumb_url="https://telegra.ph/file/d651c3858b99538bdb311.jpg",
            description="ask movie/series in group",
            input_message_content=InputTextMessageContent(
                message_text="**request on group**đŞ đ",
                disable_web_page_preview=True),
                reply_markup=InlineKeyboardMarkup(buttons)))
    if '|' in query.query:
        string, file_type = query.query.split('|', maxsplit=1)
        string = string.strip()
        file_type = file_type.strip().lower()
    elif '++' in query.query:       
        me, string = query.query.split('++', maxsplit=1)
        vie = string.strip()
        if len(vie) <= 2:
            return
        movies = await get_post(vie, bulk=True)
        # imdbcap = f"**{movie}**\n\n**ââ/yá´á´Ę: {imdb['year']}**\n**â |Ęá´á´ÉŞÉ´É˘âââââ: {imdb['rating']}/10ââââ**\n**â\É˘á´É´Ęá´: #{imdb['genres']}**\n\n__Ęá´É´á´ÉŞá´á´: {imdb['runtime']}á´ÉŞÉ´__\n __Ęá´É´É˘á´á´É˘á´ęą: #{imdb['languages']}__\n đĄ__Ęá´Ęá´á´ęąá´ á´á´á´á´: {imdb['release_date']}__\n\n**đżĘĘâ[đžÉ´đ°ÉŞĘ_đÉŞĘá´á´Ęáľáľáľ](https://t.me/On_air_Filter_bot)**"
        if not movies:
            await query.answer(results=[],
                               cache_time=0,
                               switch_pm_text='No imdb Results',
                               switch_pm_parameter="okay")
            return
        for movie in movies:
            titl = movie.get('title').strip()
            year = movie.get('year')
            title = f"{titl} {year}"
            mid = movie.movieID
            imdb = await get_post(mid, id=True)
            poster=None
            if imdb:
               imdbcap = f"**{titl}**\n\n**ââ/yá´á´Ę: {year}**\n**â |Ęá´á´ÉŞÉ´É˘âââââ: {imdb['rating']}/10ââââ**\n**â\É˘á´É´Ęá´: #{imdb['genres']}**\n\n__Ęá´É´á´ÉŞá´á´: {imdb['runtime']}á´ÉŞÉ´__\n __Ęá´É´É˘á´á´É˘á´ęą: #{imdb['languages']}__\nđĄ__Ęá´Ęá´á´ęąá´ á´á´á´á´: {imdb['release_date']}__\n\n **đżĘĘâ[đžÉ´đ°ÉŞĘ_đÉŞĘá´á´Ęáľáľáľ](https://t.me/On_air_Filter_bot)**"
               poster = imdb['poster']
               imdbdis = f"Ęá´á´ÉŞÉ´É˘âââââ: {imdb['rating']}/10âââ  É˘á´É´Ęá´: #{imdb['genres']} \n Ęá´É´á´ÉŞá´á´: {imdb['runtime']}á´ÉŞÉ´"
               buttons = [[InlineKeyboardButton("É˘Ęá´á´á´Š 1", url="https://t.me/+PBGW_EV3ldY5YjJl"), InlineKeyboardButton("đŞ ÉŞÉ´ę°á´ ", callback_data=f"imdb#{imdb['imdb_id']}"), InlineKeyboardButton("É˘Ęá´á´á´Š 2", url="https://t.me/+eDjzTT2Ua6kwMTI1")]]
               if not poster:
                   poster = "https://telegra.ph/file/9075ca7cbad944afaa823.jpg"
            else:
               imdbcap = f"**{titl} đż {year}**"
               imdbdis = "None"
               buttons = [[InlineKeyboardButton("É˘Ęá´á´á´Š 1", url="https://t.me/+PBGW_EV3ldY5YjJl"), InlineKeyboardButton("É˘Ęá´á´á´Š 2", url="https://t.me/+eDjzTT2Ua6kwMTI1")]]
               poster = "https://telegra.ph/file/9075ca7cbad944afaa823.jpg"
            results.append(
                InlineQueryResultPhoto(
                    photo_url=poster,
                    thumb_url=poster,
                    title=f"{titl} đż {year}",
                    description=imdbdis,
                    caption=imdbcap,
                    reply_markup=InlineKeyboardMarkup(buttons)))
        try:
            await query.answer(results=results,
                           is_personal = True,                         
                           cache_time=0,
                           switch_pm_text='Ęá´ęąá´Ęá´ęą đ',
                           switch_pm_parameter="start")                         
        except QueryIdInvalid:
            pass
        except Exception as e:
            logging.exception(str(e))
    else:
        string = query.query.strip()
        file_type = None

    offset = int(query.offset or 0)
    reply_markup = get_reply_markup(query=string)
    files, next_offset = await get_search_results(string,
                                                  file_type=file_type,
                                                  max_results=10,
                                                  offset=offset)
    for file in files:
        at = file.file_name
        title = re.sub(r"(#|\@|\~|\ÂŠ|\[|\]|\_|\.)", " ", at, flags=re.IGNORECASE)
        size = file.file_size        
        results.append(
            InlineQueryResultCachedDocument(
                title=title,
                file_id=file.file_id,
                caption=f"<u><b>#đľđ¸đťđ´_đ˝đ°đźđ´â{title}</b></u>\n\n <b>âĄď¸ĘĘâ[đžÉ´đ°ÉŞĘ_đÉŞĘá´á´Ęáľáľáľ](https://t.me/On_air_Filter_bot)</b>\n\n<b>âĄ ă¤Â Â  âă¤Â Â Â Â  âÂ Â Â Â Â  â˛\nËĄáśŚáľáľÂ  áśáľáľáľáľâżáľÂ Â  Ë˘áľáľáľÂ Â  Ë˘Ę°áľĘłáľ</b>",
                description=f'đż {file.file_type} Size: {get_size(file.file_size)}',
                reply_markup=reply_markup))
    if results:
        switch_pm_text = f"results"
        if string:
            switch_pm_text += f" for {string}"
        try:
            await query.answer(results=results,
                           is_personal = True,
                           cache_time=cache_time,
                           switch_pm_text=switch_pm_text,
                           switch_pm_parameter="start",
                           next_offset=str(next_offset))
        except QueryIdInvalid:
            pass
        except Exception as e:
            logging.exception(str(e))
    else:
        switch_pm_text = f'{emoji.CROSS_MARK} No results'
        if string:
            switch_pm_text += f' for "{string}"'
        try:
            await query.answer(results=nd,
                           is_personal = True,
                           cache_time=cache_time,
                           switch_pm_text=switch_pm_text,
                           switch_pm_parameter="okay")
        except QueryIdInvalid:
            pass
        except Exception as e:
            logging.exception(str(e))

def get_reply_markup(query):
    buttons = [[InlineKeyboardButton("É˘Ęá´á´á´Š 1", url="https://t.me/+PBGW_EV3ldY5YjJl"), InlineKeyboardButton("É˘Ęá´á´á´Š 2", url="https://t.me/+eDjzTT2Ua6kwMTI1")]]
    """buttons += [
        [
            InlineKeyboardButton('đ đđ´đ°đđ˛đˇ ę°ÉŞĘá´ đ', switch_inline_query_current_chat=query)
        ]
        ]"""
    return InlineKeyboardMarkup(buttons)


def get_size(size):
    """Get size in readable format"""

    units = ["Bytes", "á´Ę", "á´Ę", "É˘Ę", "TB", "PB", "EB"]
    size = float(size)
    i = 0
    while size >= 1024.0 and i < len(units):
        i += 1
        size /= 1024.0
    return "%.2f %s" % (size, units[i])
