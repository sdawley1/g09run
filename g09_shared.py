import os

def mem_and_name():
    """
    Returns
    -------
    memory (string)
    filename (string)
    """
    # Name of .gjf file
    filename = input('Enter name of .gjf file to process (DO NOT INCLUDE EXTENSION): ')

    # Entering memory
    while True:
        try:
            temp_mem = input('Enter an integer memory value to reserve (implied GB units): ')
            memory = int(temp_mem)
            break
        except ValueError:
            print('Please submit an integer memory value')
        else:
            break

    return memory, filename

def write_g09_shared(N):
    """
    This function attains user information be used in `.sh` file sent to MARCC
    Parameters
    ----------
    N (float) = number of files to upload

    Returns
    -------
    user_info (dict) = Dictionary containing all inputs
    user_info = {'email':[], 'time':'24:00:00', 'nodes':'1', 'npnode':'24', 'memory':[], 'filename':[]}

    file_path (str) = String with path to saved files
    """
    # Write g09run file to be created into a .txt and .sh
    # When finished print where file is saved to
    file_path = os.getcwd()
    # User information
    user_info = {'time': '24:0:0', 'nodes': '1', 'npnode': '24'}
    print('Enter information to be sent to MARCC')
    print('Partition is assumed to be \'shared\'')
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

    # Entering memory and filenames
    mems = []
    filenames = []
    for _ in range(int(N)):
        memory, filename = mem_and_name()
        mems.append(str(memory))
        filenames.append(filename)
    user_info['memory'] = mems
    user_info['filename'] = filenames

    # Reviewing information
    while True:
        res = input('Review information? (Yes or No) ')
        if res.lower() == 'yes':
            try:
                print('')
                print('User Information')
                print('----------------')
                print('Email: {}'.format(user_info['email']))
                print('Time: {}'.format('24:0:0'))
                print('Nodes: {}'.format('1'))
                print('Number of Tasks per Node: {}'.format('24'))
                print('Memory: {}'.format(mems))
                print('Filename(s): {}'.format(filenames))
                print('')
                ans = input('Is the preceding information correct? (Yes or No): ')
                if ans.lower() == 'yes':
                    break
                elif ans.lower() == 'no':
                    begin = input('Type \'stop\' to quit the program otherwise start again from beginning: ')
                    if begin.lower() == 'stop':
                        print('Program terminated.')
                        return
                    else:
                        return write_g09_shared(N)
                else:
                    raise ValueError()
            except:
                print('Answer \'Yes\' or \'No\'')
        elif res.lower() == 'no':
            break
        else:
            print('Answer \'Yes\' or \'No\'')
            continue

    print('User information documented.')
    return user_info, file_path

if __name__ == '__main__':
    while True:
        try:
            N = input('Number of files we\'re working with: ')
            N = int(N)
            break
        except ValueError:
            print('That\'s not a number.')

    write_g09_shared(N)


