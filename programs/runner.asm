define cactus_x_pos 1i
define map_end 15i
define dino_y_pos 0i

main:
# set up variables
    wra 0i
    sta dino_y_pos
    wra 16i
    sta cactus_x_pos

    wrb 1i

loop:
# update dino
    lda dino_y_pos
    gnz fall

    lda 7i4 0i4
    xor
    giz jump

    lda cactus_x_pos
    wrb 4i
    xor
    giz lose
    wrb 1i

draw:
# move cactus
    lda cactus_x_pos
    sub
    sta cactus_x_pos
# draw cactus
    lda cactus_x_pos
    wrb 00001111
    and
    sta cactus_x_pos
    shl
    shl
    shl
    sta 7i4 0i4

# draw dino
    lda dino_y_pos
    wrb 00000111
    and
    wrb 00100000
    or
    sta 7i4 0i4

# update drawn frame
    wra 10000000
    sta 7i4 0i4
    wrb 1i
    goto loop

jump:
    lda dino_y_pos
    add
    add
    add
    sta dino_y_pos
    goto draw

fall:
    sub
    sta dino_y_pos
    goto draw

lose:
    lda dino_y_pos
    wrb 0i
    xor
    wrb 1i
    gnz draw
hlt