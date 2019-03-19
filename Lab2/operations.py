from transform import FourierTransform
import numpy as np


class SignalProcessor:
    complexity_counter = 0

    @staticmethod
    def correlation_convolution(first_sequence, second_sequence, length, operation):
        if length <= 0:
            raise Exception('Length must be a positive value! Got {}'.format(length))

        if operation != 1 and operation != -1:
            raise Exception('Operation must equal to 1(correlation) ot -1(convolution)! Got {}'.format(operation))

        if len(first_sequence) < length or len(second_sequence) < length:
            raise Exception('Sequence length must not be less than passed length param!')

        SignalProcessor.complexity_counter = 0

        result = []
        for i in range(length):
            temp = 0
            for j in range(length):
                k = (i + (j * operation)) % length
                temp += first_sequence[j] * second_sequence[k]

                SignalProcessor.complexity_counter += 1

            temp /= length
            result.append(temp)

        return result

    @staticmethod
    def correlation_convolution_fft_based(first_sequence, second_sequence, length, operation):
        if length <= 0:
            raise Exception('Length must be a positive value! Got {}'.format(length))

        if operation != 1 and operation != -1:
            raise Exception('Operation must equal to 1(correlation) ot -1(convolution)! Got {}'.format(operation))

        if len(first_sequence) < length or len(second_sequence) < length:
            raise Exception('Sequence length must not be less than passed length param!')

        SignalProcessor.complexity_counter = 0

        first_fft = FourierTransform.fft(first_sequence, length)
        SignalProcessor.complexity_counter += FourierTransform.complexity_counter

        second_fft = FourierTransform.fft(second_sequence, length)
        SignalProcessor.complexity_counter += FourierTransform.complexity_counter

        processed_first_fft = first_fft
        if operation == 1:
            processed_first_fft = np.conj(first_fft)

        temp = np.multiply(processed_first_fft, second_fft)
        SignalProcessor.complexity_counter += length

        result = FourierTransform.fft(temp, length, -1)
        SignalProcessor.complexity_counter += FourierTransform.complexity_counter

        return FourierTransform.normalize_transform(result, length)
