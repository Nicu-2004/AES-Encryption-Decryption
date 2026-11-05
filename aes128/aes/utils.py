xtime = lambda a: (((a << 1) ^ 0x1B) & 0xFF) if (a & 0x80) else (a << 1)

def bytes2matrix(text):
    matrix = []
    for i in range(0, len(text), 4):
        row = []
        for j in range(i, i+4):
            row.append(text[j])
        matrix.append(row)
    return matrix

def matrix2bytes(matrix):
    flat = []
    for i in range(4):
        for j in range(4):
            flat.append(matrix[i][j])
    return bytes(flat)

def pad(data):
    n = 16 - (len(data) % 16)
    return data + bytes([n] * n)

def unpad(data):
    n = data[-1]
    return data[:-n]

def split_blocks(data):
    return [data[i:i+16] for i in range(0, len(data), 16)]