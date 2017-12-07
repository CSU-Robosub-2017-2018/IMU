%% heading
% created by Billy Phillips
% robo sub

%% House keeping
clear
clc
close all

%% filter 
order = 1;
filtCutOff = 0.1;
[b, a] = butter(order, filtCutOff, 'low');

%% set aceeleration
rampUp = linspace(0,9.8);
stedyHigh(1:100) = 9.8;
rampDown = linspace(9.8,-9.8,200);
stedyLow(1:100) = -9.8;
rampUp2 = linspace(-9.8,0);

acc = [rampUp,stedyHigh,rampDown,stedyLow,rampUp2];

%% add noise

snr = 0.00001;
accnoise = awgn(acc, snr);

%% plot accleration

figure()
hold;
plot(acc)
plot(accnoise);

%%  integrate into vel
vel = cumtrapz(acc)/100;
velnoise = cumtrapz(accnoise)/100;

velfilt =  filtfilt(b,a,velnoise);

figure();
hold;
plot(velnoise);

%%  integrate into pos

pos = cumtrapz(velnoise)/100;
posfilt = cumtrapz(velfilt)/100;
posfilt =  filtfilt(b,a,posfilt);
plot(pos);
plot(posfilt, 'g');






