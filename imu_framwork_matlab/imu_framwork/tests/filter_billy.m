% Billy Phillips
% 
% filter in imaginery land


%% House keeping
clear
clc
close all

%% input constants 

samplePeriod = 1/100;

%% read in constants
raw_data = csvread('data_10312017_fuckingaround.csv',1);
addpath('quaternion_library');	% include quatenrion library

%% parse

acc = [raw_data(:,2), raw_data(:,3), raw_data(:,4)];
gyr = [raw_data(:,5), raw_data(:,6), raw_data(:,7)];
mag = [raw_data(:,8), raw_data(:,9), raw_data(:,10)];

%% constants

acc = acc/206.5501;             
acc(:,1) = acc(:,1)/9.81;
acc(:,2) = acc(:,2)/9.81;
acc(:,3) = acc(:,3)/9.81;

gyr(:,1) = gyr(:,1)/110;
gyr(:,2) = gyr(:,2)/110;
gyr(:,3) = gyr(:,3)/110;

mag(:,1) = mag(:,1)*1*exp(-7);
mag(:,2) = mag(:,2)*1*exp(-7);
mag(:,3) = mag(:,3)*1*exp(-7);

%% tilt compensaation

ahrs = MahonyAHRS('SamplePeriod', samplePeriod, 'Kp', 1);

R = zeros(3,3,length(gyr));     % rotation matrix describing sensor relative to Earth

for i = 1:length(gyr)
    ahrs.UpdateIMU(gyr(i,:) * (pi/180), acc(i,:));	% gyroscope units must be radians
    R(:,:,i) = quatern2rotMat(ahrs.Quaternion)';    % transpose because ahrs provides Earth relative to sensor
end

tcAcc = zeros(size(acc));  % accelerometer in Earth frame

for i = 1:length(acc)
    tcAcc(i,:) = R(:,:,i) * acc(i,:)';
end

tcAcc(:,3) = tcAcc(:,3)-1;

tcAcc(:,1) = tcAcc(:,1)-0.000556963031196;
tcAcc(:,2) = tcAcc(:,2)+8.199637751306068e-04;
tcAcc(:,3) = tcAcc(:,3)-7.061865562880675e-04;
tcAcc = tcAcc*9.81;

   %% Time specifications:
   Fs = 100;                      % samples per second
   dt = 1/Fs;                     % seconds per sample
   N = size(acc,1);
   %% Fourier Transform:
   X = fftshift(fft(tcAcc));
   %% Frequency specifications:
   dF = Fs/N;                      % hertz
   f = -Fs/2:dF:Fs/2-dF;           % hertz
   %% Plot the spectrum:
%    figure;
%    plot(f,abs(X(:,1))/N);
%    xlabel('Frequency (in hertz)');
%    title('Magnitude Response');
   
   %% filter spectrum
   
   for(i = 1:length(f))
  
   if(abs(f(i))>=10 || abs(f(i))<=5)
       X(i,:) = [0,0,0];
   
   end
   
   end
   
%    figure;
%    plot(f,abs(X(:,1))/N);
%    xlabel('Frequency (in hertz)');
%    title('Magnitude Filtered Response');  
   
 %% invers fft  
   filtered_acc = ifft(X);
%    
%    figure;
%    plot(tcAcc(:,1), 'g');
%    hold;
%    plot(filtered_acc(:,1), 'r');
   
   %% test filter
   
   test_filter = bandPassFilter( tcAcc,5, 10 );

   
   figure;
   plot(test_filter(:,1), 'g');
   hold;
   plot(filtered_acc(:,1), 'r'); 
   
   