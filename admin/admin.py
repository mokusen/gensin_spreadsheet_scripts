from gui.weapon import (
    index,
    register,
    update
)
import PySimpleGUI as sg

# ボタンサイズ
B_SIZE = (15, 1)


def main(character_json_folder_path: str, relic_json_folder_path: str, weapon_json_folder_path: str):
    sg.theme('Dark Blue 3')

    layout = [
        [sg.Submit(button_text='キャラ効果登録', size=B_SIZE), sg.Submit(button_text='キャラ効果更新', size=B_SIZE)],
        [sg.Submit(button_text='聖遺物効果登録', size=B_SIZE), sg.Submit(button_text='聖遺物効果更新', size=B_SIZE)],
        [sg.Submit(button_text='武器効果登録', size=B_SIZE), sg.Submit(button_text='武器一覧', size=B_SIZE), sg.Submit(button_text='武器効果更新', size=B_SIZE)]
    ]

    window = sg.Window('メイン画面', layout)

    while True:
        event, values = window.read()

        if event is None:
            break

        if event == '武器効果登録':
            register.open(weapon_json_folder_path)
        elif event == '武器一覧':
            index.open(weapon_json_folder_path)
        elif event == '武器効果更新':
            update.open(weapon_json_folder_path)

    window.close()

if __name__ == "__main__":
    character_json_folder_path  = "../src/character"
    relic_json_folder_path      = "../src/relic"
    weapon_json_folder_path     = "../src/weapon"
    main(character_json_folder_path, relic_json_folder_path, weapon_json_folder_path)
