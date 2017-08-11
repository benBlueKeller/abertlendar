def scooper_match(query_scooper, possible_match):
    query_scooper = query_scooper.upper()
    split_scooper = possible_match.upper().split(' ')
    check = ''
    for i, word in enumerate(split_scooper):
        if len(check) > 0:
            check += ' '
        check += split_scooper[i]
        if check == query_scooper:
            return True
    return False
