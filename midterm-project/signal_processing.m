MAX_WINDOW = 200; % K
MAX_DELAY = 125; % L
F0_MIN = 80; % Hz
F0_MAX = 222; % Hz
TIME_STEPS = 325;
CHANNELS = 64;

ar0 = load("data/ar0.dat");
ar0_grid = reshape(ar0, [325, 64]).';

acg = zeros(MAX_DELAY, CHANNELS);
for channel = 1:CHANNELS
   for delay = 1:MAX_DELAY
       for window = 1:MAX_WINDOW
           acg(delay, channel) = acg(delay, channel) + (ar0_grid(channel, window) * ar0_grid(channel, window + delay));
       end
   end
end
