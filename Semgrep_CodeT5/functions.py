def prime_generator():
    D = {}
    q = 2  # Starting number
    while True:
        if q not in D:
            yield q
            D[q * q] = [q]
        else:
            for p in D[q]:
                D.setdefault(p + q, []).append(p)
            del D[q]
        q += 1

def reverse_words(sentence):
    words = []
    current_word = []
    for char in sentence:
        if char == ' ':
            if current_word:
                words.append(''.join(current_word))
                current_word = []
        else:
            current_word.append(char)
    if current_word:
        words.append(''.join(current_word))
    return ' '.join(words[::-1])


def generate_magic_square(n):
    if n % 2 == 0 or n < 1:
        raise ValueError("Only odd numbers >= 1 are allowed")
    square = [[0] * n for _ in range(n)]
    i, j = 0, n // 2
    num = 1
    while num <= n * n:
        square[i][j] = num
        num += 1
        new_i, new_j = (i - 1) % n, (j + 1) % n
        if square[new_i][new_j]:
            i += 1
        else:
            i, j = new_i, new_j
    return square


 while num <= n * n:
        square[i][j] = num
        num += 1
        new_i, new_j = (i - 1) % n, (j + 1) % n
        if square[new_i][new_j]:
            i += 1
        else:
            i, j = new_i, new_j