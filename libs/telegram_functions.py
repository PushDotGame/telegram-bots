import telegram


def user2name(user: telegram.User):
    names = list()

    if user.first_name:
        names.append(user.first_name)
    if user.last_name:
        names.append(user.last_name)

    return ' '.join(names)
