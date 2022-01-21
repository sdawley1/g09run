
def write_g09():
    """
    This function attains user information be used in the instruction file sent to MARCC.

    Returns
    -------
    user_info (dict) = Dictionary containing all inputs
    """
    # Write g09run file to be created into an .sh
    # User information
    user_info = {}
    print("")
    print('Enter job request information')
    print("Partition is assumed to be 'shared'")
    print('-------------------------------------')
    # Ask all questions to attain user info/requests and add answers to info_user
    while True:
        try:
            user_info['email'] = input("Enter JHU email: ")
            if "@jhu.edu" not in user_info['email']:
                raise ValueError
        except ValueError:
            print("Email address must end in '@jhu.edu'.")
        else:
            break
    # Time to reserve
    print("")
    while True:
        try:
            user_info['time'] = input("Enter integer number of hours (default is 24): ")
            if not len(user_info['time']):
                user_info['time'] = "24"
                break
            assert user_info['time'].isdigit()
            if int(user_info['time']) < 1 or int(user_info['time']) > 72:
                raise ValueError
        except AssertionError:
            print("Time must be a valid integer.")
        except ValueError:
            print("Time must be between 1 and 72 (hrs).")
        else:
            break
    # Nodes to reserve
    print("")
    while True:
        try:
            user_info['nodes'] = input("Enter # of nodes to reserve (default is 1): ")
            if not len(user_info['nodes']):
                user_info['nodes'] = "1"
                break
            assert user_info['nodes'].isdigit()
        except AssertionError:
            print("Please submit an integer number of nodes.")
        else:
            break
    # Number of tasks per node ('ntasks-per-node')
    print("")
    while True:
        try:
            user_info['npnode'] = input('Enter tasks per node (default is 24): ')
            if not len(user_info['npnode']):
                user_info['npnode'] = "24"
                break
            assert user_info['npnode'].isdigit()
        except AssertionError:
            print("Please submit an integer number of ntasks-per-node.")
        else:
            break
    # Memory to reserve
    print("")
    while True:
        try:
            user_info['memory'] = input('Enter an GB of memory to reserve (default is 100): ')
            if not len(user_info['memory']):
                user_info['memory'] = "100"
                break
            assert user_info['memory'].isdigit()
            if int(user_info['memory']) < 5 or int(user_info['memory']) > 117:
                raise ValueError
        except AssertionError:
            print("Memory must be a valid integer.")
        except ValueError:
            print("Memory must be a valid integer between 5 and 117 (GB).")
        else:
            break
    # Name of .gjf file
    print("")
    while True:
        user_info['filename'] = input('Enter name of .gjf file to process (DO NOT INCLUDE EXTENSION): ')
        if len(user_info['filename']):
            break
        else:
            print("Enter a name for the data file.")

    # Reviewing information
    print("")
    while True:
        res = input('Review information? (y/n) ')
        if res.lower() == 'y':
            try:
                print('')
                print('User Information')
                print('----------------')
                print(f"Email: {user_info['email']}")
                print(f"Time (hrs): {user_info['time']}:00:00")
                print(f"Nodes: {user_info['nodes']}")
                print(f"Number of Tasks per Node: {user_info['npnode']}")
                print(f"Memory (GB): {user_info['memory']}")
                print(f"Data file: {user_info['filename']}.gjf")
                print('')
                ans = input('Is the preceding information correct? (y/n): ')
                if ans.lower() == 'y':
                    break
                elif ans.lower() == 'n':
                    begin = input("Type 'stop' to quit the program otherwise start again from beginning: ")
                    if begin.lower() == 'stop':
                        print("Program terminated.")
                        return
                    else:
                        return write_g09()
                else:
                    raise ValueError
            except ValueError:
                print("Answer 'y' or 'n'")
        elif res.lower() == 'n':
            break
        else:
            print("Answer 'y' or 'n'")
            continue

    print('User information documented.')
    return user_info

if __name__ == '__main__':
    write_g09()


