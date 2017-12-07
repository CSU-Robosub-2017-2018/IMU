%% heading
% created by Billy Phillips
% robo sub

%% House keeping
clear
clc
close all

%% input constants 

samplePeriod = 1/100;

velBuffer = 500;

%% read in constants
raw_data = csvread('keep.csv',1);
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

order = 1;
filtCutOff = 0.1;
[b, a] = butter(order, (2*filtCutOff)/(1/samplePeriod), 'high');
[d, c] = butter(order, 0.9, 'low');

R = zeros(3,3);     % rotation matrix describing sensor relative to Earth
R_bank = zeros(3,3);

raw_acc_bank = [0,0,0];
tc_acc_bank = [0, 0, 0];
filtered_acc_bank = [0, 0, 0];

raw_vel = [0,0,0];
raw_vel_bank =[0,0,0];
filtered_vel_bank = [0, 0, 0];

raw_pos = [0,0,0];
raw_pos_bank = [0,0,0];
filtered_pos_bank = [0, 0, 0];

for i = 1:length(gyr)
    ahrs.UpdateIMU(gyr(i,:) * (pi/180), acc(i,:));	% gyroscope units must be radians
    R(:,:) = quatern2rotMat(ahrs.Quaternion)';    % transpose because ahrs provides Earth relative to sensor
    
    
    
    tcAcc(1,:) = R(:,:) * acc(i,:)';
    tcAcc(1,3) = tcAcc(:,3)-1;
    tcAcc(:,1) = tcAcc(:,1)-5.113477569707675e-04;
    tcAcc(:,2) = tcAcc(:,2)-0.002636871607988;
    tcAcc(:,3) = tcAcc(:,3)-4.357790047748496e-04;
    tcAcc = tcAcc*9.81;
    
    raw_acc_bank = [raw_acc_bank;tcAcc];
    
    R_bank = cat(3,R_bank,R);
    
    if(i>=500)
        raw_vel = raw_vel(1,:) + tcAcc(1,:)*samplePeriod;
        raw_vel_bank = [raw_vel_bank; raw_vel];
        [velRow, velColumn] = size(raw_vel_bank);
        if(i>=500+velBuffer)     % ignore the first 500 samples

            filtered_vel = raw_vel_bank(velRow-velBuffer : velRow,:);
            filtered_vel = filtfilt(b, a, filtered_vel);
            filtered_vel_bank = [filtered_vel_bank; filtered_vel(velBuffer,:)];

            raw_pos = raw_pos(1,:) + filtered_vel(velBuffer,:)*samplePeriod;

            raw_pos_bank = [raw_pos_bank;raw_pos];
            [posRow, posColumn] = size(raw_pos_bank);
            if(i>=500+2*velBuffer)
                filtered_pos = raw_pos_bank(posRow-velBuffer : posRow,:);
                filtered_pos = filtfilt(b, a, filtered_pos);
                filtered_pos_bank = [filtered_pos_bank; filtered_pos(velBuffer,:)];
            end
        end
    end
end

%% plot shit
% figure()
% plot(-filtered_pos_bank(:,1),-filtered_pos_bank(:,2))
% plot(filtered_pos_bank(:,3))
% plot(filtered_vel_bank(:,:))


%% Play animation

SamplePlotFreq = 15;
    
    SixDOFanimation(filtered_pos_bank, R_bank, ...
                'SamplePlotFreq', SamplePlotFreq, 'Trail', 'Off', ...
                'Position', [9 39 1280 720], ...
                'AxisLength', 0.1, 'ShowArrowHead', false, ...
                'Xlabel', 'X (m)', 'Ylabel', 'Y (m)', 'Zlabel', 'Z (m)', 'ShowLegend', false, 'Title', 'Unfiltered',...
                'CreateAVI', false, 'AVIfileNameEnum', false, 'AVIfps', ((1/samplePeriod) / SamplePlotFreq));  
