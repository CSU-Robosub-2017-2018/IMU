addpath('ximu_matlab_library');	% include x-IMU MATLAB library
addpath('quaternion_library');	% include quatenrion library
close all;                     	% close all figures
clear;                         	% clear all variables
clc;                          	% clear the command terminal


xIMUdata = xIMUdataClass('LoggedData/LoggedData');

% View = [30 20];
% Xlabel = 'X';
% Ylabel = 'Y';
% Zlabel = 'Z';
% Position = [9 39 1280 720];
% fig = figure(); % FIXME - hardcoded the figure number fr debugging
% set(fig, 'Position', Position);
% set(gca, 'drawmode', 'fast');
% lighting phong;
% set(gcf, 'Renderer', 'zbuffer');
% hold on;
% axis equal;
% grid on;
% view(View(1, 1), View(1, 2));
% xlabel(Xlabel);
% ylabel(Ylabel);
% zlabel(Zlabel);
% plot3(1000, 1000, 1000);

gyr = [xIMUdata.CalInertialAndMagneticData.Gyroscope.X...
       xIMUdata.CalInertialAndMagneticData.Gyroscope.Y...
       xIMUdata.CalInertialAndMagneticData.Gyroscope.Z];        % gyroscope
acc = [xIMUdata.CalInertialAndMagneticData.Accelerometer.X...
       xIMUdata.CalInertialAndMagneticData.Accelerometer.Y...
       xIMUdata.CalInertialAndMagneticData.Accelerometer.Z];	% accelerometer
   
samplePeriod = 1/256;

[rows, columns] = size(acc);
n = 1000;
t = 1;
T = 1;
% gyrin = zeros(n,3);
% accin = zeros(n,3);
scriptFunction(gyr,acc,samplePeriod)


% while (t < rows-1)
%     i = 1;
%     T=t;
%     while (T <= t+n)
%         gyrin(i,:) = gyr(T,:);
%         accin(i,:) = acc(T,:);
%         i = i+1;
%         T = T+1;
%     end
%     t = t+n+1;
%     hold on;
%     scriptFunction(gyrin,accin,samplePeriod)
%     hold off;
% %     clf; % FIXME no clear needed
%     View = [30 20];
%     Xlabel = 'X';
%     Ylabel = 'Y';
%     Zlabel = 'Z';
%     Position = [9 39 1280 720];
%     fig = figure(); % FIXME - hardcoded the figure number fr debugging
%     set(fig, 'Position', Position);
%     set(gca, 'drawmode', 'fast');
%     lighting phong;
%     set(gcf, 'Renderer', 'zbuffer');
%     hold on;
%     axis equal;
%     grid on;
%     view(View(1, 1), View(1, 2));
%     xlabel(Xlabel);
%     ylabel(Ylabel);
%     zlabel(Zlabel);
%     plot3(1000, 1000, 1000);
% 
% end