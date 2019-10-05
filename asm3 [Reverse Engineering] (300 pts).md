# asm3 [Reverse Engineering] (300 pts)

What does asm3(0xaeed09cb,0xb7acde91,0xb7facecd) return? Submit the flag as a hexadecimal value (starting with '0x'). NOTE: Your submission for this question will NOT be in the normal flag format. [Source](https://2019shell1.picoctf.com/static/03606da9fe90cfe7e76b9d78259c0630/test.S) located in the directory at /problems/asm3_0_9cdf5fc9325b2a6276fb8e5908f0b5df.

------

Since machines are little endian, the parameters will be stored like this on the stack (addresses are relative to the base pointer):

| Address | 8    | 9    | a    | b    | c    | d    | e    | f    | 10   | 11   | 12   | 13   |
| ------- | ---- | ---- | ---- | ---- | ---- | ---- | ---- | ---- | ---- | ---- | ---- | ---- |
| Value   | cb   | 09   | ed   | ae   | 91   | de   | ac   | b7   | cd   | ce   | fa   | b7   |

```assembly
<+3>:   xor    eax,eax
```

`eax` is set to 0.

```assembly
<+5>:   mov    ah,BYTE PTR [ebp+0xb]
```

`ah` is set to 0xae.

```assembly
<+8>:   shl    ax,0x10
```

`ax` becomes 0 again.

```assembly
<+12>:  sub    al,BYTE PTR [ebp+0xe]
```

`al` becomes 0x54 (equivalent to ~0xac+1).

```assembly
<+15>:  add    ah,BYTE PTR [ebp+0xd]
```

`ah` becomes 0xde.

```assembly
<+18>:  xor    ax,WORD PTR [ebp+0x12]
```

`ax` becomes 0x69ae (0xde54^0xb7fa).

The flag is 0x69ae.