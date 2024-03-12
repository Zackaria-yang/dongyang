#把一张图片改成1920*1080的大小，存在r_images文件夹下
import PIL.Image as Image
img=Image.open('r_images/0.png')
img=img.resize((1920,1080))
img.save('r_images/0.png')
