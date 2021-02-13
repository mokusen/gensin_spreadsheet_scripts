from .. import (
    handle_json,
    meta
)
import PySimpleGUI as sg


def weapon_register(weapon_json_path: str, input_values: dict, start_diff_value: int = 0) -> bool:
    """入力された武器情報を、.jsonの武器ファイルに登録する

    Args:
        weapon_json_path    : 武器JSONフォルダパス
        input_values        : 入力エリアデータ
        start_diff_value    : 入力エリア開始差分値

    Returns:
        is_valid            : 入力不正判定結果
    """
    # 初期変数
    update_weapon_dict = {}
    range_dict = {
        "normal": [2, 8, 14],
        "duplicate": [20, 26, 32],
        "special_1": [38, 44, 50],
        "special_2": [56, 62, 68]
    }
    is_valid = False

    # 差分値反映
    for key in range_dict:
        range_dict[key] = [value + start_diff_value for value in range_dict[key]]
    weapon_type_index = 0 + start_diff_value
    weapon_name_index = 1 + start_diff_value

    # 武器タイプ名が入力されているときだけ処理を行う
    if input_values[weapon_type_index] == "" or input_values[weapon_name_index] == "":
        sg.popup("武器タイプ、武器名は入力必須です")
    else:
        # 武器情報取得
        weapon_type_meta_name = meta.meta_weapon_type_dict[input_values[weapon_type_index]]
        weapon_name = input_values[weapon_name_index]
        update_weapon_dict[weapon_name] = {}

        # 武器Jsonを取得する
        weapon_file_path = f"{weapon_json_path}/{weapon_type_meta_name}.json"
        weapon_json_dict = handle_json.read(weapon_file_path)

        # 取得データを更新辞書に登録する
        for range_key, range_list in range_dict.items():
            # 入力エリアの3行分登録する
            for effect_index in range_list:
                # 効果タイプが入力されているときだけ処理を行う
                if input_values[effect_index] != "":
                    # 効果タイプメタ名
                    weapon_effect_meta_name = meta.meta_name_dict[input_values[effect_index]]

                    # 範囲リストを処理する
                    for weapon_dict_index in range(1, 6):
                        input_value = input_values[effect_index + weapon_dict_index]
                        # 数値が入力されているなら処理を行う
                        if input_value != "":
                            update_weapon_dict[weapon_name] = _update_dict(update_weapon_dict[weapon_name], weapon_dict_index, range_key, weapon_effect_meta_name, input_value)

        # 更新した結果、何も効果が入力されていない場合は、ポップアップを出す
        if update_weapon_dict[weapon_name] == {}:
            sg.popup("効果を入力してください。")
            is_valid = True
        else:
            update_weapon_json_dict(weapon_file_path, weapon_json_dict, update_weapon_dict)
    return is_valid


def _update_dict(update_weapon_name_dict: dict, w_index: int, w_type: str, w_effect: str, w_value: str) -> dict:
    """入力されたデータを、武器JSONデータ形式に合うように変形し、返却する

    Args:
        update_weapon_name_dict : 武器JSON更新データ
        w_index                 : 武器精錬ランク
        w_type                  : 武器タイプ
        w_effect                : 武器効果
        w_value                 : 武器効果値

    Returns:
        update_weapon_name_dict : 武器JSON更新データ
    """
    # インデックスの存在確認を行い、存在しない場合は初期設定を行う
    if w_index not in update_weapon_name_dict:
        update_weapon_name_dict[w_index] = {"normal": {}, "duplicate": {}, "special_1": {}, "special_2": {}}

    update_weapon_name_dict[w_index][w_type][w_effect] = float(w_value)
    return update_weapon_name_dict


def update_weapon_json_dict(weapon_file_path: str, weapon_json_dict: dict, update_weapon_dict: dict):
    """武器JSONデータを更新し、.jsonファイルを更新する

    Args:
        weapon_file_path    : 武器ファイルパス
        weapon_json_dict    : 武器JSONデータ
        update_weapon_dict  : 武器JSON更新データ
    """
    weapon_json_dict.update(update_weapon_dict)
    handle_json.write(weapon_file_path, weapon_json_dict)


def input_area_all_clear(window: sg.Window, values_key_list: list):
    """指定されたエリアを初期化する

    Args:
        window          : PySimpleGui.Window
        values_key_list : 初期化したいエリアインデックスリスト
    """
    for index in values_key_list:
        window[index].update('')


def check_input_confirm(check_flg: bool, msg: str, title: str) -> bool:
    """入力チェック後の登録実行画面のテンプレート

    Args:
        check_flg   : 入力チェックフラグ
        msg         : 登録画面に出力する文字列
        title       : タイトル

    Returns:
        return_flg  : 登録に同意したかの判定フラグ
    """
    return_flg = True
    if check_flg:
        return_flg = False if sg.popup_ok_cancel(msg, title=title) == "Cancel" else True
    return return_flg
