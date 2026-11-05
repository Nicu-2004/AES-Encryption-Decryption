from .tables import s_box, inv_s_box, r_con
from .utils import bytes2matrix, matrix2bytes, xtime

N_ROUNDS = 10

def add_round_key(s, k):
    for i in range(4):
        for j in range(4):
            s[i][j] ^= k[i][j]

def inv_sub_bytes(s):
    for i in range(4):
        for j in range(4):
            s[i][j] = inv_s_box[s[i][j]]

def mix_single_column(a):
    t = a[0] ^ a[1] ^ a[2] ^ a[3]
    u = a[0]
    a[0] ^= t ^ xtime(a[0] ^ a[1])
    a[1] ^= t ^ xtime(a[1] ^ a[2])
    a[2] ^= t ^ xtime(a[2] ^ a[3])
    a[3] ^= t ^ xtime(a[3] ^ u)

def mix_columns(s):
    for i in range(4):
        mix_single_column(s[i])

def inv_mix_columns(s):
    for i in range(4):
        u = xtime(xtime(s[i][0] ^ s[i][2]))
        v = xtime(xtime(s[i][1] ^ s[i][3]))
        s[i][0] ^= u
        s[i][1] ^= v
        s[i][2] ^= u
        s[i][3] ^= v
    mix_columns(s)

def expand_key(master_key):
    key_columns = bytes2matrix(master_key)
    iteration_size = len(master_key) // 4

    i = 1
    while len(key_columns) < (N_ROUNDS + 1) * 4:
        word = list(key_columns[-1])

        if len(key_columns) % iteration_size == 0:
            word.append(word.pop(0))
            word = [s_box[b] for b in word]
            word[0] ^= r_con[i]
            i += 1
        elif len(master_key) == 32 and len(key_columns) % iteration_size == 4:
            word = [s_box[b] for b in word]

        word = [a ^ b for a, b in zip(word, key_columns[-iteration_size])]
        key_columns.append(word)

    return [key_columns[4*i : 4*(i+1)] for i in range(len(key_columns) // 4)]

def sub_bytes(s):
    for i in range(4):
        for j in range(4):
            s[i][j] = s_box[s[i][j]]

def shift_rows(s):
    for i in range(1, 4):
        old = [s[col][i] for col in range(4)]
        for col in range(4):
            s[col][i] = old[(col + i) % 4]

def inv_shift_rows(s):
    for i in range(1, 4):
        old = [s[col][i] for col in range(4)]
        for col in range(4):
            s[(col + i) % 4][i] = old[col]

def encrypt_block(key, plaintext):
    round_keys = expand_key(key)
    state = bytes2matrix(plaintext)

    add_round_key(state, round_keys[0])
    for i in range(1, N_ROUNDS):
        sub_bytes(state)
        shift_rows(state)
        mix_columns(state)
        add_round_key(state, round_keys[i])

    sub_bytes(state)
    shift_rows(state)
    add_round_key(state, round_keys[N_ROUNDS])
    return matrix2bytes(state)

def decrypt_block(key, ciphertext):
    round_keys = expand_key(key)
    state = bytes2matrix(ciphertext)

    add_round_key(state, round_keys[N_ROUNDS])
    for i in range(N_ROUNDS - 1, 0, -1):
        inv_shift_rows(state)
        inv_sub_bytes(state)
        add_round_key(state, round_keys[i])
        inv_mix_columns(state)

    inv_shift_rows(state)
    inv_sub_bytes(state)
    add_round_key(state, round_keys[0])
    return matrix2bytes(state)