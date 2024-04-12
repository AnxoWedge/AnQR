import qrcode
from PIL import Image


#Taking image that user wants 
Logo_link = 'example.jpg'
logo = Image.open(Logo_link)

#width 
basewidth = 150

#adjust image size 
wpercent = (basewidth/float(logo.size[0]))
hsize = int((float(logo.size[1])*float(wpercent)))
logo = logo.resize((basewidth,hsize),Image.ANTIALIAS)
Qrcode = qrcode.QRcode(error_correction=qrcode.constant.ERROR_CORRECT_H)

#Taking URL/text/information the QR code holds
url= "https://example.xyz"

#adding URL or text to QRcode and generating QRcode
QRcode.add_data(url)
QRcode.make()

#Asking for color  and adding color
QRcolor = '#000'
BGcolor = '#fff'

QRimg = QRcode.make_image(
    fill_color=QRcolor,
    back_color=BGcolor,
).convert('RGB')

# set size of the QRcode and pos of the logo
if(logo):
    pos = ((QRimg.size[0] - logo.size[0]) // 2,
        (QRimg.size[1] - logo.size[1]) // 2)
    QRimg.paste(logo,pos)

#Saving the QRcode 
QRimg.save('QRgenerated.png')

print('QR code has been generated')

