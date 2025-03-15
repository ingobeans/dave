define current_x 0i
define current_y 1i
define temp_x 2i

define slope_value 1i

loop:
    lda current_x
    shl
    shl
    shl
    sta temp_x
    lda current_x
    wrb 1i
    add
    sta current_x

# calc y
    lda current_y
    wrb slope_value
    add
    sta current_y
# check if y is too big
    wrb 11110111
    or
    wrb 11111111
    xor
    giz end
# restore a reg to y
    lda current_y
    wrb 00000111
    and
# write point
    ldb temp_x
    or
    sta 7i4 0i4
    goto loop

end:
# flush screen
    wra 10000000
    sta 7i4 0i4
    f:
    goto f