"""
Prompt: I stopped using YellowPages and moved onto WhitePages... but the page they gave me is all blank!

File: UTF-8 text file, consisting of the SPACE character (20) and the EM SPACE character (e28083).

Solution: Map all the EM SPACE characters to 0 bit and SPACE characters to 1 bit. Then decode with ASCII.
"""

with open('whitepages.txt', 'rb') as f:
    unicode_str = f.read().decode('UTF-8')
    bit_list = []
    for unicode_char in unicode_str:
        if unicode_char == '\u0020':
            bit_list.append('1')
        elif unicode_char == '\u2003':
            bit_list.append('0')
    bit_int = int(''.join(bit_list), 2)
    ascii_str = bit_int.to_bytes((bit_int.bit_length() + 7) // 8, 'big').decode()
    print(ascii_str)

