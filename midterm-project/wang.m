function acg = wang(data, MAX_DELAY, CHANNELS, MAX_WINDOW)
    acg = zeros(MAX_DELAY, CHANNELS);
    for channel = 1:CHANNELS
       for delay = 1:MAX_DELAY
           for window = 1:MAX_WINDOW
               acg(delay, channel) = acg(delay, channel) + (data(channel, window) * data(channel, window + delay));
           end
       end
    end
end

