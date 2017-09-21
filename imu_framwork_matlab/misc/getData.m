function [ XAaccelData,...
YAaccelData,...
ZAaccelData,...
mQuat,...
XQuat,...
YQuat,...
ZQuat,...
timeStamp] = getData( ser, val, acc, quat,outAcc, outQuat, )
%UNTITLED3 Summary of this function goes here
%   Detailed explanation goes here
k = 1;
i =1;



while k<=2&&i<=2;
inter = fscanf(ser);
    inter = strrep(inter,':',',');
    c = strsplit(inter, ',');
    val = [val; c];

    if strcmp(val(k,1),'A')
        acc=[acc; val(k,1:5)];
        outAcc = [outAcc; str2double(acc(accCount,2:5))]
        accCount = accCount +1;
    else
        quat=[quat; val(k,1:5)];
        outQuat = [outAcc; str2double(quat(quatCount,2:5))]
        quatCount = quatCount +1;
    end
    
    k=k+1;
    i = i+1;
end
% seperate data
XAaccelData = outAcc(2);
YAaccelData = outAcc(3);
ZAaccelData = outAcc(4);
mQuat = outQuat(1);
XQuat = outQuat(2);
YQuat = outQuat(3);
ZQuat = outQuat(4);
timeStamp = outAcc(1);




end

