
:: Home/Away probability plots for each provider
python probability_plots.py --provider AE
python probability_plots.py --provider Asolvo

:: Home/Away binomial test for each provider 
python binomial_test.py --provider AE
python binomial_test.py --provider Asolvo

:: Compare AE and Asolvo
python AEAScomparison.py