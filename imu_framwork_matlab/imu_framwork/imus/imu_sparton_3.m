% Billy Phillips
% killik
% 
% IMU plot 3d for presentaiton

% pre stuff

close all;
clear;
clc;


% veribles and strings
XAaccelData = 0;
YAaccelData = 0;
ZAaccelData = 0;
mQuat = 0;
XQuat = 0;
YQuat = 0;
ZQuat = 0;
timeStamp = 0;

val='';
out(4) =0;
quat= ['','','','',''];
acc= ['','','','',''];

outAcc = [0,0,0,0];
outQuat = [0,0,0,0];

quatCount = 1;
accCount = 1;


% open serial
com = 'COM4';
BauRate = 115200;
ser = serial('COM4', 'BaudRate', 115200, 'FlowControl', 'software');
fopen(ser);

discard = fscanf(ser);
discard = fscanf(ser);
discard = fscanf(ser);
discard = fscanf(ser);

% while i <=200
%     inter = fscanf(ser);
%     inter = strrep(inter,':',',');
%     c = strsplit(inter, ',');
%     val = [val; c];
% 
%     if strcmp(val(k,1),'A')
%         acc=[acc; val(k,1:5)];
%         outAcc = [outAcc; str2double(acc(accCount,2:5))]
%         accCount = accCount +1;
%     else
%         quat=[quat; val(k,1:5)];
%         outQuat = [outAcc; str2double(quat(quatCount,2:5))]
%         quatCount = quatCount +1;
%     end
%    
%     
%     k=k+1;
%     i = i+1;
% seperate data

getDataEnd = 20;
getVeloctyEnd = 20;
sample = 2000;
iterationSample = 0;

while iterationSample <=sample
    for k = 1:getVeloctyEnd
        for i = 1:getDataEnd
           
            
            data = getData(ser, val);
            
            
            prev_timeStamp=timeStamp;

            XAaccelData = data(1);
            YAaccelData = data(2);
            ZAaccelData = data(3);
            mQuat = data(4);
            XQuat = data(5);
            YQuat = data(6);
            ZQuat = data(7);
            timeStamp = data(8);
            
            deltaT=(timeStamp-prev_timeStamp)/1000;

            eulerzyx = quat2eul(mQuat, XQuat, YQuat, ZQuat);

            % accel 
            ax = [ax; XAaccelData];
            ay = [ay; YAaccelData];
            az = [az; ZAaccelData];


           % velocity data
            vxtemp = [vxtemp; XAaccelData*deltaT];
            vytemp = [vytemp; YAaccelData*deltaT];
            vztemp = [vztemp; ZAaccelData*deltaT];
        end
     % process data into velocity
        vxtemperary = sum(vxtemp)/getDataEnd;
        vytemperary = sum(vytemp)/getDataEnd;
        vztemperary = sum(vztemp)/getDataEnd;

        vx = [vx; sum(vx) + vxtemp];
        vy = [vy; sum(vy) + vytemp];
        vz = [vz; sum(vz) + vztemp];
        
       % position data
        pxtemp = [pxtemp; vxtemperary*deltaT];
        pytemp = [pytemp; vytemperary*deltaT];
        pztemp = [pztemp; vztemperary*deltaT];        
        
    end
    pxtemperary = sum(pxtemp)/getVeloctyEnd;
    pytemperary = sum(pytemp)/getVeloctyEnd;
    pztemperary = sum(pztemp)/getVeloctyEnd;   
    

    % process data into position

    px = [px; sum(px) + pxtemp];
    py = [py; sum(py) + pytemp];
    pz = [pz; sum(pz) + pztemp]; 



    % print live movment
iterationSample = 1+iterationSample;
end
% close serial
fclose(ser);
