%% heading
% created by Billy Phillips
% robo sub

%% House keeping
clear
clc
close all

raw_data = csvread('data_10312017_fuckingaround.csv',1);

str = {'Packet number', 'Gyroscope X (deg/s)', 'Gyroscope Y (deg/s)',...
       'Gyroscope Z (deg/s)', 'Accelerometer X (g)', 'Accelerometer Y (g)',... 
       'Accelerometer Z (g)', 'Magnetometer X (G)', 'Magnetometer Y (G)',...
       'Magnetometer Z (G)'};

%% raw_data
legth_raw = size(raw_data);

timestamp = [1:legth_raw(1)]';

raw_output = [timestamp,... 
              raw_data(:,5), raw_data(:,6), raw_data(:,7),...
              raw_data(:,2), raw_data(:,3), raw_data(:,4),...
              raw_data(:,8), raw_data(:,9), raw_data(:,10)];

% dlmwrite('rawout.txt' ,raw_output,'delimiter',',');

%% set aceeleration
acc = [raw_data(:,2), raw_data(:,3), raw_data(:,4)];
% convert = mean(acc(:,3))/9.81;
acc = acc/206.5501;

%% offset calculation
acc(:,1) = acc(:,1) - 0.3465;
acc(:,2) = acc(:,2) - 0.3324;

acc(:,1) = acc(:,1)/9.81;
acc(:,2) = acc(:,2)/9.81;
acc(:,3) = acc(:,3)/9.81;

%% threshold clacultion
% accXthresh = 1.0;
% accYthresh = 1.0;
% 
% x = acc(:,1);
% y = acc(:,2);
% 
% x(abs(x(:,1)) <= accXthresh) = 0;
% y(abs(y(:,1)) <= accYthresh) = 0;
% 
% acc(:,1) = x;
% acc(:,2) = y;

raw_output = [timestamp,... 
              raw_data(:,5)/110, raw_data(:,6)/110, raw_data(:,7)/110,...
              acc(:,1), acc(:,2), acc(:,3),...
              raw_data(:,8)*1*exp(-7 ), raw_data(:,9)*1*exp(-7), raw_data(:,10)*1*exp(-7)];

% raw_output = [str; raw_output]          
%           


%% csv file

filename = 'C:\Users\bob\Desktop\IMU\imu_framwork_matlab\x-imu\LoggedData\LoggedData_CalInertialAndMag.csv';
commaHeader = [str;repmat({','},1,numel(str))]; %insert commaas
commaHeader = commaHeader(:)';
textHeader = cell2mat(commaHeader); %cHeader in text with commas
%write header to file
fid = fopen(filename,'w'); 
fprintf(fid,'%s\n',textHeader);
fclose(fid);
%write data to end of file
dlmwrite(filename, raw_output, '-append', 'delimiter',',')





