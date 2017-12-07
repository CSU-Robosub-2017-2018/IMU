function [ filtered_acc ] = lowPass( inputData,setZeroBeond)
%% Time specifications:
   Fs = 100;                      % samples per second
   dt = 1/Fs;                     % seconds per sample
   N = size(inputData,1);
   %% Fourier Transform:
   X = fftshift(fft(inputData));
   %% Frequency specifications:
   dF = Fs/N;                      % hertz
   f = -Fs/2:dF:Fs/2-dF;           % hertz
   %% Plot the spectrum:
   figure;
   plot(f,abs(X(:,1))/N);
   xlabel('Frequency (in hertz)');
   title('Magnitude Response');
   
   %% filter spectrum
   
   for(i = 1:length(f))
  
   if(abs(abs(f(i))>=setZeroBeond))
       X(i,:) = [0,0,0];
   
   end
   
   end
   
   figure;
   plot(f,abs(X(:,1))/N);
   xlabel('Frequency (in hertz)');
   title('Magnitude Filtered Response');  
   
 %% invers fft  
   filtered_acc = ifft(X);
   
   figure;
   plot(inputData(:,1), 'g');
   hold;
   plot(filtered_acc(:,1), 'r');
   
end

