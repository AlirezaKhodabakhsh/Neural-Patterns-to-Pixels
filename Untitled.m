clearvars;
close all;
clc;
% 76, 195
data = niftiread('sub-01_ses-perceptionNaturalImageTraining15_func_sub-01_ses-perceptionNaturalImageTraining15_task-perception_run-01_bold.nii');
s=30;
t=60;
figure()
data=double(data(:,:,s,t));
data=255*(data./max(data(:)));
imshow(data,[])
title(['s = ', num2str(s),', t = ', num2str(t)])