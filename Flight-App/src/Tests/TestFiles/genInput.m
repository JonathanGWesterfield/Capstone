%% Collect user input
filename = 'random_size1200_legal80.txt'
totalSize = 1200
percentageLegal = 0.8

%% Generate data set of size 'total' with 'percentageTrue' legal inputs
numOnes = round(totalSize/(1/percentageLegal))
legalInput = zeros(1, totalSize); % All zeros to start.
% Now assign a percentageTrue of them to 1
indexes = randperm(totalSize, numOnes);
legalInput(indexes) = 1
sum(legalInput)  % Check to make sure.  Should be percentageTrue*total.

%% Initialize values
x = zeros([totalSize 1])
y = zeros([totalSize 1])
z = zeros([totalSize 1])
fid = fopen(filename,'wt')

%% Fill with 'percentageTrue' legal input
% Legal input is x <= 30, y <= 15, z <= 10, x>0, y>0, z>0 
for i=1:totalSize
    if (legalInput(i) == 1)
        % Generate legal input
        x(i) = 30*rand;
        y(i) = 15*rand;
        z(i) = 10*rand;
    else
        % Generate illegal input
        det = randi(3);
        if (det == 1)
            x(i) = -30*rand;
            while (x(i) == 0)
                x(i) = -30*rand;
            end
            y(i) = 15*rand;
            z(i) = 10*rand;
        elseif (det == 2)
            x(i) = 30*rand;
            y(i) = -15*rand;
            while (y(i) == 0)
                y(i) = -15*rand;
            end
            z(i) = 10*rand;
        else
            x(i) = 30*rand;
            y(i) = 15*rand;
            z(i) = -10*rand;
            while (z(i) == 0)
                z(i) = -10*rand;
            end
        end   
    end
    fprintf(fid,'%.20f %.20f %.20f\n', x(i), y(i), z(i));
end
fclose(fid)