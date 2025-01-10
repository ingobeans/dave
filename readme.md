# dave

dave is a cpu i built in scrap mechanic. i made an emulator and assembler for it in this project.

assembler.py will convert a file of instructions to binary, and export to output/binary.txt and output/readable.txt

which you can copy to the "physical" machine or run directly in emulator.

recommended extension: [Assembler code syntax and highlight](https://marketplace.visualstudio.com/items?itemName=Toeffe3.asm-syntaxhighlight)

# instructions

```
X 00000000			nop
X 00000001	i4 i4	        lda
X 00000010	i4 i4	        ldb
X 00000011	i4 i4	        sta
X 00000100	i4 i4	        stb
X 00000101			add
X 00000110			sub
_ 00000111			mul
_ 00001000			div
X 00001001	i8		goto
X 00001010	i8		giz
X 00001011	i8		gnz
_ 00001100
X 00001101	d8		wra
X 00001110	d8		wrb
_ 00001111
X 00010000			and
X 00010001			or
X 00010010			xor
X 00010011			nand
X 00010100			nor
X 00010101			xnor
X 00010110          shr
X 00010111          shl
X 11111111			hlt
```
