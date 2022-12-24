#Загружаемые модули
#pyTelegramBotAPI
#requests bs4
#pyshorteners
#wget

#Импорты
import asyncore #import file_dispatcher
import telebot
import requests
from telebot import types
import config
import datetime
import requests
import pyshorteners
from urllib.parse import urlparse, urljoin
from bs4 import BeautifulSoup


global scheduleSolar
global scheduleSolarChange
global scheduleShabulino
global scheduleShabulinoChange

global fileLink

bot = telebot.TeleBot(config.TOKEN)

#Обработка комманды старт
@bot.message_handler(commands=['start'])
def welcome(message):
    #Стикер
    sti = open('static/welcome.webp', 'rb')
    bot.send_sticker(message.chat.id, sti)
    #Клавиатура
    markup= types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton("Основная информация")
    item2 = types.KeyboardButton("Профессии")
    item3 = types.KeyboardButton("Специальности")
    item4 = types.KeyboardButton("Зачисление")
    item5 = types.KeyboardButton("Общежитие")
    item6 = types.KeyboardButton("Расписание")
    item7 = types.KeyboardButton("Контакты")

    markup.add(item1, item2, item3, item4, item5, item6, item7)

    #Сообщение
    bot.send_message(message.chat.id,
    """
Вас приветствует команда приёмной комиссии "Рязанского Политехнического Колледжа"
Используйте меню или следующие комманды:
 <b>/info</b> - Основная информация
 <b>/prof</b> - Профессии
 <b>/spec</b> - Специальности
 <b>/enrol</b> - Зачисление
 <b>/hostel</b> - Общежитие
 <b>/sched</b> - Расписание
 <b>/contacts</b> - Контакты
    
Более подробную информацию можете найти здесь: http://polytech-rzn.ru/?page_id=13748
    """, parse_mode = 'html', reply_markup = markup)

#команда информация
@bot.message_handler(commands=['info'])
def command_schedule(message):
    info(message)

#команда профессии
@bot.message_handler(commands=['prof'])
def command_schedule(message):
    prof(message)

#команда специальности
@bot.message_handler(commands=['spec'])
def command_schedule(message):
    spec(message)

#команда зачисление
@bot.message_handler(commands=['enrol'])
def command_schedule(message):
    enrol(message)

#команда общежитие
@bot.message_handler(commands=['hostel'])
def command_schedule(message):
    hostel(message)

#Команда расписания
@bot.message_handler(commands=['sched'])
def command_schedule(message):
    schedule(message)

#Контакты
@bot.message_handler(commands=['contacts'])
def command_schedule(message):
    contacts(message)

#Эхо
#@bot.message_handler(content_types=['text'])
#def repeat(message):
#    bot.send_message(message.chat.id, message.text)

#Реакция на сообщения
@bot.message_handler(content_types=['text'])
def chating(message):
    if message.chat.type == 'private':
        if message.text == 'Основная информация':
            info(message)
        elif message.text == 'Профессии':
            prof(message)
        elif message.text == 'Специальности':
            spec(message)
        elif message.text == 'Зачисление':
            enrol(message)
        elif message.text == 'Общежитие':
            hostel(message)
        elif message.text == 'Расписание':
            schedule(message)
        elif message.text == 'Контакты':
            contacts(message)
        else:
            bot.send_message(message.chat.id,
    """
Воспользуйтесь меню или следующими командами:
 <b>/info</b> - Основная информация
 <b>/prof</b> - Профессии
 <b>/spec</b> - Специальности
 <b>/enrol</b> - Зачисление
 <b>/hostel</b> - Общежитие
 <b>/sched</b> - Расписание
 <b>/contacts</b> - Контакты
    
Более подробную информацию можете найти здесь: http://polytech-rzn.ru/?page_id=13748
    """, parse_mode = 'html')

#Отображение основной информации
def info(message):
    global fileLink

    getLinks('http://polytech-rzn.ru/?page_id=109')
    bot.send_document(message.chat.id, fileLink, caption =
    """
<b>Прием документов для поступления производится несколькими способами</b>:
 Заполнение заявления в колледже;
 Почтой России;
    
<b>График работы приёмной комиссии</b>:
 город Рязань, улица Солнечная, 6
 Понедельник-Пятница 08:00–16:30
 Суббота-Воскресение: выходной
    
<b>Для подачи заявления с помощью Почты России</b>:
 Необходимо отправить письмо по адресу: 390000, Рязанская область, город Рязань, улица Солнечная, 6
 В письме должны присутствовать:
  Заявление;
  Аттестат с приложением (оригинал или ксерокопия);
  Ксерокопия паспорта с пропиской;
  Медицинская справка 086-У (при наличии);
  Фото абитуриента 3х4  6 шт;
    """,
    parse_mode = 'html')

#Отображение профессий
def prof(message):
    #Добавление клавиатуры к сообщению
    markup= types.InlineKeyboardMarkup(row_width=3)
    item1 = types.InlineKeyboardButton("11.01.01 Монтажник радиоэлектронной аппаратуры и приборов", callback_data="11.01.01")
    item2 = types.InlineKeyboardButton("15.01.32 Оператор станков с программным управлением", callback_data="15.01.32")
    item3 = types.InlineKeyboardButton("09.01.03 Мастер по обработке цифровой информации", callback_data="09.01.03")

    markup.add(item1, item2, item3)
    bot.send_message(message.chat.id, "Выберете интересующую вас професию", reply_markup=markup)

#Отображение информации о Специальности
def spec(message):
    #Добавление клавиатуры к сообщению
    markup= types.InlineKeyboardMarkup(row_width=10)
    item1 = types.InlineKeyboardButton("46.02.01 Документационное обеспечение управления и архивоведение", callback_data="46.02.01")
    item2 = types.InlineKeyboardButton("38.02.01 Экономика и бухгалтерский учет (по отраслям)", callback_data="38.02.01")
    item3 = types.InlineKeyboardButton("43.02.13 Технология парикмахерского искусства (ТОП-50)", callback_data="43.02.13")
    item4 = types.InlineKeyboardButton("43.02.12 Технология эстетических услуг (ТОП-50)", callback_data="43.02.12")
    item5 = types.InlineKeyboardButton("15.02.15 Технология металлообрабатывающего производства (ТОП-50)", callback_data="15.02.15")
    item6 = types.InlineKeyboardButton("23.02.05 Эксплуатация транспортного электрооборудования и автоматики (по видам транспорта, за исключением водного)", callback_data="23.02.05")
    item7 = types.InlineKeyboardButton("11.02.16 Монтаж, техническое обслуживание и ремонт электронных приборов и устройств (ТОП-50)", callback_data="11.02.16")
    item8 = types.InlineKeyboardButton("35.02.03 Технология деревообработки", callback_data="35.02.03")
    item9 = types.InlineKeyboardButton("09.02.07 Информационные системы и программирование (ТОП-50)", callback_data="09.02.07")
    item10 = types.InlineKeyboardButton("08.02.09 Монтаж, наладка и эксплуатация электрооборудования промышленных и гражданских зданий", callback_data="08.02.09")

    markup.add(item1, item2, item3, item4, item5, item6, item7, item8, item9, item10)
    bot.send_message(message.chat.id, "Выберете интересующую вас специальность", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: True)
def call_prof(call):
    try:
        button = ""
        if call.message:
            #Професии
            if (call.data == "11.01.01"):
                bot.send_message(
                    call.message.chat.id,
                    """
  <b>11.01.01 Монтажник радиоэлектронной аппаратуры и приборов</b>

<b>Квалификация выпускника</b>:
 Монтажник радиоэлектронной аппаратуры и приборов.

<b>Форма обучения</b>: Очная
<b>Срок обучения</b>: 2 года 10 месяцев (на базе основного общего образования).

<b>Область профессиональной деятельности выпускника</b>:
 Монтаж, сборка, регулировка элементов, узлов, блоков и устройств радиоэлектронной аппаратуры и приборов, их контроль, испытание и проверка качества работы.

<b>Объекты профессиональной деятельности выпускника</b>:
 Узлы, блоки, приборы радиоэлектронной аппаратуры, аппаратуры проводной связи.
 Элементы устройств импульсной и вычислительной техники.
 Электрические монтажные схемы.
 Техническая документация.
 Технологические процессы обслуживания радиоэлектронной аппаратуры и приборов.
 Технологические процессы электрической и механической проверки и регулировки блоков приборов и устройств радиоэлектронной аппаратуры.

<b>В результате изучения дисциплин обучающийся должен</b>:
 <b>Иметь практический опыт</b>:
  Монтажа и демонтажа узлов, блоков, приборов радиоэлектронной аппаратуры, аппаратуры проводной связи, элементов устройств импульсной и вычислительной техники и комплектующих.
  Выполнения типовых слесарных и слесарно-сборочных работ.
  Проверки сборки и монтажа узлов, блоков и элементов радиоэлектронной аппаратуры.
  Монтаж чип-компонентов в современной радиоэлектронной аппаратуре (модемы сотовой связи).

<b>Уметь</b>:
 Выполнять различные виды пайки и лужения.
 Обрабатывать монтажные провода и кабели с полной заделкой и распайкой проводов и соединений для подготовки к монтажу.
 Выполнять правила демонтажа печатных плат.
 Проводить контроль, испытание и проверку радиоэлементов.
 Осуществлять приемку и сдачу обслуживаемой аппаратуры с учетом всех требований согласно схемам, чертежам и техническим условиям.

<b>Знать</b>:
 Общую технологию производства радиоэлектронной аппаратуры и приборов.
 Основные виды сборочных и монтажных работ.
 Виды и назначение электромонтажных материалов.
 Технологию лужения и пайки.
 Сведения о припоях и флюсах, контроль качества паяных соединений.
 Конструктивные виды печатного монтажа, технологию его выполнения.
 Правила и технологию выполнения демонтажа узлов.
 Виды слесарных операций, назначение, приемы и правила выполнения.
 Правила выполнения промежуточного контроля, методы проверки качества монтажа на соответствие технологическим требованиям.
 Требования к качеству выполняемых работ, технические условия на приемку узлов, блоков и приборов радиоэлектронной аппаратуры.

<b>Итоговая аттестация студентов</b>:
Включает защиту выпускной квалификационной работы (выпускная практическая квалификационная работа и письменная экзаменационная работа)
                    """, parse_mode = 'html'
                )
                getLinks("http://polytech-rzn.ru/?page_id=82", "prikaz")
                f1 = fileLink
                getLinks("http://polytech-rzn.ru/?page_id=82", "plan")
                f2 = fileLink
                getLinks("http://polytech-rzn.ru/?page_id=82", "planLong")
                f3= fileLink
                getLinks("http://polytech-rzn.ru/?page_id=82", "ppkrs")
                f4 = fileLink
                bot.send_media_group(call.message.chat.id, [types.InputMediaDocument(f1), types.InputMediaDocument(f2), types.InputMediaDocument(f3), types.InputMediaDocument(f4)])

                button = "11.01.01 Монтажник радиоэлектронной аппаратуры и приборов"

            elif (call.data == "15.01.32"):
                sti = open('static/outoforder.webp', 'rb')
                bot.send_sticker(call.message.chat.id, sti)
                bot.send_message(call.message.chat.id, "Раздел ещё редактируется")
                button = "15.01.32 Оператор станков с программным управлением"

            elif (call.data == "09.01.03"):
                bot.send_message(call.message.chat.id,
                """
  <b>09.01.03 Мастер по обработке цифровой информации</b>

<b>Квалификация выпускника</b>:
Оператор электронно-вычислительных и вычислительных машин

<b>Форма обучения</b>: Очная.
<b>Срок обучения</b>: 2 года 10 месяцев (на базе основного общего образования).

<b>Область профессиональной деятельности выпускника</b>:
 Ввод, хранение, обработка, передача и публикация цифровой информации, в т.ч. звука, изображений, видео и мультимедиа на персональном компьютере, а также в локальных и глобальных компьютерных сетях.

<b>Объекты профессиональной деятельности выпускника</b>:
 Аппаратное и программное обеспечение персональных компьютеров и серверов;
 Периферийное оборудование;
 Источники аудиовизуальной информации;
 Звуко- и видеозаписывающее и воспроизводящее мультимедийное оборудование;
 Информационные ресурсы локальных и глобальных компьютерных сетей.

<b>В результате изучения профессиональных модулей обучающийся должен</b>:
 <b>Иметь практический опыт</b>:
  Подключения кабельной системы персонального компьютера, периферийного и мультимедийного оборудования;
  Настройки параметров функционирования персонального компьютера, периферийного и мультимедийного оборудования;
  Ввода цифровой и аналоговой информации в персональный компьютер с различных носителей, периферийного и мультимедийного оборудования;
  Сканирования, обработки и распознавания документов;
  Конвертирования медиафайлов в различные форматы, экспорта и импорта файлов в различные программы-редакторы;
  Обработки аудио-, визуального и мультимедийного контента с помощью специализированных программ-редакторов;
  Создания и воспроизведения видеороликов, презентаций, слайд-шоу, медиафайлов и другой итоговой продукции из исходных аудио, визуальных и мультимедийных компонентов;
  Осуществления навигации по ресурсам, поиска, ввода и передачи данных с помощью технологий и сервисов сети Интернет;
  Управления медиатекой цифровой информации;
  Передачи и размещения цифровой информации;
  Тиражирования мультимедиа контента на съемных носителях информации;
  Осуществления навигации по ресурсам, поиска, ввода и передачи данных с помощью технологий и сервисов сети Интернет;
  Публикации мультимедиа контента в сети Интернет;
  Обеспечения информационной безопасности;
  Подключать периферийные устройства и мультимедийное оборудование к персональному компьютеру и настраивать режимы их работы;
  Создавать и структурировать хранение цифровой информации в медиатеке персональных компьютеров и серверов;
  Передавать и размещать цифровую информацию на дисках персонального компьютера, а также дисковых хранилищах локальной и глобальной компьютерной сети;
  Тиражировать мультимедиа контент на различных съемных носителях информации;
  Осуществлять навигацию по веб-ресурсам Интернета с помощью веб-браузера;
  Создавать и обмениваться письмами электронной почты;
  Публиковать мультимедиа контент на различных сервисах в сети Интернет;
  Осуществлять резервное копирование и восстановление данных;
  Осуществлять антивирусную защиту персонального компьютера с помощью антивирусных программ;
  Осуществлять мероприятия по защите персональных данных;
  Вести отчетную и техническую документацию;
""", parse_mode = 'html'
)
                bot.send_message(call.message.chat.id,
                """
<b>Уметь</b>:
 Подключать и настраивать параметры функционирования персонального компьютера, периферийного и мультимедийного оборудования;
 Настраивать основные компоненты графического интерфейса операционной системы и специализированных программ-редакторов;
 Управлять файлами данных на локальных, съемных запоминающих устройствах, а также на дисках локальной компьютерной сети и в сети Интернет;
 Производить распечатку, копирование и тиражирование документов на принтере и других периферийных устройствах вывода;
 Распознавать сканированные текстовые документы с помощью программ распознавания текста;
 Вводить цифровую и аналоговую информацию в персональный компьютер с различных носителей, периферийного и мультимедийного оборудования;
 Создавать и редактировать графические объекты с помощью программ для обработки растровой и векторной графики;
 Конвертировать файлы с цифровой информацией в различные форматы;
 Производить сканирование прозрачных и непрозрачных оригиналов;
 Производить съемку и передачу цифровых изображений с фото- и видеокамеры на персональный компьютер;
 Обрабатывать аудио, визуальный контент и медиафайлы средствами звуковых, графических и видео-редакторов;
 Создавать видеоролики, презентации, слайд-шоу, медиафайлы и другую итоговую продукцию из исходных аудио, визуальных и мультимедийных компонентов;
 Воспроизводить аудио, визуальный контент и медиафайлы средствами персонального компьютера и мультимедийного оборудования;
 Производить распечатку, копирование и тиражирование документов на принтере и других периферийных устройствах вывода;
 Использовать мультимедиа-проектор для демонстрации содержимого экранных форм с персонального компьютера;
 Вести отчетную и техническую документацию;

<b>Знать</b>:
 Устройство персональных компьютеров, основные блоки, функции и технические характеристики;
 Архитектуру, состав, функции и классификацию операционных систем персонального компьютера;
 Виды и назначение периферийных устройств, их устройство и принцип действия, интерфейсы подключения и правила эксплуатации;
 Принципы установки и настройки основных компонентов операционной системы и драйверов периферийного оборудования;
 Принципы цифрового представления звуковой, графической, видео и мультимедийной информации в персональном компьютере;
 Виды и параметры форматов аудио-, графических, видео- и мультимедийных файлов и методы их конвертирования;
 Назначение, возможности, правила эксплуатации мультимедийного оборудования;
 Основные типы интерфейсов для подключения мультимедийного оборудования;
 Основные приемы обработки цифровой информации;
 Назначение, разновидности и функциональные возможности программ обработки звука;
 Назначение, разновидности и функциональные возможности программ обработки графических изображений;
 Назначение, разновидности и функциональные возможности программ обработки видео- и мультимедиа контента;
 Структуру, виды информационных ресурсов и основные виды услуг в сети Интернет;
 Назначение, разновидности и функциональные возможности программ для создания веб-страниц;
 Нормативные документы по охране труда при работе с персональным компьютером, периферийным, мультимедийным оборудованием и компьютерной оргтехникой;
 Назначение, разновидности и функциональные возможности программ для публикации мультимедиа контента;
 Принципы лицензирования и модели распространения мультимедийного контента;
 Нормативные документы по установке, эксплуатации и охране труда при работе с персональным компьютером, периферийным оборудованием и компьютерной оргтехникой;
 Структуру, виды информационных ресурсов и основные виды услуг в сети Интернет;
 Основные виды угроз информационной безопасности и средства защиты информации;
 Принципы антивирусной защиты персонального компьютера;
 Состав мероприятий по защите персональных данных.

<b>Итоговая аттестация студентов</b>:
Включает защиту выпускной квалификационной работы (выпускная практическая квалификационная работа и письменная экзаменационная работа).
                """, parse_mode = 'html'
)
                getLinks("http://polytech-rzn.ru/?page_id=7852", "standart")
                f1 = fileLink
                getLinks("http://polytech-rzn.ru/?page_id=7852", "plan")
                f2= fileLink
                getLinks("http://polytech-rzn.ru/?page_id=7852", "ppkrs")
                f3 = fileLink
                bot.send_media_group(call.message.chat.id, [types.InputMediaDocument(f1), types.InputMediaDocument(f2), types.InputMediaDocument(f3)])

                button = "09.01.03 Мастер по обработке цифровой информации"
            #Специальности
            elif (call.data == "46.02.01"):
                bot.send_message(call.message.chat.id,
                """
<b>46.02.01 Документационное обеспечение управления и архивоведение</b>

<b>Квалификация выпускника</b>: Специалист по документационному обеспечению управления, архивист (углубленная подготовка)
<b>Форма обучения</b>: Очная
<b>Срок обучения</b>: 3 года 10 месяцев (углубленная подготовка)

<b>Область профессиональной деятельности выпускника</b>:
 Организация документационного обеспечения управления и функционирования организации.
 Организация архивной и справочно-информационной работы по документам организации.
 Проектирование и внедрение систем управления электронным документооборотом организаций на основе применения баз и банков данных и других автоматизированных технологий.
 Документы, созданные любым способом документирования.
 Системы документационного обеспечения управления.
 Системы электронного документооборота.
 Архивные документы.
 Контроль за состоянием делопроизводства в организации.

<b>Объекты профессиональной деятельности выпускника</b>:
 <b>В результате изучения дисциплин обучающийся должен</b>:
  <b>Иметь практический опыт</b>:
   Организации документационного обеспечения управления и функционирования организации.
   Организации архивной и справочно-информационной работы по документам организации.

<b>Уметь</b>:
 Применять нормативные правовые акты в управленческой деятельности.
 Подготавливать проекты управленческих решений.
 Обрабатывать входящие и исходящие документы, систематизировать их, составлять номенклатуру дел и формировать документы в дела.

<b>Знать</b>:
 Нормативные правовые акты в области организации управленческой деятельности.
 Основные правила хранения и защиты служебной информации.
 Организовывать деятельность архива с учетом статуса и профиля организации.
 Работать в системах электронного документооборота.
 Использовать в деятельности архива современные компьютерные технологии.
 Применять современные методики консервации и реставрации архивных документов.
 Систему архивного управления в Российской Федерации и организацию Архивного фонда Российской Федерации.
 Систему хранения и обработки документов.

<b>Итоговая аттестация студентов</b>:
 Защита выпускной квалификационной работы (дипломная работа, дипломный проект)
                """, parse_mode = 'html'
)
                f1 = downloadFile("https://s31vla.storage.yandex.net/rdisk/8a0af71f549e8c2030d785c3d3c145ed47968d0f2302207641df365c1edcc0df/6267891c/6DORuVENicJrHHk1NJVYk3b-gDyi8ZY9vVstpLvv_b6JsklH1ssuyWRT01rh4YbeCkdSrWLzeCnG5PMlwdwNfQ==?uid=0&filename=46.02.01%20%D0%94%D0%BE%D0%BA%D1%83%D0%BC%D0%B5%D0%BD%D1%82%D0%B0%D1%86%D0%B8%D0%BE%D0%BD%D0%BD%D0%BE%D0%B5%20%D0%BE%D0%B1%D0%B5%D1%81%D0%BF%D0%B5%D1%87%D0%B5%D0%BD%D0%B8%D0%B5%20%D1%83%D0%BF%D1%80%D0%B0%D0%B2%D0%BB%D0%B5%D0%BD%D0%B8%D1%8F%20%D0%B8%20%D0%B0%D1%80%D1%85%D0%B8%D0%B2%D0%BE%D0%B2%D0%B5%D0%B4%D0%B5%D0%BD%D0%B8%D0%B5.pdf&disposition=attachment&hash=oLv0ePzFEwlBtLH0hyDPl/LTUN5mnCD%2Bek%2Bc6lrDlPI%3D&limit=0&content_type=application%2Fpdf&owner_uid=244466476&fsize=305248&hid=7459a9af5847a74a09f62263033e0f49&media_type=document&tknv=v2&rtoken=AW7bfGO3e5PD&force_default=no&ycrid=na-cccc55386eee722084479c5105aa75c3-downloader9h&ts=5dd8853df7f00&s=aced344f9655ceecdead9e9af6dbadfbb48cfa8933d013731f0e2017b93d2270&pb=U2FsdGVkX182VsFN8ol1jd_1YV9OxoKvb-faal_ZjmH30fmhOUc_FNO85pEJInD5YxvGjkzKTuME_9UUMUqKMLELQDYsosrY8dPYdzhqYwY")
                f2= downloadFile("http://polytech-rzn.ru/metal/wp-content/uploads/2021/09/46.02.01-%D0%94%D0%9E%D0%A3-2021.pdf")
                f3 = downloadFile("http://polytech-rzn.ru/metal/wp-content/uploads/2014/07/1-%D0%94%D0%9E%D0%A3.pdf")
                bot.send_media_group(call.message.chat.id, [types.InputMediaDocument(f1), types.InputMediaDocument(f2), types.InputMediaDocument(f3)])

                button = "46.02.01 Документационное обеспечение управления и архивоведение"

            elif (call.data == "38.02.01"):
                bot.send_message(call.message.chat.id,
                """
38.02.01 Экономика и бухгалтерский учет (по отраслям)

Квалификация выпускника: Бухгалтер, специалист по налогообложению (углубленная подготовка)
Форма обучения: Очная
Срок обучения: 3 года 10 месяцев (углубленная подготовка)

Область профессиональной деятельности выпускника:
 Учет имущества и обязательств организации, проведение и оформление хозяйственных операций, обработка бухгалтерской информации, проведение расчетов с бюджетом и внебюджетными фондами, формирование бухгалтерской отчетности, налоговый учет, налоговое планирование.

Объекты профессиональной деятельности выпускника:
 Бухгалтер, специалист по налогообложению готовится к следующим видам деятельности.
 Документирование хозяйственных операций и ведение бухгалтерского учета имущества организации.
 Ведение бухгалтерского учета источников формирования имущества, выполнение работ по инвентаризации имущества и финансовых обязательств организации.
 Проведение расчетов с бюджетом и внебюджетными фондами.
 Составление и использование бухгалтерской отчетности.
 Осуществление налогового учета и налогового планирования в организации.
 Выполнение работ по одной или нескольким профессиям рабочих, должностям служащих (приложение к ФГОС).

В результате изучения дисциплин обучающийся должен:
 Иметь практический опыт:
  Организации документационного обеспечения управления и функционирования организации.
  Организации архивной и справочно-информационной работы по документам организации.

Уметь:
 Документально оформлять и отражать на счетах бухгалтерского учета операции, связанные с движением основных средств, товарно-материальных ценностей, денежных средств, расчетов и т.д.
 Составлять бухгалтерскую и статистическую отчетность.
 Анализировать хозяйственно-финансовую деятельность организации.
 Оценивать ликвидность и платежеспособность организации.
 Пользоваться нормативными документами и инструкциями Министерства финансов РФ, Министерства по налогам и сборам РФ и других государственных органов, регулирующими порядок бухгалтерского учета, отчетности и налогообложения.
 Использовать вычислительную технику для обработки учетно-финансовой информации.

Знать:
 Рыночные методы хозяйствования, экономику, организацию труда и управления.
 Законодательные акты, постановления, распоряжения, приказы, руководящие методические и нормативные материалы по организации бухгалтерского учета имущества, обязательств и хозяйственных операций и составлению отчетности.
 формы и методы бухгалтерского учета в организации.
 План и корреспонденцию счетов.
 о рганизацию документооборота по участкам бухгалтерского учета.
 налоговое законодательство РФ, формы и методы анализа финансово-хозяйственной деятельности и контрольно-ревизионной работы.
 Компьютерное обеспечение бухгалтерской деятельности.

Итоговая аттестация студентов:
 Защита выпускной квалификационной работы (дипломная работа, дипломный проект)
                """, parse_mode = 'html'
)
                f1 = downloadFile("https://s52vla.storage.yandex.net/rdisk/ba22a79d4abf34f90b15b63425c4ac6b58ebc1c94e7dc750ecc4f417e0018837/62678d49/BtkuYquvF30FOoFl9OTWYPxAZ-VtnthcUQm8uPasRJrnurkay7qYbhs_wxUHvaxTFLQ8GJ4n5kfWdM-4oNFK0g==?uid=0&filename=38.02.01%20%D0%AD%D0%BA%D0%BE%D0%BD%D0%BE%D0%BC%D0%B8%D0%BA%D0%B0%20%D0%B8%20%D0%B1%D1%83%D1%85%D0%B3%D0%B0%D0%BB%D1%82%D0%B5%D1%80%D1%81%D0%BA%D0%B8%D0%B9%20%D1%83%D1%87%D0%B5%D1%82.pdf&disposition=attachment&hash=B9QDnTdsgLxnz7edYrnatE1w/XCiWlT8ocdLCS17tlc%3D&limit=0&content_type=application%2Fpdf&owner_uid=244466476&fsize=396730&hid=ac0fbc00ed37e78194589dc479828b8e&media_type=document&tknv=v2&rtoken=qIVUF1ZIp3Up&force_default=no&ycrid=na-b1f6e41518884a40e16e8228075cd9b0-downloader1e&ts=5dd8893972440&s=21c77d5657b5ba961de0563b306621225cd89efa2bc552c3c2aeb69ef1ae4494&pb=U2FsdGVkX1-XKJ3QsazBhIs6MkrMt8nX9QTQcwf6q_nN9ebWBmDF16Us_OcDupOAvNoHOhLxWTzOQVTpcLZ_43GmQwdUf-tXzTJpupuOVZ4")
                f2= downloadFile("http://polytech-rzn.ru/metal/wp-content/uploads/2021/09/38.02.01-%D0%AD%D0%BA%D0%BE%D0%BD%D0%BE%D0%BC%D0%B8%D0%BA%D0%B0-2021.pdf")
                f3 = downloadFile("http://polytech-rzn.ru/metal/wp-content/uploads/2014/07/14-%D0%AD%D0%91%D0%A3.pdf")
                bot.send_media_group(call.message.chat.id, [types.InputMediaDocument(f1), types.InputMediaDocument(f2), types.InputMediaDocument(f3)])

                button = "38.02.01 Экономика и бухгалтерский учет (по отраслям)"
            
            elif (call.data == "43.02.13"):
                sti = open('static/outoforder.webp', 'rb')
                bot.send_sticker(call.message.chat.id, sti)
                bot.send_message(call.message.chat.id, "Раздел ещё редактируется")
                button = "43.02.13 Технология парикмахерского искусства (ТОП-50)"
            
            elif (call.data == "43.02.12"):
                sti = open('static/outoforder.webp', 'rb')
                bot.send_sticker(call.message.chat.id, sti)
                bot.send_message(call.message.chat.id, "Раздел ещё редактируется")
                button = "43.02.12 Технология эстетических услуг (ТОП-50)"
            
            elif (call.data == "15.02.15"):
                sti = open('static/outoforder.webp', 'rb')
                bot.send_sticker(call.message.chat.id, sti)
                bot.send_message(call.message.chat.id, "Раздел ещё редактируется")
                button = "15.02.15 Технология металлообрабатывающего производства (ТОП-50)"

            elif (call.data == "23.02.05"):
                sti = open('static/outoforder.webp', 'rb')
                bot.send_sticker(call.message.chat.id, sti)
                bot.send_message(call.message.chat.id, "Раздел ещё редактируется")
                button = "23.02.05 Эксплуатация транспортного электрооборудования и автоматики (по видам транспорта, за исключением водного)"

            elif (call.data == "11.02.16"):
                sti = open('static/outoforder.webp', 'rb')
                bot.send_sticker(call.message.chat.id, sti)
                bot.send_message(call.message.chat.id, "Раздел ещё редактируется")
                button = "11.02.16 Монтаж, техническое обслуживание и ремонт электронных приборов и устройств (ТОП-50)"
            
            elif (call.data == "35.02.03"):
                sti = open('static/outoforder.webp', 'rb')
                bot.send_sticker(call.message.chat.id, sti)
                bot.send_message(call.message.chat.id, "Раздел ещё редактируется")
                button = "35.02.03 Технология деревообработки"

            elif (call.data == "09.02.07"):
                sti = open('static/outoforder.webp', 'rb')
                bot.send_sticker(call.message.chat.id, sti)
                bot.send_message(call.message.chat.id, "Раздел ещё редактируется")
                button = "09.02.07 Информационные системы и программирование (ТОП-50)"

            elif (call.data == "08.02.09"):
                sti = open('static/outoforder.webp', 'rb')
                bot.send_sticker(call.message.chat.id, sti)
                bot.send_message(call.message.chat.id, "Раздел ещё редактируется")
                button = "08.02.09 Монтаж, наладка и эксплуатация электрооборудования промышленных и гражданских зданий"

            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text = f"Вы выбали: {button}",
        reply_markup = None)
    except Exception as ex:
        print(repr(ex))

#Отображение информации о зачислении
def enrol(message):
    global fileLink

    getLinks("https://polytech-rzn.ru/?page_id=18458", "stList")
    date = datetime.datetime.now().strftime('%Y')
    bot.send_document(message.chat.id, fileLink, caption = f"Приказ о зачислении в состав студентов на {date} год")

#Отображение информации о общежитии
def hostel(message):
    bot.send_message(message.chat.id, "<b>Общежитие</b>: улица Полетаева, дом 13", parse_mode = 'html')
    bot.send_location(message.chat.id, latitude = 54.605970, longitude = 39.723358)

    f1 = downloadFile("https://s288vla.storage.yandex.net/rdisk/47b629f0f45a43eecc907e4bc61143f01c31f0ef25f95257de901f816b81a91d/626771f8/5KkIT5_vNYHSvjbhGzj1M0cjXlk9uWeX6PRNm5Q83UpNRtWnrSR6oxoV6ElMfdpX4WKHUv3SoBLRkt5rUThylg==?uid=0&filename=%D0%A3%D1%81%D0%BB%D0%BE%D0%B2%D0%B8%D1%8F%20%20%D0%BF%D1%80%D0%BE%D0%B6%D0%B8%D0%B2%D0%B0%D0%BD%D0%B8%D1%8F%20%D0%BE%D0%B1%D1%83%D1%87%D0%B0%D1%8E%D1%89%D0%B8%D1%85%D1%81%D1%8F%20%D0%B2%20%D0%BE%D0%B1%D1%89%D0%B5%D0%B6%D0%B8%D1%82%D0%B8%D0%B8%20%20%D0%9E%D0%93%D0%91%D0%9F%D0%9E%D0%A3%20%C2%AB%D0%A0%D0%9F%D0%A2%D0%9A%C2%BB.pdf&disposition=attachment&hash=klEef6Qm10m4MnxBnELvgqZDNsk1MwsTbvoFPuL3KhQ%3D&limit=0&content_type=application%2Fpdf&owner_uid=244466476&fsize=219658&hid=1e236817d7525412fc259dca812975bc&media_type=document&tknv=v2&rtoken=H2HQJbeShu8e&force_default=no&ycrid=na-41fe7d94dbc530ede428a588e60af96b-downloader1f&ts=5dd86f2c66e00&s=e7c8422062158a08fea294936efa97c282e2632bd9236737f8dfa3ff24c395df&pb=U2FsdGVkX1_VbQ6i3Z4dg_MI3wplJzbRXoRNO4mok4pBzNIdwPnJ8OKyzVUOOWDLGbf2Pr06RyYsvfN2AbJ-jMtc402Zs3OAV76QTbRX1aM")
    f2 = downloadFile("https://s246vla.storage.yandex.net/rdisk/d3368691a6889920108865fa587c06ec5dff55a4e6369c9a14a231f5aaa9dfff/62677341/5KkIT5_vNYHSvjbhGzj1MzTt8UfZoV0OJHyoH4meu5BJnLRnaIdx_FkXrDYnMR8ixjaKUPNNmROYthL66EL6Hg==?uid=0&filename=%D0%9F%D0%BE%D0%BB%D0%BE%D0%B6%D0%B5%D0%BD%D0%B8%D0%B5%20%D0%BE%20%D0%BF%D0%BE%D1%80%D1%8F%D0%B4%D0%BA%D0%B5%20%D0%BE%D0%BF%D0%BB%D0%B0%D1%82%D1%8B%20%D0%BF%D1%80%D0%BE%D0%B6%D0%B8%D0%B2%D0%B0%D0%BD%D0%B8%D1%8F%20%D0%B2%20%D0%BE%D0%B1%D1%89%D0%B5%D0%B6%D0%B8%D1%82%D0%B8%D0%B8%20%D0%9E%D0%93%D0%91%D0%9F%D0%9E%D0%A3%20%C2%AB%D0%A0%D0%9F%D0%A2%D0%9A%C2%BB.pdf&disposition=attachment&hash=sLw2vwBFLlcqSrWHUAVQEaDykNb%2BgC5u1Zgy05LHDOw%3D&limit=0&content_type=application%2Fpdf&owner_uid=244466476&fsize=134881&hid=d6d926aa311fc41447525286977c797e&media_type=document&tknv=v2&rtoken=8vMbIaHGcHVB&force_default=no&ycrid=na-65d0d4ebc321cc6e001c078d3a7f4583-downloader6h&ts=5dd8706629240&s=90c8912bba698ecb17a4cf666160b36288281cbd298a6c6dd4ad0e1764414443&pb=U2FsdGVkX182eOB-iQLC1_TYvOyhrZYb8_-gPvuYgpC51sgFU011ZIDP8sA8dGFmShhSYHVovupeqtq73_xkpUcsjON8nhRM1_vrkKkOwQg")
    f3 = downloadFile("https://s84vla.storage.yandex.net/rdisk/44f31709abfc2f65d637f081f3445c8a0eca623068073dce2f527f811f015afc/6267742e/5KkIT5_vNYHSvjbhGzj1M6Z49EEuQKZwh7TUH0e_hhMCAFfnixo7JttoSvN1sBEBtjlLVnMEOq21kM7QKZVdUA==?uid=0&filename=%D0%9F%D0%BE%D0%BB%D0%BE%D0%B6%D0%B5%D0%BD%D0%B8%D0%B5%20%D0%BE%20%D1%81%D1%82%D1%83%D0%B4%D0%B5%D0%BD%D1%87%D0%B5%D1%81%D0%BA%D0%BE%D0%BC%20%D0%BE%D0%B1%D1%89%D0%B5%D0%B6%D0%B8%D1%82%D0%B8%D0%B8%20%D0%9E%D0%93%D0%91%D0%9F%D0%9E%D0%A3%20%C2%AB%D0%A0%D0%9F%D0%A2%D0%9A%C2%BB.pdf&disposition=attachment&hash=w/%2BJYg24FNBPItzQbE0GUSfR80kvHFVzyzWmLHbhDNo%3D&limit=0&content_type=application%2Fpdf&owner_uid=244466476&fsize=319046&hid=a4760a8f33da741358c097228679542d&media_type=document&tknv=v2&rtoken=y4K11fJLqzpp&force_default=no&ycrid=na-7ff2e8d7d235cbed52fb483781bd06ad-downloader12e&ts=5dd871482e780&s=524783d6ab43f645e1325c456056b3256ffbe9c368efe54d04efa06614b1f240&pb=U2FsdGVkX19GiyTVlIeoNQfic5AcHNlpO1b8AzNJYdXAile4XCOReGPpRPCfwdNO0MAG3reYkVs42mcDqL5ne9gIpH0tNhM453dWf9bVub0")
    f4 = downloadFile("https://s308man.storage.yandex.net/rdisk/14344c252bc6fca27f58127ad01a28f68bdd00702b8133380c81a21e6abbc31d/62677497/5KkIT5_vNYHSvjbhGzj1M1ShzmfeJiDgiEk7ALUJHTKT4CfjKRSW5FK3DeA-vhNAMDt6NDzzkNMRmC3BxLtj-g==?uid=0&filename=%D0%9F%D0%BE%D0%BB%D0%BE%D0%B6%D0%B5%D0%BD%D0%B8%D0%B5%20%D0%BE%20%D1%81%D1%82%D1%83%D0%B4%D0%B5%D0%BD%D1%87%D0%B5%D1%81%D0%BA%D0%BE%D0%BC%20%D0%A1%D0%BE%D0%B2%D0%B5%D1%82%D0%B5%20%D0%BE%D0%B1%D1%89%D0%B5%D0%B6%D0%B8%D1%82%D0%B8%D1%8F%20%D0%9E%D0%93%D0%91%D0%9F%D0%9E%D0%A3%20%C2%AB%D0%A0%D0%9F%D0%A2%D0%9A%C2%BB.pdf&disposition=attachment&hash=5XUZum8uqHXrn8PdK5b2UKeqWFznYYpBz1hHSc41bZw%3D&limit=0&content_type=application%2Fpdf&owner_uid=244466476&fsize=3131411&hid=ea17bc076d7417c49672d5a20e5c814f&media_type=document&tknv=v2&rtoken=o6DzmxxWEcd8&force_default=no&ycrid=na-55b655b5b6f9a4eabdb4ed56ebca6ca5-downloader12e&ts=5dd871ac513c0&s=efd65ae475b483bc4f8a5e311acc007852eaed0d1fcbb9ef31a2d0e705bde30b&pb=U2FsdGVkX19aVjmN9ZAuFJD6mhHelAE8rzh3yHjT5FRu2eQivCOrQikg55oOLF8gRYtVT8wYENR9ZmwJJNn3Lo2xHvtiGYsKxZCpRmqKU_Q")

    bot.send_media_group(message.chat.id, [types.InputMediaDocument(f1), types.InputMediaDocument(f2), types.InputMediaDocument(f3), types.InputMediaDocument(f4)])


#Отображение расписания
def schedule(message):
    global scheduleSolar
    global scheduleSolarChange
    global scheduleShabulino
    global scheduleShabulinoChange
    #Солнечная
    bot.send_message(message.chat.id, "Расписание звонков ул. Солнечная")
    img1 = open('static/schedule_ring_solar.png', 'rb')
    bot.send_photo(message.chat.id, img1)
    #Шабулино
    bot.send_message(message.chat.id, "Расписание звонков ул. Шабулино")
    img2 = open('static/schedule_ring_shabulino.png', 'rb')
    bot.send_photo(message.chat.id, img2)
    getLinks('https://polytech-rzn.ru/?page_id=14410')
    date = datetime.datetime.now().strftime('%d.%m.%Y')
    bot.send_message(message.chat.id,
f"""
Расписание на {date}
 <b>Солнечная</b>
  Расписание: {scheduleSolar}
  Изменения в расписании: {scheduleSolarChange}
 <b>Шабулино</b>
  Расписание: {scheduleShabulino}
  Изменения в расписании: {scheduleShabulinoChange}
"""
    , parse_mode = 'html')

def contacts(message):
    vk = open('static/vk.webp', 'rb')
    rutube = open('static/rutube.webp', 'rb')
    youtube = open('static/youtube.webp', 'rb')
    bot.send_sticker(message.chat.id, vk)
    bot.send_sticker(message.chat.id, rutube)
    bot.send_sticker(message.chat.id, youtube)
    bot.send_message(message.chat.id,
    """
<b>Контактная информация</b>

<b>Наименование учреждения</b>: Областное государственное бюджетное профессиональное образовательное учреждение «Рязанский политехнический колледж»
<b>Сокращенное наименование учреждения</b>: ОГБПОУ «РПТК»

<b>Адрес фактического местонахождения</b>: 390000, Рязанская область, город Рязань , улица Солнечная, 6

<b>Директор</b>: Смыслов Анатолий Федорович
<b>Контактный телефон</b>: (+7) 4912 29-82-62
<b>Адрес электронной почты</b>: politeh.coll.rzn@ryazangov.ru

<b>Главный бухгалтер</b>: Канунникова Ирина Владимировна
<b>Контактный телефон</b>: (+7) 4912 25-66-20
<b>Адрес электронной почты</b>: politeh.coll.rzn@ryazangov.ru

<b>Заместитель директора по учебной работе</b>: Свечникова Людмила Владимировна
<b>Контактный телефон</b>: (+7) 4912 25-50-15
<b>Адрес электронной почты</b>: politeh.coll.rzn@ryazangov.ru

<b>Заместитель директора по учебно-воспитательной работе</b>: Диянова Валентина Николаевна
<b>Контактный телефон</b>: (+7) 4912 25-73-95
<b>Адрес электронной почты</b>: politeh.coll.rzn@ryazangov.ru

<b>Заведующая учебной частью</b>: Копьева Марина Анатольевна
<b>Контактный телефон</b>: (+7) 4912 29-84-14
<b>Адрес электронной почты</b>: politeh.coll.rzn@ryazangov.ru

<b>Учебный корпус №2</b>: проезд Шабулина, дом 25

<b>Заместитель директора по учебно-производственной работе</b>: Мацнев Владимир Владимирович
<b>Контактный телефон</b>: +7 (4912) 93-85-41
<b>Адрес электронной почты</b>: politeh.coll.rzn@ryazangov.ru

<b>Заведующий учебной частью</b>: Рыжих Светлана Ивановна
<b>Контактный телефон</b>: +7 (4912) 93-85-41
<b>Адрес электронной почты</b>: politeh.coll.rzn@ryazangov.ru

<b>Группа ВК</b>: https://vk.com/polytech62
<b>Rutube</b>: https://rutube.ru/channel/24611460
<b>Youtube</b>: https://www.youtube.com/channel/UCzQsJf-s1h1zUZdctkQ_Z1A
    """, parse_mode = 'html')

    #функция сокращения ссылок
def shortLinks(link):
    s = pyshorteners.Shortener()
    return s.tinyurl.short(link)

#Получение актуальных ссылок с сайта колледжа
def getLinks(url, doc = ""):
    global scheduleSolar
    global scheduleSolarChange
    global scheduleShabulino
    global scheduleShabulinoChange

    global fileLink

    internal_urls = []
    # все URL-адреса `url`
    urls = set()
    urls.clear()
    # доменное имя URL без протокола
    domain_name = urlparse(url).netloc
    soup = BeautifulSoup(requests.get(url).content, "html.parser")
    #i = 0
    for a_tag in soup.findAll("a"):
        href = a_tag.attrs.get("href")
        if href == "" or href is None:
            # пустой тег href
            continue
        if href in internal_urls:
            # уже в наборе
            continue
        #i+=1
        #print(f"Internal link: {href} {i}")
        urls.add(href)
        internal_urls.append(href)
    if (url == 'https://polytech-rzn.ru/?page_id=14410'):
        scheduleSolar = shortLinks(internal_urls[81])
        scheduleSolarChange = shortLinks(internal_urls[82])
        scheduleShabulino = shortLinks(internal_urls[83])
        scheduleShabulinoChange = shortLinks(internal_urls[84])
    elif(url == "http://polytech-rzn.ru/?page_id=109"):
        fileLink = downloadFile(internal_urls[80], "http://polytech-rzn.ru/?page_id=109")

    #Профессия 11.01.01
    elif(url == "http://polytech-rzn.ru/?page_id=82" and doc == "prikaz"):
        getLinks(internal_urls[81])
    elif(url == "http://polytech-rzn.ru/?page_id=82" and doc == "plan"):
        fileLink = downloadFile(internal_urls[82], "http://polytech-rzn.ru/?page_id=82", "plan")
    elif(url == "http://polytech-rzn.ru/?page_id=82" and doc == "planLong"):
        fileLink = downloadFile(internal_urls[83], "http://polytech-rzn.ru/?page_id=82", "planLong")
    elif(url == "http://polytech-rzn.ru/?page_id=82" and doc == "ppkrs"):
        fileLink = downloadFile(internal_urls[84], "http://polytech-rzn.ru/?page_id=82", "ppkrs")
    elif(url == "https://yadi.sk/i/xn5LIeLnrL3Jk"):
        fileLink = downloadFile("https://s432man.storage.yandex.net/rdisk/1432fbc3b7796cbdaf8f2bb828dae229c815a9ade6ae3ee73421d47c17efc021/626752ae/5KkIT5_vNYHSvjbhGzj1Myc10w5Qoc_jJp0Zu8jsfwrSVsqrBQ1HC1tu_Ck9x_5cYCsGhlsM3dbVgVxB-sLTXA==?uid=0&filename=%D0%A4%D0%93%D0%9E%D0%A1%20%2011.01.01%20%D0%9C%D0%BE%D0%BD%D1%82%D0%B0%D0%B6%D0%BD%D0%B8%D0%BA%20%D1%80%D0%B0%D0%B4%D0%B8%D0%BE%D1%8D%D0%BB%D0%B5%D0%BA%D1%82%D1%80%D0%BE%D0%BD%D0%BD%D0%BE%D0%B9%20%D0%B0%D0%BF%D0%BF%D0%B0%D1%80%D0%B0%D1%82%D1%83%D1%80%D1%8B%20%D0%B8%20%D0%BF%D1%80%D0%B8%D0%B1%D0%BE%D1%80%D0%BE%D0%B2.pdf&disposition=attachment&hash=TXbjhW332%2FjlTTkhWqNQCix0eVsbsVIxZhEmZg0Jew4%3D&limit=0&content_type=application%2Fpdf&owner_uid=244466476&fsize=343781&hid=f693a1665360856140c6c3700dad82fb&media_type=document&tknv=v2&rtoken=6rxMUdcy5BYM&force_default=no&ycrid=na-eefa258b7772b68560e27f5dae55e95b-downloader5e&ts=5dd8515578780&s=783b8f5cfca2e93270a7f4b0483feb762a87230742adc3a2eeda94f4cc0d0798&pb=U2FsdGVkX1-R-DvIdUIH_VbXpj5tITHjp_fMIdZEQoSd0JtHH6jnY37CDZRxwjcQLUaKXBKMA8RQuh-FZL8Jc_kko5G5AqdD4NQDyU_v-Hc", "https://yadi.sk/i/xn5LIeLnrL3Jk", "prikaz")
    
    #Профессия 09.01.03
    elif(url == "http://polytech-rzn.ru/?page_id=7852" and doc == "standart"):
        getLinks(internal_urls[81])
    elif(url == "https://yadi.sk/i/cf2r8Z2FrMRr3"):
        fileLink = downloadFile("https://s263sas.storage.yandex.net/rdisk/5c2e950bf44839a0d5834faaefbf8c6fa37830330a257f922e571a65d829a3d0/626769e9/5KkIT5_vNYHSvjbhGzj1M7MdZvm1HWpQEe1bgVkaIMsnKaw2UA-2TTjr26mHGZlnEsCMyFlO9xRw-W42MP7-xw==?uid=0&filename=%D0%A4%D0%93%D0%9E%D0%A1%2009.01.03%20%D0%9C%D0%B0%D1%81%D1%82%D0%B5%D1%80%20%D0%BF%D0%BE%20%D0%BE%D0%B1%D1%80%D0%B0%D0%B1%D0%BE%D1%82%D0%BA%D0%B5%20%D1%86%D0%B8%D1%84%D1%80%D0%BE%D0%B2%D0%BE%D0%B9%20%D0%B8%D0%BD%D1%84%D0%BE%D1%80%D0%BC%D0%B0%D1%86%D0%B8%D0%B8.pdf&disposition=attachment&hash=Rk7kgDf3eimeI%2Fl4MxLYKl6jOzxGRljYOYXpLq8aQkg%3D&limit=0&content_type=application%2Fpdf&owner_uid=244466476&fsize=336222&hid=06d75d86426d7c15026b694ab84426b5&media_type=document&tknv=v2&rtoken=xBXovvu60x0q&force_default=no&ycrid=na-158490d4d6c4dd4c00e6cb1952f8c765-downloader5f&ts=5dd8677cf8c40&s=65a4b0d199001cc2db9dc8bf1988bf998fbca6c3326c3a93a7764ea31f26e0e5&pb=U2FsdGVkX1-Q5nDeRMt0hUTC17NutIHxFW2AvHQHM7pFhgNqTLALxy7Py_dytehhSw8Iiv2GVhre9Y60L_11QEZWj1JPxeLP6byTlx6VNpE", "https://yadi.sk/i/cf2r8Z2FrMRr3", "standart")
    elif(url == "http://polytech-rzn.ru/?page_id=7852" and doc == "plan"):
        fileLink = downloadFile(internal_urls[82], "http://polytech-rzn.ru/?page_id=7852", "plan")
    elif(url == "http://polytech-rzn.ru/?page_id=7852" and doc == "ppkrs"):
        fileLink = downloadFile(internal_urls[83], "http://polytech-rzn.ru/?page_id=7852", "ppkrs")

    #Зачисление
    elif(url == "https://polytech-rzn.ru/?page_id=18458" and doc == "stList"):
        fileLink = downloadFile(internal_urls[81], "https://polytech-rzn.ru/?page_id=18458", "stList")

#Скачивание файлов
def downloadFile(url, site = "", doc = ""):
    name = ''
    if (site == "http://polytech-rzn.ru/?page_id=109" and doc == ""):
        r = requests.get(url)
        name = 'static/doc/Заявление.pdf'
        file = open(name, 'wb')
        file.write(r.content)
        file.close
    
    #Профессия 11.01.01
    elif (site == "https://yadi.sk/i/xn5LIeLnrL3Jk" and doc == "prikaz"):
        r = requests.get(url)
        name = 'static/doc/Приказ Монтажник радиоэлектронной аппаратуры и приборов.pdf'
        file = open(name, 'wb')
        file.write(r.content)
        file.close
    elif (site == "http://polytech-rzn.ru/?page_id=82" and doc == "plan"):
        r = requests.get(url)
        name = 'static/doc/Учебный план по специальности 11.01.01.pdf'
        file = open(name, 'wb')
        file.write(r.content)
        file.close
    elif (site == "http://polytech-rzn.ru/?page_id=82" and doc == "planLong"):
        r = requests.get(url)
        name = 'static/doc/Учебный план по специальности 11.01.01(10 месяцев).pdf'
        file = open(name, 'wb')
        file.write(r.content)
        file.close
    elif (site == "http://polytech-rzn.ru/?page_id=82" and doc == "ppkrs"):
        r = requests.get(url)
        name = 'static/doc/ППКРС 11.01.01.pdf'
        file = open(name, 'wb')
        file.write(r.content)
        file.close

    #Профессия 09.01.03
    elif (site == "https://yadi.sk/i/cf2r8Z2FrMRr3" and doc == "standart"):
        r = requests.get(url)
        name = 'static/doc/СТАНДАРТ СРЕДНЕГО ПРОФЕССИОНАЛЬНОГО ОБРАЗОВАНИЯ по профессии 09.01.03.pdf'
        file = open(name, 'wb')
        file.write(r.content)
        file.close
    elif (site == "http://polytech-rzn.ru/?page_id=7852" and doc == "plan"):
        r = requests.get(url)
        name = 'static/doc/Учебный план для специальности 09.01.03.pdf'
        file = open(name, 'wb')
        file.write(r.content)
        file.close
    elif (site == "http://polytech-rzn.ru/?page_id=7852" and doc == "ppkrs"):
        r = requests.get(url)
        name = 'static/doc/ППКРС 09.01.03.pdf'
        file = open(name, 'wb')
        file.write(r.content)
        file.close

    #Общежитие
    elif (url == "https://s288vla.storage.yandex.net/rdisk/47b629f0f45a43eecc907e4bc61143f01c31f0ef25f95257de901f816b81a91d/626771f8/5KkIT5_vNYHSvjbhGzj1M0cjXlk9uWeX6PRNm5Q83UpNRtWnrSR6oxoV6ElMfdpX4WKHUv3SoBLRkt5rUThylg==?uid=0&filename=%D0%A3%D1%81%D0%BB%D0%BE%D0%B2%D0%B8%D1%8F%20%20%D0%BF%D1%80%D0%BE%D0%B6%D0%B8%D0%B2%D0%B0%D0%BD%D0%B8%D1%8F%20%D0%BE%D0%B1%D1%83%D1%87%D0%B0%D1%8E%D1%89%D0%B8%D1%85%D1%81%D1%8F%20%D0%B2%20%D0%BE%D0%B1%D1%89%D0%B5%D0%B6%D0%B8%D1%82%D0%B8%D0%B8%20%20%D0%9E%D0%93%D0%91%D0%9F%D0%9E%D0%A3%20%C2%AB%D0%A0%D0%9F%D0%A2%D0%9A%C2%BB.pdf&disposition=attachment&hash=klEef6Qm10m4MnxBnELvgqZDNsk1MwsTbvoFPuL3KhQ%3D&limit=0&content_type=application%2Fpdf&owner_uid=244466476&fsize=219658&hid=1e236817d7525412fc259dca812975bc&media_type=document&tknv=v2&rtoken=H2HQJbeShu8e&force_default=no&ycrid=na-41fe7d94dbc530ede428a588e60af96b-downloader1f&ts=5dd86f2c66e00&s=e7c8422062158a08fea294936efa97c282e2632bd9236737f8dfa3ff24c395df&pb=U2FsdGVkX1_VbQ6i3Z4dg_MI3wplJzbRXoRNO4mok4pBzNIdwPnJ8OKyzVUOOWDLGbf2Pr06RyYsvfN2AbJ-jMtc402Zs3OAV76QTbRX1aM" and doc == ""):
        r = requests.get(url)
        name = 'static/doc/Условия проживания обучающихся в общежитии ОГБПОУ «РПТК».pdf'
        file = open(name, 'wb')
        file.write(r.content)
        file.close
    elif (url == "https://s246vla.storage.yandex.net/rdisk/d3368691a6889920108865fa587c06ec5dff55a4e6369c9a14a231f5aaa9dfff/62677341/5KkIT5_vNYHSvjbhGzj1MzTt8UfZoV0OJHyoH4meu5BJnLRnaIdx_FkXrDYnMR8ixjaKUPNNmROYthL66EL6Hg==?uid=0&filename=%D0%9F%D0%BE%D0%BB%D0%BE%D0%B6%D0%B5%D0%BD%D0%B8%D0%B5%20%D0%BE%20%D0%BF%D0%BE%D1%80%D1%8F%D0%B4%D0%BA%D0%B5%20%D0%BE%D0%BF%D0%BB%D0%B0%D1%82%D1%8B%20%D0%BF%D1%80%D0%BE%D0%B6%D0%B8%D0%B2%D0%B0%D0%BD%D0%B8%D1%8F%20%D0%B2%20%D0%BE%D0%B1%D1%89%D0%B5%D0%B6%D0%B8%D1%82%D0%B8%D0%B8%20%D0%9E%D0%93%D0%91%D0%9F%D0%9E%D0%A3%20%C2%AB%D0%A0%D0%9F%D0%A2%D0%9A%C2%BB.pdf&disposition=attachment&hash=sLw2vwBFLlcqSrWHUAVQEaDykNb%2BgC5u1Zgy05LHDOw%3D&limit=0&content_type=application%2Fpdf&owner_uid=244466476&fsize=134881&hid=d6d926aa311fc41447525286977c797e&media_type=document&tknv=v2&rtoken=8vMbIaHGcHVB&force_default=no&ycrid=na-65d0d4ebc321cc6e001c078d3a7f4583-downloader6h&ts=5dd8706629240&s=90c8912bba698ecb17a4cf666160b36288281cbd298a6c6dd4ad0e1764414443&pb=U2FsdGVkX182eOB-iQLC1_TYvOyhrZYb8_-gPvuYgpC51sgFU011ZIDP8sA8dGFmShhSYHVovupeqtq73_xkpUcsjON8nhRM1_vrkKkOwQg" and doc == ""):
        r = requests.get(url)
        name = 'static/doc/Положение о порядке оплаты проживания в общежитии ОГБПОУ «РПТК».pdf'
        file = open(name, 'wb')
        file.write(r.content)
        file.close
    elif (url == "https://s84vla.storage.yandex.net/rdisk/44f31709abfc2f65d637f081f3445c8a0eca623068073dce2f527f811f015afc/6267742e/5KkIT5_vNYHSvjbhGzj1M6Z49EEuQKZwh7TUH0e_hhMCAFfnixo7JttoSvN1sBEBtjlLVnMEOq21kM7QKZVdUA==?uid=0&filename=%D0%9F%D0%BE%D0%BB%D0%BE%D0%B6%D0%B5%D0%BD%D0%B8%D0%B5%20%D0%BE%20%D1%81%D1%82%D1%83%D0%B4%D0%B5%D0%BD%D1%87%D0%B5%D1%81%D0%BA%D0%BE%D0%BC%20%D0%BE%D0%B1%D1%89%D0%B5%D0%B6%D0%B8%D1%82%D0%B8%D0%B8%20%D0%9E%D0%93%D0%91%D0%9F%D0%9E%D0%A3%20%C2%AB%D0%A0%D0%9F%D0%A2%D0%9A%C2%BB.pdf&disposition=attachment&hash=w/%2BJYg24FNBPItzQbE0GUSfR80kvHFVzyzWmLHbhDNo%3D&limit=0&content_type=application%2Fpdf&owner_uid=244466476&fsize=319046&hid=a4760a8f33da741358c097228679542d&media_type=document&tknv=v2&rtoken=y4K11fJLqzpp&force_default=no&ycrid=na-7ff2e8d7d235cbed52fb483781bd06ad-downloader12e&ts=5dd871482e780&s=524783d6ab43f645e1325c456056b3256ffbe9c368efe54d04efa06614b1f240&pb=U2FsdGVkX19GiyTVlIeoNQfic5AcHNlpO1b8AzNJYdXAile4XCOReGPpRPCfwdNO0MAG3reYkVs42mcDqL5ne9gIpH0tNhM453dWf9bVub0" and doc == ""):
        r = requests.get(url)
        name = 'static/doc/Положение о студенческом общежитии ОГБПОУ «РПТК».pdf'
        file = open(name, 'wb')
        file.write(r.content)
        file.close
    elif (url == "https://s308man.storage.yandex.net/rdisk/14344c252bc6fca27f58127ad01a28f68bdd00702b8133380c81a21e6abbc31d/62677497/5KkIT5_vNYHSvjbhGzj1M1ShzmfeJiDgiEk7ALUJHTKT4CfjKRSW5FK3DeA-vhNAMDt6NDzzkNMRmC3BxLtj-g==?uid=0&filename=%D0%9F%D0%BE%D0%BB%D0%BE%D0%B6%D0%B5%D0%BD%D0%B8%D0%B5%20%D0%BE%20%D1%81%D1%82%D1%83%D0%B4%D0%B5%D0%BD%D1%87%D0%B5%D1%81%D0%BA%D0%BE%D0%BC%20%D0%A1%D0%BE%D0%B2%D0%B5%D1%82%D0%B5%20%D0%BE%D0%B1%D1%89%D0%B5%D0%B6%D0%B8%D1%82%D0%B8%D1%8F%20%D0%9E%D0%93%D0%91%D0%9F%D0%9E%D0%A3%20%C2%AB%D0%A0%D0%9F%D0%A2%D0%9A%C2%BB.pdf&disposition=attachment&hash=5XUZum8uqHXrn8PdK5b2UKeqWFznYYpBz1hHSc41bZw%3D&limit=0&content_type=application%2Fpdf&owner_uid=244466476&fsize=3131411&hid=ea17bc076d7417c49672d5a20e5c814f&media_type=document&tknv=v2&rtoken=o6DzmxxWEcd8&force_default=no&ycrid=na-55b655b5b6f9a4eabdb4ed56ebca6ca5-downloader12e&ts=5dd871ac513c0&s=efd65ae475b483bc4f8a5e311acc007852eaed0d1fcbb9ef31a2d0e705bde30b&pb=U2FsdGVkX19aVjmN9ZAuFJD6mhHelAE8rzh3yHjT5FRu2eQivCOrQikg55oOLF8gRYtVT8wYENR9ZmwJJNn3Lo2xHvtiGYsKxZCpRmqKU_Q" and doc == ""):
        r = requests.get(url)
        name = 'static/doc/Положение о студенческом Совете общежития ОГБПОУ «РПТК».pdf'
        file = open(name, 'wb')
        file.write(r.content)
        file.close

    #Зачисление
    elif (site == "https://polytech-rzn.ru/?page_id=18458" and doc == "stList"):
        r = requests.get(url)
        name = 'static/doc/Зачисление.pdf'
        file = open(name, 'wb')
        file.write(r.content)
        file.close

    #Специальность
    elif (url == "https://s31vla.storage.yandex.net/rdisk/8a0af71f549e8c2030d785c3d3c145ed47968d0f2302207641df365c1edcc0df/6267891c/6DORuVENicJrHHk1NJVYk3b-gDyi8ZY9vVstpLvv_b6JsklH1ssuyWRT01rh4YbeCkdSrWLzeCnG5PMlwdwNfQ==?uid=0&filename=46.02.01%20%D0%94%D0%BE%D0%BA%D1%83%D0%BC%D0%B5%D0%BD%D1%82%D0%B0%D1%86%D0%B8%D0%BE%D0%BD%D0%BD%D0%BE%D0%B5%20%D0%BE%D0%B1%D0%B5%D1%81%D0%BF%D0%B5%D1%87%D0%B5%D0%BD%D0%B8%D0%B5%20%D1%83%D0%BF%D1%80%D0%B0%D0%B2%D0%BB%D0%B5%D0%BD%D0%B8%D1%8F%20%D0%B8%20%D0%B0%D1%80%D1%85%D0%B8%D0%B2%D0%BE%D0%B2%D0%B5%D0%B4%D0%B5%D0%BD%D0%B8%D0%B5.pdf&disposition=attachment&hash=oLv0ePzFEwlBtLH0hyDPl/LTUN5mnCD%2Bek%2Bc6lrDlPI%3D&limit=0&content_type=application%2Fpdf&owner_uid=244466476&fsize=305248&hid=7459a9af5847a74a09f62263033e0f49&media_type=document&tknv=v2&rtoken=AW7bfGO3e5PD&force_default=no&ycrid=na-cccc55386eee722084479c5105aa75c3-downloader9h&ts=5dd8853df7f00&s=aced344f9655ceecdead9e9af6dbadfbb48cfa8933d013731f0e2017b93d2270&pb=U2FsdGVkX182VsFN8ol1jd_1YV9OxoKvb-faal_ZjmH30fmhOUc_FNO85pEJInD5YxvGjkzKTuME_9UUMUqKMLELQDYsosrY8dPYdzhqYwY" and doc == ""):
        r = requests.get(url)
        name = 'static/doc/СТАНДАРТ СРЕДНЕГО ПРОФЕССИОНАЛЬНОГО ОБРАЗОВАНИЯ по специальности 46.02.01.pdf'
        file = open(name, 'wb')
        file.write(r.content)
        file.close
    
    elif (url == "http://polytech-rzn.ru/metal/wp-content/uploads/2021/09/46.02.01-%D0%94%D0%9E%D0%A3-2021.pdf" and doc == ""):
        r = requests.get(url)
        name = 'static/doc/Учебный план для специальности 46.02.01.pdf'
        file = open(name, 'wb')
        file.write(r.content)
        file.close
    
    elif (url == "http://polytech-rzn.ru/metal/wp-content/uploads/2014/07/1-%D0%94%D0%9E%D0%A3.pdf" and doc == ""):
        r = requests.get(url)
        name = 'static/doc/ППССЗ 46.02.01.pdf'
        file = open(name, 'wb')
        file.write(r.content)
        file.close
    
    elif (url == "https://s52vla.storage.yandex.net/rdisk/ba22a79d4abf34f90b15b63425c4ac6b58ebc1c94e7dc750ecc4f417e0018837/62678d49/BtkuYquvF30FOoFl9OTWYPxAZ-VtnthcUQm8uPasRJrnurkay7qYbhs_wxUHvaxTFLQ8GJ4n5kfWdM-4oNFK0g==?uid=0&filename=38.02.01%20%D0%AD%D0%BA%D0%BE%D0%BD%D0%BE%D0%BC%D0%B8%D0%BA%D0%B0%20%D0%B8%20%D0%B1%D1%83%D1%85%D0%B3%D0%B0%D0%BB%D1%82%D0%B5%D1%80%D1%81%D0%BA%D0%B8%D0%B9%20%D1%83%D1%87%D0%B5%D1%82.pdf&disposition=attachment&hash=B9QDnTdsgLxnz7edYrnatE1w/XCiWlT8ocdLCS17tlc%3D&limit=0&content_type=application%2Fpdf&owner_uid=244466476&fsize=396730&hid=ac0fbc00ed37e78194589dc479828b8e&media_type=document&tknv=v2&rtoken=qIVUF1ZIp3Up&force_default=no&ycrid=na-b1f6e41518884a40e16e8228075cd9b0-downloader1e&ts=5dd8893972440&s=21c77d5657b5ba961de0563b306621225cd89efa2bc552c3c2aeb69ef1ae4494&pb=U2FsdGVkX1-XKJ3QsazBhIs6MkrMt8nX9QTQcwf6q_nN9ebWBmDF16Us_OcDupOAvNoHOhLxWTzOQVTpcLZ_43GmQwdUf-tXzTJpupuOVZ4" and doc == ""):
        r = requests.get(url)
        name = 'static/doc/СТАНДАРТ СРЕДНЕГО ПРОФЕССИОНАЛЬНОГО ОБРАЗОВАНИЯ по специальности 38.02.01.pdf'
        file = open(name, 'wb')
        file.write(r.content)
        file.close
    elif (url == "http://polytech-rzn.ru/metal/wp-content/uploads/2021/09/38.02.01-%D0%AD%D0%BA%D0%BE%D0%BD%D0%BE%D0%BC%D0%B8%D0%BA%D0%B0-2021.pdf" and doc == ""):
        r = requests.get(url)
        name = 'static/doc/Учебный план по специальности 38.02.01.pdf'
        file = open(name, 'wb')
        file.write(r.content)
        file.close
    elif (url == "http://polytech-rzn.ru/metal/wp-content/uploads/2014/07/14-%D0%AD%D0%91%D0%A3.pdf" and doc == ""):
        r = requests.get(url)
        name = 'static/doc/ППССЗ 38.02.01.pdf'
        file = open(name, 'wb')
        file.write(r.content)
        file.close
        
    return open(name, 'rb')

#Запуск
bot.polling(none_stop=True)