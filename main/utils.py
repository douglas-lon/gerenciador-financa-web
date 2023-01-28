
def is_number(n):
    n = n.strip()

    if ',' in n:
        n = n.split(',')
    if '.' in n:
        n = n.split('.')

    if type(n) == list:

        digits = 0
        for s in n:
            if s.isdigit() or n[0][0] == '-':
                digits += 1
        
        if digits == len(n):
            return '.'.join(n)
    else:
        
        if n.startswith('-'):
            n = n.replace('-', '')
            if n.isdigit():
                return '-' + n
        elif n.isdigit():
            return n

    return ''

if __name__ == '__main__':
    print(is_number('65,36'))
    print(is_number('-65,36'))
    print(is_number('-65.36'))
    print(is_number('65.36'))
    if is_number('22'):
        print('BBBBB')
    print(is_number('-22'))
    print(is_number('ab'))
    if is_number('22,ba'):
        print('aaaa')
