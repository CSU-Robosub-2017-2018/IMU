%% clear everything
close all;                     	% close all figures
clear;                         	% clear all variables
clc;                          	% clear the command terminal

%% Set veralbles
% Specify the folder where the files live and the name of the csv file desired.
myFolder = 'C:\Users\bob\Desktop\IMU\imu_framwork_matlab\imu_framwork\tests\test_data';
fullFileName = 'data_still.csv';

sampleFreuency = 100;            % Sampling frequency    aproximently 100 samples per sec                
T = 1/sampleFreuency;             % Sampling period       

samplePeriod = 1/sampleFreuency;   % used in butter filter and integration
filtCutOff = 0.1;       % used in the butter filter
order = 2;              % used in the butter filter

bufferSize = 100;

[b, a] = butter(order, (filtCutOff)/(1/samplePeriod), 'high');

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



%% get average


offSetAccel_x = mean(raw_data(:,2))*-1
offSetAccel_y = mean(raw_data(:,3))*-1
offSetAccel_Z = mean(raw_data(:,4))*-1

