clear 
clc
direc1 = 'Data/TEdata/tolerance_rnaught15/';
direc2 = 'Data/TEdata/tolerance_rnaught30/';
direc3 = 'Data/TEdata/tolerance_rnaught45/';
labels = ["global connectivity (\epsilon)", "border tolerance (\tau)", "initially infected (\rho)", "infection rate (R_0)"];
x_label = labels(2);
hold on
%Plot the mean and CI for TD and BU data
plot_TE(direc1, 1);
plot_TE(direc2, 2);
plot_TE(direc3, 3);
% Sets figure parameters
xticks([0.1:0.1:0.9]);
set(gca, 'Color', [0.94, 0.94, 0.94]);
xlabel(x_label);
ylabel('transfer entropy (TE)');
legend('Average T_{M\rightarrow X} R_0 = 0.15',...
    'Average T_{X\rightarrow M} R_0 = 0.15',...
    'Average T_{M\rightarrow X} R_0 = 0.30',...
    'Average T_{X\rightarrow M} R_0 = 0.30',...
    'Average T_{M\rightarrow X} R_0 = 0.45',...
    'Average T_{X\rightarrow M} R_0 = 0.45',...
    'Location', 'Southeastoutside');

function plot_TE(direc, direc_no)
    % Values of epsilon: ranging from 0 to 1 at increments of 0.05
    epsvals = [0.1:0.1:0.9];
    augx = [epsvals, fliplr(epsvals)];
    [c1, c2] = get_colors(direc_no);
    [muTD, muBU, augy_TD, augy_BU] = get_plot_data(direc, epsvals);  
    plot(epsvals, muTD, 'Color', c1, 'Linewidth', 1.2);
    plot(epsvals, muBU, 'Color', c2, 'linewidth', 1.2);
    fill(augx, augy_TD, 1, 'facealpha', 0.2, 'edgecolor', 'none', ...
        'HandleVisibility', 'off', 'facecolor', c1);
    fill(augx, augy_BU, 1, 'facealpha', 0.2, 'edgecolor', 'none', ...
        'HandleVisibility', 'off', 'facecolor', c2);
end

function [c1, c2] = get_colors(direc_no)
    if direc_no == 1
       c1 = [0.89, 0.10, 0.11];
       c2 = [0.98, 0.60, 0.60];
    elseif direc_no == 2
        c1 = [0.20, 0.63, 0.17];
        c2 = [0.70, 0.87, 0.54];
    elseif direc_no == 3
        c1 = [0.12, 0.47, 0.71];
        c2 = [0.65, 0.81, 0.89];
    end
end

function [muTD, muBU, augy_TD, augy_BU] = get_plot_data(direc, epsvals)
    %Import the data
    TD = readmatrix(strcat(direc, 'TD_data.csv'));
    BU = readmatrix(strcat(direc, 'BU_data.csv'));
    %Calculate mean and standard deviation of both TD and BU data
    muTD = mean(TD,2);
    muBU = mean(BU,2);
    sdTD = std(TD, 0, 2);
    sdBU = std(BU, 0, 2);    
    % Calculate 95% confidence intervals around the mean for TD and BU
    cisTD = zeros(length(epsvals), 2);
    cisBU = zeros(length(epsvals), 2);
    %2.045 from a t-distribution table for 95% confidence and 30 samples
    cisTD(:, 1) = muTD - 2.045*(sdTD./sqrt(length(TD(1,:))));
    cisTD(:, 2) = muTD + 2.045*(sdTD./sqrt(length(TD(1,:))));
    cisBU(:, 1) = muBU - 2.045*(sdBU./sqrt(length(BU(1,:))));
    cisBU(:, 2) = muBU + 2.045*(sdBU./sqrt(length(BU(1,:))));
    augy_TD =[cisTD(:,1)', flipud(cisTD(:,2))'];
    augy_BU =[cisBU(:,1)', flipud(cisBU(:,2))'];
end