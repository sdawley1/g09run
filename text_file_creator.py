def infile_2_outfile(user_info, filepath):
    '''
    Parameters
    ----------
    user_info = user_info dictionary from g09_write.write_g09()
    file_path = pathname from g09_write.write_g09()
    '''

    with open(user_info['filename']+'.txt', 'w') as g09file:
        g09file.write('''#!/bin/bash -l

    #SBATCH --partition=shared
    #SBATCH --job-name=Gaussian09
    #SBATCH --time={0}
    #SBATCH --nodes={1}
    #SBATCH --ntasks-per-node={2}
    #SBATCH --mail-type=end
    #SBATCH --mail-user={3}
    #SBATCH --mem={4}

    module load gaussian

    export GAUSS_SCRDIR=/scratch/users/{5}/gtmp
    if [ ! -a $GAUSS_SCRDIR ]; then
        echo "Scratch directory $GAUSS_SCRDIR created."
        mkdir -p $GAUSS_SCRDIR
    fi
    export GAUSS_SCRDIR
    echo "Using $GAUSS_SCRDIR for temporary Gaussian 09 files."
    ls -l $GAUSS_SCRDIR
    time g09 {6}.gjf
    date
    #'''.format(user_info['time'], user_info['nodes'], user_info['npnode'],
                user_info['email'], user_info['memory'], user_info['email'],
                user_info['filename'])
    )

    with open(user_info['filename']+'.txt', 'r') as infile:
        with open(user_info['filename']+'.sh', 'w') as outfile:
            for line in infile:
                outfile.write(line)

    print('Saved {0}/{1} '.format(filepath, user_info['filename']+'.txt'))
    print('Saved {0}/{1} '.format(filepath, user_info['filename']+'.sh'))

    # File that we'll be transferring over SFTP later
    OutFile = user_info['filename']+'.sh'

    return OutFile

if __name__ == '__main__':
    from g09_write import write_g09
    user_info, file_path = write_g09()
    infile_2_outfile(user_info, file_path)
    
