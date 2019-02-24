K = 200; % Window width
L = 125; % Longest lag
F0_MIN = 80; % Hz
F0_MAX = 222; % Hz
TIME_STEPS = 325;
CHANNELS = 64;

ar0 = load("data/ar0.dat");
ar0_grid = reshape(ar0, [325, 64]);

autocorrelation(ar0_grid, 1, 1, K, L)
