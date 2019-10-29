th = 0:pi/599.5:2*pi;
length = 1200
xunit = 15 * cos(th) + 15;
yunit = 7.5 * sin(th) + 7.5;
z = linspace(0,10,length)
scatter3(xunit, yunit, z);
hold off

fid = fopen('spiral_size1200_legal100.txt','wt')
for i=1:length
    fprintf(fid,'%.20f %.20f %.20f\n', xunit(i), yunit(i), z(i))
end

fclose(fid)