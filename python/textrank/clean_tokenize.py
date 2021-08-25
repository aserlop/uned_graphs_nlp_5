import re
from typing import List, Tuple


def clean_tokenize(raw_text: str,
                   repeated_char_list: List[str],
                   valid_pattern: str,
                   valid_tag_list: List[str]) -> List[str]:
    """
    From a raw text, if follows these steps:
        - Remove repeated characters
        - Split the text in a token list
        - Validate token-tag pattern
        - Get only valid tags
        - Lower words
    :param raw_text: Raw text to process
    :param repeated_char_list: list of characters to remove consecutive repetitions
    :param valid_pattern: Pattern of the tokens
    :param valid_tag_list: Tags to filter
    :return: List of cleaned tokens
    """
    clean_text = remove_repeated_char(raw_text, repeated_char_list)

    token_list = [token for token in clean_text.split(' ')]
    token_list = [token for token in token_list if re.match(valid_pattern, token) and len(token.split('/')) == 2]

    if len(valid_tag_list) > 0:
        token_list = [token for token in token_list if check_tag_is_valid(token, valid_tag_list)]

    token_list = [lower_only_word(token) for token in token_list]

    return token_list


def remove_repeated_char(input_str: str, remove_char_list: List[str]) -> str:
    """
    Remove from a string repeated characters based on a list
    :param input_str: input to remove characters
    :param remove_char_list: characters to remove
    :return: clean string
    """

    output_str = input_str
    for c in remove_char_list:
        pattern = re.compile(f'{c}' + '{2,}', re.I)
        output_str = re.sub(pattern, c, input_str)

    return output_str


def untag(word_tag: str) -> Tuple[str, str]:
    """
    Separe any token in two chunks, the word and the token.
    :param word_tag: word-tag separated by '/', it must only have one '/' in the wort-tag
    :return: splitted word and tag
    """

    wt_list = word_tag.split('/')

    return wt_list[0], wt_list[1]


def lower_only_word(word_tag: str) -> str:
    """
    Lowers only the word in the wort-tag
    :param word_tag: word-tag containing the word to lower
    :return: lowered word-tag
    """
    w, t = untag(word_tag)
    w = w.lower()
    lowered_token_tag = '/'.join([w, t])

    return lowered_token_tag


def check_tag_is_valid(word_tag: str, valid_tag_list: List[str]) -> bool:
    """
    Check if tag is valid based on a list and returns a boolean
    :param word_tag: word-tag to validate
    :param valid_tag_list: valid tags list
    :return: boolean indicating if condition is met
    """
    w, t = untag(word_tag)

    if t in valid_tag_list:
        return True
    else:
        return False









