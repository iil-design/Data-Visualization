import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Rectangle, Ellipse
from matplotlib.colors import LinearSegmentedColormap

plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

# -------------------------------------------------
# 1️⃣ 读数 & 时间过滤
# -------------------------------------------------
df = pd.read_csv(r'D:\pythonProject\fake_orders.csv', parse_dates=['shipping_date'])
df = df[(df['shipping_date'] >= '2025-06-01') & (df['shipping_date'] <= '2025-12-31')]

# 2️⃣ 按平台统计订单笔数（internal_order_number 去重）
target_platforms = ['拼多多', '抖音', '小红书', '京东', '天猫', '得物', '淘宝']
platform_orders = (df[df['platform'].isin(target_platforms)]
                   .groupby('platform')['internal_order_number']
                   .nunique()
                   .reindex(target_platforms, fill_value=0)
                   .reset_index(name='orders'))

avg_orders = platform_orders['orders'].mean()
platform_orders['平均值'] = avg_orders

# 3️⃣ 绘图（深蓝背景 + 每个柱子不同颜色 + 标签同色）
plt.style.use('dark_background')
fig, ax = plt.subplots(figsize=(10, 6), dpi=120)
fig.patch.set_facecolor('#0A1045')
ax.set_facecolor('#0A1045')

# 每个柱子不同的颜色列表（可以自定义）
colors = ["#FF6F61", "#6B5B95", "#88B04B", "#F7CAC9", "#92A8D1", "#955251", "#B565A7"]
x = np.arange(len(platform_orders))
bar_width = 0.45
max_val = platform_orders['orders'].max()
radius = max_val * 0.03
grad_steps = 100  # 渐变分段数量

for i, (val, color) in enumerate(zip(platform_orders['orders'], colors)):
    # 将柱子分成 grad_steps 小段实现渐变
    for j in range(grad_steps):
        y0 = j * (val - radius) / grad_steps
        y1 = (j + 1) * (val - radius) / grad_steps
        # 渐变从亮到暗，可以用 alpha 调整
        rect = Rectangle((i - bar_width/2, y0), bar_width, y1 - y0,
                         facecolor=color, edgecolor='none', alpha=0.7 + 0.3*j/grad_steps)
        ax.add_patch(rect)
    # 顶部半圆
    top = Ellipse((i, val - radius), bar_width, 2*radius,
                  facecolor=color, edgecolor='none')
    ax.add_patch(top)
    # 数值标签（颜色与柱子相同）
    ax.text(i, val + max_val*0.01,
            f'{int(val)}', ha='center', va='bottom',
            fontsize=11, color=color, fontweight='bold')

# 平均值虚线
ax.axhline(avg_orders, color='#FFD700', linestyle='--', linewidth=1.5)
ax.text(len(platform_orders)-0.5, avg_orders + max_val*0.01,
        f'全国平均 {avg_orders:.0f}', color='#FFD700', fontsize=11, ha='right', fontweight='bold')

# 标题 & 副标题
ax.set_title('2025年下半年重点平台订单笔数分布（多彩圆角柱）',
             fontsize=16, fontweight='bold', color='white', loc='left', pad=5)
ax.text(0, max_val*1.12,
        f'全国平均订单笔数约 {avg_orders:.0f}，抖音订单最多，得物偏低',
        fontsize=12, color='white', alpha=0.85)

# 坐标轴 & 网格
ax.set_xticks(x)
ax.set_xticklabels(platform_orders['platform'], color='white', fontsize=11)
ax.set_ylabel('订单笔数（单）', fontsize=12, color='white', labelpad=10)
ax.tick_params(axis='y', colors='white', labelsize=11)
ax.yaxis.grid(True, ls='--', alpha=0.2)
ax.xaxis.grid(False)
for spine in ['top', 'right', 'left']:
    ax.spines[spine].set_visible(False)
ax.spines['bottom'].set_color('#444')
ax.set_xlim(-0.5, len(platform_orders) - 0.5)

# 数据来源
plt.text(0, -max_val*0.08,
         '*数据来源：公司销售系统（统计日期：2025.06–2025.12）',
         fontsize=10, color='#aaaaaa')

plt.tight_layout()
plt.show()

# 4️⃣ 导出结果
output_path = r'D:\pythonProject\platform_orders_summary_2025H2.csv'
platform_orders.to_csv(output_path, index=False, encoding='utf-8-sig')
print("✅ 多彩圆角柱图完成，并已导出汇总文件：", output_path)
print(platform_orders)
