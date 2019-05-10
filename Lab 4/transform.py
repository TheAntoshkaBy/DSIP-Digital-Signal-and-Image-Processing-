import numpy as np


def linear_convolution(first_sequence: list, second_sequence: list, full: bool = False):
    second_length = len(second_sequence)

    if full:
        processed_sequence = [0] * (second_length - 1) + first_sequence[:]
        processed_sequence_length = len(processed_sequence)
    else:
        processed_sequence = first_sequence[:]
        processed_sequence_length = len(processed_sequence) - 1

    result = []
    for i in range(processed_sequence_length):
        temp = 0
        for j in range(second_length):
            if full:
                k = (i + j) % processed_sequence_length
                temp += processed_sequence[k] * second_sequence[j]
            else:
                if i + j < processed_sequence_length + 1:
                    temp += processed_sequence[i + j] * second_sequence[j]

        result.append(temp)

    return result


def decimate(sequence: list):
    return sequence[0::2]


def fwt(signal: list, low_pass: list, high_pass: list, max_decomposition_depth: int):
    decomposition_depth = int(min(np.log2(len(signal)), max_decomposition_depth))

    return __fwt(signal, low_pass, high_pass, decomposition_depth), decomposition_depth


def __fwt(signal: list, low_pass: list, high_pass: list, max_decomposition: int):
    if len(signal) == 1 or max_decomposition == 0:
        return signal

    approximation = decimate(linear_convolution(signal, low_pass))
    detail = decimate(linear_convolution(signal, high_pass))

    result = detail.copy()

    result += __fwt(approximation, low_pass, high_pass, max_decomposition - 1)

    return result


def interpolate(sequence: list):
    return [sequence[i] if i % 2 == 0 else 0 for i in range(len(sequence) * 2)]


def ifwt(wavelet_coefficients: list, low_pass: list, high_pass: list, decomposition_depth: int):


# def ifwt(wavelet_coefficients: list, low_pass: list, high_pass: list, decomposition_depth: int):
#     temp_wavelet_coefficients = wavelet_coefficients[:]
#     temp_wavelet_coefficients.reverse()
#
#     return __ifwt(wavelet_coefficients, low_pass, high_pass, decomposition_depth)


# def __ifwt(wavelet_coefficients: list, low_pass: list, high_pass: list, decomposition_depth: int):
#     higher_level_approximation = linear_convolution(interpolate(wavelet_coefficients), low_pass)
#     higher_level_detail = linear_convolution(interpolate(wavelet_coefficients), high_pass)
#
#     result = [higher_level_approximation[i] + higher_level_detail[i] for i in range(len(higher_level_approximation))]
#
#     return __ifwt(result, low_pass, high_pass, decomposition_depth)
