def infile_outfile_shared(user_info, filepath):
    """
    Parameters
    ----------
    user_info = user_info dictionary from g09_write.write_g09()
    file_path = pathname from g09_write.write_g09()

    Returns
    -------
    shFiles (list) contains all `.sh` files to submit requests for
    gjfFiles (list) is corresponding list of files containing Gaussian data

    Creates `.txt` and `.sh` file from user inputted data
    """
    shFiles = []
    gjfFiles = []
    for index in range(len(user_info['filename'])):
        with open(user_info['filename'][index] + '.txt', 'w') as g09file:
            g09file.write('''#!/bin/bash -l

#SBATCH --partition=shared
#SBATCH --job-name=Gaussian09
#SBATCH --time=24:0:0
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=24
#SBATCH --mail-type=end
#SBATCH --mail-user={0}
#SBATCH --mem={1}

module load gaussian

# Setup for Gaussian 09:
# =======================
# Make a scratch directory if it doesn't already exist.
export GAUSS_SCRDIR=/scratch/users/{0}/gtmp
if [ ! -a $GAUSS_SCRDIR ]; then
    echo "Scratch directory $GAUSS_SCRDIR created."
    mkdir -p $GAUSS_SCRDIR
fi
export GAUSS_SCRDIR
echo "Using $GAUSS_SCRDIR for temporary Gaussian 09 files."
ls -l $GAUSS_SCRDIR
time g09 {2}.gjf
date
#

#### execute code and write output file to OUT-24log.

#### mpiexec by default uses all cores requested'''.format(user_info['email'], user_info['memory'][index], user_info['filename'][index]))

        with open(user_info['filename'][index] + '.txt', 'r') as infile:
            with open(user_info['filename'][index] + '.sh', 'w') as outfile:
                for line in infile:
                    outfile.write(line)

        current_filename = user_info['filename'][index] + '.sh'
        current_gjf = user_info['filename'][index] + '.gjf'
        print('Saved {0}/{1} '.format(filepath, current_filename))
        shFiles.append(current_filename)
        gjfFiles.append(current_gjf)

    return shFiles, gjfFiles

if __name__ == '__main__':
    N = 1
    from g09_shared import write_g09_shared
    user_info, file_path = write_g09_shared(N)
    infile_outfile_shared(user_info, file_path)

