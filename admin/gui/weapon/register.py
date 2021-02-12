from .. import (
    meta
)

from . import (
    common,
    index
)
from .settings import *
import PySimpleGUI as sg


def open(weapon_json_path: str):
    """武器登録画面を表示する

    Args:
        weapon_json_path    : 武器情報格納パス
    """
    sg.theme('Dark Blue 3')

    # メタ名
    meta_tuple = tuple(meta.meta_name_dict.keys())
    weapon_type_tuple = tuple(meta.meta_weapon_type_dict.keys())

    layout = [
        [sg.Text('武器タイプ', size=H_ONE_SIZE), sg.Drop(values=weapon_type_tuple, size=H_TWO_SIZE), sg.Text('武器名', size=H_THREE_SIZE), sg.In(size=H_FOUR_SIZE), sg.Text('', size=H_FIVE_SIZE), sg.Submit(button_text='武器一覧表示', size=H_SIX_SIZE)],
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
        [sg.Checkbox('確認画面を表示する', default=False)],
        [sg.Submit(button_text='連続登録（入力欄初期化）'), sg.Submit(button_text='登録（入力欄初期化なし）'), sg.Submit(button_text='登録して終了（メイン画面へ戻る）')]
    ]

    # セクション 2 - ウィンドウの生成
    window = sg.Window('武器効果登録画面', layout)

    while True:
        event, values = window.read()
        if event is None:
            break
        elif event == '武器一覧表示':
            index.open(weapon_json_path, False)
        elif event == '連続登録（入力欄初期化）':
            print(values, flush=True)
            if common.check_input_confirm(values[74], "登録処理を行います。\n登録後、入力欄は初期化されますがよろしいですか。", "登録チェック画面"):
                is_valid = common.weapon_register(weapon_json_path, values)
                if not is_valid:
                    common.input_area_all_clear(window, values.keys())
        elif event == '登録（入力欄初期化なし）':
            print(values, flush=True)
            if common.check_input_confirm(values[74], "登録処理を行いますがよろしいですか。", "登録チェック画面"):
                common.weapon_register(weapon_json_path, values)
        elif event == '登録して終了（メイン画面へ戻る）':
            print(values, flush=True)
            if common.check_input_confirm(values[74], "登録処理を行います。\n登録後、メイン画面へ戻りますがよろしいですか。", "登録チェック画面"):
                is_valid = common.weapon_register(weapon_json_path, values)
                if not is_valid:
                    break
    window.close()
