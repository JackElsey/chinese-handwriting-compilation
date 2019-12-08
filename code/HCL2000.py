import numpy as np
import matplotlib.pyplot as plt
import glob

def get_char_img(writer_no, char_no):
    hcl_files = glob.glob('../HCL2000/*.hcl')
    data = np.fromfile(hcl_files[writer_no], dtype='ubyte')
    
    start_ind = 511+char_no*512
    img = np.zeros(64*64)
    
    for i in range(start_ind,(start_ind+512)):
        binary_str = '{0:08b}'.format(data[i])
        for j in range(8):
            img[(i-start_ind)*8+j] = int(binary_str[j])

    img = np.reshape(img, (64,64))
    img = np.concatenate((img[:,8:], img[:,:8]), axis=1)
    
    return img
    
def save_image(img, filename):
   
    sizes = np.shape(img)
    height = float(sizes[0])
    width = float(sizes[1])
     
    fig = plt.figure()
    fig.set_size_inches(width/height, 1, forward=False)
    ax = plt.Axes(fig, [0., 0., 1., 1.])
    ax.set_axis_off()
    fig.add_axes(ax)
 
    ax.imshow(img, cmap='binary')
    plt.savefig(filename, dpi = height) 
    plt.close()
    
def save_char_img_arr(char_no, filename, dim=(4,4)):
    writers = np.random.randint(0, 999, dim)
    m = 10 # margin pixels
    img_arr = np.zeros((dim[0]*(64+m)+m, dim[1]*(64+m)+m))
    
    for i in range(dim[0]):
        for j in range(dim[1]):
            img_arr[(m+i*(64+m)):(m+i*(64+m)+64), (m+j*(64+m)):(m+j*(64+m)+64)] = get_char_img(writers[i,j],char_no)

    save_image(img_arr, filename)

if __name__ == '__main__':
    with open('../GB2312.txt', 'r') as file_object:
        characters = file_object.read()
    
    for i in range(3755):
        char = characters[i]
        save_char_img_arr(i, '../output/'+char)
