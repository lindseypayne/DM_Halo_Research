import numpy as np
import matplotlib.pyplot as plt

filename = 'halo_data.txt'

# Reading in DM halo data from a file and plotting the positions of subhaloes around a couple of hose haloes.
def main():
    print('hey')
    load_halo_data(filename)





def plot_one_halo():



def load_halo_data(filename):
    # returns an array where each element is a COLUMN from the file
    """
    :param filename: a text file containing data from a Dark Matter halo simulation
    :return: array of data where each element of the array is a COLUMN of data from the file describing a property
             of the host halo (first row in each new index category) or subhalo

    Columns of interest:
        0: Index (number assigmnent, a means of naming) of HOST halo
        3: Mass of each halo/subhalo
        4: Radius (virial) of each halo/subhalo
        8: x-position
        9: y-position
        (10: z-position ... but ignoring this because I'm creating a 2D plot)
    """
    array = np.loadtxt(filename, ).T
    print(array)





if __name__ == '__main__':
    main()
