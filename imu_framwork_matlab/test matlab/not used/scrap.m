%% clear everything
close all;                     	% close all figures
clear;                         	% clear all variables
clc;                          	% clear the command terminal

%% Set veralbles
bufferSize = 50;


%% live data / buffer start
len = length(raw_data(:,1));
buffCounter = 1;
time = 1;

raw_acc_bank = [0, 0, 0];
raw_gro_bank = [0, 0, 0];


filtered_acc_bank = [0, 0, 0];
filtered_vel_bank = [0, 0, 0];
filtered_pos_bank = [0, 0, 0];

raw_vel = [0, 0, 0];
raw_vel_bank = [0, 0, 0];

raw_pos = [0, 0, 0];
raw_pos_bank = [0, 0, 0];

while(time < len)
    
    packet = raw_data(time,1);
    raw_acc = [raw_data(time,2), raw_data(time,3), raw_data(time,4)];
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
    

    time = time + 1;
end


