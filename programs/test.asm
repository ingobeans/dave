wra 0i
sta 0i

loop:
    lda 0i
    wrb 1i
    add
    sta 0i
    
    wrb 10i
    xor
    giz end
    
    goto loop
end:
    lda 0i
    hlt