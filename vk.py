import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.utils import get_random_id


def main():
    vk_session = vk_api.VkApi(
        token="e6580105a6219e09a3e35347cce1f31ef50e952ea3b5c4cf64f333c686774977b81b5b38ab6a5402a4d1b")
    vk = vk_session.get_api()
    longpoll = VkLongPoll(vk_session)
    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
            if str(event.text).lower() == "здрасьте" or str(event.text).lower() == "здрасте":
                vk.messages.send(
                    user_id=event.user_id,
                    random_id=get_random_id(),
                    message="Пизду покрасьте!"
                )
            elif str(event.text).endswith("ет".lower()):
                vk.messages.send(
                    user_id=event.user_id,
                    random_id=get_random_id(),
                    message="Говна пакет"
                )
            elif str(event.text).endswith("да".lower()):
                vk.messages.send(
                    user_id=event.user_id,
                    random_id=get_random_id(),
                    message="Пизда!"
                )
            elif str(event.text).lower() == "приветик":
                vk.messages.send(
                    user_id=event.user_id,
                    random_id=get_random_id(),
                    message="Пукни в пакетик!"
                )
            else:
                vk.messages.send(
                    user_id=event.user_id,
                    random_id=get_random_id(),
                    message="Попу мыл?"
                )


if __name__ == "__main__":
    main()
