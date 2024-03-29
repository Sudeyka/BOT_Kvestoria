import telebot 
from telebot import types, util
 
class User: 
    def __init__(self, id, name): 
        self.id = id 
        self.name = name 
        self.kvest1 = False 
 
users = {} 
 
client = telebot.TeleBot('5911761685:AAEBXnW9MWLrY6hckAnN2V-xXrXCj1RIWac') 
       
def check_user(func):
    def wrapper(*args, **kwargs):
        if args[0].from_user.id not in users.keys():
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
            key_start = types.KeyboardButton('/start')
            markup.add(key_start)
            client.send_message(args[0].message.chat.id, 'Необходимо зарегистрироваться', parse_mode='html', reply_markup=markup)
            return None
        return func(*args, **kwargs)
    return wrapper


def check_kvest(user_id): 
    if user_id not in users.keys(): 
        return False 
    if users[user_id].kvest1: 
        return 'kvest1' 
    else: 
        return False 
 
@client.message_handler(commands=['start']) 
def start(message): 
    if message.from_user.id not in users.keys(): 
        users[message.from_user.id] = User(message.from_user.id, message.from_user.first_name) 
 
    out_text = f'Приветствую, <b>{message.from_user.first_name}</b>!\n Вы забрели в мою лавку приключений!\n Что это такое? Лавка приключений — это дом для всех, кто хочет стать частью истории! Если ты, путник, жаждешь приключений и неизведанных миров, то ты пришёл в нужное место)\n Здесь меня называют Сказочником. По всем вопросам обращайся ко мне( /help). Чтобы стать частью приключения тебе нужно вызвать книгу квестов и выбрать понравившийся) (/kvest)'
    client.send_message(message.chat.id, out_text, parse_mode='html') 
    client.send_message(message.chat.id, 'Вы зарегистрированны!', parse_mode='html', reply_markup=types.ReplyKeyboardRemove()) 
 
@client.message_handler(commands=['help']) 
def help(message): 
    out_text = f'Привет, путник. У тебя возникли вопросы? Думаю что я могу угадать их: \n/help - показать список команд\n/start - записаться в книгу гостей\n/kvest - открыть книгу квестов'
    client.send_message(message.chat.id, out_text, parse_mode='html') 
 
@client.message_handler(commands=['kvest']) 
@check_user 
def help(message): 
    out_text = f'Вижу ты решил открыть книгу квестов, тогда выбирай мир по душе\n/kvest1 - Квест: "Похищение"' 
    client.send_message(message.chat.id, out_text, parse_mode='html') 
 
@client.message_handler(commands=['kvest1']) 
@check_user 
def help(message): 
    out_text = f'Что делать если вы оказались в тёмной комнате? А если за вами погоня? Проверьте свои навыки везения и выживания' 
    markup = util.quick_markup({ 
        'Отправиться': {'callback_data': 'kvest1'}, 
        'Вернуться': {'callback_data': 'cancel'} 
    }, row_width=2) 
    client.send_message(message.chat.id, out_text, parse_mode='html', reply_markup=markup) 
 
@client.callback_query_handler(func= lambda callback: callback.data) 
@check_user
def check_callback(callback): 
    if callback.data == 'kvest1': 
        users[callback.from_user.id].kvest1 == True 
        out_text = 'Вы оказались в тёмной комнате. Вы не помните ничего. Как вы тут оказались? И кто вы такой? Хотя нет, вы помните имя и где ваш дом.' 
        markup = util.quick_markup({ 
        'Посмотреть в окно': {'callback_data': 'var1.1'}, 
        'Сидеть на месте': {'callback_data': 'var1.2'}, 
        'Попытаться найти дверь': {'callback_data': 'var1.3'} 
        }, row_width=2) 
        client.send_message(callback.message.chat.id, out_text, parse_mode='html', reply_markup=markup) 
 
    if callback.data == 'var1': 
        out_text = 'Вы оказались в тёмной комнате. Вы не помните ничего. Как вы тут оказались? И кто вы такой? Хотя нет, вы знаете где ваш дом.' 
        markup = util.quick_markup({ 
        'Посмотреть в окно': {'callback_data': 'var1.1'}, 
        'Сидеть на месте': {'callback_data': 'var1.2'}, 
        'Попытаться найти дверь': {'callback_data': 'var1.3'} 
        }, row_width=2)
        client.send_message(callback.message.chat.id, out_text, parse_mode='html', reply_markup=markup)
 
    if callback.data == 'var1.1': 
        out_text = 'Вы увидели нескольких людей в чёрном. Они что-то обсуждали' 

        markup = util.quick_markup({ 
        'Позвать их': {'callback_data': 'var2.1'}, 
        'Вернуться в комнату': {'callback_data': 'var1'}, 
        'Подождать': {'callback_data': 'var1.2'} 
        }, row_width=2) 
        client.send_message(callback.message.chat.id, out_text, parse_mode='html', reply_markup=markup) 

    if callback.data == 'var2.1': 
        out_text = 'К вам пришли громилы. Настоения у них явно не было, поэтому они убили вас' 
        markup = util.quick_markup({  
        'Вернуться': {'callback_data': 'cancel'}
        }, row_width=2) 
        client.send_message(callback.message.chat.id, out_text, parse_mode='html', reply_markup=markup) 
  
    if callback.data == 'var1.2': 
        out_text = 'Вы услышали, как кто-то на улице ушёл, после вы заметили, что этот кто-то оставил машину' 
        markup = util.quick_markup({ 
        'Пойти к машине': {'callback_data': 'var2.2'}, 
        'Остаться в комнате': {'callback_data': 'var1'}, 
        'Подождать ещё': {'callback_data': 'var2.3'} 
        }, row_width=2) 
        client.send_message(callback.message.chat.id, out_text, parse_mode='html', reply_markup=markup)

    if callback.data == 'var2.2': 
        out_text = 'Пока вас не видели, вы подошли к машине. Ключа не было' 
        markup = util.quick_markup({  
        'Попробовать угнать': {'callback_data': 'var3.6'},
        'Искать ключ': {'callback_data': 'var3.7'}
        }, row_width=2) 
        client.send_message(callback.message.chat.id, out_text, parse_mode='html', reply_markup=markup)

    if callback.data == 'var3.7': 
        out_text = 'Решив, что ключи могут быть где-то здесь, вы решаете осмотреться. Но где именно их искать?' 
        markup = util.quick_markup({ 
        'Под машиной': {'callback_data': 'var4.4'}, 
        'В машине': {'callback_data': 'var4.5'}, 
        'Вокруг машины': {'callback_data': 'var4.6'} 
        }, row_width=2) 
        client.send_message(callback.message.chat.id, out_text, parse_mode='html', reply_markup=markup)

    if callback.data == 'var4.4': 
        out_text = 'Ваша голова застряла под машиной. Когда те люди пришли, вы уже умерли от нехватки воздуха' 
        markup = util.quick_markup({  
        'Вернуться': {'callback_data': 'cancel'}
        }, row_width=2) 
        client.send_message(callback.message.chat.id, out_text, parse_mode='html', reply_markup=markup)

    if callback.data == 'var4.6': 
        out_text = 'Вас заметили и убили' 
        markup = util.quick_markup({  
        'Вернуться': {'callback_data': 'cancel'}
        }, row_width=2) 
        client.send_message(callback.message.chat.id, out_text, parse_mode='html', reply_markup=markup)

    if callback.data == 'var4.5': 
        out_text = 'Вы успешно нашли ключи и уехали. Куда вам ехать?' 
        markup = util.quick_markup({ 
        'На заправку': {'callback_data': 'var5.9'}, 
        'Домой': {'callback_data': 'var5.8'}, 
        'В деревню': {'callback_data': 'var5.7'} 
        }, row_width=2) 
        client.send_message(callback.message.chat.id, out_text, parse_mode='html', reply_markup=markup)

    if callback.data == 'var5.8': 
        out_text = 'Вы не смогли доехать и умерли от голода' 
        markup = util.quick_markup({  
        'Вернуться': {'callback_data': 'cancel'}
        }, row_width=2) 
        client.send_message(callback.message.chat.id, out_text, parse_mode='html', reply_markup=markup)

    if callback.data == 'var5.7': 
        out_text = 'Вы заехали в деревню, где бабушка предложила вам помощь. Вы попросите у неё:' 
        markup = util.quick_markup({ 
        'Спрятать вас': {'callback_data': 'var5.7.1'}, 
        'Бензин': {'callback_data': 'var5.7.2'}, 
        'Покушать': {'callback_data': 'var5.7.3'} 
        }, row_width=2) 
        client.send_message(callback.message.chat.id, out_text, parse_mode='html', reply_markup=markup)

    if callback.data == 'var5.7.1': 
        out_text = 'Добрая женщина дала вам свою одежду. Теперь вы пастушка Мария.' 
        markup = util.quick_markup({  
        'Поздравляем!': {'callback_data': 'cancel'}
        }, row_width=2) 
        client.send_message(callback.message.chat.id, out_text, parse_mode='html', reply_markup=markup)

    if callback.data == 'var5.7.2': 
        out_text = 'Добрая женщина дала вам бензин вы благополучно доехали домой' 
        markup = util.quick_markup({  
        'Поздравляем!': {'callback_data': 'cancel'}
        }, row_width=2) 
        client.send_message(callback.message.chat.id, out_text, parse_mode='html', reply_markup=markup)

    if callback.data == 'var5.7.3': 
        out_text = 'Добрая женщина дала вам суп. Но кажется она перепутала соль и отраву для мышей. Вы не мышь, но такое не пережили' 
        markup = util.quick_markup({  
        'Вернуться': {'callback_data': 'cancel'}
        }, row_width=2) 
        client.send_message(callback.message.chat.id, out_text, parse_mode='html', reply_markup=markup)

    if callback.data == 'var5.9': 
        out_text = 'Вы заехали на заправку и попросили наполнить бак. Но денег у вас не оказалось. Вам сказали, либо денги, либо рабство' 
        markup = util.quick_markup({ 
        'Поискать в левом кармане': {'callback_data': 'var5.9.1'}, 
        'Убежать': {'callback_data': 'var5.9.2'}, 
        'Поискать в правом кармане': {'callback_data': 'var5.9.3'} 
        }, row_width=2) 
        client.send_message(callback.message.chat.id, out_text, parse_mode='html', reply_markup=markup)

    if callback.data == 'var5.9.1': 
        out_text = 'К счастью вы нашли деньги и уехали домой' 
        markup = util.quick_markup({  
        'Поздравляем!': {'callback_data': 'cancel'}
        }, row_width=2) 
        client.send_message(callback.message.chat.id, out_text, parse_mode='html', reply_markup=markup)

    if callback.data == 'var5.9.2': 
        out_text = 'У вас ничего не получилось. Как только вы сделали шаг в сторону, в вас выстрелили и убили' 
        markup = util.quick_markup({  
        'Вернуться': {'callback_data': 'cancel'}
        }, row_width=2) 
        client.send_message(callback.message.chat.id, out_text, parse_mode='html', reply_markup=markup)

    if callback.data == 'var5.9.3': 
        out_text = 'Вы не нашли денги, поэтому вас продали в рабство на 1.201.018 лет' 
        markup = util.quick_markup({  
        'Вернуться': {'callback_data': 'cancel'}
        }, row_width=2) 
        client.send_message(callback.message.chat.id, out_text, parse_mode='html', reply_markup=markup)

    if callback.data == 'var3.6': 
        out_text = 'Как в крутых боевиках, вам нужно выбрать провод' 
        markup = util.quick_markup({ 
        'Чёрный': {'callback_data': 'var3.6.1'}, 
        'Красный': {'callback_data': 'var3.6.1'}, 
        'Зелёный': {'callback_data': 'var3.6.2'} 
        }, row_width=2) 
        client.send_message(callback.message.chat.id, out_text, parse_mode='html', reply_markup=markup)

    if callback.data == 'var3.6.1': 
        out_text = 'Все в радиусе 5 километров услышали взрыв, а вы нет, потому что умерли(' 
        markup = util.quick_markup({ 
        'Вернуться': {'callback_data': 'cancel'} 
        }, row_width=2) 
        client.send_message(callback.message.chat.id, out_text, parse_mode='html', reply_markup=markup)   

    if callback.data == 'var3.6.2': 
        out_text = 'Не зря вы смотри боевики, так как машина быстро завелась и вы уехали домой' 
        markup = util.quick_markup({ 
        'Поздравляем!': {'callback_data': 'cancel'} 
        }, row_width=2) 
        client.send_message(callback.message.chat.id, out_text, parse_mode='html', reply_markup=markup)   
  
    if callback.data == 'var2.3': 
        out_text = 'Вы так долго находились здесь,что умерли от голода' 
        markup = util.quick_markup({ 
        'Вернуться': {'callback_data': 'cancel'} 
        }, row_width=2) 
        client.send_message(callback.message.chat.id, out_text, parse_mode='html', reply_markup=markup) 
 
    if callback.data == 'var1.3': 
        out_text = 'В комнате было ужасно темно, поэтому осмотреть комнату у вас не получилось' 
        markup = util.quick_markup({ 
        'Ощупать стены': {'callback_data': 'var2.4'}, 
        'Вернуться': {'callback_data': 'var1'}, 
        'Осмотреть карманы': {'callback_data': 'var2.5'} 
        }, row_width=2) 
        client.send_message(callback.message.chat.id, out_text, parse_mode='html', reply_markup=markup) 

    if callback.data == 'var2.4': 
        out_text = 'Через десять минут вы смогли найти дверь' 
        markup = util.quick_markup({ 
        'Открыть дверь': {'callback_data': 'var3.1'}, 
        'Выбить её головой': {'callback_data': 'var3.2'}, 
        'Поговорить с дверью': {'callback_data': 'var3.3'} 
        }, row_width=2) 
        client.send_message(callback.message.chat.id, out_text, parse_mode='html', reply_markup=markup) 

    if callback.data == 'var3.2': 
        out_text = 'Вы отходите и со всей силы врезаетесь головой в дверь. Как жаль, что она была железной(' 
        markup = util.quick_markup({
        'Вернуться': {'callback_data': 'cancel'}
        }, row_width=2) 
        client.send_message(callback.message.chat.id, out_text, parse_mode='html', reply_markup=markup) 

    if callback.data == 'var3.3': 
        out_text = 'Вы сели напротив двери' 
        markup = util.quick_markup({ 
        'Привет!': {'callback_data': 'var3.3.1'}, 
        'Тебе нравится Маяковский?': {'callback_data': 'var3.3.2'}, 
        'Ты мне не нравишься(': {'callback_data': 'var3.3.3'} 
        }, row_width=2) 
        client.send_message(callback.message.chat.id, out_text, parse_mode='html', reply_markup=markup) 

    if callback.data == 'var3.3.1': 
        out_text = 'Удивительно, но дверь поздоровалась с вами. Она оказалась очень интересным собеседником. Казалось вы могли говорить с ней вечно' 
        markup = util.quick_markup({ 
        'Далее': {'callback_data': 'var2.3'}
        }, row_width=2) 
        client.send_message(callback.message.chat.id, out_text, parse_mode='html', reply_markup=markup)

    if callback.data == 'var3.3.2': 
        out_text = 'Дверь ответила вам, что больше любит Есенина. У вас завязался спор. Вы пали жертвой своей точки зрения' 
        markup = util.quick_markup({ 
        'Вернуться': {'callback_data': 'cancel'}
        }, row_width=2) 
        client.send_message(callback.message.chat.id, out_text, parse_mode='html', reply_markup=markup) 

    if callback.data == 'var3.3.3': 
        out_text = 'Оказалось двери очень обидчивые и знают техники каратэ' 
        markup = util.quick_markup({
        'Вернуться': {'callback_data': 'cancel'}
        }, row_width=2) 
        client.send_message(callback.message.chat.id, out_text, parse_mode='html', reply_markup=markup) 

    if callback.data == 'var2.5': 
        out_text = 'Сунув руку в свой карман, вы нашли там телефон.' 
        markup = util.quick_markup({ 
        'Позвонить в полицию': {'callback_data': 'var3.4'}, 
        'Включить фонарик': {'callback_data': 'var2.4'}, 
        'Пограть в игры': {'callback_data': 'var3.5'} 
        }, row_width=2) 
        client.send_message(callback.message.chat.id, out_text, parse_mode='html', reply_markup=markup)

    if callback.data == 'var3.1': 
        out_text = 'Открыв дверь, вы оказались на развилке. Там было три коридора, над которыми были таблички с разными рисунками: паука, капли и без рисунка. В какой же коридор пойти' 
        markup = util.quick_markup({
        'С пауком': {'callback_data': 'var4.1'}, 
        'С каплей': {'callback_data': 'var4.2'}, 
        'Без рисунка': {'callback_data': 'var4.3'} 
        }, row_width=2) 
        client.send_message(callback.message.chat.id, out_text, parse_mode='html', reply_markup=markup)

    if callback.data == 'var4.3': 
        out_text = 'Вы долго шли по коридору и вышли в белое помещение. Осмотревшись, вы поняли, что это лаборотория. Тут к вам подошла женщина, на её бейдже было написанно: "Светлана Александровна Ч.". Она сторого посмотрела на вас. Тогда вы сказали: ' 
        markup = util.quick_markup({
        'Привет!': {'callback_data': 'var5.4'}, 
        'Где я?': {'callback_data': 'var5.5'}, 
        'Здраствуйте, Светлана Александровна': {'callback_data': 'var5.6'} 
        }, row_width=2) 
        client.send_message(callback.message.chat.id, out_text, parse_mode='html', reply_markup=markup)

    if callback.data == 'var5.6': 
        out_text = 'Вас приняли за нового сотрудника. Вы проработали здесь месяц и с первой зарплатой уехади домой' 
        markup = util.quick_markup({  
        'Поздравляем!': {'callback_data': 'cancel'}
        }, row_width=2) 
        client.send_message(callback.message.chat.id, out_text, parse_mode='html', reply_markup=markup)

    if callback.data == 'var5.4': 
        out_text = f'"Ты идёшь со мной" - ответила вам Светлана Александровна. Вас привели в комнату со стульями, однако смущало то, что все они были расставлены в <b>кружочек</b>. Ровно два стула были не заняты. На один села Светлана Александровна, другой, напротив, достался вам.' 
        markup = util.quick_markup({  
        'Сбежать': {'callback_data': 'var5.5'},
        'Остаться': {'callback_data': 'var5.4.1'}
        }, row_width=2) 
        client.send_message(callback.message.chat.id, out_text, parse_mode='html', reply_markup=markup)

    if callback.data == 'var5.4.1': 
        out_text = 'Вы просидели так пять часов. Если бы остались живы, вы бы считали пытки милой игрой' 
        markup = util.quick_markup({  
        'Вернуться': {'callback_data': 'cancel'}
        }, row_width=2) 
        client.send_message(callback.message.chat.id, out_text, parse_mode='html', reply_markup=markup)

    if callback.data == 'var5.5': 
        out_text = '"Подопытный сбежал!" - громко крикнула женщина. Вас быстро поймали и отправили на опыты' 
        markup = util.quick_markup({  
        'Вернуться': {'callback_data': 'cancel'}
        }, row_width=2) 
        client.send_message(callback.message.chat.id, out_text, parse_mode='html', reply_markup=markup)

    if callback.data == 'var4.1': 
        out_text = 'Вы долго шли по коридору, как неожиданно проход вакрылся. Из всех щелей полезли пауки и съели вас' 
        markup = util.quick_markup({  
        'Вернуться': {'callback_data': 'cancel'}
        }, row_width=2) 
        client.send_message(callback.message.chat.id, out_text, parse_mode='html', reply_markup=markup)

    if callback.data == 'var4.2': 
        out_text = 'Вы долго шли по коридору, вдруг вы вышли на берег моря' 
        markup = util.quick_markup({  
        'Уплыть': {'callback_data': 'var5.1'}, 
        'Подождать корабль': {'callback_data': 'var5.2'}, 
        'Пойти к странному человеку': {'callback_data': 'var5.3'} 
        }, row_width=2) 
        client.send_message(callback.message.chat.id, out_text, parse_mode='html', reply_markup=markup)   

    if callback.data == 'var5.1': 
        out_text = 'Вы уверенно зашли в воду и даже проплыли несколько метров. Ах, если бы вы не прогуливали секцию плавания' 
        markup = util.quick_markup({  
        'Вернуться': {'callback_data': 'cancel'}
        }, row_width=2) 
        client.send_message(callback.message.chat.id, out_text, parse_mode='html', reply_markup=markup) 

    if callback.data == 'var5.2': 
        out_text = 'Прождав не больше часа, к берегу приплыл корабль. Вы смогли договориться и вас увезли домой.' 
        markup = util.quick_markup({  
        'Поздравляем!': {'callback_data': 'cancel'}
        }, row_width=2) 
        client.send_message(callback.message.chat.id, out_text, parse_mode='html', reply_markup=markup)

    if callback.data == 'var5.3': 
        out_text = 'Вы подошли к странной женщине-татарке. Она спросила у вас пароль.' 
        markup = util.quick_markup({  
        'Мин сине яратам': {'callback_data': 'var5.3.1'}, 
        'Кэжэ бугы ашатам': {'callback_data': 'var5.3.1'}, 
        'Подкрадуб Бархотяг!': {'callback_data': 'var5.3.2'} 
        }, row_width=2) 
        client.send_message(callback.message.chat.id, out_text, parse_mode='html', reply_markup=markup)

    if callback.data == 'var5.3.1': 
        out_text = 'Пароль оказался неверным и эта странная женщина вас съела' 
        markup = util.quick_markup({  
        'Вернуться': {'callback_data': 'cancel'}
        }, row_width=2) 
        client.send_message(callback.message.chat.id, out_text, parse_mode='html', reply_markup=markup)

    if callback.data == 'var5.3.2': 
        out_text = 'Она довольно кивнула и протянула вам бархатные тяги' 
        markup = util.quick_markup({  
        'Взять с собой': {'callback_data': 'var5.3.3'}, 
        'Выбросить': {'callback_data': 'var5.3.4'}, 
        'Подкрадуб Бархотяг!': {'callback_data': 'var5.3.5'} 
        }, row_width=2) 
        client.send_message(callback.message.chat.id, out_text, parse_mode='html', reply_markup=markup)
    
    if callback.data == 'var5.3.3': 
        out_text = 'Вы долго шли по дороге, но вам очень хотелось есть, тогда вы съели бархатные тяги и умерли от несварения желудка' 
        markup = util.quick_markup({  
        'Вернуться': {'callback_data': 'cancel'}
        }, row_width=2) 
        client.send_message(callback.message.chat.id, out_text, parse_mode='html', reply_markup=markup)
    
    if callback.data == 'var5.3.4': 
        out_text = 'Вы ужасно разозли странную женщину, она наслала на вас порчу на понос. И вы умерли(' 
        markup = util.quick_markup({  
        'Вернуться': {'callback_data': 'cancel'}
        }, row_width=2) 
        client.send_message(callback.message.chat.id, out_text, parse_mode='html', reply_markup=markup)

    if callback.data == 'var5.3.5': 
        out_text = 'Странная женщина от счастья дала вам денег, еды и воды. Вы надели бархатные тяги и счастливо добрались домой.' 
        markup = util.quick_markup({  
        'Поздравляем!': {'callback_data': 'cancel'}
        }, row_width=2) 
        client.send_message(callback.message.chat.id, out_text, parse_mode='html', reply_markup=markup)

    if callback.data == 'var3.5': 
        out_text = 'Вы играли достаточно долго, и вот вы почти победили главного боса, но телефон разрядился. Вы были настолько расстроены, что в порыве гнва кинули телефон в стену. Это была легендарная Nokia 3310, она отлетела от стены и попала прямо вам в голову' 
        markup = util.quick_markup({  
        'Вернуться': {'callback_data': 'cancel'} 
        }, row_width=2) 
        client.send_message(callback.message.chat.id, out_text, parse_mode='html', reply_markup=markup)

    if callback.data == 'var3.4': 
        out_text = 'Вы смогли дозвониться до полиции. Вам сказали, что в течении 2-х дней за вами приедут' 
        markup = util.quick_markup({  
        'Попросить ускориться': {'callback_data': 'var3.4.1'},
        'Подождать': {'callback_data': 'var2.3'},
        'Сказать, что вы важная шишка': {'callback_data': 'var3.4.2'}
        }, row_width=2) 
        client.send_message(callback.message.chat.id, out_text, parse_mode='html', reply_markup=markup) 

    if callback.data == 'var3.4.2': 
        out_text = 'Уже через минуту приехал наряд полиции и спас вас' 
        markup = util.quick_markup({  
        'Поздравляем!': {'callback_data': 'cancel'}
        }, row_width=2) 
        client.send_message(callback.message.chat.id, out_text, parse_mode='html', reply_markup=markup) 

    if callback.data == 'var3.4.1': 
        out_text = 'Через час приехал наряд полиции, но они приняли вас за террориста и убили' 
        markup = util.quick_markup({  
        'Вернуться': {'callback_data': 'cancel'}
        }, row_width=2) 
        client.send_message(callback.message.chat.id, out_text, parse_mode='html', reply_markup=markup) 

    if callback.data == 'cancel':
        users[callback.from_user.id].kvest1 == False
        out_text = 'До встречи) Прошу вас оценить бота: https://forms.gle/uHwn1T76QMDxyqtU8' 
        markup = util.quick_markup({  
        'Начать заново': {'callback_data': 'kvest1'}
        }, row_width=2) 
        client.send_message(callback.message.chat.id, out_text, parse_mode='html', reply_markup=markup) 

    return 
 
client.polling(non_stop=True, interval=0)
