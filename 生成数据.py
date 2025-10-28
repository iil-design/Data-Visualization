#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
批量生成 1000 条虚拟订单并保存为 CSV
python3 fake_orders_to_csv.py
"""
import random
import pandas as pd
from faker import Faker
from datetime import datetime, timedelta
import os

# ----------------- 可调参数 -----------------
OUTPUT_CSV = 'fake_orders.csv'      # 输出文件名
GENERATE_NUM = 1000                 # 需要生成的订单行数
# ------------------------------------------

fake = Faker('zh_CN')

# 如果 sku_data_base 表拿不到，就用 faker 造 200 条假 SKU 数据
sku_rows = []
for _ in range(200):
    sku_rows.append((
        'SKU' + fake.uuid4()[:6],
        'SPU' + fake.uuid4()[:6],
        fake.catch_phrase(),
        fake.color_name(),
        fake.color_name(),
        random.randint(99, 999)
    ))

platforms   = ['淘宝', '天猫', '京东', '抖音', '得物', '小红书', '拼多多']
status_list = ['已发货', '已签收', '已完成']
refund_list = ['未申请退款', '申请退款', '成功退款', '退款关闭']
gift_list   = ['是', '否']
store_names = ['安娜旗舰店', '安娜直播店', '安娜奥莱店', '安娜分销店']

def make_order() -> dict:
    """生成一条虚拟订单（字典结构）"""
    sku, spu, prod_name, color_spec, color, basic_price = random.choice(sku_rows)
    qty = random.randint(1, 3)
    unit_price = round(basic_price * random.uniform(0.7, 1.3), 2)
    product_amount = round(unit_price * qty, 2)
    payable = round(product_amount * random.uniform(0.8, 1.0), 2)
    paid = round(payable * random.uniform(0.95, 1.0), 2)

    order_time = fake.date_time_between(start_date='-180d', end_date='-1d')
    payment_date = order_time + timedelta(hours=random.randint(0, 24))
    shipping_date = payment_date + timedelta(hours=random.randint(6, 72))

    refund = random.choice(refund_list)
    if refund == '成功退款':
        shipping_date = None

    return dict(
        internal_order_number=fake.uuid4().upper()[:18],
        online_order_number='OL' + fake.uuid4().upper()[:18],
        store_name=random.choice(store_names),
        full_channel_user_id=fake.uuid4()[:20],
        shipping_date=shipping_date,
        payment_date=payment_date,
        payable_amount=payable,
        paid_amount=paid,
        status=random.choice(status_list),
        consignee=fake.name(),
        spu=spu,
        order_time=order_time,
        province=fake.province(),
        city=fake.city(),
        platform=random.choice(platforms),
        sub_order_number='SUB' + fake.uuid4().upper()[:16],
        online_sub_order_number='ONLINESUB' + fake.uuid4().upper()[:16],
        original_online_order_number='ORIG' + fake.uuid4().upper()[:16],
        sku=sku,
        quantity=qty,
        unit_price=unit_price,
        product_name=prod_name,
        color_and_spec=color_spec,
        product_amount=product_amount,
        original_price=round(unit_price / random.uniform(0.6, 0.95), 2),
        is_gift=random.choice(gift_list),
        sub_order_status='正常',
        refund_status=refund,
        registered_quantity=qty if refund == '申请退款' else 0,
        actual_refund_quantity=qty if refund == '成功退款' else 0
    )

if __name__ == '__main__':
    rows = [make_order() for _ in range(GENERATE_NUM)]
    df = pd.DataFrame(rows)

    # 时间列统一转字符串，避免 Excel 打开时格式异常
    time_cols = ['order_time', 'payment_date', 'shipping_date']
    for col in time_cols:
        df[col] = df[col].dt.strftime('%Y-%m-%d %H:%M:%S')

    df.to_csv(OUTPUT_CSV, index=False, encoding='utf-8-sig')
    print(f'成功生成 {GENERATE_NUM} 条虚拟订单，已保存至 {os.path.abspath(OUTPUT_CSV)}')