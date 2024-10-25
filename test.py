def PrintY():
    print('Y')
def PrintN():
    print('N')

e = input('Which: ')    
eval(f'Print{e.title()}()')