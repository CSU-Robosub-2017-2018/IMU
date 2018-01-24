%% clear everything
close all;                     	% close all figures
clear;                         	% clear all variables
clc;                          	% clear the command terminal

%% Set veralbles
% Specify the folder where the files live and the name of the csv file desired.
myFolder = 'C:\Users\bob\Desktop\IMU\imu_framwork_matlab\imu_framwork\tests\test_data';
fullFileName = 'data_updown.csv';

sampleFreuency = 100;            % Sampling frequency    aproximently 100 samples per sec                    
samplePeriod = 1/sampleFreuency;   % used in integration

bufferSize = 50;


%% Get test data
% Check to make sure that folder actually exists.  Warn user if it doesn't.
if ~isdir(myFolder)
  errorMessage = sprintf('Error: The following folder does not exist:\n%s', myFolder);
  uiwait(warndlg(errorMessage));
  return;
end

% Get a list of all files in the folder with the desired file name pattern.
fullFileName = strcat(myFolder,'\',fullFileName);
raw_data = csvread(fullFileName,1);

%% live data / buffer start
len = length(raw_data(:,1));
buffCounter = 1;
time = 1;

raw_acc_bank = [0, 0, 0];
raw_gro_bank = [0, 0, 0];
raw_mag_bank = [0, 0, 0];

filtered_acc_bank = [0, 0, 0];
filtered_vel_bank = [0, 0, 0];
filtered_pos_bank = [0, 0, 0];

raw_vel = [0, 0, 0];
raw_vel_bank = [0, 0, 0];

raw_pos = [0, 0, 0];
raw_pos_bank = [0, 0, 0];

offSetAccel_x = -0.1181;
offSetAccel_y =  -0.0623;
offSetAccel_Z = -9.8280;

while(time < len)
    
    packet = raw_data(time,1);
    raw_acc = [raw_data(time,2) + offSetAccel_x,...
               raw_data(time,3) + offSetAccel_y,...
               (raw_data(time,4) + offSetAccel_Z)*-1 ];
    raw_acc = round(raw_acc, 2);
    
    raw_gro = [raw_data(time,5), raw_data(time,6), raw_data(time,7)];
    raw_mag = [raw_data(time,8), raw_data(time,9), raw_data(time,10)];
    
    raw_acc_bank = [raw_acc_bank; raw_acc];
    raw_gro_bank = [raw_gro_bank; raw_gro];
    raw_mag_bank = [raw_mag_bank; raw_mag];
    
    %filter acc
    if(time > bufferSize)
        filtered_x_acc = mean(raw_acc_bank(time-bufferSize : time, 1) );
        filtered_y_acc = mean(raw_acc_bank(time-bufferSize : time, 2) );
        filtered_z_acc = mean(raw_acc_bank(time-bufferSize : time, 3) );        
        filtered_acc_bank = [filtered_acc_bank; filtered_x_acc, ...
            filtered_y_acc, filtered_z_acc];
    end
    
    
    raw_vel = round(raw_vel + raw_acc * samplePeriod, 2);
    raw_vel_bank = [raw_vel_bank; raw_vel];
    
    %filter vel
    if(time > 2*bufferSize)
        filtered_x_vel = mean(raw_vel_bank(time-bufferSize : time, 1) );
        filtered_y_vel = mean(raw_vel_bank(time-bufferSize : time, 2) );
        filtered_z_vel = mean(raw_vel_bank(time-bufferSize : time, 3) );        
        filtered_vel_bank = [filtered_vel_bank; filtered_x_vel, ...
            filtered_y_vel, filtered_z_vel];
    end

    raw_pos = round( raw_pos + raw_vel * samplePeriod, 2);
    raw_pos_bank = [raw_pos_bank; raw_pos];
    
    %filter pos
    if(time > 3*bufferSize)
        filtered_x_pos = mean(raw_pos_bank(time-bufferSize : time, 1) );
        filtered_y_pos = mean(raw_pos_bank(time-bufferSize : time, 2) );
        filtered_z_pos = mean(raw_pos_bank(time-bufferSize : time, 3) );        
        filtered_pos_bank = [filtered_pos_bank; filtered_x_pos, ...
            filtered_y_pos, filtered_z_pos];
    end  

    time = time + 1;
end

%% plot comparing acceleration

figure('name','raw z acc and filtered acc');
plot(raw_acc_bank(:, 3), 'g');
hold;
plot(filtered_acc_bank(:, 3), 'r');

%% plot x y z acceleration

figure('name','x y z acceleration');
plot(filtered_acc_bank(:, 1));
hold;
plot(filtered_acc_bank(:, 2));
plot(filtered_acc_bank(:, 3));

%% plot z acceleration

figure('name','z acceleration');
plot(filtered_acc_bank(:, 3));

%% plot x y z velocity

figure('name','x y z velocity');
plot(filtered_vel_bank(:, 1));
hold;
plot(filtered_vel_bank(:, 2));
plot(filtered_vel_bank(:, 3));

%% z velocity

figure('name','x y z velocity');
plot(filtered_vel_bank(:, 3));

%% plot x y z position

figure('name','x y z position')
plot(filtered_pos_bank(:, 1));
hold;
plot(filtered_pos_bank(:, 2));
plot(filtered_pos_bank(:, 3));

%% plot z

figure('name','z position')
plot(filtered_pos_bank(:, 3));

%% plot 3d position

figure('name','3D position')
plot3(filtered_pos_bank(:,1), filtered_pos_bank(:,1), filtered_pos_bank(:,3))
