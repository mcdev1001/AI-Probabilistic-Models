clear all;
x = [1:20];
y = [1:20];

% Create input and output fuzzy membership functions
xMF = trimf(x, [1 10 20]);
yMF = trimf(y, [1 10 20]);

% Generate control surface
for i = 1:20
    for j = 1:20
        z(i, j) = 0.6 * exp(-0.003 * (x(i) - 20)^2 - 0.015 * (y(j) - 14)^2);
    end
end

% Create fuzzy inference system
fis = newfis('FIS_Surface');

% Add input and output variables to the FIS
fis = addvar(fis, 'input', 'x', [min(x), max(x)]);
fis = addvar(fis, 'input', 'y', [min(y), max(y)]);
fis = addvar(fis, 'output', 'z', [min(z(:)), max(z(:))]);

% Add membership functions to the FIS
fis = addmf(fis, 'input', 1, 'Low', 'trimf', [1 5 10]);
fis = addmf(fis, 'input', 1, 'Medium', 'trimf', [5 10 15]);
fis = addmf(fis, 'input', 1, 'High', 'trimf', [10 15 20]);

fis = addmf(fis, 'input', 2, 'Low', 'trimf', [1 5 10]);
fis = addmf(fis, 'input', 2, 'Medium', 'trimf', [5 10 15]);
fis = addmf(fis, 'input', 2, 'High', 'trimf', [10 15 20]);

fis = addmf(fis, 'output', 1, 'Low', 'trimf', [min(z(:)), min(z(:)), mean(z(:))]);
fis = addmf(fis, 'output', 1, 'Medium', 'trimf', [min(z(:)), mean(z(:)), max(z(:))]);
fis = addmf(fis, 'output', 1, 'High', 'trimf', [mean(z(:)), max(z(:)), max(z(:))]);

% Add rules to the FIS
ruleList = [
    1 1 1 1 1; % If x is Low and y is Low, then z is Low
    1 2 2 1 1; % If x is Low and y is Medium, then z is Medium
    1 3 3 1 1; % If x is Low and y is High, then z is High
    2 1 2 1 1; % If x is Medium and y is Low, then z is Medium
    2 2 3 1 1; % If x is Medium and y is Medium, then z is High
    2 3 3 1 1; % If x is Medium and y is High, then z is High
    3 1 2 1 1; % If x is High and y is Low, then z is Medium
    3 2 3 1 1; % If x is High and y is Medium, then z is High
    3 3 3 1 1; % If x is High and y is High, then z is High
];
fis = addrule(fis, ruleList);

% Evaluate the fuzzy inference system
[xGrid, yGrid] = meshgrid(x, y);
output = evalfis([xGrid(:) yGrid(:)], fis);

% Reshape the output to match the input grid
outputGrid = reshape(output, size(xGrid));

% Plot the original control surface and the fuzzy output
%figure;
% Plot the original control surface
figure;
surf(x, y, z);
title('Control Surface');
xlabel('X');
ylabel('Y');
zlabel('Control (Z)');
colormap('parula'); % You can replace 'parula' with the desired colormap



% Plot the original control surface
subplot(1, 3, 1);
surf(x, y, z);
title('Control Surface');
xlabel('X');
ylabel('Y');
zlabel('Control (Z)');

% Plot the fuzzy output as a contour plot
subplot(1, 3, 2);
contour(outputGrid);
title('Fuzzy Surface');

% Plot the fuzzy output as a 3D surface plot
subplot(1, 3, 3);
surf(x, y, outputGrid);
title('Fuzzy Surface 3D');
xlabel('X');
ylabel('Y');
zlabel('Output (Z)');

% Adjust subplot layout
colormap('spring');
sgtitle('Surface Plots');

% Set axis limits to ensure the point (16, 16) is visible
% for both the contour plot and the 3D surface plot
subplot(1, 3, 2);
xlim([min(x), max(x)]);
ylim([min(y), max(y)]);

subplot(1, 3, 3);
xlim([min(x), max(x)]);
ylim([min(y), max(y)]);

% Test Point 1: (X, Y) = (5, 5)
point1_output = evalfis([5, 5], fis);

% Test Point 2: (X, Y) = (16, 16)
point2_output = evalfis([16, 16], fis);

disp(['Output at Point 1 (X=5, Y=5): ', num2str(point1_output)]);
disp(['Output at Point 2 (X=16, Y=16): ', num2str(point2_output)]);



