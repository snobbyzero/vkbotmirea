from flask import Flask
import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.utils import get_random_id
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
import rasp
from flask import Flask

app = Flask(__name__)

@app.route('/', methods=["GET"])
def main():
    professors_arr = []
    vk_session = vk_api.VkApi(
        token="e6580105a6219e09a3e35347cce1f31ef50e952ea3b5c4cf64f333c686774977b81b5b38ab6a5402a4d1b")
    vk = vk_session.get_api()
    longpoll = VkLongPoll(vk_session)
    #главная клавиатура
    keyboard = VkKeyboard()
    keyboard.add_button("Сегодня")
    keyboard.add_button("Завтра")
    keyboard.add_line()
    keyboard.add_button("На эту неделю")
    keyboard.add_button("На следующую неделю")
    keyboard.add_line()
    keyboard.add_button("Какая неделя")
    keyboard.add_button("Какая группа")
    #клавиатура для поиска преподавателя 
    lecturer_keyboard = VkKeyboard()
    lecturer_keyboard.add_button("сегодня")
    lecturer_keyboard.add_button("завтра")
    lecturer_keyboard.add_line()
    lecturer_keyboard.add_button("эта неделя")
    lecturer_keyboard.add_button("следующая неделя")
    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
            if (
                str(event.text) == "Начать" or
                str(event.text).lower() == "инструкция"
            ):
                vk.messages.send(
                    user_id=event.user_id,
                    random_id=get_random_id(),
                    message="""
                        Краткая инструкция по работе с ботом:
                        1. Чтобы узнать сегодняшние пары -- "сегодня"
                        2. Чтобы узнать завтрашние пары -- "завтра"
                        3. Чтобы узнать пары на неделю -- "на неделю"
                        4. Чтобы узнать пары на следующую неделю -- "на следующую неделю"
                        5. Чтобы узнать номер недели -- "какая неделя"
                        6. Чтобы узнать группу, для которой выводится расписание -- "какая группа"

                        Для начала работы введите номер группы:
                        """,
                    keyboard = keyboard.get_keyboard()
                )
            elif len(professors_arr) == 1:
                if (
                    str(event.text) == "сегодня" or
                    str(event.text) == "завтра" or
                    str(event.text) == "эта неделя" or
                    str(event.text) == "следующая неделя"
                ):
                    vk.messages.send(
                        user_id=event.user_id,
                        random_id=get_random_id(),
                        message=rasp.professor_rasp(professors_arr[0], str(event.text)),
                        keyboard = keyboard.get_keyboard()
                    )
                    professors_arr.clear()
            elif (str(event.text).upper() in rasp.groups_list):
                vk.messages.send(
                    user_id=event.user_id,
                    random_id=get_random_id(),
                    message="Я записал Вашу группу",
                    keyboard = keyboard.get_keyboard()
                )
                rasp.set_group(event.user_id, str(event.text).upper())
            elif (
                str(event.text).split(" ")[0].lower() in
                ["понедельник", "вторник", "среда", "четверг", "пятница", "суббота"] and
                str(event.text).split(" ")[1].upper() in rasp.groups_list
            ):
                vk.messages.send(
                    user_id=event.user_id,
                    random_id=get_random_id(),
                    message="".join(rasp.daygroup_rasp(
                        ["понедельник", "вторник", "среда", "четверг", "пятница", "суббота"]
                        .index(str(event.text).split(" ")[0].lower()),
                        str(event.text).split(" ")[1].upper())),
                    keyboard = keyboard.get_keyboard()
                )
            elif (
                str(event.text).lower() == "сегодня" or
                str(event.text).lower() == "пары" or
                str(event.text).lower() == "пары сегодня" or 
                str(event.text).lower() == "пары на сегодня" or
                str(event.text).lower() == "сегодняшние пары"
            ):
                vk.messages.send(
                    user_id=event.user_id,
                    random_id=get_random_id(),
                    message="".join(rasp.today_rasp(event.user_id)),
                    keyboard = keyboard.get_keyboard()
                )
            elif (
                str(event.text).lower() == "завтра" or 
                str(event.text).lower() == "пары завтра" or
                str(event.text).lower() == "пары на завтра" or
                str(event.text).lower() == "завтрашние пары"
            ):
                vk.messages.send(
                    user_id=event.user_id,
                    random_id=get_random_id(),
                    message="".join(rasp.tomorrow_rasp(event.user_id)),
                    keyboard = keyboard.get_keyboard()
                )
            elif (
                str(event.text).lower() == "на эту неделю" or
                str(event.text).lower() == "на неделю" or
                str(event.text).lower() == "пары на неделю" or
                str(event.text).lower() == "пары на эту неделю"
            ):
                vk.messages.send(
                    user_id=event.user_id,
                    random_id=get_random_id(),
                    message="".join(rasp.week_rasp(event.user_id)),
                    keyboard = keyboard.get_keyboard()
                )
            elif (
                str(event.text).lower() == "на следующую неделю" or
                str(event.text).lower() == "пары на следующую неделю"
            ):
                vk.messages.send(
                    user_id=event.user_id,
                    random_id=get_random_id(),
                    message="".join(rasp.nextweek_rasp(event.user_id)),
                    keyboard = keyboard.get_keyboard()
                )
            elif (
                str(event.text).lower() == "какая группа" or
                str(event.text).lower() == "номер группы"
            ):
                vk.messages.send(
                    user_id=event.user_id,
                    random_id=get_random_id(),
                    message="Я смотрю расписание для группы " + rasp.get_group(event.user_id),
                    keyboard = keyboard.get_keyboard()
                )
            elif (
                str(event.text).lower() == "какая неделя" or
                str(event.text).lower() == "номер недели"
            ):
                vk.messages.send(
                    user_id=event.user_id,
                    random_id=get_random_id(),
                    message="Сейчас идет " + rasp.get_week() + " неделя",
                    keyboard = keyboard.get_keyboard()
                )
            elif (
                str(event.text).lower().startswith("найти")
            ):
                professors_arr = rasp.professors(str(event.text).lower().replace("найти ", ""))
                # Если преподаватель не найден
                if len(professors_arr) == 0:
                    vk.messages.send(
                        user_id=event.user_id,
                        random_id=get_random_id(),
                        message="Преподаватель не найден"
                    )
                elif len(professors_arr) == 1:
                    # Если найден лишь один преподаватель с данной фамилией
                    vk.messages.send(
                        user_id=event.user_id,
                        random_id=get_random_id(),
                        message="Выберите день или неделю",
                        keyboard = lecturer_keyboard.get_keyboard()
                    )
                else:
                    # Создание клавиатуры с фамилиями и инициалами преподавателя
                    professors_keyboard = VkKeyboard()
                    professors_keyboard.add_button(professors_arr[0])
                    for i in range(1, len(professors_arr)):
                        professors_keyboard.add_line()
                        professors_keyboard.add_button(professors_arr[i])
                    vk.messages.send(
                        user_id=event.user_id,
                        random_id=get_random_id(),
                        message="Уточните инициалы преподователя:",
                        keyboard=professors_keyboard.get_keyboard()
                    )
            # Если преподаватель найден или выбран среди предложенных,
            # появляется клавиатура с выбором дня или недели
            elif str(event.text) in professors_arr:
                vk.messages.send(
                    user_id=event.user_id,
                    random_id=get_random_id(),
                    message="Выберите день или неделю",
                    keyboard = lecturer_keyboard.get_keyboard()
                )
                professors_arr.clear()
                professors_arr.append(str(event.text))
            else:
                vk.messages.send(
                    user_id=event.user_id,
                    random_id=get_random_id(),
                    message="Я ничего не смог найти, не ругайтесь, пожалуйста",
                    keyboard = keyboard.get_keyboard()
                )


if __name__ == "__main__":
    app.run(debug=True)
