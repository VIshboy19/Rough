L = 0.0823e-3;

R = 0.299 ;

J = 142/(1000*100*100) ;

Ktau = 30.2/1000; 

b = 5.212e-6;

Kw =  0.03012;


xData = clockx.Data(:, 1);
yData = INPUT.Data(:, 1);

outputt=OUTPUT.Data(:,1);


plot(xData,yData,'b',xData,outputt,'r');
xlabel("time(s)")
ylabel("angular velocity(rad/s)")
legend("Input","Output")