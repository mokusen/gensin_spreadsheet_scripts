from .. import (
    handle_json,
    meta
)
from ..win_print import win_print
from . import (
    common
)
from .settings import *
import PySimpleGUI as sg


def open(weapon_json_path: str, default_weapon_info_dict: dict = {}):
    """武器更新画面を表示する

    Args:
        weapon_json_path    : 武器情報格納パス
    """
    sg.theme('Dark Blue 3')

    # メタ名
    meta_tuple = tuple(meta.meta_name_dict.keys())
    weapon_type_tuple = tuple(meta.meta_weapon_type_dict.keys())
    weapon_name_list = []

    layout = []
    # 初期値が与えられている場合は、Layoutを変更する
    if default_weapon_info_dict == {}:
        layout = _normal_layout(meta_tuple, weapon_type_tuple, weapon_name_list)
    else:
        layout = _index_to_layout(meta_tuple, weapon_type_tuple, weapon_name_list, default_weapon_info_dict)

    # セクション 2 - ウィンドウの生成
    window = sg.Window('武器効果更新画面', layout, finalize=True)

    # 初期値が与えられている場合は、武器名検索も実行しておく
    if default_weapon_info_dict != {}:
        update_search_weapon_info_list(window, weapon_json_path, default_weapon_info_dict)

    while True:
        event, values = window.read()
        if event is None:
            break
        elif event == '武器検索':
            if values[0] == "":
                sg.popup("武器タイプは入力必須です")
            else:
                window[1].update('')
                window[1].update(values=update_search_weapon_name_list(weapon_json_path, values))
        elif event == '武器情報表示':
            if values[0] == "" or values[1] == "":
                sg.popup("武器タイプ、武器名は入力必須です")
            else:
                update_search_weapon_info_list(window, weapon_json_path, values)
        elif event == '連続更新（入力欄初期化）':
            win_print(values)
            if common.check_input_confirm(values[76], "更新処理を行います。\n更新後、入力欄は初期化されますがよろしいですか。", "更新チェック画面"):
                is_valid = weapon_update(weapon_json_path, values)
                if not is_valid:
                    common.input_area_all_clear(window, values.keys())
        elif event == '更新（入力欄初期化なし）':
            win_print(values)
            if common.check_input_confirm(values[76], "更新処理を行いますがよろしいですか。", "更新チェック画面"):
                weapon_update(weapon_json_path, values)
        elif event == '更新して終了（メイン画面へ戻る）':
            win_print(values)
            if common.check_input_confirm(values[76], "更新処理を行います。\n更新後、メイン画面へ戻りますがよろしいですか。", "更新チェック画面"):
                is_valid = weapon_update(weapon_json_path, values)
                if not is_valid:
                    break
    window.close()


def _normal_layout(meta_tuple: tuple, weapon_type_tuple: tuple, weapon_name_list: list):
    return [
        [sg.Text('更新対象検索', font='Any 15')],
        [sg.Text('武器タイプ', size=H_ONE_SIZE), sg.Drop(values=weapon_type_tuple, size=H_TWO_SIZE), sg.Submit(button_text='武器検索'), sg.Text('武器名', size=H_THREE_SIZE), sg.Drop(values=weapon_name_list, size=H_FOUR_SIZE), sg.Submit(button_text='武器情報表示')],
        [sg.Text('')],
        [sg.Text('更新対象情報', font='Any 15')],
        [sg.Text('武器タイプ', size=H_ONE_SIZE), sg.Drop(values=weapon_type_tuple, size=H_TWO_SIZE), sg.Text('武器名', size=H_THREE_SIZE), sg.In(size=H_FOUR_SIZE)],
        [sg.Text('#', size=T_ONE_SIZE), sg.Text('効果名称', size=T_TWO_SIZE), sg.Text('1', size=T_THREE_SIZE), sg.Text('2', size=T_FOUR_SIZE), sg.Text('3', size=T_FIVE_SIZE), sg.Text('4', size=T_SIX_SIZE), sg.Text('5', size=T_SEVEN_SIZE)],
        [sg.Text('通常系', size=T_ONE_SIZE), sg.Drop(values=meta_tuple, size=T_TWO_SIZE), sg.In(size=T_THREE_SIZE), sg.In(size=T_FOUR_SIZE), sg.In(size=T_FIVE_SIZE), sg.In(size=T_SIX_SIZE), sg.In(size=T_SEVEN_SIZE)],
        [sg.Text('', size=T_ONE_SIZE), sg.Drop(values=meta_tuple, size=T_TWO_SIZE), sg.In(size=T_THREE_SIZE), sg.In(size=T_FOUR_SIZE), sg.In(size=T_FIVE_SIZE), sg.In(size=T_SIX_SIZE), sg.In(size=T_SEVEN_SIZE)],
        [sg.Text('', size=T_ONE_SIZE), sg.Drop(values=meta_tuple, size=T_TWO_SIZE), sg.In(size=T_THREE_SIZE), sg.In(size=T_FOUR_SIZE), sg.In(size=T_FIVE_SIZE), sg.In(size=T_SIX_SIZE), sg.In(size=T_SEVEN_SIZE)],
        [sg.Text('重複系', size=T_ONE_SIZE), sg.Drop(values=meta_tuple, size=T_TWO_SIZE), sg.In(size=T_THREE_SIZE), sg.In(size=T_FOUR_SIZE), sg.In(size=T_FIVE_SIZE), sg.In(size=T_SIX_SIZE), sg.In(size=T_SEVEN_SIZE)],
        [sg.Text('', size=T_ONE_SIZE), sg.Drop(values=meta_tuple, size=T_TWO_SIZE), sg.In(size=T_THREE_SIZE), sg.In(size=T_FOUR_SIZE), sg.In(size=T_FIVE_SIZE), sg.In(size=T_SIX_SIZE), sg.In(size=T_SEVEN_SIZE)],
        [sg.Text('', size=T_ONE_SIZE), sg.Drop(values=meta_tuple, size=T_TWO_SIZE), sg.In(size=T_THREE_SIZE), sg.In(size=T_FOUR_SIZE), sg.In(size=T_FIVE_SIZE), sg.In(size=T_SIX_SIZE), sg.In(size=T_SEVEN_SIZE)],
        [sg.Text('特殊1', size=T_ONE_SIZE), sg.Drop(values=meta_tuple, size=T_TWO_SIZE), sg.In(size=T_THREE_SIZE), sg.In(size=T_FOUR_SIZE), sg.In(size=T_FIVE_SIZE), sg.In(size=T_SIX_SIZE), sg.In(size=T_SEVEN_SIZE)],
        [sg.Text('', size=T_ONE_SIZE), sg.Drop(values=meta_tuple, size=T_TWO_SIZE), sg.In(size=T_THREE_SIZE), sg.In(size=T_FOUR_SIZE), sg.In(size=T_FIVE_SIZE), sg.In(size=T_SIX_SIZE), sg.In(size=T_SEVEN_SIZE)],
        [sg.Text('', size=T_ONE_SIZE), sg.Drop(values=meta_tuple, size=T_TWO_SIZE), sg.In(size=T_THREE_SIZE), sg.In(size=T_FOUR_SIZE), sg.In(size=T_FIVE_SIZE), sg.In(size=T_SIX_SIZE), sg.In(size=T_SEVEN_SIZE)],
        [sg.Text('特殊2', size=T_ONE_SIZE), sg.Drop(values=meta_tuple, size=T_TWO_SIZE), sg.In(size=T_THREE_SIZE), sg.In(size=T_FOUR_SIZE), sg.In(size=T_FIVE_SIZE), sg.In(size=T_SIX_SIZE), sg.In(size=T_SEVEN_SIZE)],
        [sg.Text('', size=T_ONE_SIZE), sg.Drop(values=meta_tuple, size=T_TWO_SIZE), sg.In(size=T_THREE_SIZE), sg.In(size=T_FOUR_SIZE), sg.In(size=T_FIVE_SIZE), sg.In(size=T_SIX_SIZE), sg.In(size=T_SEVEN_SIZE)],
        [sg.Text('', size=T_ONE_SIZE), sg.Drop(values=meta_tuple, size=T_TWO_SIZE), sg.In(size=T_THREE_SIZE), sg.In(size=T_FOUR_SIZE), sg.In(size=T_FIVE_SIZE), sg.In(size=T_SIX_SIZE), sg.In(size=T_SEVEN_SIZE)],
        [sg.Checkbox('確認画面を表示する', default=True)],
        [sg.Submit(button_text='連続更新（入力欄初期化）'), sg.Submit(button_text='更新（入力欄初期化なし）'), sg.Submit(button_text='更新して終了（メイン画面へ戻る）')]
    ]


def _index_to_layout(meta_tuple: tuple, weapon_type_tuple: tuple, weapon_name_list: list, default_weapon_info_dict: dict):
    return [
        [sg.Text('更新対象検索', font='Any 15')],
        [
            sg.Text('武器タイプ', size=H_ONE_SIZE),
            sg.Drop(values=weapon_type_tuple, size=H_TWO_SIZE, default_value=default_weapon_info_dict[0]),
            sg.Submit(button_text='武器検索'),
            sg.Text('武器名', size=H_THREE_SIZE),
            sg.Drop(values=weapon_name_list, size=H_FOUR_SIZE, default_value=default_weapon_info_dict[1]),
            sg.Submit(button_text='武器情報表示')
        ],
        [sg.Text('')],
        [sg.Text('更新対象情報', font='Any 15')],
        [sg.Text('武器タイプ', size=H_ONE_SIZE), sg.Drop(values=weapon_type_tuple, size=H_TWO_SIZE), sg.Text('武器名', size=H_THREE_SIZE), sg.In(size=H_FOUR_SIZE)],
        [sg.Text('#', size=T_ONE_SIZE), sg.Text('効果名称', size=T_TWO_SIZE), sg.Text('1', size=T_THREE_SIZE), sg.Text('2', size=T_FOUR_SIZE), sg.Text('3', size=T_FIVE_SIZE), sg.Text('4', size=T_SIX_SIZE), sg.Text('5', size=T_SEVEN_SIZE)],
        [sg.Text('通常系', size=T_ONE_SIZE), sg.Drop(values=meta_tuple, size=T_TWO_SIZE), sg.In(size=T_THREE_SIZE), sg.In(size=T_FOUR_SIZE), sg.In(size=T_FIVE_SIZE), sg.In(size=T_SIX_SIZE), sg.In(size=T_SEVEN_SIZE)],
        [sg.Text('', size=T_ONE_SIZE), sg.Drop(values=meta_tuple, size=T_TWO_SIZE), sg.In(size=T_THREE_SIZE), sg.In(size=T_FOUR_SIZE), sg.In(size=T_FIVE_SIZE), sg.In(size=T_SIX_SIZE), sg.In(size=T_SEVEN_SIZE)],
        [sg.Text('', size=T_ONE_SIZE), sg.Drop(values=meta_tuple, size=T_TWO_SIZE), sg.In(size=T_THREE_SIZE), sg.In(size=T_FOUR_SIZE), sg.In(size=T_FIVE_SIZE), sg.In(size=T_SIX_SIZE), sg.In(size=T_SEVEN_SIZE)],
        [sg.Text('重複系', size=T_ONE_SIZE), sg.Drop(values=meta_tuple, size=T_TWO_SIZE), sg.In(size=T_THREE_SIZE), sg.In(size=T_FOUR_SIZE), sg.In(size=T_FIVE_SIZE), sg.In(size=T_SIX_SIZE), sg.In(size=T_SEVEN_SIZE)],
        [sg.Text('', size=T_ONE_SIZE), sg.Drop(values=meta_tuple, size=T_TWO_SIZE), sg.In(size=T_THREE_SIZE), sg.In(size=T_FOUR_SIZE), sg.In(size=T_FIVE_SIZE), sg.In(size=T_SIX_SIZE), sg.In(size=T_SEVEN_SIZE)],
        [sg.Text('', size=T_ONE_SIZE), sg.Drop(values=meta_tuple, size=T_TWO_SIZE), sg.In(size=T_THREE_SIZE), sg.In(size=T_FOUR_SIZE), sg.In(size=T_FIVE_SIZE), sg.In(size=T_SIX_SIZE), sg.In(size=T_SEVEN_SIZE)],
        [sg.Text('特殊1', size=T_ONE_SIZE), sg.Drop(values=meta_tuple, size=T_TWO_SIZE), sg.In(size=T_THREE_SIZE), sg.In(size=T_FOUR_SIZE), sg.In(size=T_FIVE_SIZE), sg.In(size=T_SIX_SIZE), sg.In(size=T_SEVEN_SIZE)],
        [sg.Text('', size=T_ONE_SIZE), sg.Drop(values=meta_tuple, size=T_TWO_SIZE), sg.In(size=T_THREE_SIZE), sg.In(size=T_FOUR_SIZE), sg.In(size=T_FIVE_SIZE), sg.In(size=T_SIX_SIZE), sg.In(size=T_SEVEN_SIZE)],
        [sg.Text('', size=T_ONE_SIZE), sg.Drop(values=meta_tuple, size=T_TWO_SIZE), sg.In(size=T_THREE_SIZE), sg.In(size=T_FOUR_SIZE), sg.In(size=T_FIVE_SIZE), sg.In(size=T_SIX_SIZE), sg.In(size=T_SEVEN_SIZE)],
        [sg.Text('特殊2', size=T_ONE_SIZE), sg.Drop(values=meta_tuple, size=T_TWO_SIZE), sg.In(size=T_THREE_SIZE), sg.In(size=T_FOUR_SIZE), sg.In(size=T_FIVE_SIZE), sg.In(size=T_SIX_SIZE), sg.In(size=T_SEVEN_SIZE)],
        [sg.Text('', size=T_ONE_SIZE), sg.Drop(values=meta_tuple, size=T_TWO_SIZE), sg.In(size=T_THREE_SIZE), sg.In(size=T_FOUR_SIZE), sg.In(size=T_FIVE_SIZE), sg.In(size=T_SIX_SIZE), sg.In(size=T_SEVEN_SIZE)],
        [sg.Text('', size=T_ONE_SIZE), sg.Drop(values=meta_tuple, size=T_TWO_SIZE), sg.In(size=T_THREE_SIZE), sg.In(size=T_FOUR_SIZE), sg.In(size=T_FIVE_SIZE), sg.In(size=T_SIX_SIZE), sg.In(size=T_SEVEN_SIZE)],
        [sg.Checkbox('確認画面を表示する', default=True)],
        [sg.Submit(button_text='連続更新（入力欄初期化）'), sg.Submit(button_text='更新（入力欄初期化なし）'), sg.Submit(button_text='更新して終了（メイン画面へ戻る）')]
    ]


def update_search_weapon_name_list(weapon_json_path: str, input_values: dict) -> list:
    """武器タイプから、武器名リストを作成し返却する

    Args:
        weapon_json_path    : 武器情報格納パス
        input_values        : 画面から取得したValues情報

    Returns:
        weapon_name_list    : 武器名リスト
    """
    # 武器情報取得
    weapon_type_meta_name = meta.meta_weapon_type_dict[input_values[0]]

    # 武器Jsonを取得する
    weapon_file_path = f"{weapon_json_path}/{weapon_type_meta_name}.json"
    weapon_json_dict = handle_json.read(weapon_file_path)
    weapon_name_list = list(weapon_json_dict.keys())
    return weapon_name_list


def update_search_weapon_info_list(window: sg.Window, weapon_json_path: str, input_values: dict):
    """武器タイプと、武器名から武器情報を取得し返却する

    Args:
        weapon_json_path    : 武器情報格納パス
        input_values        : 画面から取得したValues情報

    Returns:
        weapon_json_dict    : 武器情報
    """
    # 武器情報取得
    weapon_type_meta_name = meta.meta_weapon_type_dict[input_values[0]]

    # 武器Jsonを取得する
    weapon_file_path = f"{weapon_json_path}/{weapon_type_meta_name}.json"
    weapon_json_dict = handle_json.read(weapon_file_path)
    if input_values[1] in weapon_json_dict.keys():
        # ここで出力エリアを初期化しておく
        common.input_area_all_clear(window, list(input_values.keys())[2:-1])

        # 取得した武器情報で更新作業を行う
        update_window_weapon_info(window, input_values[0], input_values[1], weapon_json_dict[input_values[1]])
    else:
        sg.popup("選択された武器名は存在しませんでした。\n再度武器タイプを検索実行し、武器名のドロップボックスより選択してください。", title="武器名チェックのお願い")


def update_window_weapon_info(window: sg.Window, weapon_type_meta_name: str, weapon_name: str, weapon_json_dict: dict):
    """武器情報から、出力エリアに順次出力する

    Args:
        window                  : PySimpleGui.Window
        weapon_type_meta_name   : 武器メタ名
        weapon_name             : 武器名
        weapon_json_dict        : 1武器のJSONデータ
    """
    # window[2]から武器タイプ指定
    window[2].update(weapon_type_meta_name)
    window[3].update(weapon_name)

    # 武器凸効果順に取得する（1 -> 5）
    for weapon_convex_index, weapon_convex_item in enumerate(weapon_json_dict.values()):
        # 武器効果系を取得する（normal, duplicate, special_1, special_2）
        for weapon_effect_type, weapon_effect_item in weapon_convex_item.items():
            _update_window_weapon_info(window, weapon_effect_item, weapon_effect_type, weapon_convex_index)


def _update_window_weapon_info(window: sg.Window, weapon_effect_item: dict, weapon_effect_type: str, weapon_convex_index: int):
    """武器情報から、精錬ランクに応じたエリアに対して情報出力する

    Args:
        window              : PySimpleGui.Window
        weapon_effect_item  : 武器効果のアイテム（辞書）
        weapon_effect_type  : 武器効果タイプ（通常など）
        weapon_convex_index : 武器精錬ランク（0-4表記）
    """
    # 初期変数
    effect_start_value_dict = {
        "normal": 4,
        "duplicate": 22,
        "special_1": 40,
        "special_2": 58
    }
    effect_start_value = effect_start_value_dict[weapon_effect_type]
    # 0 ~ 4表記を1 ~ 5表記に変換する
    weapon_convex_index += 1

    # 1効果系に含まれる効果名を取り出す
    i = 0
    for weapon_effect_name, weapon_effect_value in weapon_effect_item.items():
        use_effect_index_value = effect_start_value + i + 5 * i
        if weapon_convex_index == 1:
            window[use_effect_index_value].update(meta.meta_name_reverse_dict[weapon_effect_name])
        window[use_effect_index_value + weapon_convex_index].update(weapon_effect_value)
        i += 1


def weapon_update(weapon_json_path: str, input_values: dict) -> bool:
    # 旧データを破棄して更新する
    old_weapon_file_path = f"{weapon_json_path}/{meta.meta_weapon_type_dict[input_values[0]]}.json"
    old_weapon_json_dict = handle_json.read(old_weapon_file_path)
    old_weapon_json_dict.pop(input_values[1], None)
    handle_json.write(old_weapon_file_path, old_weapon_json_dict)

    # 現データを登録する
    is_valid = common.weapon_register(weapon_json_path, input_values, start_diff_value=2)
    return is_valid
