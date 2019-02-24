from bs4.element import NavigableString, Tag


def parse_content(content):
    '''Parses string content from nested BeautifulSoup objects

    Args:
        content (bs4.element): element to pull string info out of

    Returns:
        string: concatenation of all embedded string elements
    '''
    parsed_content = ""
    for item in content:
        if type(item) is NavigableString:
            parsed_content += item.string
        elif type(item) is Tag:
            parsed_content += parse_content(item)
        else:
            print('what is going on')
    return parsed_content
