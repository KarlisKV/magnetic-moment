# magnetic-moment
A program that calculates the magnetic moments of magnetic dipoles from magnetic field values that are measured with a Gauss meter. 
Program uses Scipy's Nelder-Mead optimization method, it searches for the magnetic moment value of a dipole from measured magnetic field 
values and theoretical magnetic field values based on this equation: B_dip (r)=μ_0/4π  1/r^3  (3(m∙r_hat) r_hat ̂- m ), where r is the 
distance from the measured point to the dipole and r_hat is the unit vector from the point to the dipole. μ_0 is the magnetic constant 
and m is the magnetic moment value of the dipole. 
Runs on Python 3 Will need to import the used libraries to work
