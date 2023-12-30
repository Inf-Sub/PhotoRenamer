import asyncio
# import json module
import json

# from concurrent.futures import ThreadPoolExecutor

from misc import find_files, find_barcode, barcode_reader, save_data_to_json, save_photo, print_data_from_json


# _executor = ThreadPoolExecutor(1)


# def sync_blocking(seconds: int = 1):
#     time.sleep(seconds)


# async def main(dst_path: str, extension: list, pattern_barcode: str, pattern_photo_name: str, data_file: str):
async def main(
        src_path: str,
        extension: list,
        data_file: str,
        dir_barcode_len: int,
        dst_path: str = None,
        action_move: bool = None
    ):
    patterns = {
        'barcode': r'^21\d{11}',
        'extension': r'.*[.](\w{3,4})$',
        'photo_name': r'^DSC_(\d{4})[.]',
        'find_files': f'.*[.](?:{{extension}})$',
        'photo_files': f'{{photo_name}}(?:{{extension}})$',
        'barcode_name_files': f'{{barcode}}[-][a-z][.](?:{{extension}})$',
    }

    ext = '|'.join(map(str, extension))

    patterns['find_files'] = patterns['find_files'].format(extension=ext)
    patterns['photo_files'] = patterns['photo_files'].format(photo_name=patterns['photo_name'], extension=ext)
    patterns['barcode_name_files'] = patterns['barcode_name_files'].format(barcode=patterns['barcode'], extension=ext)
    patterns['barcode'] += '$'

    dict_with_photo = await find_files(src_path, patterns['find_files'])

    # dict_with_photo = {'all': dict_with_photo}

    dict_with_photo = await find_barcode(
        barcode_reader=barcode_reader,
        dict_with_photo=dict_with_photo,
        patterns=patterns
    )

    # await print_data_from_json(dict_with_photo)

    await save_data_to_json(path=data_file, data=dict_with_photo)

    if dst_path is not None:
        if action_move is None:
            action_move = False
        await save_photo(
            src_path=src_path,
            dst_path=dst_path,
            data=dict_with_photo,
            dir_barcode_len=dir_barcode_len,
            action_move=action_move
        )

    # await print_data_from_json(dict_with_files)

    # run blocking function in another thread,
    # and wait for it's result:
    # await loop.run_in_executor(_executor, sync_blocking)


if __name__ == '__main__':
    examples_dir = 'examples'
    # photo_dir = examples_dir

    photo_dir = r'e:\SLS-Photo-for-Test'
    # photo_dir = r'e:\SLS-Photo-for-Test\2023\2023.05\ОБРАЗЦЫ С ВАРШАВКИ_(74)'
    # photo_dir = r'e:\SLS-Photo-for-Test\СЕНТЯБРЬ_2023'

    result_path = r'e:\SLS-Photo-for-Test-result'

    data_json_file = r'db/.data.json'

    photo_ext = ['jpg', 'jpeg', 'png']

    dir_name_barcode_len = 9

    try:
        asyncio.run(
            main(
                src_path=photo_dir,
                extension=photo_ext,
                data_file=data_json_file,
                dir_barcode_len=dir_name_barcode_len,
                dst_path=result_path,
                action_move=False
            )
        )
        # loop = asyncio.get_event_loop()
        # loop.run_until_complete(main(photo_dir, photo_ext))
        # loop.close()
    except (KeyboardInterrupt, SystemExit):
        print('Program was stopped by user.')

