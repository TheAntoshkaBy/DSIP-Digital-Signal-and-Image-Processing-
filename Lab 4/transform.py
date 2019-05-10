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
