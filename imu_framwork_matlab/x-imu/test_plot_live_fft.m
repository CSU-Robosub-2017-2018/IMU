%% link data and folder to this file
addpath('ximu_matlab_library');	% include x-IMU MATLAB library
addpath('quaternion_library');	% include quatenrion library
close all;                     	% close all figures
clear;                         	% clear all variables
clc;                          	% clear the command terminal

xIMUdata = xIMUdataClass('LoggedData/LoggedData');

%% get data from cv file


gyr = [xIMUdata.CalInertialAndMagneticData.Gyroscope.X...
       xIMUdata.CalInertialAndMagneticData.Gyroscope.Y...
       xIMUdata.CalInertialAndMagneticData.Gyroscope.Z];        % gyroscope
acc = [xIMUdata.CalInertialAndMagneticData.Accelerometer.X...
       xIMUdata.CalInertialAndMagneticData.Accelerometer.Y...
       xIMUdata.CalInertialAndMagneticData.Accelerometer.Z];	% accelerometer

%% set varaibles
samplePeriod = 1/256;   % used in butter filter and integration
filtCutOff = 0.1;       % used in the butter filter
order = 1;              % used in the butter filter

numFilt = 40;           % the number of data points to be filtered

t = 1 ;                 % start point and counter for the while loop that runs the program
x = 0 ;                 %
startSpot = 0;          % used for moving axis
step = 1 ;  
filtered = 0;
allData = 0;
plotCounter = 1;


%% main function
len = length(acc())-1;
filt = zeros(numFilt, 1);
[b, a] = butter(order, (2*filtCutOff)/(1/samplePeriod), 'high');
buffCounter = 1;        % data buffer counter

while ( t <len )

    if(buffCounter <= numFilt)
        filt(buffCounter) = acc(t,1);             % fill the buffer up with acc data until numFilt data points have been reached
        buffCounter = buffCounter + 1;
        t = t + 1;
    else
        buffCounter = 1;
        filtered = filtfilt(b, a, filt)/1000;        
%         while (plotCounter < numFilt)
%             plot(filtered(plotCounter)) ;
% 
%             startSpot = (t/(step*numFilt))-100;
%             axis([ startSpot, (t/step), -5 , 5 ]);
%             grid
%             plotCounter = plotCounter + step;
%             drawnow;
%             pause(0.01)
%         end
        plot(filtered)
        allData = [allData; filtered];

    end
    t = t + step;
      
end  
  
plot(allData, 'b')
hold;
plot(acc(:,1)/1000, 'r')
   