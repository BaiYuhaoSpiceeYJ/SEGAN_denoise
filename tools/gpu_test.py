import torch
flag = torch.cuda.is_available()
print(flag)
n_gpu = 1
device = torch.device("cuda:0" if flag and n_gpu > 0 else "cpu")
print(device)
print(torch.cuda.get_device_name(0))
print(torch.rand(3, 3).cuda)