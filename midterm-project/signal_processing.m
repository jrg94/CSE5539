K = 200; % Window width
L = 125; % Longest lag
F0_MIN = 80; % Hz
F0_MAX = 222; % Hz
TIME_STEPS = 325;

ar0 = load("data/ar0.dat");

% Running autocorrelation
for i = 1:64
    for j = 1:325
        k = ((i - 1) * 325) + j;
        ar0(k);
    end
end
