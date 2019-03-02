MAX_WINDOW = 200; % K
MAX_DELAY = 125; % L
F0_MIN = 80; % Hz
F0_MAX = 222; % Hz
CHANNELS = 64;
SAMPLING_FQ = 10000; % Hz

ar0 = load("data/ar0.dat");
ar0_grid = reshape(ar0, [64, 325]); 
[~, summary] = correlogram(ar0_grid, MAX_DELAY, CHANNELS, MAX_WINDOW);
f0_ar0 = fundamental_frequency(SAMPLING_FQ, F0_MIN, F0_MAX, summary);

er4 = load("data/er4.dat");
er4_grid = reshape(er4, [64, 325]); 
[~, summary] = correlogram(er4_grid, MAX_DELAY, CHANNELS, MAX_WINDOW);
f0_er4 = fundamental_frequency(SAMPLING_FQ, F0_MIN, F0_MAX, summary);
