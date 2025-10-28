import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Rectangle
from matplotlib.colors import LinearSegmentedColormap

plt.rcParams['font.sans-serif'] = ['SimHei']  # 黑体
plt.rcParams['axes.unicode_minus'] = False
# ----------------------------------
# 1️⃣ 区域映射表
# ----------------------------------
REGION_MAP = {
    '北京市': '华北', '天津市': '华北', '河北省': '华北', '山西省': '华北', '内蒙古自治区': '华北',
    '山东省': '华东', '江苏省': '华东', '安徽省': '华东', '浙江省': '华东', '福建省': '华东', '江西省': '华东', '上海市': '华东',
    '广东省': '华南', '广西壮族自治区': '华南', '海南省': '华南', '香港特别行政区': '华南', '澳门特别行政区': '华南',
    '河南省': '华中', '湖北省': '华中', '湖南省': '华中',
    '辽宁省': '东北', '吉林省': '东北', '黑龙江省': '东北',
    '四川省': '西南', '重庆市': '西南', '贵州省': '西南', '云南省': '西南', '西藏自治区': '西南',
    '陕西省': '西北', '甘肃省': '西北', '青海省': '西北', '宁夏回族自治区': '西北', '新疆维吾尔自治区': '西北',
    '台湾省': '华东'
}

# ----------------------------------
# 2️⃣ 读取数据并统计
# ----------------------------------
df = pd.read_csv(r'D:\pythonProject\fake_orders.csv', parse_dates=['shipping_date'])

# 时间过滤（2025年6月～12月）
df = df[(df['shipping_date'] >= pd.Timestamp('2025-06-01')) &
        (df['shipping_date'] <= pd.Timestamp('2025-12-31'))]

# 映射大区
df['region'] = df['province'].map(REGION_MAP).fillna('其他')

# 汇总区域销量
order = ['华北', '华南', '华中', '东北', '西北', '西南', '华东', '其他']
region_qty = df.groupby('region')['quantity'].sum().reindex(order, fill_value=0).reset_index()

# 计算平均销量
avg_sales = region_qty['quantity'].mean()
region_qty['平均值'] = avg_sales

# ----------------------------------
# 3️⃣ 绘制现代商务风格渐变蓝柱状图 + 平均线
# ----------------------------------
plt.style.use('dark_background')
fig, ax = plt.subplots(figsize=(10, 6), dpi=120)
fig.patch.set_facecolor('#0A1045')
ax.set_facecolor('#0A1045')

# 创建蓝色渐变 colormap（从浅蓝到深蓝）
cmap = LinearSegmentedColormap.from_list("blue_gradient", ["#00CFFF", "#004CFF"])

# 柱宽度和位置
x = np.arange(len(region_qty))
bar_width = 0.4

# 绘制渐变柱体
for i, val in enumerate(region_qty['quantity']):
    # 在每个柱子的矩形区域中生成渐变色
    gradient = np.linspace(0, 1, 256).reshape(-1, 1)
    ax.imshow(gradient, extent=[i - bar_width / 2, i + bar_width / 2, 0, val],
              origin='lower', aspect='auto', cmap=cmap, alpha=0.95)
    # 添加边框（浅蓝色）
    # 数值标签
    ax.text(i, val + 50, f'{int(val)}',
            ha='center', va='bottom', fontsize=11, color='white', fontweight='bold')

# 平均线（黄色）
ax.axhline(y=avg_sales, color='yellow', linestyle='--', linewidth=2, label=f'平均销量：{avg_sales:.0f}')
ax.legend(loc='upper right', fontsize=11, facecolor='#0A1045', edgecolor='none', labelcolor='white')

# 标题与说明
ax.set_title('2025年下半年各区域销量分布（渐变蓝风格）',
             fontsize=18, fontweight='bold', color='white', loc='left', pad=10)
ax.text(0, max(region_qty['quantity']) * 1.1,
        f'全国平均销量约为 {avg_sales:.0f}，华东销量最高，华中偏低',
        fontsize=12, color='white', alpha=0.85)

# 坐标轴与网格
ax.set_xticks(x)
ax.set_xticklabels(region_qty['region'], color='white', fontsize=11)
ax.set_ylabel('销量（单位）', fontsize=12, color='white', labelpad=10)
ax.tick_params(axis='y', colors='white', labelsize=11)
ax.yaxis.grid(True, linestyle='--', alpha=0.2)
ax.xaxis.grid(False)

# 去掉多余边框
for spine in ['top', 'right', 'left']:
    ax.spines[spine].set_visible(False)
ax.spines['bottom'].set_color('#444')

ax.set_xlim(-0.5, len(region_qty) - 0.5)

# 数据来源说明
plt.text(0, -max(region_qty['quantity']) * 0.2,
         '*数据来源：公司销售系统（统计日期：2025.06–2025.12）',
         fontsize=10, color='#aaaaaa')

plt.tight_layout()
plt.show()

# ----------------------------------
# 4️⃣ 输出结果表格文件
# ----------------------------------
output_path = r'D:\pythonProject\region_sales_summary_2025H2.csv'
region_qty.to_csv(output_path, index=False, encoding='utf-8-sig')

print("✅ 图表绘制完成，并已导出汇总文件：", output_path)
print(region_qty)
