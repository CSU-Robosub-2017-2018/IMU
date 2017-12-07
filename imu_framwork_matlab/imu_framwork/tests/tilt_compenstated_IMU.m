%% heading
% created by Billy Phillips
% robo sub

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

% xmean = mean(tcAcc(1000:50000,1)); % still = 0.005526963031196 g
% ymean = mean(tcAcc(1000:50000,2)); % still = -8.199637751306068e-04 g
% zmean = mean(tcAcc(1000:50000,3)); % still = 7.061865562880675e-04 g
% figure()
% plot(tcAcc(:,:))
% figure()
% plot(tcAcc(500:2001,:))

%% ignore the first 500 samples this will be the startup

linAcc = tcAcc(199:length(acc), :);

%% acc to velocity

linVel = zeros(size(linAcc));

for i = 2:length(linAcc)
    linVel(i,:) = linVel(i-1,:) + linAcc(i,:) * samplePeriod;
end

order = 1;
filtCutOff = 0.1;
[b, a] = butter(order, (2*filtCutOff)/(1/samplePeriod), 'high');
linVelHP = filtfilt(b, a, linVel);

% figure()
% plot(linVel(:,:))
% figure()
% plot(linVelHP(:,:))

%% vel to pos

linPos = zeros(size(linVelHP));

for i = 2:length(linVelHP)
    linPos(i,:) = linPos(i-1,:) + linVelHP(i,:) * samplePeriod;
end

order = 1;
filtCutOff = 0.1;
[b, a] = butter(order, (2*filtCutOff)/(1/samplePeriod), 'high');
linPosHP = filtfilt(b, a, linPos);

% figure()
% plot(linPos(:,:))
% figure()
% plot(linPosHP(:,:))

%% plot shit
% 
% figure();
% plot(linPos(:,:));
% 
figure()
plot(linPosHP(:,:))
% 
figure()
plot(-linPos(:,1),-linPos(:,2))

% figure()
% plot(-linPos(:,1),linPos(:,3))
% 
% figure()
% plot3(-linPos(:,1),-linPos(:,2),linPos(:,3))


%% Play animation

% SamplePlotFreq = 15;
%     
%     SixDOFanimation(linPosHP, R, ...
%                 'SamplePlotFreq', SamplePlotFreq, 'Trail', 'Off', ...
%                 'Position', [9 39 1280 720], ...
%                 'AxisLength', 0.1, 'ShowArrowHead', false, ...
%                 'Xlabel', 'X (m)', 'Ylabel', 'Y (m)', 'Zlabel', 'Z (m)', 'ShowLegend', false, 'Title', 'Unfiltered',...
%                 'CreateAVI', false, 'AVIfileNameEnum', false, 'AVIfps', ((1/samplePeriod) / SamplePlotFreq));            
 
%% test filter

test_filter = bandPassFilter( linVel, 0.1, 2);
% test_filter = bandPassFilter( linVelHP,0, 0.01);





