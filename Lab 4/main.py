import transform as tr


def main():
    max_decomposition_depth = 4
    analysis_low_pass = [0.5, 0.5]
    analysis_high_pass = [0.5, -0.5]
    synthesis_low_pass = [1, 1]
    synthesis_high_pass = [1, -1]
    initial_data = [10, 6, 6, 1, 7, 2, 13, 4, 12, 10, 11, 8, 6, 10, 12, 13]

    wavelet_transform_result, decomposition_level = \
        tr.fwt(initial_data, analysis_low_pass, analysis_high_pass, max_decomposition_depth)

    print(wavelet_transform_result, decomposition_level)

    # print(tr.linear_convolution([1,1,5,5], [3,4]))


if __name__ == '__main__':
    main()
