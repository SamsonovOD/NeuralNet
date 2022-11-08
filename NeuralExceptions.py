class SizeException(Exception):
    def __str__(self):
        return "Вход не соответствует размеру нейрона!"


class ReadyException(Exception):
    def __str__(self):
        return "Нейрон уже обработан!"


class TypeException(Exception):
    def __str__(self):
        return "Ввод не числовой!"


class PrivateException(Exception):
    def __str__(self):
        return "Изменение не через публичный метод!"
