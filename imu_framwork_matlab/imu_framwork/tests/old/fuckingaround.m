%% heading
% created by Billy Phillips
% robo sub

%% House keeping
clear
clc
close all

raw_data = csvread('data_10312017_fuckingaround.csv',1);

%% set aceeleration
acc = [raw_data(:,2), raw_data(:,3), raw_data(:,4)];
% convert = mean(acc(:,3))/9.81;
acc = acc/206.5501;

%% offset calculation
acc(:,1) = acc(:,1) - 0.3465;
acc(:,2) = acc(:,2) - 0.3324;

%% threshold clacultion
accXthresh = 1.0;
accYthresh = 1.0;

x = acc(:,1);
y = acc(:,2);

x(abs(x(:,1)) <= accXthresh) = 0;
y(abs(y(:,1)) <= accYthresh) = 0;

acc(:,1) = x;
acc(:,2) = y;

%% plot acc
figure()
hold;
plot(acc(:,1))
plot(acc(:,2))

%%  integrate into vel
vel = cumtrapz(acc)/100;

figure();
hold;
plot(vel(:,1));
plot(vel(:,2));

%%  integrate into pos
pos = cumtrapz(vel)/100;

figure()
hold;
plot(pos(:,1));
plot(pos(:,2));

%% plot x vs y

figure()
plot(pos(:,1),pos(:,2))




