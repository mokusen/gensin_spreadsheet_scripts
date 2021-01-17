// @ts-nocheck
function base() {
  // スプレッドシート、シート取得
  let spreadsheet = SpreadsheetApp.getActiveSpreadsheet();
  let input_sheet = spreadsheet.getSheetByName("入力エリア_詳細");
  let meta_sheet = spreadsheet.getSheetByName("メタデータ");

  // メタ情報を取得する
  let meta_last_row = meta_sheet.getRange(1, 1).getNextDataCell(SpreadsheetApp.Direction.DOWN).getRow() - 1;
  let meta_data_list = meta_sheet.getRange(2, 1, meta_last_row, 2).getValues();
  let meta_data_dict = {};
  for (let meta_list of meta_data_list) {
    meta_data_dict[meta_list[0]] = meta_list[1];
  }

  // 入力値から変数を取得する
  let character_name = input_sheet.getRange(2, 2).getValue();
  let character_lv = input_sheet.getRange(2, 3).getValue();
  let character_convex = input_sheet.getRange(2, 4).getValue();
  let weapon_name = input_sheet.getRange(3, 2).getValue();
  let weapon_lv = input_sheet.getRange(3, 3).getValue();
  let weapon_convex = input_sheet.getRange(3, 4).getValue();
  let natural_gift_normal_lv = input_sheet.getRange(6, 2).getValue();
  let natural_gift_skill_lv = input_sheet.getRange(7, 2).getValue();
  let natural_gift_explosion_lv = input_sheet.getRange(8, 2).getValue();

  // 聖遺物情報を取得し、辞書化して返却する
  let relic_data_dict = get_relic_data_dict(input_sheet, meta_data_dict);

  // キャラ性能から変数を取得する
  add_character_parameter(spreadsheet, meta_data_dict, character_name, character_lv);

  // 武器性能から変数を更新する
  add_weapon_parameter(spreadsheet, meta_data_dict, weapon_name, weapon_lv);

  // 聖遺物,セット効果のセット効果を反映する
  let parameter_dict_result = add_relic_parameter(spreadsheet, meta_data_dict, relic_data_dict);

  // 結果ステータスを出力する
  output(spreadsheet, parameter_dict_result);
}

/**
 * 聖遺物データを取得し、辞書化して返却する
 */
function get_relic_data_dict(input_sheet, meta_data_dict) {
  // TODO: 場合によっては規定数5より多くすることを検討する
  let relic_loop_max = 5;
  let relic_item_max = 5;
  let relic_option_max = 5;
  let relic_data_dict = {};

  // 比較対象5つのデータを取り出す
  for (let relic_loop_index = 0; relic_loop_index < relic_loop_max; relic_loop_index++) {
    relic_data_dict[relic_loop_index] = {};
    // 1つの比較対象データを取り出す
    for (let relic_item_index = 0; relic_item_index < relic_item_max; relic_item_index++) {
      // 聖遺物のセット効果を辞書に加算する
      relic_set_effect = meta_data_dict[input_sheet.getRange(11 + 13 * relic_loop_index, 3 + relic_item_index).getValue()];
      if (relic_data_dict[relic_loop_index][relic_set_effect]) {
        relic_data_dict[relic_loop_index][relic_set_effect] += 1;
      } else {
        relic_data_dict[relic_loop_index][relic_set_effect] = 1;
      }
      // 聖遺物1つのオプション情報を取りだし、辞書に加算する
      for (let relic_option_index = 0; relic_option_index < relic_option_max; relic_option_index++) {
        // インデックスエリア
        add_index = 13 * relic_loop_index + 2 * relic_option_index;
        item_type_name = meta_data_dict[input_sheet.getRange(12 + add_index, 3 + relic_item_index).getValue()];
        if (relic_data_dict[relic_loop_index][item_type_name]) {
          relic_data_dict[relic_loop_index][item_type_name] += parseFloat(input_sheet.getRange(13 + add_index, 3 + relic_item_index).getValue());
        } else {
          relic_data_dict[relic_loop_index][item_type_name] = parseFloat(input_sheet.getRange(13 + add_index, 3 + relic_item_index).getValue());
        }
      }
    }
  }
  return relic_data_dict;
}

/**
 * キャラ性能から変数を取得する
 */
function add_character_parameter(spreadsheet, meta_data_dict, character_name, character_lv) {
  // キャラクターのスプレッドシートを指定して取り出す
  let character_sheet = spreadsheet.getSheetByName(character_name);
  // 最終行を取り出す
  let character_last_column = character_sheet.getRange(1, 1).getNextDataCell(SpreadsheetApp.Direction.NEXT).getColumn();
  let character_data_header = character_sheet.getRange(1, 1, 1, character_last_column).getValues()[0];
  let character_data_lists = character_sheet.getRange(2, 1, 8, character_last_column).getValues();

  // データリストからキャラレベルと一致する行データを取り出す
  for (let character_data_list of character_data_lists) {
    if (character_lv === character_data_list[0]) {
      // 取り出した行データからパラメータ辞書に代入する
      for (let i = 1; i < character_data_list.length; i++) {
        let param_key = meta_data_dict[character_data_header[i]];
        // 文字列の場合、0に置換する
        let add_data_value = 0;
        if (character_data_list[i] !== "") {
          add_data_value = parseFloat(character_data_list[i]);
        }
        // キャラ情報からパラメータを取り出す
        if (param_key.indexOf("percent") !== -1) {
          parameter_dict[param_key] += add_data_value / 100;
        } else {
          parameter_dict[param_key] += add_data_value;
        }
      }
      break;
    }
  }
}

/**
 * 武器性能から変数を更新する
 */
function add_weapon_parameter(spreadsheet, meta_data_dict, weapon_name, weapon_lv) {
  // 武器のスプレッドシートを指定して取り出す
  let weapon_sheet = spreadsheet.getSheetByName("武器");
  let weapon_data_header = weapon_sheet.getRange(1, 1, 1, weapon_sheet.getLastColumn()).getValues()[0];
  let weapon_data_lists = weapon_sheet.getRange(2, 1, weapon_sheet.getLastRow(), weapon_sheet.getLastColumn()).getValues();

  // データリストから武器名と一致、かつ武器レベルが一致する行データを取り出す
  for (let weapon_data_list of weapon_data_lists) {
    if (weapon_name === weapon_data_list[0] && weapon_lv === weapon_data_list[1]) {
      // 取り出した行データからパラメータ辞書に追記する
      for (let i = 2; i < weapon_data_list.length; i++) {
        let param_key = meta_data_dict[weapon_data_header[i]];
        // 文字列の場合、0に置換する
        let add_data_value = 0;
        if (weapon_data_list[i] !== "") {
          add_data_value = parseFloat(weapon_data_list[i]);
        }
        // キャラ情報からパラメータを取り出す
        if (param_key.indexOf("percent") !== -1) {
          parameter_dict[param_key] += add_data_value / 100;
        } else {
          parameter_dict[param_key] += add_data_value;
        }
      }
      break;
    }
  }
}

/**
 * 聖遺物性能、セット効果から変数を更新する
 */
function add_relic_parameter(spreadsheet, meta_data_dict, relic_data_dict) {
  let parameter_dict_result = {};
  let relic_sheet = spreadsheet.getSheetByName("聖遺物");
  // 聖遺物シートに含まれる全データ
  let relic_data_lists = relic_sheet.getRange(1, 1, relic_sheet.getLastRow(), relic_sheet.getLastColumn()).getValues();
  // 聖遺物シートのヘッダー情報
  let rellc_data_header = relic_data_lists[0];
  // 聖遺物シートの最終行
  let relic_last_row = relic_sheet.getRange(1, 1).getNextDataCell(SpreadsheetApp.Direction.DOWN).getRow() - 1;

  // 比較対象5つのデータごとにステータスを求め、算出する
  for (let relic_item_index = 0; relic_item_index < Object.keys(relic_data_dict).length; relic_item_index++) {
    // 既存ステータス情報をディープコピーし、辞書に登録する
    parameter_dict_result[relic_item_index] = Object.assign({}, parameter_dict);
    // 聖遺物1つのオプション情報を取り出し、ステータスに加算する
    for (let item_type_name of Object.keys(relic_data_dict[relic_item_index])) {
      // セット効果ではないものを処理する
      if (item_type_name.indexOf("set_") === -1) {
        // 文字列の場合、0に置換する
        let add_data_value = 0;
        if (relic_data_dict[relic_item_index][item_type_name] !== "") {
          add_data_value = parseFloat(relic_data_dict[relic_item_index][item_type_name]);
        }
        if (item_type_name.indexOf("percent") !== -1) {
          parameter_dict_result[relic_item_index][item_type_name] += add_data_value / 100;
        } else {
          parameter_dict_result[relic_item_index][item_type_name] += add_data_value;
        }
      } else {
        // 聖遺物のセット効果（特殊条件以外）を反映させる
        relic_set_count = parseFloat(relic_data_dict[relic_item_index][item_type_name]);
        // 聖遺物個数が2、4のときだけ判定するため、2で割り、除算する
        use_relic_set_count = relic_set_count - (relic_set_count % 2);
        if (use_relic_set_count >= 2) {
          // 対象聖遺物セット効果と凸状態が一致する行データを特定する
          for (let i = 1; i < relic_last_row; i++) {
            if (item_type_name === meta_data_dict[relic_data_lists[i][0]] && use_relic_set_count === relic_data_lists[i][1]) {
              // 一致した場合、そのデータをステータス辞書に加算する
              for (let k = 3; k < relic_data_lists[i].length; k++) {
                set_effect_key = meta_data_dict[rellc_data_header[k]];
                // 文字列の場合、0に置換する
                let add_data_value = 0;
                if (relic_data_lists[i][k] !== "") {
                  add_data_value = parseFloat(relic_data_lists[i][k]);
                }
                // キャラ情報からパラメータを取り出す
                if (set_effect_key.indexOf("percent") !== -1) {
                  parameter_dict_result[relic_item_index][set_effect_key] += add_data_value / 100;
                } else {
                  parameter_dict_result[relic_item_index][set_effect_key] += add_data_value;
                }
              }
              break
            }
          }
        }
      }
    }
  }
  return parameter_dict_result;
}

/**
 * 計算結果の基本ステータスを出力する
 */
function output(spreadsheet, parameter_dict_result) {
  let output_sheet = spreadsheet.getSheetByName("出力エリア");
  for (let parameter_index = 0; parameter_index < Object.keys(parameter_dict_result).length; parameter_index++) {
    let p_d = parameter_dict_result[parameter_index];
    console.log(p_d);
    output_sheet.getRange(1, 2 + parameter_index).setValue(`比較パターン${parameter_index + 1}`);
    output_sheet.getRange(2, 2 + parameter_index).setValue(Math.round(p_d["hp_upper_limit"] * (1 + p_d["hp_percent"]) + p_d["hp_fixed_value"]));
    output_sheet.getRange(3, 2 + parameter_index).setValue(Math.round(p_d["offensive_power"] * (1 + p_d["offensive_power_percent"]) + p_d["offensive_power_fixed_value"]));
    output_sheet.getRange(4, 2 + parameter_index).setValue(Math.round(p_d["defense_power"] * (1 + p_d["defense_power_percent"]) + p_d["defense_power_fixed_value"]));
    output_sheet.getRange(5, 2 + parameter_index).setValue(p_d["failiarity_with_elements"]);
    output_sheet.getRange(6, 2 + parameter_index).setValue(p_d["critical_percent"]);
    output_sheet.getRange(7, 2 + parameter_index).setValue(p_d["critical_damage_percent"]);
    output_sheet.getRange(8, 2 + parameter_index).setValue(p_d["element_charge_efficiency_percent"]);
    output_sheet.getRange(9, 2 + parameter_index).setValue(p_d["cool_time_reduction"]);
    output_sheet.getRange(10, 2 + parameter_index).setValue(p_d["shield_strengthening"]);
    output_sheet.getRange(11, 2 + parameter_index).setValue(p_d["flame_element_damage_percent"]);
    output_sheet.getRange(12, 2 + parameter_index).setValue(p_d["water_element_damage_percent"]);
    output_sheet.getRange(13, 2 + parameter_index).setValue(p_d["grass_element_damage_percent"]);
    output_sheet.getRange(14, 2 + parameter_index).setValue(p_d["lightning_element_damage_percent"]);
    output_sheet.getRange(15, 2 + parameter_index).setValue(p_d["wind_element_damage_percent"]);
    output_sheet.getRange(16, 2 + parameter_index).setValue(p_d["ice_element_damage_percent"]);
    output_sheet.getRange(17, 2 + parameter_index).setValue(p_d["rock_element_damage_percent"]);
    output_sheet.getRange(18, 2 + parameter_index).setValue(p_d["physical_damage_percent"]);
  }
}
