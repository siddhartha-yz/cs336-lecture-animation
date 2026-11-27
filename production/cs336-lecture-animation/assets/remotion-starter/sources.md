# 同一组分数的两种验证

概率台：分数为 `(0, ln 3)`。Softmax 得到 `(1/4, 3/4)`。两项同加 2，分子和分母同时乘以 `e²`，右侧两根柱不动。左侧读数显示到两位小数；自动计算用未舍入的 `ln 3`。

## 片内运行的程序

切面运行同一组分数。第一行保持原值，第二行同加 2；[PyTorch `Tensor.softmax`](https://docs.pytorch.org/docs/2.14/generated/torch.Tensor.softmax.html) 沿第 1 维归一化，也就是分别在每行的两个分数间归一化。

```python
from math import log
import torch
z = torch.tensor([0., log(3)])
x = torch.stack((z, z + 2))
p = x.softmax(dim=1)
print([[round(v, 2) for v in row] for row in p.tolist()])
```

两行均为 `[0.25, 0.75]`（显示到两位）。渲染不需要 PyTorch；在现有 PyTorch 环境里可重跑这段代码。
