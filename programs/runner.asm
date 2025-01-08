define y_pos 0i

main:
    wrb 1i
    wra 0i
    sta y_pos

loop:
    lda 7i4 0i4
    xor
    giz jump

    lda y_pos
    gnz fall

draw:
    lda y_pos
    wrb 00000111
    and
    wrb 00100000
    or
    sta 7i4 0i4
    wra 10000000
    sta 7i4 0i4
    wrb 1i
    goto loop

jump:
    lda y_pos
    add
    sta y_pos
    goto draw

fall:
    lda y_pos
    sub
    sta y_pos
    goto draw