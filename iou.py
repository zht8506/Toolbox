### 本文件是IOU计算代码

# box1=(1,1,3,3)
# box2=(2,2,4,4)
x1,y1,x2,y2 = box1 #box1的左上角坐标、右下角坐标
x3,y3,x4,y4 = box2 #box2的左上角坐标、右下角坐标

#计算交集的坐标
x_inter1 = max(x1,x3) #union的左上角x
y_inter1 = max(y1,y3) #union的左上角y
x_inter2 = min(x2,x4) #union的右下角x
y_inter2 = min(y2,y4) #union的右下角y
print(x_inter1,y_inter1,x_inter2,y_inter2)
# 计算交集部分面积，因为图像是像素点，所以计算图像的长度需要加一
# 比如有两个像素点(0,0)、(1,0)，那么图像的长度是1-0+1=2，而不是1-0=1
interArea = max(0,x_inter2-x_inter1+1)*max(0,y_inter2-y_inter1+1)
print(interArea)

# 分别计算两个box的面积
area_box1 = (x2-x1+1)*(y2-y1+1)
area_box2 = (x4-x3+1)*(y4-y3+1)

#计算IOU，交集比并集，并集面积=两个矩形框面积和-交集面积
iou = interArea/(area_box1+area_box2-interArea)
print(iou)
print(interArea,area_box1,area_box2)
