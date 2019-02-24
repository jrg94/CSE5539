function s = correlogram(data, j, L, K, N)
    s = 0;
    for i = 1:N
        s = s + autocorrelation(data, i, j, K, L);
    end
end

