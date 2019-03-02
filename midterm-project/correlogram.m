function [acg, summary] = correlogram(data, MAX_DELAY, CHANNELS, MAX_WINDOW)
    acg = zeros(MAX_DELAY, CHANNELS);
    summary = zeros(MAX_DELAY, 1);
    for channel = 1:CHANNELS
       for delay = 1:MAX_DELAY
           for window = 1:MAX_WINDOW
               acg(delay, channel) = acg(delay, channel) + (data(channel, window) * data(channel, window + delay));
           end
           summary(delay, 1) = summary(delay, 1) + acg(delay, channel);
       end
    end
end

