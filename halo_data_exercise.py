import numpy as np
import matplotlib.pyplot as plt
import random

filename = 'halo_data.txt'
num_halos = 9742
hmm = 100

# Reading in DM halo data from a file and plotting the positions of subhaloes around a couple of those host haloes.
# only plot subhaloes with Mvir > 1e12 Msun/h
def main():
    print('hey')

    # create empty, labeled plot
    fig, ax = plt.subplots(figsize=(7,7), dpi=100)
    fig.suptitle('Plotting DM haloes and their subhaloes')
    ax.set_xlabel('Halo x-position')
    ax.set_ylabel('Halo y-position')
    ax.axis("equal")
    ax.set(xlim=(0, 150), ylim=(0, 150))

    """
    # call this block if you want to plot only ONE host halo and ONE subhalo
    all_halo_indices, properties_list, plot_host = plot_host_halo_one_time(filename, ax)
    plot_one_subhalo(all_halo_indices, properties_list, ax)
    plt.show()
    """

    # call this block if you want to plot a host halo and MULTIPLE (or all) of its subhaloes
    # enter chosen amount of numbers from 0-48 here to plot host haloes and their subhaloes
    halo_group_list = []
    host_halo_num = input('If you want all host haloes plottes type "ALL", otherwise type one number between 0 and 48 to choose a host halo: ')
    print('\n')
    for i in range(hmm):
        new_host_halo_num = host_halo_num

        if host_halo_num == 'ALL':
            halo_group_list = np.arange(0, 48).tolist()
            break

        elif int(new_host_halo_num) < 0 or int(new_host_halo_num) > 48:
            print('This is not a host halo number.')
            host_halo_num = input('Enter a new host halo number between 0 and 48: ')
            print('\n')

        elif int(new_host_halo_num) in halo_group_list:
            print('This halo is already in your list of haloes to plot.')
            host_halo_num = input('Enter a new host halo number between 0 and 48: ')
            while host_halo_num in halo_group_list:
                print('This halo is already in your list of haloes to plot.')
                host_halo_num = input('Enter a new host halo number between 0 and 48: ')
                print('\n')
            new_host_halo_num = host_halo_num

            """
            while int(host_halo_num) < 0 or int(host_halo_num) > 48:
                print('This is not a host halo number.')
                host_halo_num = input('Enter a new host halo number between 0 and 48: ')
            ####buggy
            if host_halo_num in halo_group_list:
                print('This halo is already in your list of haloes to plot.')
                host_halo_num = input('Enter a new host halo number between 0 and 48: ')
                while host_halo_num in halo_group_list:
                    print('This halo is already in your list of haloes to plot.')
                    host_halo_num = input('Enter a new host halo number between 0 and 48: ')
            else:
                halo_group_list.append(int(host_halo_num))
                print(halo_group_list)
            print('Do you want to add more haloes to your list to be plotted?')
            host_halo_num = input('If not type "NO", if yes, enter a new host halo number between 0 and 48: ')
            if host_halo_num == 'NO':
                break
            """
        else:
            halo_group_list.append(int(new_host_halo_num))
            print('Do you want to add more haloes to your list to be plotted?')
            host_halo_num = input('If not type "NO", if yes, enter a new host halo number between 0 and 48: ')
            new_host_halo_num = host_halo_num
            print('\n')
            if new_host_halo_num == 'NO':
                break

    plot_host_list = []
    for halo_group in halo_group_list:
        all_halo_indices, properties_list, plot_host = plot_host_halo(filename, halo_group, ax)
        plot_subhaloes(all_halo_indices, properties_list, ax)
        plot_host_list.append(plot_host)
        #ax.legend(handles, labels)
    #handles, labels = ax.get_legend_handles_labels()
    #ax.legend(handles, labels)
    #ax.legend(handles=[plot_host_list], loc='upper left', fontsize=5)
    ax.grid(True)
    plt.show()


def load_halo_data(filename):
    # returns an array where each element is a COLUMN from the file
    """
    :param filename: a text file containing data from a Dark Matter halo simulation
    :return: an array of data for each column of interest for all halos in the simulation text file

             returns array of data where each element of the array is a COLUMN of data from the file describing a property
             of the host halo (first row in each new index category) or subhalo

    Columns of interest:
        0: Index (number assigmnent, a means of naming) of HOST halo
        3: Mass of each halo/subhalo
        4: Radius (virial) of each halo/subhalo
        8: x-position
        9: y-position
        (10: z-position ... but ignoring this because I'm creating a 2D plot)
    """
    array = np.loadtxt(filename, usecols=(0,3,4,8,9)).T     # array with 5 elements, each element is itself
    #print(array)

    # take out one element of array and make it a list
    index_arr = array[0]
    mass_arr = array[1]
    radius_arr = array[2]
    x_arr = array[3]
    y_arr = array[4]

    properties_list = [index_arr, mass_arr, radius_arr, x_arr, y_arr]
    return properties_list, index_arr


# file index refers to the naming convention used for the host halo in the data file, subhaloes have same index as host
# array index refers to the index starting at 0 for lists and arrays
def get_host_halo_data_one_time(filename):
    properties_list, index_arr = load_halo_data(filename)
    # index_arr has 9742 elements, so 9742 halos in data file
    host_halo_file_index_num = []    # stores first instance of new file index number in a list
    for i in range(num_halos):
        previous_halo = index_arr[i-1]
        current_halo = index_arr[i]
        if previous_halo != current_halo and i < num_halos - 1:
            host_halo_file_index_num.append(current_halo)

    # ask for user input on which host halo they want to plot
    num_host_haloes = len(host_halo_file_index_num)
    print('You can pick a host halo between 0 and ' + str(num_host_haloes - 1))
    host_halo_num = input("Enter your subhalo number: ")

    # inputted number (host_halo) maps to a host halo in file index list
    # returns an array with the first element being a list of indexes in index_arr where that host_halo index number is
    host_halo_arr_index_list = np.where(index_arr == host_halo_file_index_num[int(host_halo_num)])
    # only the FIRST occurence of this host's file index number is where the host's data is located
    # ... in the other arrays in properties_list
    host_halo_arr_index = host_halo_arr_index_list[0][0]     # used to locate index of data value for any host halo in arrays in properties_list
    all_halo_indices = host_halo_arr_index_list[0]           # array indices of both specific halo and all its subhaloes

    # for host halo of choice, adds its index, mass, radius, and positional data to a list
    host_halo_properties = []
    for arr in properties_list:
        host_halo_properties.append(arr[host_halo_arr_index])
    #print(host_halo_properties)
    return host_halo_properties, all_halo_indices, properties_list, host_halo_num

# file index refers to the naming convention used for the host halo in the data file, subhaloes have same index as host
# array index refers to the index starting at 0 for lists and arrays
def get_host_halo_data(filename, host_halo):
    properties_list, index_arr = load_halo_data(filename)
    # index_arr has 9742 elements, so 9742 halos in data file
    host_halo_file_index_num = []    # stores first instance of new file index number in a list
    for i in range(num_halos):
        previous_halo = index_arr[i-1]
        current_halo = index_arr[i]
        if previous_halo != current_halo and i < num_halos - 1:
            host_halo_file_index_num.append(current_halo)

    # inputted number (host_halo) maps to a host halo in file index list
    # returns an array with the first element being a list of indexes in index_arr where that host_halo index number is
    host_halo_arr_index_list = np.where(index_arr == host_halo_file_index_num[int(host_halo)])
    # only the FIRST occurence of this host's file index number is where the host's data is located
    # ... in the other arrays in properties_list
    host_halo_arr_index = host_halo_arr_index_list[0][0]     # used to locate index of data value for any host halo in arrays in properties_list
    all_halo_indices = host_halo_arr_index_list[0]           # array indices of both specific halo and all its subhaloes

    # for host halo of choice, adds its index, mass, radius, and positional data to a list
    host_halo_properties = []
    for arr in properties_list:
        host_halo_properties.append(arr[host_halo_arr_index])
    #print(host_halo_properties)
    return host_halo_properties, all_halo_indices, properties_list


def plot_host_halo_one_time(filename, ax):
    r = random.random()
    b = random.random()
    g = random.random()
    random_color = (r, g, b)
    host_halo_properties, all_halo_indices, properties_list, host_halo_num = get_host_halo_data_one_time(filename)
    plot_host = plt.Circle((host_halo_properties[3], host_halo_properties[4]), host_halo_properties[2]*6, color=random_color, alpha=0.5, clip_on=False, ec=None, label='host halo ' + str(host_halo_properties[0]))
    # plot host halo
    ax.add_artist(plot_host)
    ax.legend(handles=[plot_host], loc='upper left', fontsize=5)
    return all_halo_indices, properties_list, plot_host


def plot_host_halo(filename, host_halo, ax):
    r = random.random()
    b = random.random()
    g = random.random()
    random_color = (r, g, b)
    host_halo_properties, all_halo_indices, properties_list = get_host_halo_data(filename, host_halo)
    plot_host = plt.Circle((host_halo_properties[3], host_halo_properties[4]), host_halo_properties[2]*6, color=random_color, alpha=0.5, clip_on=False, ec=None, label='host halo ' + str(host_halo_properties[0]))
    # plot host halo
    ax.add_artist(plot_host)
    ax.legend(handles=[plot_host], loc='upper left', fontsize=5)
    return all_halo_indices, properties_list, plot_host



def plot_subhaloes(all_halo_indices, properties_list, ax):
    # make lists containing subhalo plotting data
    properties_list_no_index = properties_list[1:]
    all_subhalo_property_lists = []
    for i in range(len(all_halo_indices)):
        index = all_halo_indices[i]      # not including first index because that maps to the host halo
        subhalo_properties = []
        for arr in properties_list_no_index:
            data_value = arr[index]
            subhalo_properties.append(data_value)     # making a list of the properties for each subhalo in host halo (4 elements in list)
        all_subhalo_property_lists.append(subhalo_properties)  # making a list of all of the subhalo propoerty lists to parse through later on for relevant subhaloes

    all_subhalo_property_lists.remove(all_subhalo_property_lists[0])   # removing first list which contains data for HOST halo

    # parsing through lists for relevant subhalo data and then plotting the subhalo
    for subhalo_list in all_subhalo_property_lists:
        if subhalo_list[0] < 1e12:
            all_subhalo_property_lists.remove(subhalo_list)     # gets rid of this subhalo to be plotted
        else:
            subhalo = plt.Circle((subhalo_list[2], subhalo_list[3]), subhalo_list[1]*5, clip_on=False, ec='black')
            ax.add_artist(subhalo)


def plot_one_subhalo(all_halo_indices, properties_list, ax):
    properties_list_no_index = properties_list[1:]
    all_subhalo_property_lists = []
    for i in range(len(all_halo_indices)):
        index = all_halo_indices[i]  # not including first index because that maps to the host halo
        subhalo_properties = []
        for arr in properties_list_no_index:
            data_value = arr[index]
            subhalo_properties.append(
                data_value)  # making a list of the properties for each subhalo in host halo (4 elements in list)
        all_subhalo_property_lists.append(subhalo_properties)  # making a list of all of the subhalo propoerty lists to parse through later on for relevant subhaloes

    all_subhalo_property_lists.remove(
        all_subhalo_property_lists[0])  # removing first list which contains data for HOST halo

    num_subhaloes = len(all_subhalo_property_lists)
    print('You can pick a subhalo between 0 and ' + str(num_subhaloes - 1))
    subhalo_num = input("Enter your subhalo number: ")
    subhalo_list = all_subhalo_property_lists[int(subhalo_num)]
    subhalo = plt.Circle((subhalo_list[2], subhalo_list[3]), subhalo_list[1] * 5, clip_on=False, ec='black')
    ax.add_artist(subhalo)
    plt.show()


if __name__ == '__main__':
    main()
