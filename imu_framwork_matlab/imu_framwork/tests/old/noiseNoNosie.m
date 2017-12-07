%% heading
% created by Billy Phillips
% robo sub

%% House keeping
clear
clc
close all

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

figure();
hold;
plot(velnoise, 'r');
plot(vel, 'g')

%%  integrate into pos

pos = cumtrapz(velnoise)/100;
posnoise = cumtrapz(vel)/100;

figure()
hold;
plot(posnoise, 'r')
plot(pos, 'g');






