MAX_WINDOW = 200; % K
MAX_DELAY = 125; % L
F0_MIN = 80; % Hz
F0_MAX = 222; % Hz
TIME_STEPS = 325;
CHANNELS = 64;
SAMPLING_FQ = 10000; % Hz
LOWER_FQ = 80; % Hz
UPPER_FQ = 4000; % Hz

ar0 = load("data/ar0.dat");
ar0_grid = reshape(ar0, [64, 325]); 

[acg, summary] = correlogram(ar0_grid, MAX_DELAY, CHANNELS, MAX_WINDOW);
f0_ar0 = fundamental_frequency(SAMPLING_FQ, F0_MIN, F0_MAX, summary);

plot(summary)
xlabel("Lag Index")
