
clear

com = 'COM4';
BauRate = 115200;
ser = serial('COM4', 'BaudRate', 115200, 'FlowControl', 'software');
fopen(ser);
i =1;
discard = fscanf(ser);
discard = fscanf(ser);
discard = fscanf(ser);
discard = fscanf(ser);
val='';
out(4) =0;
quat= ['','','','',''];
acc= ['','','','',''];

outAcc = [0,0,0,0];
outQuat = [0,0,0,0];

quatCount = 1;
accCount = 1;

k=1;
while i <=5000
    inter = fscanf(ser);
    inter = strrep(inter,':',',');
    c = strsplit(inter, ',')
    val = [val; c];

    if strcmp(val(k,1),'A')
        acc=[acc; val(k,1:5)];
        outAcc = [outAcc; str2double(acc(accCount,2:5))];
%         display(['Accel: ' c])
        accCount = accCount +1;
    else
        quat=[quat; val(k,1:5)];
        outQuat = [outAcc; str2double(quat(quatCount,2:5))];
        quatCount = quatCount +1;
    end
   
    
    k=k+1;
    i = i+1;
end
% fprintf(ser, '\r\n\r\nprinttrigger 1 .s set drop\r\n', 'utf-8');
fclose(ser);




