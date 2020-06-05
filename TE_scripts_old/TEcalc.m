% This program is used to calculate the transfer entropy (both top-down
% and bottom-up) of the sampled population data.  
clear
clc
samples = 10;
epsvals = 9;
global TD_TE
global BU_TE
TD_TE = zeros(epsvals, 3*samples);
BU_TE = zeros(epsvals, 3*samples);

direc = 'Data/TEdata/tolerance_rnaught45/';
for eps = 1:epsvals
    for sample = 1:samples
        filename = sprintf(strcat(direc,'MX_%d_%d.csv'), eps-1, sample-1);
        if exist(filename, 'file')
            D = readmatrix(filename);
            storeTE(eps, sample, D);
        end
    end
    fprintf('Finished eps %d\n',eps);
end
csvwrite(strcat(direc, 'TD_data.csv'),TD_TE)
csvwrite(strcat(direc, 'BU_data.csv'),BU_TE)

function storeTE(eps, sample, D)
    global TD_TE
    global BU_TE
    for i = 1:3
        TD_TE(eps, (sample-1)*3+i) = calcTE(D(:,1),D(:,i+1), 1);
        BU_TE(eps, (sample-1)*3+i) = calcTE(D(:,i+1),D(:,1), 1);
    end
end

% Code generated from JIDT 
function result = calcTE(v1, v2, k)
    % Add JIDT jar library to the path, and disable warnings that it's already there:
    warning('off','MATLAB:Java:DuplicateClass');
    javaaddpath('C:\Users\cathe\Documents\CS523\infodynamics-dist-1.4\infodynamics.jar');
    % Add utilities to the path
    addpath('C:\Users\cathe\Documents\CS523\infodynamics-dist-1.4\demos\octave');
    % 0. Load/prepare the data:
    source = octaveToJavaIntArray(v1);
    destination = octaveToJavaIntArray(v2);
    
    % 1. Construct the calculator:
    calc = javaObject('infodynamics.measures.discrete.TransferEntropyCalculatorDiscrete', 101, k, 1, 1, 1, 1);
    % 2. No other properties to set for discrete calculators.
    % 3. Initialise the calculator for (re-)use:
    calc.initialise();
    % 4. Supply the sample data:
    calc.addObservations(source, destination);
    % 5. Compute the estimate:
    result = calc.computeAverageLocalOfObservations();

    %fprintf('TE_Discrete(col_1 -> col_0) = %.4f bits\n', result);
end