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

    weapon_table_dict = get_weapon_table_dict(weapon_json_path, "")
    table_key = 'Weapon_Table'
    search_input_key = 'Search_Weapon'
    msg = '表示したい武器の行をダブルクリックすることで、更新画面が表示されます。' if to_update else 'この画面を閉じるまで、元の画面ではボタン操作は実行できません。'

    layout = [
        [sg.Text(msg)],
        [sg.Text('検索武器名'), sg.In(key=search_input_key, size=(max(35, weapon_table_dict["max_name_bytes"]), 1)), sg.Submit(button_text='再読み込み')],
        [
            sg.Table(
                key=table_key,
                values=weapon_table_dict["window_table_data_list"],
                headings=weapon_table_dict["header_list"],
                justification='left',
                auto_size_columns=False,
                col_widths=[max(20, weapon_table_dict["max_type_bytes"]), max(35, weapon_table_dict["max_name_bytes"])],
                num_rows=30,
                bind_return_key=to_update
            )
        ]
    ]

    window = sg.Window('武器一覧画面', layout)

    while True:
        event, values = window.read()
        if event is None:
            break
        elif event == 'Weapon_Table':
            click_weapon_info_dict = {index: value for index, value in enumerate(weapon_table_dict["window_table_data_list"][values[event][0]])}
            update.open(weapon_json_path, click_weapon_info_dict)
        elif event == '再読み込み':
            search_weapon_name = values[search_input_key]
            weapon_table_dict = get_weapon_table_dict(weapon_json_path, search_weapon_name)
            refresh(window, [table_key], weapon_table_dict)
    window.close()


def get_weapon_table_dict(weapon_json_path: str, search_weapon_name: str) -> dict:
    """武器情報をテーブル形式に変形させt返却する

    Args:
        weapon_json_path            : 武器情報格納パス
        search_weapon_name          : 検索武器名

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
        "window_table_data_list": [],
        "max_type_bytes": 0,
        "max_name_bytes": 0
    }
    # 全武器の情報を取得する
    for weapon_type_name, weapon_type_meta_name in meta.meta_weapon_type_dict.items():
        weapon_json_dict = handle_json.read(f"{weapon_json_path}/{weapon_type_meta_name}.json")
        return_weapon_table_dict["window_table_data_list"].extend([[weapon_type_name, weapon_name] for weapon_name in weapon_json_dict.keys() if search_weapon_name == "" or search_weapon_name in weapon_name])

    # 列幅が文字数でカウントされるために、日本語文字列では見えてほしい領域まで見えないため、最大Byte数を取得しておく。
    if return_weapon_table_dict["window_table_data_list"] != []:
        return_weapon_table_dict["max_type_bytes"] = max([len(weapon_table_datas[0].encode('utf-8')) for weapon_table_datas in return_weapon_table_dict["window_table_data_list"]])
        return_weapon_table_dict["max_name_bytes"] = max([len(weapon_table_datas[1].encode('utf-8')) for weapon_table_datas in return_weapon_table_dict["window_table_data_list"]])

    return return_weapon_table_dict


def refresh(window: sg.Window, input_values_keys: list, weapon_table_dict: dict):
    for values_key in input_values_keys:
        window[values_key].update(values=weapon_table_dict["window_table_data_list"])
