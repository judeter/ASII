% Code generated from JIDT
function result = get_TE(v1, v2, k)
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