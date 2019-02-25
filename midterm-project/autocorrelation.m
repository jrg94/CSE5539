function A = autocorrelation(data, i, j, t, K, SAMPLING_FQ)
    A = 0;
    for k = 0: K - 1
        r1 = data(i, j - k);
        r2 = data(i, j - k - t);
        w = k / SAMPLING_FQ;
        A = A + (r1 * r2 * w);
    end
end
