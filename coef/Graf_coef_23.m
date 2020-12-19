
LP_file = fopen('C:\Users\marcb\Downloads\lp_2_3.txt','r');
LPCC_file = fopen('C:\Users\marcb\Downloads\lpcc_2_3.txt','r');
MFCC_file = fopen('C:\Users\marcb\Downloads\mfcc_2_3.txt','r');

formatSpec = '%f %f';
sizeA = [2 Inf];
sz = 2;

LP = fscanf(LP_file,formatSpec,sizeA);
LPCC = fscanf(LPCC_file,formatSpec,sizeA);
MFCC = fscanf(MFCC_file,formatSpec,sizeA);

fclose(LP_file);
fclose(LPCC_file);
fclose(MFCC_file);

LP = LP';
LPCC = LPCC';
MFCC = MFCC';

figure
scatter(LP(:,1), LP(:,2), sz,'filled', 'black');
title('LP');
figure
scatter(LPCC(:,1), LPCC(:,2), sz,'filled', 'black');
title('LPCC');
figure
scatter(MFCC(:,1), MFCC(:,2), sz,'filled', 'black');
title('MFCC');


