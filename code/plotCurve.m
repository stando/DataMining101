r = 5;
b = 40;
x = linspace(0,1,100);
y = 1 - (1-x.^r).^b;
plot(x, y)
