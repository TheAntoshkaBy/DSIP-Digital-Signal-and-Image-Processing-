import numpy as np


def linear_convolution(first_sequence: list, second_sequence: list,):
    second_length = len(second_sequence)

    processed_sequence = [0] * (second_length - 1) + first_sequence[:]
    processed_sequence_length = len(processed_sequence)

    result = []
    for i in range(processed_sequence_length):
        temp = 0
        for j in range(second_length):
            k = (i + j) % processed_sequence_length
            temp += processed_sequence[k] * second_sequence[j]

        result.append(temp)

    return result


def decimate(sequence: list):
    return sequence[0::2]


def fwt(signal: list, low_pass: list, high_pass: list, max_decomposition_depth: int):
    decomposition_depth = int(min(np.log2(len(signal)), max_decomposition_depth))

    return __fwt(signal, low_pass, high_pass, decomposition_depth), decomposition_depth


def __fwt(signal: list, low_pass: list, high_pass: list, decomposition_depth: int):
    if len(signal) == 1 or decomposition_depth == 0:
        return signal

    approximation = decimate(wkeep(linear_convolution(signal, low_pass), len(signal)))
    detail = decimate(wkeep(linear_convolution(signal, high_pass), len(signal)))

    result = detail.copy()

    result += __fwt(approximation, low_pass, high_pass, decomposition_depth - 1)

    return result


def interpolate(sequence: list):
    return [sequence[int(i / 2)] if i % 2 == 0 else 0 for i in range(len(sequence) * 2)]


def ifwt(wavelet_coefficients: list, low_pass: list, high_pass: list, decomposition_depth: int):
    temp_wavelet_coefficients = wavelet_coefficients[:]
    temp_wavelet_coefficients.reverse()

    return __ifwt(wavelet_coefficients, low_pass, high_pass, decomposition_depth)


def wkeep(x: list, y: int):
    if len(x) <= y:
        return x

    diff = len(x) - y
    if diff % 2 == 0:
        return x[int(diff / 2):-int(diff / 2):]
    else:
        return x[int(diff / 2):-(int(diff / 2) + 1):]


def __ifwt(wavelet_coefficients: list, low_pass: list, high_pass: list, decomposition_depth: int):
    if len(wavelet_coefficients) == 1 or decomposition_depth == 0:
        return wavelet_coefficients

    length = len(wavelet_coefficients)
    halfed_length = int(length / 2)

    detail = wavelet_coefficients[halfed_length:]
    approximation = __ifwt(wavelet_coefficients[:halfed_length], low_pass, high_pass, decomposition_depth - 1)

    detail = wkeep(linear_convolution(interpolate(detail), high_pass), length)
    approximation = wkeep(linear_convolution(interpolate(approximation), low_pass), length)

    return [x + y for x, y in zip(approximation, detail)]


def temp_fwt(signal: list, decomposition_depth: int):
    if len(signal) == 1 or decomposition_depth == 0:
        return signal

    detail = [(signal[i] - signal[i + 1]) / 2 for i in range(0, len(signal), 2)]
    approximation = [(signal[i] + signal[i + 1]) / 2 for i in range(0, len(signal), 2)]

    result = detail + temp_fwt(approximation, decomposition_depth - 1)

    return result


def temp_ifwt(wavelet_coefficients: list, decomposition_depth: int):
    if len(wavelet_coefficients) == 1:
        return wavelet_coefficients

    detail = [x for x in wavelet_coefficients[int(len(wavelet_coefficients) / 2)::]]

    approximation = temp_ifwt(detail, decomposition_depth - 1)

    if decomposition_depth > 1:
        return approximation

    result = []
    for i in range(int(len(wavelet_coefficients) / 2)):
        result.append(approximation[i] + wavelet_coefficients[i])
        result.append(approximation[i] - wavelet_coefficients[i])

    return result
