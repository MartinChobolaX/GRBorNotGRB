# GRBorNotGRB

Machine learning technique to detect Gamma Ray Bursts


Speedrun to Mgr.
-----------------------------------------------
2.3. (1/75)
- Introduction to LSTM
- Applying LSTM on GRBalpha data (surprisingly good results)
- predicting 6th point by previous five points (only on rate)
  didn't checked with known GRB
- tried to predict only the path of satelite (didn't finish)
- bought Colab pro, ordered new componets for PC

TO DO TOMORROW
- check predictions during known GRB x
- finish LSTM model with more variables (lat,lon,..) 🗸

-----------------------------------------------
3.3. (2/75)
- made progress with more variables (lat, lon) in LSTM intro
  output has correct shape
- liturature reading and searching for references

TO DO TOMORROW
- build PC with new components x
- find indexes of known GRB and check predictions 🗸
- continue on LSTM with lat,lon variables 🗸

-----------------------------------------------
4.3. (3/75)
- predicting lat lon didn't go well (lat was better then lon)
- found index of solar flare (predicted flare, not bkg), aka I am doing something wrong
- tried three features (lon,lat,cps)
- added few sentences in overleaf on satelites
- colab had run out of memory few times on not so complicated model (this is bad)
- new components didn't fix broken PC (I AM A BIG DUMMY DUM!)
  bought the right ones, will see on Monday
  
TO DO TOMMOROW
- find more known GRB x
- tuning the LSTM model x


-----------------------------------------------
5.3. (4/75)
- fixed PC

TO DO TOMMOROW
- set up Linux for conda env and get started 🗸
- set up dest at faculty (ask for a PC) 🗸
- find more known GRB x
- tuning the LSTM model x

-----------------------------------------------
6.3. (5/75)
- set up PC

TO DO TOMMOROW
- find more known GRB 
- tuning the LSTM model

-----------------------------------------------
7.3. (6/75)
- desk and pc prepared
- LSTM //
(lat,log,rate) -> (rate)

-----------------------------------------------
8.3. (7/75)
- LSTM - WINDOW_SIZE = (5,20,50,100,200)

-----------------------------------------------
9.3. (8/75)
Meeting AKA TO DO TOMMOROW 
- try d_dt
- add chapters (neuron, activation func, types of NN and how do they work, loss func, ADAM,...)
- find references, images and usage of NN in astro
- somehow sort data and find the GRB + check for info gaps (when it didnt work)

-----------------------------------------------
10.3. (9/75)
- d_dt doesn't work so well
- prepared PC on faculty - Linux is ready - on Monday - download and sort data

-----------------------------------------------
11.3. (10/75)
- d_dt still doesn't work so well - changed WINDOW_SIZE, complexity and added log, lat - nuffin' -  (x-x_true)/x_true
- cumsum of d_dt doesn't give original lc
- HUGE addition on ML on overleaf

-----------------------------------------------
12.3. (11/75)
- more addition on ML

-----------------------------------------------
13.3. (12/75)
- working system in faculty
- worked on data sorting and how to properly work with them (stored them in one (pacquet) file)
- large gaps - not good for sequential work

-----------------------------------------------
14.3. (13/75)
- SICK DAY
- added few paragraphs on x-ray satellites

-----------------------------------------------
15.3. (14/75)
- gained access to Cthulhu
- added few paragraphs on ML structure
- figured out how to give to LSTM window_size data without time gaps in them
- sorted few GRBs

TO DO TOMORROW
- try on new model the few GRBs

-----------------------------------------------
16.3. (15/75)
- set up workstation on Cthulhu
- figured out how to have individual GRB in dict

TO DO TOMORROW
- train models with various number of variables and window_size, then test them on GRBs
  just to predict bkg, subtract it and ... GRB found????
