
clear

com = 'COM3';
BauRate = 115200;
ser = serial('COM3', 'BaudRate', 115200, 'FlowControl', 'software');
fopen(ser);
i =1;
discard = fscanf(ser);
discard = fscanf(ser);
discard = fscanf(ser);
discard = fscanf(ser);
val='';
out(4) =0;
vel= ['','',''];
acc= ['','',''];

outAcc = [0,0,0];
outVel = [0,0,0];


while i <=4000
    inter = fscanf(ser)
    inter = strrep(inter,':',',');
    c = strsplit(inter, ',');
    val = [val; c];

   
    acc=[acc; val(i,2:4)];
    outAcc = [outAcc; str2double(acc(i,:))];
    
    acc=[acc; val(i,5:7)];
    outAcc = [outAcc; str2double(acc(i,:))];
    
    vel=[vel; val(i,8:10)];
    
    outVel = [outVel; str2double(vel(i,:))];

    i = i+1;
end
% fprintf(ser, '\r\n\r\nprinttrigger 1 .s set drop\r\n', 'utf-8');
fclose(ser);




