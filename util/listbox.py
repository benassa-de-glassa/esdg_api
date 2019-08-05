

def list_to_option(string_list):
    """
    takes a list and returns it as html option tags
    """
    options = ''
    for element in string_list:
        options += '<option value="{}"> {} </option>'.format(element, element)
    return options