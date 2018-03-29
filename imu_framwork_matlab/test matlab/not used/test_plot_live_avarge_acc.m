%% link data and folder to this file
addpath('ximu_matlab_library');	% include x-IMU MATLAB library
addpath('quaternion_library');	% include quatenrion library
close all;                     	% close all figures
clear;                         	% clear all variables
clc;                          	% clear the command terminal

xIMUdata = xIMUdataClass('LoggedData/LoggedData');

%% get data from cv file
samplePeriod = 1/256;

gyr = [xIMUdata.CalInertialAndMagneticData.Gyroscope.X...
       xIMUdata.CalInertialAndMagneticData.Gyroscope.Y...
       xIMUdata.CalInertialAndMagneticData.Gyroscope.Z];        % gyroscope
acc = [xIMUdata.CalInertialAndMagneticData.Accelerometer.X...
       xIMUdata.CalInertialAndMagneticData.Accelerometer.Y...
       xIMUdata.CalInertialAndMagneticData.Accelerometer.Z];	% accelerometer

len = length(acc())-1;

%% main function
t = 1 ;
x = 0 ;
startSpot = 0;
step = 1 ; % lowering step has a number of cycles and then acquire more data

numFilt = 40;
filt = zeros(numFilt, 1);
n = 1;
m = 0;
k = 0;
order = 1;
filtCutOff = 0.1;
[b, a] = butter(order, (2*filtCutOff)/(1/samplePeriod), 'high');
while ( t <len )

    % plot live data
%     b = acc(t,1);
%     x = [ x, b ];
%     plot(x) ;
%       if ((t/step)-100 < 0)
%           startSpot = 0;
%       else
%           startSpot = (t/step)-100;
%       end
%       axis([ startSpot, (t/step+50), -5 , 5 ]);
%       grid
%       t = t + step;
%       drawnow;
%       pause(0.01)

    if(t <= numFilt)
        filt(t) = acc(t,1);
    else
        while ( n < numFilt );
            filt(n) = filt(n+1);
            n = n + 1;
        end
        n = 1;
        filt(numFilt) = acc(t,1);
%         filtered = filtfilt(b, a, filt)/1000
        filtered = mean(filt);

        b = filtered;
        x = [ x, b ];
        plot(x) ;
          if ((t/step)-100 < 0)
              startSpot = 0;
          else
              startSpot = (t/(step*numFilt))-100;
          end
          axis([ startSpot, (t/step), -5 , 5 ]);
          grid
          t = t + step;
          drawnow;
          pause(0.01)




    end
    t = t + step;
      
  end
  
   