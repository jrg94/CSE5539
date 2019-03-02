function f = fundamental_frequency(SAMPLING_FQ, F0_MIN, F0_MAX, summary)
    starting_bound = int64(SAMPLING_FQ / F0_MAX);
    ending_bound = int64(SAMPLING_FQ / F0_MIN);
    [~, i] = max(summary(starting_bound:ending_bound));
    f = (1.0 / double(i + starting_bound - 1)) * SAMPLING_FQ;
end
