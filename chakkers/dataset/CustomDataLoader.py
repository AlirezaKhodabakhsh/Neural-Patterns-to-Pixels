from torch.utils.data import Dataset
import bdpy
import cv2
import os
import h5py
import nilearn
import nibabel as nib
import numpy as np

# nsd_subj01_08_id_img = pd.read_csv('E:/Amozesh/Dr. Zahra Bahmani/Paper/Dataset/New folder/Label/nsd_subj01_08_id_img.csv')
# nsd_subj01_08_id_img = nsd_subj01_08_id_img.to_numpy()
# root_image = "E:/Amozesh/Dr. Zahra Bahmani/Paper/Dataset/New folder/nsd_stimuli/nsd_stimuli.hdf5"
# root_fmri = 'E:/Amozesh/Dr. Zahra Bahmani/Paper/Dataset/New folder/func1pt8mm_betas_fithrf_GLMdenoise_RR/betas_session0'
# item = 751
# fMRI_adrr = root_fmri + str(nsd_subj01_08_id_img[item,2]) + '.nii.gz'
# betas_session01 = image.load_img(fMRI_adrr)
# root_fmri = image.index_img(betas_session01, nsd_subj01_08_id_img[item,4]).get_fdata()



class CustomDataLoader(Dataset):
    """
    Args:
        fmri_file : str :
        imagenet_folder : str
        roi_selector : str
        transform :

    Return:
        image : np.array : (N, H, W, C)
        fmri  : np.array : (N, T)
    """
    def __init__(self, root_fmri:str, root_image:str, self_ROI_array, nsd_subj01_08_id_img, transform = None):
        super(CustomDataLoader, self).__init__()

        self.root_fmri = root_fmri
        self.root_image = root_image
        self.self_ROI_array = self_ROI_array
        self.nsd_subj01_08_id_img = nsd_subj01_08_id_img
        self.transform = transform



    def __getitem__(self, item):
        nsd_stimuli = h5py.File(self.root_image, 'r')
        imgBrick = nsd_stimuli.get('imgBrick')
        NSD_adrr = np.array(imgBrick[self.nsd_subj01_08_id_img[item, 3]:self.nsd_subj01_08_id_img[item, 3] + 1])
        first_betas_session011 = self.self_ROI_array * self.root_fmri
        first_betas_session011 = np.where(first_betas_session011 > 0, first_betas_session011, None)

        fmri = np.zeros((1, 31330), dtype=float)
        m = 0
        for i in range(104):
            for j in range(83):
                for k in range(81):
                    if (first_betas_session011[k, i, j] != None):
                        fmri[0, m] = first_betas_session011[k, i, j]
                        m += 1

        image = NSD_adrr.reshape(1, 425, 425, 3)

        if self.transform is not None:
            image = self.transform(image)

        return image, fmri




    def __len__(self):
        return len(self.fmri_labels)








class Custom_real_DataLoader(Dataset):
    """
    Args:
        imagenet_folder : str

    Return:
        image : np.array : (N, H, W, C)
        labels  : np.array : (N, 1)
    """
    def __init__(self, coco_folder: str, transform=None):
        super(Custom_real_DataLoader, self).__init__()

        self.coco_folder = coco_folder
        self.transform = transform


    def __getitem__(self, item):
        image = cv2.imread(self.coco_folder + f'/{os.listdir(self.coco_folder)[item]}')
        label = 1

        if self.transform is not None:
            image = self.transform(image)

        return image, label


    def __len__(self):
        return len(os.listdir(self.coco_folder))