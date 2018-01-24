%% Housekeeping
 
addpath('ximu_matlab_library');	% include x-IMU MATLAB library
addpath('quaternion_library');	% include quatenrion library
close all;                     	% close all figures
clear;                         	% clear all variables
clc;                          	% clear the command terminal
 
%% Import data

xIMUdata = xIMUdataClass('LoggedData/LoggedData');

samplePeriod = 1/100;

gyr_1 = [xIMUdata.CalInertialAndMagneticData.Gyroscope.X...
       xIMUdata.CalInertialAndMagneticData.Gyroscope.Y...
       xIMUdata.CalInertialAndMagneticData.Gyroscope.Z];        % gyroscope
acc_1 = [xIMUdata.CalInertialAndMagneticData.Accelerometer.X...
       xIMUdata.CalInertialAndMagneticData.Accelerometer.Y...
       xIMUdata.CalInertialAndMagneticData.Accelerometer.Z];	% accelerometer

   
   %% Set veralbles
bufferSize = 3;


%% live data / buffer start
len = length(gyr_1(:,1));
buffCounter = 1;
time = 1;

acc_2 = [0, 0, 0];
gyr_2 = [0, 0, 0];


filtered_acc_bank = [0, 0, 0];
filtered_vel_bank = [0, 0, 0];
filtered_pos_bank = [0, 0, 0];

while(time < len)
       
    acc_2 = [acc_2; acc_1];
    gyr_2 = [gyr_2; gyr_1];
    
    %filter acc
    if(time > bufferSize)
        
        acc  = acc_2(time-bufferSize : time, :);
        gyr = gyr_2(time-bufferSize : time, :);

           %% Process data through AHRS algorithm (calcualte orientation)
        % See: http://www.x-io.co.uk/open-source-imu-and-ahrs-algorithms/

        R = zeros(3,3,length(gyr));     % rotation matrix describing sensor relative to Earth

        ahrs = MahonyAHRS('SamplePeriod', samplePeriod, 'Kp', 1);

        for i = 1:length(gyr)
            ahrs.UpdateIMU(gyr(i,:) * (pi/180), acc(i,:));	% gyroscope units must be radians
            R(:,:,i) = quatern2rotMat(ahrs.Quaternion)';    % transpose because ahrs provides Earth relative to sensor
        end

        %% Calculate 'tilt-compensated' accelerometer

        tcAcc = zeros(size(acc));  % accelerometer in Earth frame

        for i = 1:length(acc)
            tcAcc(i,:) = R(:,:,i) * acc(i,:)';
        end



        %% Calculate linear acceleration in Earth frame (subtracting gravity)

        linAcc = tcAcc - [zeros(length(tcAcc), 1), zeros(length(tcAcc), 1), ones(length(tcAcc), 1)];
        % linAcc = linAcc * 9.81;     % convert from 'g' to m/s/s
        linAcc = linAcc;     % convert from 'g' to m/s/s



        %% Calculate linear velocity (integrate acceleartion)

        linVel = zeros(size(linAcc));

        for i = 2:length(linAcc)
            linVel(i,:) = linVel(i-1,:) + linAcc(i,:) * samplePeriod;
        end


        %% High-pass filter linear velocity to remove drift

        order = 1;
        filtCutOff = 0.1;
        [b, a] = butter(order, (2*filtCutOff)/(1/samplePeriod), 'high');
        linVelHP = filtfilt(b, a, linVel);

        %% Calculate linear position (integrate velocity)

        linPos = zeros(size(linVelHP));

        for i = 2:length(linVelHP)
            linPos(i,:) = linPos(i-1,:) + linVelHP(i,:) * samplePeriod;
        end

        %% High-pass filter linear position to remove drift

        order = 1;
        filtCutOff = 0.1;
        [b, a] = butter(order, (2*filtCutOff)/(1/samplePeriod), 'high');
        linPosHP = filtfilt(b, a, linPos);

        filtered_pos_bank = [filtered_pos_bank; linPosHP(bufferSize,:)];


    end
   
    time = time + 1;
end


%% added
figure()
plot(-filtered_pos_bank(:,1), -filtered_pos_bank(:,2));


%% End of script