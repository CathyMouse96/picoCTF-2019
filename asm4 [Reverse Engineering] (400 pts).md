# asm4 [Reverse Engineering] (400 pts)

What will asm4("picoCTF_75806") return? Submit the flag as a hexadecimal value (starting with '0x'). NOTE: Your submission for this question will NOT be in the normal flag format. [Source](https://2019shell1.picoctf.com/static/97b85761d65b68113bf3c3f6143b17a6/test.S) located in the directory at /problems/asm4_6_0a1c480ca5c932037f143f80d653e3a8.

------

After the initial setup, the stack looks like this:

| Address  | Content                    |
| -------- | -------------------------- |
| ebp+8    | Address of "picoCTF_75806" |
| ebp+4    | Return address             |
| ebp      | Old ebp                    |
| ebp-4    | Old ebx                    |
| ebp-8    |                            |
| ebp-0xc  | 0x0                        |
| ebp-0x10 | 0x276                      |

```assembly
<+23>:  add    DWORD PTR [ebp-0xc],0x1
<+27>:  mov    edx,DWORD PTR [ebp-0xc]
<+30>:  mov    eax,DWORD PTR [ebp+0x8]
<+33>:  add    eax,edx
<+35>:  movzx  eax,BYTE PTR [eax]
<+38>:  test   al,al
<+40>:  jne    0x514 <asm4+23>
```

This part counts the number of characters in the input string and stores it at `ebp-0xc`. So after this part, the value stored at `ebp-0xc` will be 0xd.

```assembly
<+42>:  mov    DWORD PTR [ebp-0x8],0x1
<+49>:  jmp    0x587 <asm4+138>
```

Stores 0x1 at `ebp-0x8`. Updated stack:

| Address  | Content |
| -------- | ------- |
| ebp-8    | 0x1     |
| ebp-0xc  | 0xd     |
| ebp-0x10 | 0x276   |

```assembly
<+138>: mov    eax,DWORD PTR [ebp-0xc]
<+141>: sub    eax,0x1
<+144>: cmp    DWORD PTR [ebp-0x8],eax
<+147>: jl     0x530 <asm4+51>
```

0x1 is less than 0xc, so we jump to `asm4+51`.

This is a long loop, so let's dissect it little by little:

```assembly
<+51>:  mov    edx,DWORD PTR [ebp-0x8]
<+54>:  mov    eax,DWORD PTR [ebp+0x8]
<+57>:  add    eax,edx
<+59>:  movzx  eax,BYTE PTR [eax]
<+62>:  movsx  edx,al
```

`edx` now contains `input_string[1]`, which is 'i'.

```assembly
<+65>:  mov    eax,DWORD PTR [ebp-0x8]
<+68>:  lea    ecx,[eax-0x1]
<+71>:  mov    eax,DWORD PTR [ebp+0x8]
<+74>:  add    eax,ecx
<+76>:  movzx  eax,BYTE PTR [eax]
<+79>:  movsx  eax,al
```

`eax` now contains `input_string[0]`, which is 'p'.

```assembly
<+82>:  sub    edx,eax
<+84>:  mov    eax,edx
<+86>:  mov    edx,eax
<+88>:  mov    eax,DWORD PTR [ebp-0x10]
<+91>:  lea    ebx,[edx+eax*1]
```

The value of `edx` becomes 'i' - 'p', which is -7. The value of `ebx` becomes -7 + 0x276 = 0x26f.

```assembly
<+94>:  mov    eax,DWORD PTR [ebp-0x8]
<+97>:  lea    edx,[eax+0x1]
<+100>: mov    eax,DWORD PTR [ebp+0x8]
<+103>: add    eax,edx
<+105>: movzx  eax,BYTE PTR [eax]
<+108>: movsx  edx,al
```

`edx` now contains `input_string[2]`, which is 'c'.

```assembly
<+111>: mov    ecx,DWORD PTR [ebp-0x8]
<+114>: mov    eax,DWORD PTR [ebp+0x8]
<+117>: add    eax,ecx
<+119>: movzx  eax,BYTE PTR [eax]
<+122>: movsx  eax,al
```

`eax` now contains `input_string[1]`, which is 'i'.

```assembly
<+125>: sub    edx,eax
<+127>: mov    eax,edx
<+129>: add    eax,ebx
<+131>: mov    DWORD PTR [ebp-0x10],eax
<+134>: add    DWORD PTR [ebp-0x8],0x1
<+138>: mov    eax,DWORD PTR [ebp-0xc]
<+141>: sub    eax,0x1
<+144>: cmp    DWORD PTR [ebp-0x8],eax
<+147>: jl     0x530 <asm4+51>
```

The value of `edx` becomes 'c' - 'i', which is -6. The value stored at `ebp-0x10` becomes -6 + 0x26f = 0x269.

Updated stack:

| Address  | Content |
| -------- | ------- |
| ebp-8    | 0x2     |
| ebp-0xc  | 0xd     |
| ebp-0x10 | 0x269   |

0x2 is less than 0xc, so we jump to `asm4+51` again.

By now we can stop manually going over the loops, because we've already figured out what the code does. Essentially, for each `i` in 1 to 11, it calculates `input_string[i]` - `input_string[i-1]` + `input_string[i+1]` - `input_string[i]` and adds to the total, which is initially 0x276. So we can write a simple Python script for calculating this, and the result turns out to be 515, or 0x203 in hex.