%% heading
% created by Billy Phillips
% robo sub

%% House keeping
clear
clc
close all

%% filter 
order = 1;
filtCutOff = 0.01;
[b, a] = butter(order, filtCutOff, 'low');

%% set aceeleration
rampUp = linspace(0,9.8);
stedyHigh(1:100) = 9.8;
rampDown = linspace(9.8,-9.8,200);
stedyLow(1:100) = -9.8;
rampUp2 = linspace(-9.8,0);

acc = [rampUp,stedyHigh,rampDown,stedyLow,rampUp2];

%% plot accleration

figure()
hold;
plot(acc)

%%  integrate into vel
vel = cumtrapz(acc)/100;

velfilt =  filtfilt(b,a,vel);

figure();
hold;
plot(velfilt, 'r');
plot(vel, 'g')

%%  integrate into pos

pos = cumtrapz(vel)/100;
posfilt = cumtrapz(velfilt)/100;
posfilt =  filtfilt(b,a,posfilt);

figure()
hold;
plot(posfilt, 'r');
plot(pos, 'g');





