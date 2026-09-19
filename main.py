import time
import random
import json
import urllib.request
from unixgram import Bot
from unixgram.exceptions import NetworkError, ApiError

BOT_TOKEN = "1285176092:DYVrQkYroDYjS5QRchrCWotNyoxrHs9U"
bot = Bot(BOT_TOKEN)

KNOWN_USERS = {}
PENDING_GAMES = {}

FACTS = [
    {"q": "Столица Австралии — Сидней", "a": False},
    {"q": "Водород — самый распространённый элемент во Вселенной", "a": True},
    {"q": "У крокодилов нет потовых желёз", "a": True},
    {"q": "Верхняя часть Эйфелевой башни зимой отклоняется от вертикали на ~15 см из-за расширения металла от солнца", "a": True},
    {"q": "Осьминоги имеют три сердца", "a": True},
    {"q": "Нильский крокодил может жить без еды до трёх лет", "a": True},
    {"q": "Бананы — это ягоды, а клубника — нет", "a": True},
    {"q": "На Луне есть атмосфера", "a": False},
    {"q": "Пчёлы умеют летать со скоростью до 30 км/ч", "a": True},
    {"q": "Калории — это мера веса", "a": False},
    {"q": "У слонов есть только один сезон размножения в году", "a": False},
    {"q": "Айсберг на 90% скрыт под водой", "a": True},
    {"q": "Пирамида Хеопса — самое большое сооружение из когда-либо построенных человеком", "a": False},
    {"q": "В Южной Африке 11 официальных языков", "a": True},
    {"q": "Белые медведи — единственные медведи, которые считаются морскими млекопитающими", "a": True},
    {"q": "Земля вращается вокруг Солнца со скоростью около 30 км/с", "a": True},
    {"q": "Самая длинная река в мире — Амазонка", "a": True},
    {"q": "У кошек 200 костей в скелете", "a": True},
    {"q": "Солнце — это звезда второго типа", "a": True},
    {"q": "В космосе можно услышать взрывы звёзд", "a": False},
    {"q": "Горячая вода замерзает быстрее холодной (эффектом Пампера)", "a": True},
    {"q": "В중앙альной Африке нет пустынь", "a": False},
    {"q": "Собаки не видят цвета — только чёрно-белое", "a": True},
    {"q": "Человек использует только 10% мозга", "a": False},
    {"q": "У дельфинов есть лёгкие и они дышат воздухом", "a": True},
    {"q": "Каша из гречки на самом деле семена травы, а не зерно", "a": True},
    {"q": "На Марсе есть вулканы", "a": True},
    {"q": "Человек может жить без воды дольше, чем без еды", "a": False},
    {"q": "Титаник был самым большим кораблём своего времени", "a": True},
    {"q": "В Антарктиде нет постоянно проживающего населения", "a": True},
    {"q": "Крысы могут жить без воды дольше, чем верблюды", "a": True},
    {"q": "У верблюдов два горба", "a": True},
    {"q": "Луна вращается вокруг Земли примерно за 27 суток", "a": True},
    {"q": "Во рту человека обитает больше бактерий, чем людей на Земле", "a": True},
    {"q": "Рост человека уменьшается к вечеру", "a": True},
    {"q": "Пингвины — единственные птицы, которые летают вниз головой", "a": False},
    {"q": "Одно дерево может производить кислород для двух человек в год", "a": True},
    {"q": "Вещество, из которого состоят рога носорога, тот же белок, что и в ногтях человека", "a": True},
    {"q": "Некоторые виды черепах могут дышать через задний проход", "a": True},
    {"q": "В состав мёда входит мёртвые пчёлы", "a": True},
]

FILMS = [
    {"t": "Дюна", "y": "2021", "g": "Фантастика", "i": "tt1160419"},
    {"t": "Дюна: Часть вторая", "y": "2024", "g": "Фантастика", "i": "tt15239678"},
    {"t": "Оппенгеймер", "y": "2023", "g": "Биография", "i": "tt15398776"},
    {"t": "Аватар: Путь воды", "y": "2022", "g": "Фантастика", "i": "tt1630029"},
    {"t": "Топ Ган: Мэверик", "y": "2022", "g": "боевик", "i": "tt1745960"},
    {"t": "Бедные-несчастные", "y": "2023", "g": "Драма", "i": "tt14230458"},
    {"t": "Бэтмен", "y": "2022", "g": "боевик", "i": "tt1345836"},
    {"t": "Человек-паук: Нет пути домой", "y": "2021", "g": "боевик", "i": "tt10872600"},
    {"t": "Довод", "y": "2020", "g": "Фантастика", "i": "tt6723592"},
    {"t": "Остров проклятых", "y": "2020", "g": "Триллер", "i": "tt1189340"},
    {"t": "Достать ножи", "y": "2022", "g": "Детектив", "i": "tt11389872"},
    {"t": "Убийцы цветочной луны", "y": "2023", "g": "Драма", "i": "tt1490785"},
    {"t": "Субстанция", "y": "2024", "g": "Ужасы", "i": "tt17526714"},
    {"t": "Анатомия падения", "y": "2023", "g": "Драма", "i": "tt17009711"},
    {"t": "Зона интересов", "y": "2023", "g": "Драма", "i": "tt7180544"},
    {"t": "Солтберн", "y": "2023", "g": "Драма", "i": "tt14849164"},
    {"t": "Май декабрь", "y": "2023", "g": "Драма", "i": "tt13611334"},
    {"t": "Джон Уик 4", "y": "2023", "g": "боевик", "i": "tt10356306"},
    {"t": "Стражи Галактики 3", "y": "2023", "g": "боевик", "i": "tt6791350"},
    {"t": "Флэш", "y": "2023", "g": "боевик", "i": "tt0439572"},
    {"t": "Миссия невыполнима: Племя изгоя", "y": "2023", "g": "боевик", "i": "tt9603778"},
    {"t": "Наполеон", "y": "2023", "g": "Исторический", "i": "tt13435446"},
    {"t": "Убийца", "y": "2023", "g": "боевик", "i": "tt11375946"},
    {"t": "Ребель Муун", "y": "2023", "g": "Фантастика", "i": "tt1603054"},
    {"t": "Гладиатор 2", "y": "2024", "g": "боевик", "i": "tt14849164"},
    {"t": "Фуриоса", "y": "2024", "g": "боевик", "i": "tt12037190"},
    {"t": "Дэдпул и Росомаха", "y": "2024", "g": "боевик", "i": "tt6263850"},
    {"t": "Алиен: Ромул", "y": "2024", "g": "Ужасы", "i": "tt10461735"},
    {"t": "Дикий робот", "y": "2024", "g": "Мультфильм", "i": "tt29623480"},
    {"t": "Внутри себя 2", "y": "2024", "g": "Мультфильм", "i": "tt22022452"},
    {"t": "Дикий робот", "y": "2024", "g": "Мультфильм", "i": "tt29623480"},
    {"t": "Злые волки 4", "y": "2024", "g": "Мультфильм", "i": "tt7189384"},
    {"t": "Человек-клещ 2", "y": "2024", "g": "Комедия", "i": "tt13761951"},
    {"t": "Полицейский из Беверли-Хиллз 4", "y": "2024", "g": "боевик", "i": "tt17548164"},
    {"t": "Тихое место: Начало", "y": "2024", "g": "Ужасы", "i": "tt10359286"},
    {"t": "Кладбище домашних животных: Воскрешение", "y": "2024", "g": "Ужасы", "i": "tt11881192"},
    {"t": "Падение", "y": "2024", "g": "боевик", "i": "tt11301648"},
    {"t": "Химера", "y": "2024", "g": "Ужасы", "i": "tt21371216"},
    {"t": "Офис", "y": "2024", "g": "Комедия", "i": "tt12345678"},
    {"t": "Шогун", "y": "2024", "g": "Драма", "i": "tt27883165"},
    {"t": "Джентльмены", "y": "2024", "g": "боевик", "i": "tt14857708"},
    {"t": "Рипли", "y": "2024", "g": "Триллер", "i": "tt14935602"},
    {"t": "Белый лотос", "y": "2021-2025", "g": "Драма", "i": "tt13238346"},
    {"t": "Дом дракона", "y": "2022-2024", "g": "Фантастика", "i": "tt11198530"},
    {"t": "Фоллаут", "y": "2024", "g": "Фантастика", "i": "tt12637874"},
    {"t": "Пацаны", "y": "2019-2025", "g": "боевик", "i": "tt1190634"},
    {"t": "Последнее из нас", "y": "2023-2025", "g": "Ужасы", "i": "tt3581920"},
    {"t": "Мандалорец", "y": "2019-2025", "g": "Фантастика", "i": "tt1190634"},
    {"t": "Андор", "y": "2022-2025", "g": "Фантастика", "i": "tt2062959"},
    {"t": "Бриджертоны", "y": "2020-2025", "g": "Мелодрама", "i": "tt8740790"},
    {"t": "Тед Лассо", "y": "2020-2023", "g": "Комедия", "i": "tt10972922"},
    {"t": "Корона", "y": "2016-2023", "g": "Драма", "i": "tt4786824"},
    {"t": "Очень странные дела", "y": "2016-2025", "g": "Фантастика", "i": "tt4574334"},
    {"t": "Слово «дирижёр»", "y": "2023", "g": "Драма", "i": "tt11724768"},
    {"t": "Последнее королевство", "y": "2015-2023", "g": "Исторический", "i": "tt4202852"},
    {"t": "Викинги: Вальхалла", "y": "2022-2024", "g": "Исторический", "i": "tt11313232"},
    {"t": "Шерлок", "y": "2010-2017", "g": "Детектив", "i": "tt1475582"},
    {"t": "Игра престолов", "y": "2011-2019", "g": "Фантастика", "i": "tt0944947"},
    {"t": "Во все тяжкие", "y": "2008-2013", "g": "Драма", "i": "tt0903747"},
    {"t": "Настоящий детектив", "y": "2014-2024", "g": "Детектив", "i": "tt2356777"},
    {"t": "Чернобыль", "y": "2019", "g": "Драма", "i": "tt7366378"},
    {"t": "Друзья", "y": "1994-2004", "g": "Комедия", "i": "tt0583459"},
    {"t": "Медведь", "y": "2022-2025", "g": "Комедия", "i": "tt14452776"},
    {"t": "Покерфейс", "y": "2023", "g": "Детектив", "i": "tt14039582"},
    {"t": "Сверхъестественное", "y": "2005-2020", "g": "Ужасы", "i": "tt0460627"},
    {"t": "Доктор Кто", "y": "2005-2025", "g": "Фантастика", "i": "tt0436992"},
    {"t": "Матрёшка", "y": "2019", "g": "Триллер", "i": "tt7704204"},
]

SERIES = [
    {"t": "Шогун", "y": "2024", "g": "Драма", "i": "tt27883165"},
    {"t": "Джентльмены", "y": "2024", "g": "боевик", "i": "tt14857708"},
    {"t": "Рипли", "y": "2024", "g": "Триллер", "i": "tt14935602"},
    {"t": "Белый лотос", "y": "2021-2025", "g": "Драма", "i": "tt13238346"},
    {"t": "Дом дракона", "y": "2022-2024", "g": "Фантастика", "i": "tt11198530"},
    {"t": "Фоллаут", "y": "2024", "g": "Фантастика", "i": "tt12637874"},
    {"t": "Пацаны", "y": "2019-2025", "g": "боевик", "i": "tt1190634"},
    {"t": "Последнее из нас", "y": "2023-2025", "g": "Ужасы", "i": "tt3581920"},
    {"t": "Мандалорец", "y": "2019-2025", "g": "Фантастика", "i": "tt1190634"},
    {"t": "Андор", "y": "2022-2025", "g": "Фантастика", "i": "tt2062959"},
    {"t": "Бриджертоны", "y": "2020-2025", "g": "Мелодрама", "i": "tt8740790"},
    {"t": "Тед Лассо", "y": "2020-2023", "g": "Комедия", "i": "tt10972922"},
    {"t": "Корона", "y": "2016-2023", "g": "Драма", "i": "tt4786824"},
    {"t": "Очень странные дела", "y": "2016-2025", "g": "Фантастика", "i": "tt4574334"},
    {"t": "Слово «дирижёр»", "y": "2023", "g": "Драма", "i": "tt11724768"},
    {"t": "Последнее королевство", "y": "2015-2023", "g": "Исторический", "i": "tt4202852"},
    {"t": "Викинги: Вальхалла", "y": "2022-2024", "g": "Исторический", "i": "tt11313232"},
    {"t": "Шерлок", "y": "2010-2017", "g": "Детектив", "i": "tt1475582"},
    {"t": "Игра престолов", "y": "2011-2019", "g": "Фантастика", "i": "tt0944947"},
    {"t": "Во все тяжкие", "y": "2008-2013", "g": "Драма", "i": "tt0903747"},
    {"t": "Настоящий детектив", "y": "2014-2024", "g": "Детектив", "i": "tt2356777"},
    {"t": "Чернобыль", "y": "2019", "g": "Драма", "i": "tt7366378"},
    {"t": "Друзья", "y": "1994-2004", "g": "Комедия", "i": "tt0583459"},
    {"t": "Медведь", "y": "2022-2025", "g": "Комедия", "i": "tt14452776"},
    {"t": "Покерфейс", "y": "2023", "g": "Детектив", "i": "tt14039582"},
    {"t": "Сверхъестественное", "y": "2005-2020", "g": "Ужасы", "i": "tt0460627"},
    {"t": "Доктор Кто", "y": "2005-2025", "g": "Фантастика", "i": "tt0436992"},
    {"t": "Матрёшка", "y": "2019", "g": "Триллер", "i": "tt7704204"},
]

def say(cid, text, parse_mode=None):
    try:
        bot.send_message(cid, text, parse_mode=parse_mode)
    except Exception as e:
        print(f"[!] send error: {e}", flush=True)

def filmru_url(title):
    import urllib.parse
    return f"https://www.film.ru/search/result?text={urllib.parse.quote(title)}&type=all&s=rel"

@bot.message_handler()
def handle(message):
    text = (message.text or "").strip()
    cid = message.chat.id
    chat_type = getattr(message.chat, "type", "private")

    msg_id = getattr(message, "message_id", None) or getattr(message, "id", None)
    from_user = getattr(message, "from_user", None) or getattr(message, "from", None)

    if from_user and getattr(from_user, "is_bot", False):
        return
    if from_user and msg_id:
        uid = getattr(from_user, "id", None)
        uname = getattr(from_user, "username", "") or ""
        fname = getattr(from_user, "first_name", "") or ""
        name = f"@{uname}" if uname else fname
        KNOWN_USERS[msg_id] = name
        if uid:
            KNOWN_USERS[uid] = name

    reply = getattr(message, "reply_to_message", None)
    if reply and isinstance(reply, dict):
        rid = reply.get("message_id")
        if rid and rid in KNOWN_USERS:
            pass
        elif rid:
            reply_from = reply.get("from")
            if reply_from:
                ru = reply_from.get("username", "") or ""
                rf = reply_from.get("first_name", "") or ""
                KNOWN_USERS[rid] = f"@{ru}" if ru else rf

    if chat_type == "private":
        if text.startswith("/"):
            cmd = text.split()[0].lstrip("/").split("@")[0].lower()
            if cmd == "хелп++":
                say(cid,
                    "<b>🌺 Мод РП для IrisBot</b>\n\n"
                    "Добавь бота в группу для использования команд.",
                    parse_mode="HTML"
                )
                return
        say(cid, "Чтобы пользоваться ботом, добавьте его в группу.\nСправка по командам: /хелп++")
        return

    if text.startswith("/"):
        cmd = text.split()[0].lstrip("/").split("@")[0].lower()

        if cmd == "привет":
            name = message.from_user.first_name or "чел"
            say(cid, f"Привет, {name}!")
            return

        if cmd == "таро":
            q = text.split(maxsplit=1)[1].strip() if len(text.split()) > 1 else ""
            if not q:
                say(cid, "Напиши вопрос: /таро будет ли дождь?")
                return
            answer = random.choice(["Да", "Нет", "Возможно", "Скорее да", "Скорее нет", "Точно нет", "Точно да"])
            say(cid, f"🔮 {q}\n\nОтвет: {answer}")
            return

        if cmd == "хелп++":
            say(cid,
                "<b>🌺 Мод РП для IrisBot</b>\n\n"
                "<code>/привет</code> — поздороваться\n\n"
                "<b>🎮 Развлечения</b>\n"
                "<code>/таро</code> — предсказание\n"
                "<code>/котик</code> — рандомный котик\n"
                "<code>/собака</code> — рандомная собака\n"
                "<code>/стрелять</code> — стрельнуть (ответь на сообщение)\n"
                "<code>/гонка</code> — кто первый жмёт /старт\n"
                "<code>/орелрешка @ник</code> — орёл и решка\n"
                "<code>/принять орёл/решка</code> — принять вызов\n"
                "<code>/верю</code> — верю/не верю\n"
                "<code>/B</code> — верю\n"
                "<code>/NB</code> — не верю\n"
                "<code>/результат</code> — показать результат\n\n"
                "<b>🎬 Что посмотреть</b>\n"
                "<code>/фильм</code> — фильм на вечер\n"
                "<code>/сериал</code> — сериал на вечер\n\n"
                "<code>/хелп++</code> — эта справка",
                parse_mode="HTML"
            )
            return

        if cmd == "котик":
            try:
                req = urllib.request.Request(
                    "https://api.thecatapi.com/v1/images/search",
                    headers={"User-Agent": "Mozilla/5.0"}
                )
                with urllib.request.urlopen(req, timeout=10) as resp:
                    data = json.loads(resp.read())
                bot.send_photo(cid, data[0]["url"])
            except Exception as e:
                print(f"[!] cat error: {e}", flush=True)
                say(cid, "Не удалось загрузить котика :(")
            return

        if cmd == "собака":
            try:
                req = urllib.request.Request(
                    "https://dog.ceo/api/breeds/image/random",
                    headers={"User-Agent": "Mozilla/5.0"}
                )
                with urllib.request.urlopen(req, timeout=10) as resp:
                    data = json.loads(resp.read())
                bot.send_photo(cid, data["message"])
            except Exception as e:
                print(f"[!] dog error: {e}", flush=True)
                say(cid, "Не удалось загрузить собаку :(")
            return

        if cmd == "стрелять":
            shooter = "Кто-то"
            if from_user:
                shooter = getattr(from_user, "first_name", None) or getattr(from_user, "username", None) or "Кто-то"

            target = None
            reply = getattr(message, "reply_to_message", None)

            if reply:
                rid = None
                if isinstance(reply, dict):
                    rid = reply.get("message_id")
                else:
                    rid = getattr(reply, "message_id", None) or getattr(reply, "id", None)
                if rid and rid in KNOWN_USERS:
                    target = KNOWN_USERS[rid]

            if not target:
                parts = text.split(maxsplit=1)
                if len(parts) > 1:
                    t = parts[1].strip().lstrip("@").split()[0]
                    if t:
                        target = f"@{t}"

            if not target and reply:
                target = "незнакомец"

            if not target:
                say(cid, "Ответь на сообщение или напиши: /стрелять @ник")
                return

            actions = [
                f"🔫 {shooter} стрельнул в {target}!\n\n💥 {target} поражён!",
                f"🔫 {shooter} стрельнул в {target}!\n\n🛡️ {target} увернулся!",
                f"🔫 {shooter} стрельнул в {target}!\n\n💀 Промах!",
                f"🔀 {shooter} промахнулся и попал в себя!",
                f"🔫 {shooter} стрельнул в {target}!\n\n❤️ {target} влюбился!",
                f"🔫 {shooter} стрельнул в {target}!\n\n🤕 {target} ранен!",
                f"🔫 {shooter} стрельнул в {target}!\n\n😂 {target} посмеялся и ушёл.",
                f"🔫 {shooter} стрельнул в {target}!\n\n💀 {target} eliminated.",
                f"🔫 {shooter} стрельнул в {target}!\n\n✨ Произошло что-то странное...",
                f"🔫 {shooter} стрельнул в {target}!\n\n🩹 {target} выжил, но еле-еле.",
                f"🔫 {shooter} стрельнул в {target}!\n\n🎯 Точное попадание!",
            ]
            say(cid, random.choice(actions))
            return

        if cmd == "гонка":
            RACES = getattr(handle, '_races', {})
            old = RACES.get(cid)
            if old and not old.get("winner") and time.time() < old["start"] + 15:
                say(cid, "Гонка уже идёт! Жми /старт!")
                return
            delay = random.randint(3, 5)
            RACES[cid] = {"start": time.time() + delay, "winner": None}
            handle._races = RACES
            say(cid, f"🏁 Гонка через {delay}...")
            return

        if cmd == "старт":
            RACES = getattr(handle, '_races', {})
            race = RACES.get(cid)
            if not race:
                return
            if race["winner"]:
                return
            now = time.time()
            if now < race["start"]:
                say(cid, "Гонка ещё не началась! Подожди.")
                return
            if now - race["start"] > 10:
                del RACES[cid]
                say(cid, "⏰ Гонка окончена. Никто не добежал.")
                return
            name = "Кто-то"
            if from_user:
                name = getattr(from_user, "first_name", None) or getattr(from_user, "username", None) or "Кто-то"
            race["winner"] = name
            say(cid, f"🥇 <b>{name}</b> победил в гонке!", parse_mode="HTML")
            return

        if cmd == "орелрешка":
            parts = text.split(maxsplit=1)
            if len(parts) < 2 or not parts[1].strip().lstrip("@").split()[0]:
                say(cid, "Напиши: /орелрешка @username")
                return
            target_nick = parts[1].strip().lstrip("@").split()[0].lower()
            challenger = "Кто-то"
            challenger_id = None
            if from_user:
                challenger = getattr(from_user, "first_name", None) or getattr(from_user, "username", None) or "Кто-то"
                challenger_id = getattr(from_user, "id", None)
            PENDING_GAMES[cid] = {
                "challenger": challenger,
                "challenger_id": challenger_id,
                "target_nick": target_nick,
                "time": time.time(),
            }
            say(cid, f"🪙 {challenger} предлагает сыграть в Орёл и Решку!\n\n@{target_nick} напиши /принять чтобы играть (2 минуты)")
            return

        if cmd == "принять":
            game = PENDING_GAMES.get(cid)
            if not game:
                say(cid, "Нет активных игр. Напиши /орелрешка @username чтобы начать.")
                return
            if time.time() - game["time"] > 120:
                del PENDING_GAMES[cid]
                say(cid, "Время вышло. Игра отменена.")
                return
            accepted = False
            if from_user:
                uid = getattr(from_user, "id", None)
                uname = (getattr(from_user, "username", "") or "").lower()
                if uname == game["target_nick"] or uid == game.get("challenger_id"):
                    accepted = True
            if not accepted:
                say(cid, "Это предложение не тебе. Используй /орелрешка чтобы начать свою.")
                return

            parts = text.split(maxsplit=1)
            side = None
            if len(parts) > 1:
                s = parts[1].strip().lower()
                if s in ("орёл", "орел", "ори", "heads"):
                    side = "орёл"
                elif s in ("решка", "tails", "решк"):
                    side = "решка"

            if not side:
                say(cid, "Выбери сторону: /принять орёл или /принять решка")
                return

            del PENDING_GAMES[cid]
            challenger = game["challenger"]
            acceptor = "Кто-то"
            if from_user:
                acceptor = getattr(from_user, "first_name", None) or getattr(from_user, "username", None) or "Кто-то"

            acceptor_side = side
            challenger_side = "решка" if side == "орёл" else "орёл"
            result = random.choice(["орёл", "решка"])
            if result == challenger_side:
                winner = challenger
            else:
                winner = acceptor
            say(cid,
                f"🪙 {challenger} vs {acceptor}!\n\n"
                f"{challenger} — {challenger_side}\n"
                f"{acceptor} — {acceptor_side}\n\n"
                f"Крутим...\n\n"
                f"Выпало: <b>{result}</b>!\n\n"
                f"🏆 Победил: {winner}",
                parse_mode="HTML"
            )
            return

        if cmd == "верю":
            GAME_STATE = getattr(handle, '_game_state', {})
            old_game = GAME_STATE.get(cid)
            if old_game:
                elapsed = time.time() - old_game["time"]
                if elapsed > 30:
                    players = old_game["players"]
                    answer = old_game["answer"]
                    del GAME_STATE[cid]
                    answer_text = "Правда ✅" if answer == "True" else "Ложь ❌"
                    if not players:
                        say(cid,
                            f"🧠 <b>Время вышло!</b>\n\n"
                            f"Никто не успел ответить.\n\n"
                            f"Ответ: <b>{answer_text}</b>",
                            parse_mode="HTML"
                        )
                    else:
                        correct = []
                        wrong = []
                        for name, vote in players.items():
                            if (vote == "В" and answer == "True") or (vote == "НВ" and answer == "False"):
                                correct.append(name)
                            else:
                                wrong.append(name)
                        correct_text = "\n".join(f"✅ {n}" for n in correct) if correct else "Никто"
                        wrong_text = "\n".join(f"❌ {n}" for n in wrong) if wrong else "Никто"
                        say(cid,
                            f"🧠 <b>Время вышло!</b>\n\n"
                            f"Ответ: <b>{answer_text}</b>\n\n"
                            f"Угадали:\n{correct_text}\n\n"
                            f"Не угадали:\n{wrong_text}",
                            parse_mode="HTML"
                        )
                else:
                    say(cid, "Игра уже идёт. Дождись результата.")
                    return
            fact = random.choice(FACTS)
            answer = "True" if fact["a"] else "False"
            GAME_STATE[cid] = {
                "answer": answer,
                "time": time.time(),
                "players": {},
            }
            handle._game_state = GAME_STATE
            say(cid,
                f"🧠 <b>Верю/Не верю</b>\n\n"
                f"{fact['q']}\n\n"
                f"Отвечай: <b>/B</b> (верю) или <b>/NB</b> (не верю)\n"
                f"30 секунд на ответ!",
                parse_mode="HTML"
            )
            return

        if cmd in ("b", "nb"):
            GAME_STATE = getattr(handle, '_game_state', {})
            game = GAME_STATE.get(cid)
            if not game:
                return
            elapsed = time.time() - game["time"]
            if elapsed > 30:
                players = game["players"]
                answer = game["answer"]
                del GAME_STATE[cid]
                answer_text = "Правда ✅" if answer == "True" else "Ложь ❌"
                if not players:
                    say(cid,
                        f"🧠 <b>Время вышло!</b>\n\n"
                        f"Никто не успел ответить.\n\n"
                        f"Ответ: <b>{answer_text}</b>",
                        parse_mode="HTML"
                    )
                else:
                    correct = []
                    wrong = []
                    for name, vote in players.items():
                        if (vote == "В" and answer == "True") or (vote == "НВ" and answer == "False"):
                            correct.append(name)
                        else:
                            wrong.append(name)
                    correct_text = "\n".join(f"✅ {n}" for n in correct) if correct else "Никто"
                    wrong_text = "\n".join(f"❌ {n}" for n in wrong) if wrong else "Никто"
                    say(cid,
                        f"🧠 <b>Время вышло!</b>\n\n"
                        f"Ответ: <b>{answer_text}</b>\n\n"
                        f"Угадали:\n{correct_text}\n\n"
                        f"Не угадали:\n{wrong_text}",
                        parse_mode="HTML"
                    )
                return
            uname = "Кто-то"
            if from_user:
                uname = getattr(from_user, "username", "") or getattr(from_user, "first_name", "") or "Кто-то"
            if uname in game["players"]:
                say(cid, "Ты уже ответил!")
                return
            vote = "В" if cmd == "b" else "НВ"
            game["players"][uname] = vote
            say(cid, f"✅ {uname} проголосовал")
            return

        if cmd == "результат":
            GAME_STATE = getattr(handle, '_game_state', {})
            game = GAME_STATE.get(cid)
            if not game:
                say(cid, "Нет активной игры. Напиши /верю чтобы начать.")
                return
            elapsed = time.time() - game["time"]
            answer = game["answer"]
            players = game["players"]
            correct = []
            wrong = []
            for name, vote in players.items():
                if (vote == "В" and answer == "True") or (vote == "НВ" and answer == "False"):
                    correct.append(name)
                else:
                    wrong.append(name)
            del GAME_STATE[cid]
            answer_text = "Правда ✅" if answer == "True" else "Ложь ❌"
            header = "🧠 <b>Результат</b>" if elapsed <= 30 else "🧠 <b>Время вышло!</b>"
            if not players:
                say(cid,
                    f"{header}\n\n"
                    f"Никто не успел ответить.\n\n"
                    f"Ответ: <b>{answer_text}</b>",
                    parse_mode="HTML"
                )
            else:
                correct_text = "\n".join(f"✅ {n}" for n in correct) if correct else "Никто"
                wrong_text = "\n".join(f"❌ {n}" for n in wrong) if wrong else "Никто"
                say(cid,
                    f"{header}\n\n"
                    f"Ответ: <b>{answer_text}</b>\n\n"
                    f"Угадали:\n{correct_text}\n\n"
                    f"Не угадали:\n{wrong_text}",
                    parse_mode="HTML"
                )
            return

        if cmd == "фильм":
            f = random.choice(FILMS)
            url = filmru_url(f['t'])
            say(cid,
                f"🎬 <b>{f['t']}</b> ({f['y']})\n"
                f"Жанр: {f['g']}\n\n"
                f"<a href=\"{url}\">🔗 Смотреть на Film.ru</a>",
                parse_mode="HTML"
            )
            return

        if cmd == "сериал":
            s = random.choice(SERIES)
            url = filmru_url(s['t'])
            say(cid,
                f"📺 <b>{s['t']}</b> ({s['y']})\n"
                f"Жанр: {s['g']}\n\n"
                f"<a href=\"{url}\">🔗 Смотреть на Film.ru</a>",
                parse_mode="HTML"
            )
            return

try:
    bot.set_my_commands([
        {"command": "привет", "description": "поздороваться"},
        {"command": "таро", "description": "задать вопрос"},
        {"command": "котик", "description": "рандомный котик"},
        {"command": "собака", "description": "рандомная собака"},
        {"command": "стрелять", "description": "стрельнуть (ответь на сообщение)"},
        {"command": "гонка", "description": "кто первый жмёт /старт"},
        {"command": "орелрешка", "description": "орёл и решка"},
        {"command": "принять", "description": "принять вызов"},
        {"command": "верю", "description": "верю/не верю"},
        {"command": "результат", "description": "результат викторины"},
        {"command": "фильм", "description": "фильм на вечер"},
        {"command": "сериал", "description": "сериал на вечер"},
        {"command": "хелп++", "description": "справка"},
    ])
except Exception:
    pass

while True:
    try:
        print("запускаю опрос…", flush=True)
        bot.polling()
    except KeyboardInterrupt:
        break
    except Exception as e:
        print("обрыв:", e, flush=True)
        time.sleep(5)
