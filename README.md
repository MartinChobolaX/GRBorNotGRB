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
- desk and pc prepared (thursday - setting up)
- LSTM
(lat,log,rate) -> (rate)
