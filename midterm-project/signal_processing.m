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

acg = zeros(MAX_DELAY, CHANNELS);
summary = zeros(MAX_DELAY);
for channel = 1:CHANNELS
   for delay = 1:MAX_DELAY
       for window = 1:MAX_WINDOW
           % see: acg[delay][chan]+=getBufferVal(&cochlea[chan],win)*getBufferVal(&cochlea[chan],win+delay);
           seconds = (window - 1) / SAMPLING_FQ;
           acg(delay, channel) = acg(delay, channel) + (ar0_grid(channel, window) * ar0_grid(channel, window + delay)) * seconds;
       end
       summary(delay) = summary(delay) + acg(delay, channel);
   end
end

for channel = 1:CHANNELS
    plot(acg(:, channel))
    hold on
end
xlabel("Lag Index")
