import os

def write_g09():
    '''
    This function attains user information be used in `.sh` file sent to MARCC
    Returns
    -------
    user_info (dict) = Dictionary containing all inputs
    user_info = {'email':[], 'time':[], 'nodes':[], 'npnode':[], 'memory':[], 'filename':[]}

    file_path (str) = String with path to saved files
    '''
    # Write g09run file to be created into a .txt and .sh
    # When finished print where file is saved to
    file_path = os.getcwd()
    # User information
    user_info = {}
    print('Enter information to be sent to MARCC')
    print('-------------------------------------')
    # Ask all questions to attain user info/requests and add answers to user_info
    while True:
        try:
            user_info['email'] = input('Enter JHU email: ')
            JHED = user_info['email'].strip('@jhu.edu')
            if '@jhu.edu' not in user_info['email']:
                raise ValueError()
        except:
            print('Email address must end in \'@jhu.edu\'')
        else:
            break 
    while True:
        try:
            temp = input('Enter hours (integer): ')
            user_info['time'] = temp + ':00:00'
            ints = [int(i) for i in temp]
        except:
            print('Please enter a valid integer')
        else:
            break
    while True:
        try:
            user_info['nodes'] = input('Enter # of nodes to reserve: ')
            nodes = int(user_info['nodes'])
        except:
            print('Please submit an integer number of nodes')
        else:
            break
    while True:
        try:
            user_info['npnode'] = input('Enter ntasks-per-node: ')
            npnode = int(user_info['npnode'])
        except:
            print('Please submit an integer number of ntasks-per-node')
        else:
            break
    while True:
        try:
            temp_mem = input('Enter an integer memory value to reserve (implied GB units): ')
            user_info['memory'] = temp_mem + 'GB'
            memory = int(temp_mem)
        except:
            print('Please submit an integer memory value')
        else:
            break
    # Name of .gjf file
    user_info['filename'] = input('Enter name of .gjf file to process (DO NOT INCLUDE EXTENSION): ')
    gjf_filename = user_info['filename'] + '.gjf'

    # Reviewing information
    while True:
        res = input('Review information? (Yes or No) ')
        if res.lower() == 'yes':
            try:
                print('')
                print('User Information')
                print('----------------')
                print('Email: {}'.format(user_info['email']))
                print('Time: {}'.format(user_info['time']))
                print('Nodes: {}'.format(user_info['nodes']))
                print('Number of Tasks per Node: {}'.format(user_info['npnode']))
                print('Memory: {}'.format(temp_mem))
                print('Filename: {}'.format(gjf_filename))
                print('')
                ans = input('Is the preceeding information correct? (Yes or No): ')
                if ans.lower() == 'yes':
                    break
                elif ans.lower() == 'no':
                    begin = input('Type \'stop\' to quit the program otherwise start again from beginning: ')
                    if begin.lower() == 'stop':
                        print('Program terminated.')
                        return
                    else: 
                        return write_g09()
                else:
                    raise ValueError()
            except:
                print('Answer \'Yes\' or \'No\'')
        elif res.lower() == 'no':
            print('\nFeeling confident today, eh?')
            break
        else:
            print('Answer \'Yes\' or \'No\'')
            continue

    print('User information documented.')
    return user_info, file_path

if __name__ == '__main__':
    write_g09()


