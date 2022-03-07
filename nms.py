# nms非极大值抑制代码
import torch

#计算某个box与其他多个box的iou值
def iou(box,boxes):
    '''
    :param box: 矩形框box的坐标
    :param boxes: 一大堆矩形框的坐标
    :return: 计算矩形框box与一大堆矩形框的iou值
    '''
    # box.shape: (4,),4个值分别是x1,y1,x2,y2
    # boxes.shape: (n,4) ,n是要计算iou的矩形框个数
    box_area=(box[2]-box[0]+1)*(box[3]-box[1]+1) #box的面积
    boxes_area=(boxes[:,2]-boxes[:,0]+1)*(boxes[:,3]-boxes[:,1]+1) #多个box的面积

    # 交集坐标
    xx1=torch.maximum(box[0],boxes[:,0]) #交集矩形框角坐标x1
    yy1=torch.maximum(box[1],boxes[:,1]) #交集矩形框角坐标y1
    xx2 = torch.minimum(box[2], boxes[:, 2])  # 交集矩形框角坐标x2
    yy2 = torch.minimum(box[3], boxes[:, 3])  # 交集矩形框角坐标y2

    # 交集面积
    inter_area=torch.max(torch.tensor((0)),xx2-xx1+1)*torch.max(torch.tensor((0)),yy2-yy1+1)

    #并集面积
    union_area=box_area + boxes_area - inter_area

    #返回iou
    iou=inter_area/union_area

    return iou


def nms(boxes,thresh=0.3):
    """
    :param boxes: 一大堆需要nms后处理的预测框
    :param thresh: iou阈值，默认取0.5
    :return:
    """
    # boxes.shape: [n,5]，n个矩形框，5分别是scores(置信度)、x1、y1、x2、y2

    # 先对boxes以scores进行排序
    # argsort可以取出排序后的下标位置
    new_boxes=boxes[torch.argsort(boxes[:,0],descending=True)]
    boxes_result = []  # 最终输出的所有预测框
    while len(new_boxes)>1: #满足大于1是因为，至少要两个box才能进行循环
        box=new_boxes[0] #置信度最大的预测框
        boxes_result.append(box) #直接将置信度最大的box加入结果中
        new_boxes=new_boxes[1:] #去除第一个box
        # 取出和第一个box的iou小于阈值的预测框（因为iou较小，这些预测框可能是其他问题）
        new_boxes=new_boxes[torch.where(iou(box,new_boxes)<thresh)]

    if len(new_boxes)>0: #如果还剩下一个box，那么直接加入结果
        boxes_result.append(new_boxes[0])

    return torch.stack(boxes_result)



if __name__=="__main__":
    # 测试iou函数
    box=torch.tensor((0,0,4,4))
    boxes=torch.tensor([[6,6,7,7],[1,1,5,5]])
    print(iou(box,boxes))

    boxes_nms= torch.tensor([[0.2,1,2,4,4],[0.7,1,1,4,4],[0.9,8,8,9,9]])
    print(nms(boxes_nms)) #只会保留第二个和第三个


