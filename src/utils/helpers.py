def check_string_is_all_alpha(string: str):
    print(string)
    return all(list(map(str.isalpha, string.split(" "))))
