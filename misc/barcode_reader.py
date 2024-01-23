from pyzbar.pyzbar import decode, ZBarSymbol
from PIL import Image  # pip install Pillow
# import time


# from asyncio import sleep


async def barcode_reader(path_to_image: str, code_count: int = 13):
    try:
        image = Image.open(path_to_image)  # PIL
    except PermissionError as e:
        print(f'Error: {e}')
        return

    # decoded_list = decode(image)
    # decoded_list = await decode(image, symbols=[ZBarSymbol.EAN13, ZBarSymbol.CODE128])
    decoded_list = decode(image, symbols=[ZBarSymbol.EAN13, ZBarSymbol.CODE128, ZBarSymbol.QRCODE])

    # await sleep(1)
    # (width, height) = image.size
    # print(f'Распознано штрих-кодов: {len(decoded_list)} | Datas: {decoded_list} | Size (width, height): {image.size}')
    # width, height = image.size

    # return [(x.data.decode()) for x in decoded_list]
    # return [(x.data.decode()) for x in decoded_list if len(x.data.decode()) == code_count]

    # print(len(decoded_list))
    # print(decoded_list)
    # print()

    return [{'barcode': x.data.decode(), 'size': image.size, 'type': x.type} for x in decoded_list
            if len(x.data.decode()) == code_count or x.data.decode() == 'NEXT']
    # return [(x.data.decode(), x.type, x.orientation) for x in decoded_list if len(x.data.decode()) == code_count]


if __name__ == '__main__':
    import asyncio

    # image_file = r'e:\SLS-Photo-for-Test\2023\2023.09\15-09-2023_(624)\DSC_7361.JPG'
    # image_file = r'C:\Users\InfSub\Clouds\NextCloud\Cloud.TkYD.ru\InfSub\PublicPhoto\PhotoTextile\Auto_\21032037\2103203779457-c.jpg'
    image_file = r'e:\SLS-Photo-for-Test\NEXT\NEXT.png'

    result = asyncio.run(barcode_reader(image_file))
    print(result)

    # При помощи PIL узнать размер можно так:
    # from PIL import Image
    #
    # im = Image.open("logo.jpg")
    # (width, height) = im.size
