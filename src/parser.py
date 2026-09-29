"""Парсер командной строки с поддержкой кавычек."""


class ParseError(Exception):
    """Ошибка разбора строки."""


def parse(line: str) -> list[str]:
    """Разбирает строку на токены с поддержкой кавычек.

    Аргументы в одинарных или двойных кавычках сохраняются
    как единый токен вместе с пробелами внутри.

    :param line: входная строка
    :type line: str
    :return: список токенов
    :rtype: list[str]
    :raises ParseError: при незакрытой кавычке
    """
    tokens: list[str] = []
    buf: list[str] = []
    quote: str | None = None

    for ch in line:
        if quote is not None:
            if ch == quote:
                quote = None
            else:
                buf.append(ch)
        elif ch in ('"', "'"):
            quote = ch
        elif ch.isspace():
            if buf:
                tokens.append("".join(buf))
                buf = []
        else:
            buf.append(ch)

    if quote is not None:
        raise ParseError("незакрытая кавычка")

    if buf:
        tokens.append("".join(buf))

    return tokens
