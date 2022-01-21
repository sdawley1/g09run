import os

def gaussian09(info_user):
    """
    This function builds the Gaussian09 job type instruction file for submission to MARCC.

    Parameters
    ----------
    info_user = info_user dictionary from user_info.write_g09()
    """

    with open(info_user['filename'] + '.sh', 'w') as g09file:
        g09file.write(f"""#!/bin/bash -l

#SBATCH --partition=shared
#SBATCH --job-name=Gaussian09
#SBATCH --time={info_user['time']}:00:00
#SBATCH --nodes={info_user['nodes']}
#SBATCH --ntasks-per-node={info_user['npnode']}
#SBATCH --mail-type=end
#SBATCH --mail-user={info_user['email']}
#SBATCH --mem={info_user['memory']}GB

module load gaussian

# Setup for Gaussian 09:
# =======================
# Make a scratch directory if it doesn't already exist.
export GAUSS_SCRDIR=/scratch/users/{info_user['email']}/gtmp
if [ ! -a $GAUSS_SCRDIR ]; then
    echo "Scratch directory $GAUSS_SCRDIR created."
    mkdir -p $GAUSS_SCRDIR
fi
export GAUSS_SCRDIR
echo "Using $GAUSS_SCRDIR for temporary Gaussian 09 files."
ls -l $GAUSS_SCRDIR
time g09 {info_user['filename']}.gjf
date
#

#### execute code and write output file to OUT-24log.

#### mpiexec by default uses all cores requested"""
                      )

    print(f"Saved {info_user['filename']}.sh")

    # File that we'll be transferring over SFTP later
    shFile = info_user['filename'] + '.sh'
    gjfFile = info_user['filename'] + '.gjf'

    return shFile, gjfFile

if __name__ == "__main__":
    from user_info import write_g09
    user_info = write_g09()
    gaussian09(user_info)
