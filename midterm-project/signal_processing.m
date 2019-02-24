K = 200; % Window width
L = 125; % Longest lag
F0_MIN = 80; % Hz
F0_MAX = 222; % Hz
TIME_STEPS = 325;

ar0 = load("data/ar0.dat");

% Running autocorrelation
for i = 1:64
    sum = 0; 
    for j = 1:325
        index = ((i - 1) * 325) + j;
        r = ar0(index); % Hair cell model output
        
    end
end
