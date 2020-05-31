import time
import torch
import torch.nn as nn
import torch.nn.functional as F


#https://pytorch.org/docs/master/nn.html#torch.nn.Conv2d

class ConvNet(nn.Module):
  bs = 1    # batch size
  xdim = 64
  kernel_len = 5 # 1, 3, 5, 7
  input_shape = (bs, 3, xdi, ydim)
  def __init__(self):
    super(ConvNet, self).__init__()
    #nn.Conv2d(in_channels, out_channels, kernel_size, stride=1, padding=0, dilation=1, groups=1, bias=True, padding_mode='zeros')
    self.layer1 = nn.Conv2d(3, 32, self.kernel_len, stride=1)
    self.layer2 = nn.Conv2d(32, 64, self.kernel_len, stride=1)
    self.layer3 = nn.Conv2d(64, 64, self.kernel_len, stride=1)


  def forward(self, x):
    x = F.relu(x)
    x = self.layer1(x)
    x = F.relu(x)
    x = self.layer2(x)
    x = F.relu(x)
    x = self.layer3(x)

    

    # Pytorch sets weights using its own formula thing

    # def reset_parameters(self):
    #     init.kaiming_uniform_(self.weight, a=math.sqrt(5))
    #     if self.bias is not None:
    #         fan_in, _ = init._calculate_fan_in_and_fan_out(self.weight)
    #         bound = 1 / math.sqrt(fan_in)
    #         init.uniform_(self.bias, -bound, bound)

def testFPS(model, n, device_on):
  frame = torch.rand(input_shape, device=device_on)
  total_time = 0;
  for i in range(n):
    start = time.time()
    hole = model(frame)
    end = time.time()
    total_time += (end-start)
  print("Number of frames: ", n)
  print("Elapsed Time: ", total_time)
  print("FPS: ", n/total_time)
  return total_time


n = 1000 #number of times we repeat the prediction

def main():
  use_cuda = True
  device = torch.device("cuda" if use_cuda else "cpu")
  model = ConvNet().to(device)
  testFPS(model, n, device)

if __name__ == "__main__":
  main()

