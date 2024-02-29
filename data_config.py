data_config= {}

data_config['AE'] = {}
data_config['Asolvo'] = {}


AEPath = 'Data/AE/100-test/'
data_config['AE'] = {
    'UCL':  AEPath + 'UCL-100-1.csv',
    'UEL':  AEPath + 'UEL-100-1.csv',
    'UECL': AEPath + 'UECL-100-1.csv',
}


AEPath = 'Data/Asolvo/100-test/'
data_config['Asolvo'] = {
    'UCL':  AEPath + 'UCL-100.csv',
    'UEL':  AEPath + 'UEL-100.csv',
    'UECL': AEPath + 'UECL-100.csv',
}


competitions = ['UCL', 'UEL', 'UECL']
providers = ['AE', 'Asolvo']
plotDir = 'plots/'