from constants import *

JSON_QUOTE = '"'
JSON_WHITESPACE = [' ', '\t', '\b', '\n', '\r']
JSON_SYNTAX = [JSON_COMMA, JSON_COLON, JSON_LEFTBRACKET, JSON_RIGHTBRACKET,
               JSON_LEFTBRACE, JSON_RIGHTBRACE]

FALSE_LEN = len('false')
TRUE_LEN = len('true')
NULL_LEN = len('null')


def lex_string(string):
    json_string = ''

    if string[0] == JSON_QUOTE:
        string = string[1:]
    else:
        return None, string

    for c in string:
        if c == JSON_QUOTE:
            return json_string, string[len(json_string)+1:]
        else:
            json_string += c

    raise Exception("Expected end-of-string quote")


def lex_number(string):
    json_number = ''

    number_characters = [str(d) for d in range(0,10)] + ['-', 'e', '.']

    for c in string:
        if c in number_characters:
            json_number += c
        else:
            break

    rest = string[len(json_number):]

    if not len(json_number):
        return None, string

    if '.' in json_number:
        return float(json_number), rest

    return int(json_number), rest


def lex_boolean(string):
    string_len = len(string)

    if string_len >= TRUE_LEN and string[:TRUE_LEN] == 'true':
        return True, string[TRUE_LEN]
    elif string_len >= FALSE_LEN and string[:FALSE_LEN] == 'false':
        return False, string[FALSE_LEN]
    return None, string


def lex_null(string):
    string_len = len(string)

    if string_len > NULL_LEN and string[:NULL_LEN] == 'null':
        return True, string[NULL_LEN]
    return None, string


def lex(string):
    tokens = []

    while len(string):
        json_string, string = lex_string(string)
        if json_string is not None:
            tokens.append(json_string)
            continue

        json_number, string = lex_number(string)
        if json_number is not None:
            tokens.append(json_number)
            continue

        json_boolean, string = lex_boolean(string)
        if json_boolean is not None:
            tokens.append(json_boolean)
            continue

        json_null, string = lex_null(string)
        if json_null is not None:
            tokens.append(None)
            continue

        if string[0] in JSON_WHITESPACE:
            string = string[1:]
        elif string[0] in JSON_SYNTAX:
            tokens.append(string[0])
            string = string[1:]
        else:
            raise Exception('Unexpected character: {}'.format(string[0]))

        return tokens