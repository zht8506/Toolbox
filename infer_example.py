# 导入必要的库
import torch
import torchvision
import torchvision.transforms as transforms

# 假设模型已经训练好了，保存在model.pth文件中
model = torch.load('model.pth')
# 设置模型为评估模式，不进行梯度更新
model.eval()

# 定义一个数据集类，继承自torch.utils.data.Dataset
class ImageDataset(torch.utils.data.Dataset):
    # 初始化函数，接受图片路径和转换函数作为参数
    def __init__(self, image_dir, transform=None):
        # 获取图片路径下的所有文件名
        self.image_names = os.listdir(image_dir)
        # 保存图片路径和转换函数
        self.image_dir = image_dir
        self.transform = transform
    
    # 返回数据集的大小
    def __len__(self):
        return len(self.image_names)
    
    # 根据索引返回一个数据样本
    def __getitem__(self, index):
        image_name = self.image_names[index]
        image_path = os.path.join(self.image_dir, image_name)
        image = Image.open(image_path)
        
        # 如果有转换函数，对图片进行转换
        if self.transform:
            image = self.transform(image)
        return image, image_name

# 定义一个转换函数，将图片转换为张量，并进行归一化
transform = transforms.Compose([
    transforms.ToTensor(),
    transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))
])

# 创建一个数据集对象，传入图片路径和转换函数
dataset = ImageDataset('images', transform)

# 创建一个数据加载器对象，传入数据集对象和批量大小
dataloader = torch.utils.data.DataLoader(dataset, batch_size=32)

# 遍历数据加载器，一个批次一个批次地进行推理
for images, names in dataloader:

    images = images.to(device)
    outputs = model(images)
    # 对输出结果进行处理，例如提取最大值，转换为类别等（根据你的模型输出和需求而定）
    # 这里假设输出结果是一个二维张量，每一行表示一个样本的类别概率分布
    _, preds = torch.max(outputs, dim=1)
    
    for name, pred in zip(names, preds):
        print(name, pred.item())