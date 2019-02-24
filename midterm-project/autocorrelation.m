function A = autocorrelation(data, i, j, K, L)
    A = 0;
    for k = 0:K
        r1 = data(i, j - k);
        r2 = data(i, j - k - L);
        w = k;
        A = A + r1 * r2 * w;
    end
end
