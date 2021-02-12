from PySimpleGUI.PySimpleGUI import T
from .. import (
    handle_json,
    meta
)
from . import (
    common,
    update
)
from .settings import *
import PySimpleGUI as sg


def open(weapon_json_path: str, to_update: bool = True):
    """武器一覧画面を表示し、武器項目を押下で、更新画面へ遷移する

    Args:
        weapon_json_path    : 武器情報格納パス
    """
    sg.theme('Dark Blue 3')

    weapon_table_dict = get_weapon_table_dict(weapon_json_path)
    msg = '表示したい武器の行をダブルクリックすることで、更新画面が表示されます。' if to_update else 'この画面を閉じるまで、元の画面ではボタン操作は実行できません。'

    layout = [
        [sg.Text(msg)],
        [
            sg.Table(
                key='Weapon_Table',
                values=weapon_table_dict["window_table_data_list"],
                headings=weapon_table_dict["header_list"],
                justification='left',
                auto_size_columns=False,
                col_widths=[max(20, weapon_table_dict["max_type_bytes"]), max(35, weapon_table_dict["max_name_bytes"])],
                bind_return_key=to_update
            )
        ],
        [sg.Submit(button_text='再読み込み')]
    ]

    window = sg.Window('武器一覧画面', layout)

    while True:
        event, values = window.read()
        if event is None:
            break
        elif event == 'Weapon_Table':
            click_weapon_info_dict = {index: value for index, value in enumerate(weapon_table_dict["window_table_data_list"][values[event][0]])}
            print(click_weapon_info_dict, flush=True)
            update.open(weapon_json_path, click_weapon_info_dict)
        elif event == '再読み込み':
            weapon_table_dict = get_weapon_table_dict(weapon_json_path)
            refresh(window, values.keys(), weapon_table_dict)
    window.close()


def get_weapon_table_dict(weapon_json_path: str) -> dict:
    """武器情報をテーブル形式に変形させt返却する

    Args:
        weapon_json_path            : 武器情報格納パス

    Returns:
        return_weapon_table_dict    : 返却する武器情報テーブル情報
    """
    # return_weapon_table_dict = {
    #     "": [],
    #     "": 0,
    #     "": 0
    # }
    # 初期変数
    return_weapon_table_dict = {
        "header_list": ["武器タイプ", "武器名"],
        "window_table_data_list": []
    }
    # 全武器の情報を取得する
    for weapon_type_name, weapon_type_meta_name in meta.meta_weapon_type_dict.items():
        weapon_json_dict = handle_json.read(f"{weapon_json_path}/{weapon_type_meta_name}.json")
        return_weapon_table_dict["window_table_data_list"].extend([[weapon_type_name, weapon_name] for weapon_name in weapon_json_dict.keys()])

    # 列幅が文字数でカウントされるために、日本語文字列では見えてほしい領域まで見えないため、最大Byte数を取得しておく。
    return_weapon_table_dict["max_type_bytes"] = max([len(weapon_table_datas[0].encode('shift_jis')) for weapon_table_datas in return_weapon_table_dict["window_table_data_list"]])
    return_weapon_table_dict["max_name_bytes"] = max([len(weapon_table_datas[1].encode('shift_jis')) for weapon_table_datas in return_weapon_table_dict["window_table_data_list"]])

    return return_weapon_table_dict


def refresh(window: sg.Window, input_values_keys: list, weapon_table_dict: dict):
    for values_key in input_values_keys:
        window[values_key].update(values=weapon_table_dict["window_table_data_list"])

