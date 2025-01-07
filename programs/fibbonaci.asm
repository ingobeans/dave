main:
    define amount_value 10i
    define num1_pos 1i
    define num2_pos 2i
    define next_num_pos 3i
    define counter_pos 0i

    wra 0i
    sta num1_pos
    wra 1i
    sta num2_pos
    sta next_num_pos
    sta counter_pos

loop:
    lda counter_pos
    wrb 1i
    add
    sta counter_pos
    wrb amount_value
    xor
    giz end
    lda num2_pos
    sta num1_pos
    ldb next_num_pos
    stb num2_pos
    lda num1_pos
    add
    sta next_num_pos
    goto loop
end:
    lda num1_pos
    hlt
