close all;                     	% close all figures
clear;                         	% clear all variables
clc;                          	% clear the command terminal
 
%% Import data
 posAndRotFileName = 'posAndRotData.csv';
 samplePeriod = 1/100;
 
 posAndRotFromCsv = csvread(posAndRotFileName);
 
 for i = 1:length(posAndRotFromCsv)
    
    linPosHP(i,:) = posAndRotFromCsv(i,1:3);
    R(1,:,i) = posAndRotFromCsv(i,4:6);
    R(2,:,i) = posAndRotFromCsv(i,7:9);
    R(3,:,i) = posAndRotFromCsv(i,10:12);
 end 

%% Play animation

SamplePlotFreq = 8;    
    SixDOFanimation(linPosHP, R, ...
                'SamplePlotFreq', SamplePlotFreq, 'Trail', 'Off', ...
                'Position', [9 39 1280 720], ...
                'AxisLength', 0.1, 'ShowArrowHead', false, ...
                'Xlabel', 'X (m)', 'Ylabel', 'Y (m)', 'Zlabel', 'Z (m)', 'ShowLegend', false, 'Title', 'Unfiltered',...
                'CreateAVI', false, 'AVIfileNameEnum', false, 'AVIfps', ((1/samplePeriod) / SamplePlotFreq));            
 
% end

%% End of script