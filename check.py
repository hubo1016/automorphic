import sympy
import numpy as np


def sqr(digits):
    digits2 = digits + [0] * len(digits)
    d_ntt = sympy.ntt(digits2, 206158430209)
    d_ntt2 = [n ** 2 for n in d_ntt]
    result = sympy.intt(d_ntt2, 206158430209)
    i = 0
    while i < len(result):
        d, r = divmod(result[i], 10)
        result[i] = r
        if d:
            if i + 1 < len(result):
                result[i + 1] += d
            else:
                result.append(d)
        i += 1
    while result and result[-1] == 0:
        result.pop()
    return result


def sqr_fft(digits):
    M = (1 << (2 * len(digits)).bit_length())
    d_fft = np.fft.rfft(digits, M)
    result = np.round(np.fft.irfft(d_fft ** 2, M)).astype(np.int)
    while True:
        d, r = np.divmod(result, 10)
        if not np.any(d):
            break
        if d[-1]:
            r = np.append(r, d[-1])
        r[1:] += d[:-1]
        result = r
    return [int(v) for v in np.trim_zeros(result, 'b')]


if __name__ == '__main__':
    import sys
    inp, oup, digits = sys.argv[1:]
    with open(inp, 'r') as f:
        inp_digits = f.read(int(digits))
    print("Read", len(inp_digits), "digits")
    inp_digits = [int(c) for c in inp_digits]
    oup_digits = sqr_fft(inp_digits)
    print("Verify:", oup_digits[:len(inp_digits)] == inp_digits)
    oup_s = ''.join(str(c) for c in oup_digits)
    with open(oup, 'w') as f:
        f.write(oup_s)
