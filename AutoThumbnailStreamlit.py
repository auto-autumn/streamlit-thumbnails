import numpy as np
from PIL import Image, ImageDraw, ImageFilter
import streamlit as st


# 何個作るか聞く
num_trials = st.slider('何個試作しますか？',0,10,0)
button = st.button('上記の設定で試作')


# 画像を後で入れる空のリスト
imgs = []

# URLを下になる画像から順に入れる
urls = ['base.png', 'field.jpg', 'yattazeyossya.png', 'Splatoon2logo.png',
        'decorators-12_2x.png', 'decorators-12_2x.png']
genres = ['base', 'back', 'person', 'logo', 'deco', 'deco']
for i, url in enumerate(urls):
    imgs.append(Image.open(url))
    
if button:
    for trials in range(num_trials):
        # 背景に色付け
        draw = ImageDraw.Draw(imgs[0])
        full_size = np.array(imgs[0].size)
        base_color = np.random.randint(0, 255, 3)
        draw.rectangle((0, 0, tuple(full_size)), fill=(
            base_color[0], base_color[1], base_color[2]))

        # 背景と混ぜた枠をセット※mode'RGBA'と'RGB'とかを揃える必要あり
        imgs[1] = imgs[1].resize(tuple(full_size))
        imgs[0] = Image.blend(imgs[0], imgs[1].convert('RGBA'), 0.5)

        # 背景画像をセット
        imgs[1] = imgs[1].resize(tuple(full_size-[20, 20]))
        imgs[0].paste(imgs[1], (15, 10))

        # 背景画像(通常1280,720)内に画像を散りばめる乱数を生成
        number = len(imgs)
        widths = []
        heights = []
        for k in range(number-2):
            img_ratio = (imgs[k+2].width / imgs[k+2].height) ** 0.5
            if genres[k+2] == 'logo':
                size_base = 400
            elif genres[k+2] == 'deco':
                size_base = 100
            elif genres[k+2] == 'person':
                size_base = 700
            new_size = tuple([round(size_base*img_ratio), round(size_base/img_ratio)])
            imgs[k+2] = imgs[k+2].resize(new_size)
            widths.append(np.random.randint(0, full_size[0]-new_size[0]))
            heights.append(np.random.randint(0, full_size[1]-new_size[1]))

        # 画像を配置
        for j, x, y in zip(range(number-2), widths, heights):
            mask = imgs[j+2].copy().convert('RGBA')
            imgs[0].paste(imgs[j+2], (x, y), mask)

        st.title('AutoThumbnail')
        st.image(imgs[0], caption='squid', use_column_width=True)