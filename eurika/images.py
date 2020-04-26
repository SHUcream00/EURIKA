from PIL import Image

def to_ico(src = str):
    '''Given a square image, saves that in ico format'''
    img = Image.open(src)
    img.save('icon.ico')
