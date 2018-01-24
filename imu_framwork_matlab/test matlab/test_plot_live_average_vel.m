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

numFilt = ;           % the number of data points to be filtered

t = 1 ;                 % start point and counter for the while loop that runs the program

xacc = 0 ;
xvcc = 0;
startSpotacc = 0;          % used for moving axis
stepacc = 1 ;  
filteredacc = 0;
vcc = 0;
lengVcc = 0;
filteredvcc = 0;
counter = 0;
%% main function
len = length(acc())-1;
filt = zeros(numFilt, 1);
[b, a] = butter(order, (2*filtCutOff)/(1/samplePeriod), 'high');
buffCounter = 1;        % data buffer counter

while ( t <len )
    
    
    
    
    
    

    if(t <= numFilt)
        filt(t) = acc(t,1);             % fill the buffer up with acc data until numFilt data points have been reached
    else
        while ( buffCounter < numFilt );          % once buffer is full data is filtered
            filt(buffCounter) = filt(buffCounter+1);
            buffCounter = buffCounter + 1;
        end
        buffCounter = 1;
        
        filt(numFilt) = acc(t,1);
        filteredacc = mean(filt);

%         b = filteredacc;
%         xacc = [ xacc, b ];
%         plot(xacc) ;
% 
%         startSpotacc = (t/(stepacc*numFilt))-100;
%         axis([ startSpotacc, (t/stepacc), -5 , 5 ]);
%         grid
%         t = t + stepacc;
%         drawnow;
%         pause(0.01)

    end
    t = t + stepacc;
    allvcc = [vcc; filteredacc*samplePeriod]
    
    lengVcc = length(vcc());
    
    
    
    
    
    
    
    
%     if(t <= numFilt)
%         filt(t) = acc(t,1);             % fill the buffer up with acc data until numFilt data points have been reached
%     else
%         while ( buffCounter < numFilt );          % once buffer is full data is filtered
%             filt(buffCounter) = filt(buffCounter+1);
%             buffCounter = buffCounter + 1;
%         end
%     end
%     buffCounter = 1;
%     
%     
%     
%     
%     
%     
%     if(lengVcc == numFilt)
%         filteredvcc = mean(vcc);
%         counter = counter +1;
%         
%         vcc = 0;
%         b = filteredvcc *1000;
%         xvcc = [ xvcc, b ];
%         plot(xvcc) ;
% 
%         startSpotacc = (t/(stepacc*numFilt))-100;
%         axis([ startSpotacc, (t/stepacc), -5 , 5 ]);
%         grid
%         drawnow;
%         pause(0.01)
%     end
    
    
    
    
    
    
      
  end
  
   