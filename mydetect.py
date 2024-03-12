import time
import numpy as np
from PIL import Image
from segformer.segformer_main import SegFormer_Segmentation
from skimage import measure

import cv2


class Segmodel():
    def __init__(self, weights, cuda=False, mix_type=2):
        #初始化模型
        self.seg = SegFormer_Segmentation(weights=weights ,cuda=cuda, mix_type=mix_type, input_shape=[512, 512])

    def init_model(self):
        print("begin load seg model")
        self.seg.init_model()
        print("seg model load successful")

    def detect(self, img,path):
        #传入参数img改为ndarray
        image = Image.open(img)
        # print(image)
        t1 = time.time()
        r_image = self.seg.detect_image(image=image)
        print("seg time:",time.time()-t1)
        r_image= np.array(r_image)
        seg_result = cv2.cvtColor(r_image, cv2.COLOR_BGR2RGB)
        cv2.imwrite(path,r_image)
        return seg_result

    def mask(self,path1,path2):
        
        img = Image.open(path1).convert('L') 
        img = np.array(img) #img为ndarray,numpy读取图像是高*宽
        for i in range(1080):
            for j in range(1920):
                if img[i][j] > 0:
                    img[i][j] = 255

        img1 = Image.fromarray(img).convert('1')
        img1.save(path2)
        return img


    def largeConnectComponent(self,bw_image):
        #bw_image = Image.open(bw_image) #输入为二值图
        labeled_img, num = measure.label(bw_image, background=0, return_num=True)
        # 这里返回的labeled_img是一幅图像，不再是一副二值图像，有几个连通域，最大值就是几，num是连通域个数，1个连通域的话num=1
    
        max_label = 0
        max_num = 0
    
        # 图像全黑，没有连通域num=0,或者是由一个连通域num=1，直接返回原图像
        if num == 0 or num == 1:
            return bw_image
        else:
            for i in range(1, num+1):  #注意这里的范围，为了与连通域的数值相对应
                # 计算面积，保留最大面积对应的索引标签，然后返回二值化最大连通域
                if np.sum(labeled_img == i) > max_num:
                    max_num = np.sum(labeled_img == i)
                    max_label = i
            lcc = (labeled_img == max_label)
            return lcc

if __name__ == "__main__":

    path_weight = 'segformer//best_epoch_weights.pth'
    path_save = 'res_images/seg.png'
    path_detect = 'r_images/0.png'
    path_bind = 'res_images/mask1.png'
    mask_path = 'res_images/mask2.png'
    segmodel = Segmodel(cuda=False, weights = path_weight, mix_type=2)
    segmodel.init_model()
    seg_result = segmodel.detect(path_detect,path_save)
    img = segmodel.mask(path_save,path_bind)
    img = segmodel.largeConnectComponent(img)
    
    img = Image.fromarray(img)
    img.save(mask_path)