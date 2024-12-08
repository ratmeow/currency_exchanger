def check_string_is_all_alpha(string: str):
    return all(list(map(str.isalpha, string.split(" "))))
