define x_pos 0i
define y_pos 1i

main:
    wrb 0i
    stb y_pos
    wra 4i
    sta x_pos

goright:
    lda x_pos
    wrb 1i
    add
    sta x_pos
    goto draw

goleft:
    lda x_pos
    wrb 1i
    sub
    sta x_pos
    goto draw

loop:
    lda 7i4 0i4
    wrb 00000001
    xor
    giz goright

    lda 7i4 0i4
    wrb 00000010
    xor
    giz goleft
    wrb 1i

draw:
    lda x_pos
    shl
    shl
    shl
    sta 7i4 0i4
    or
    wra 10000000
    sta 7i4 0i4
    goto loop
