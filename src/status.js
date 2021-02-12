// @ts-nocheck
/**
 * 比較対象データ1用
 */
function cal_comparison_one() {
  cal_status(0);
}

/**
 * 比較対象データ2用
 */
function cal_comparison_two() {
  cal_status(1);
}

/**
 * 比較対象データ3用
 */
function cal_comparison_three() {
  cal_status(2);
}

/**
 * 比較対象データ4用
 */
function cal_comparison_four() {
  cal_status(3);
}

/**
 * 比較対象データ5用
 */
function cal_comparison_five() {
  cal_status(4);
}

/**
 * ステータス情報を計算し、出力する
 */
function cal_status(comparison_index) {
  // スプレッドシート、シート取得
  let spreadsheet = SpreadsheetApp.getActiveSpreadsheet();
  let status_sheet = spreadsheet.getSheetByName("ステータス計算エリア");
  let meta_sheet = spreadsheet.getSheetByName("メタデータ");
  let weapon_sheet = spreadsheet.getSheetByName("武器_両手剣");
  let relic_sheet = spreadsheet.getSheetByName("聖遺物");
  let input_sheet = spreadsheet.getSheetByName("入力エリア");

  // メタ情報を取得する
  get_meta_data(meta_sheet);

  // 初期変数
  let base_increase_index = 18 * comparison_index;
  let base_row = 3 + base_increase_index;
  let base_column = 2;

  // キャラクター情報
  get_character_input_data(spreadsheet, status_sheet, base_row, base_column);

  // 武器情報
  get_weapon_input_data(weapon_sheet, status_sheet, base_row, base_column);

  // 聖遺物情報
  get_relic_input_data(status_sheet, base_increase_index);

  // 聖遺物セット効果
  get_relic_set_effect(relic_sheet);

  // ステータス情報を出力する
  output_status(input_sheet, comparison_index);
  console.log(calculation_data_dict);
}

/**
 * メタ情報を取得する
 */
function get_meta_data(meta_sheet) {
  // ステータスオプションのメタ情報を取得する
  let meta_option_last_row = meta_sheet.getRange(1, 1).getNextDataCell(SpreadsheetApp.Direction.DOWN).getRow() - 1;
  let meta_option_data_list = meta_sheet.getRange(2, 1, meta_option_last_row, 2).getValues();
  for (let meta_option_list of meta_option_data_list) {
    meta_data_dict["option"][meta_option_list[0]] = meta_option_list[1];
  }

  // 聖遺物のメタ情報を取得する
  let meta_relic_last_row = meta_sheet.getRange(1, 3).getNextDataCell(SpreadsheetApp.Direction.DOWN).getRow() - 1;
  let meta_relic_data_list = meta_sheet.getRange(2, 3, meta_relic_last_row, 2).getValues();
  for (let meta_relic_list of meta_relic_data_list) {
    meta_data_dict["relic"][meta_relic_list[0]] = meta_relic_list[1];
  }
}

/**
 * キャラクター情報を取得する
 */
function get_character_input_data(spreadsheet, status_sheet, base_row, base_column) {
  // キャラクター情報の入力データを取得する
  calculation_data_dict["character"]["name"] = status_sheet.getRange(base_row, base_column).getValue();
  calculation_data_dict["character"]["lv"] = status_sheet.getRange(base_row, base_column + 2).getValue();
  calculation_data_dict["character"]["convex"] = status_sheet.getRange(base_row, base_column + 3).getValue();

  // キャラクターのスプレッドシートを指定して取り出す
  let character_sheet = spreadsheet.getSheetByName(calculation_data_dict["character"]["name"]);

  // 初期変数
  let character_last_column = character_sheet.getRange(1, 1).getNextDataCell(SpreadsheetApp.Direction.NEXT).getColumn();
  let character_data_header = character_sheet.getRange(1, 1, 1, character_last_column).getValues()[0];
  let character_data_lists = character_sheet.getRange(2, 1, 8, character_last_column).getValues();
  let character_average_start_index = 0;
  let character_average_index_list = [0, 1, 2, 3];
  let character_dh_start_index = 1;

  // 完全一致するレベルが存在しない場合は、下限と上限値を取得する
  for (let cdl = 0; cdl < character_data_lists.length; cdl++) {
    if (calculation_data_dict["character"]["lv"] === character_data_lists[cdl][0]) {
      _add_status_data(character_data_header, character_data_lists[cdl], character_dh_start_index);
      break;
    } else if (character_data_lists[cdl][0] !== 90) {
      // 90のときはNextが存在しないため、イコールチェックしかしない
      if (character_data_lists[cdl][0] < calculation_data_dict["character"]["lv"] && calculation_data_dict["character"]["lv"] < character_data_lists[cdl + 1][0]) {
        _add_status_data(
          character_data_header,
          create_average_status_dict(
            calculation_data_dict["character"]["lv"],
            character_data_lists[cdl],
            character_data_lists[cdl + 1],
            character_average_start_index,
            character_average_index_list
          ),
          character_dh_start_index
        );
        break;
      }
    }
  }
}

/**
 * 武器情報を取得する
 */
function get_weapon_input_data(weapon_sheet, status_sheet, base_row, base_column) {
  // 武器情報の入力データを取得する
  calculation_data_dict["weapon"]["name"] = status_sheet.getRange(base_row + 1, base_column).getValue();
  calculation_data_dict["weapon"]["lv"] = status_sheet.getRange(base_row + 1, base_column + 2).getValue();
  calculation_data_dict["weapon"]["convex"] = status_sheet.getRange(base_row + 1, base_column + 3).getValue();

  // 初期変数
  let weapon_last_column = weapon_sheet.getRange(1, 1).getNextDataCell(SpreadsheetApp.Direction.NEXT).getColumn();
  let weapon_data_header = weapon_sheet.getRange(1, 1, 1, weapon_last_column).getValues()[0];
  let weapon_data_lists = weapon_sheet.getRange(2, 1, weapon_sheet.getLastRow(), weapon_last_column).getValues();
  let weapon_average_start_index = 2;
  let weapon_average_index_list = [2, 3];
  let weapon_dh_start_index = 2;

  // 完全一致するレベルが存在しない場合は、下限と上限値を取得する
  for (let wdl = 0; wdl < weapon_data_lists.length; wdl++) {
    // 90のときはNextが存在しないため、イコールチェックしかしない
    if (calculation_data_dict["weapon"]["lv"] === weapon_data_lists[wdl][1]) {
      _add_status_data(weapon_data_header, weapon_data_lists[wdl], weapon_dh_start_index);
      break;
    } else if (calculation_data_dict["weapon"]["lv"] !== 90) {
      if (weapon_data_lists[wdl][1] < calculation_data_dict["weapon"]["lv"] && calculation_data_dict["weapon"]["lv"] < weapon_data_lists[wdl + 1][1]) {
        _add_status_data(
          weapon_data_header,
          create_average_status_dict(
            calculation_data_dict["weapon"]["lv"],
            weapon_data_lists[wdl],
            weapon_data_lists[wdl + 1],
            weapon_average_start_index,
            weapon_average_index_list
          ),
          weapon_dh_start_index
        );
        break;
      }
    }
  }
}

/**
 * 聖遺物情報を取得する
 */
function get_relic_input_data(status_sheet, base_increase_index) {
  // 初期変数
  let relic_base_row = 7 + base_increase_index; // シートから聖遺物データを取得する初期行
  let relic_base_column = 3; // シートから聖遺物データを取得する初期列
  let relic_item_index_max = 5; // 聖遺物の個数の最大値
  let relic_option_index_max = 5; // 聖遺物のオプション個数の最大値（メイン+サブ）

  // 行 -> 列の順で取得していく
  for (let rii = 0; rii < relic_item_index_max; rii++) {
    // 聖遺物データ
    let relic_name = status_sheet.getRange(relic_base_row, relic_base_column + rii).getValue();

    // 聖遺物の名前を取得し、カウントする
    if (calculation_data_dict["relic"]["name_count_dict"][relic_name]) {
      calculation_data_dict["relic"]["name_count_dict"][relic_name] += 1;
    } else {
      calculation_data_dict["relic"]["name_count_dict"][relic_name] = 1;
    }

    // 聖遺物のオプションを取り出し、ステータス辞書の、ステータスに加算する
    for (let roi = 0; roi < relic_option_index_max; roi++) {
      // シートから取得する聖遺物オプションの加算値
      let relic_item_base_row = relic_base_row + 2 * roi + 1; // 2行飛ばしかつ、開始位置は聖遺物名の下(+1)

      // 聖遺物オプションデータ
      let relic_item_name = meta_data_dict["option"][status_sheet.getRange(relic_item_base_row, relic_base_column + rii).getValue()];
      let relic_item_value = status_sheet.getRange(relic_item_base_row + 1, relic_base_column + rii).getValue();

      // 取得した聖遺物データ値の補正処理を行う
      let relic_item_add_value = 0;
      if (relic_item_value !== "") {
        relic_item_add_value = parseFloat(relic_item_value);
      }

      // 聖遺物のオプションに％が含まれる場合は、1/100処理を行う
      if (relic_item_name.indexOf("percent") !== -1) {
        calculation_data_dict["status"][relic_item_name] += relic_item_add_value / 100;
      } else {
        calculation_data_dict["status"][relic_item_name] += relic_item_add_value;
      }
    }
  }
}

/**
 * 聖遺物の数値増加型セット効果を取得する
 */
function get_relic_set_effect(relic_sheet) {
  // 初期変数
  let relic_data_lists = relic_sheet.getRange(1, 1, relic_sheet.getLastRow(), relic_sheet.getLastColumn()).getValues();
  let relic_data_header = relic_data_lists[0];

  // 聖遺物セットリストを回す
  for (const relic_name in calculation_data_dict["relic"]["name_count_dict"]) {
    // 初期変数
    const relic_set_count = calculation_data_dict["relic"]["name_count_dict"][relic_name];
    let use_relic_set_count = relic_set_count - (relic_set_count % 2);

    // 聖遺物個数が2、4のときだけ判定を行う
    if (use_relic_set_count >= 2) {
      // 対象聖遺物セット効果と個数が一致する行データを特定する
      for (let relic_data_list of relic_data_lists) {
        if (relic_name === relic_data_list[0] && use_relic_set_count === relic_data_list[1]) {
          // 聖遺物のステータス情報を追加する
          for (let header_column = 3; header_column < relic_data_header.length; header_column++) {
            // 聖遺物のステータス名をメタ名に変更する
            let relic_status_value = relic_data_list[header_column];
            let relic_meta_name = meta_data_dict["option"][relic_data_header[header_column]];

            // 取得した聖遺物データ値の補正処理を行う
            let add_data_value = 0;
            if (relic_status_value !== "") {
              add_data_value = parseFloat(relic_status_value);
            }

            // 聖遺物のオプションに％が含まれる場合は、1/100処理を行う
            if (relic_meta_name.indexOf("percent") !== -1) {
              calculation_data_dict["status"][relic_meta_name] += add_data_value / 100;
            } else {
              calculation_data_dict["status"][relic_meta_name] += add_data_value;
            }
          }
          break;
        }
      }
    }
  }
}

/**
 * 2つの情報から平均化したデータを返却する
 */
function create_average_status_dict(target_lv, low_data_list, high_data_list, start_index, average_target_index_list) {
  // 初期変数
  let average_character_data_list = [];
  let target_lv_diff = target_lv - low_data_list[start_index];
  let low_high_lv_diff = high_data_list[start_index] - low_data_list[start_index];

  for (let i = start_index; i < low_data_list.length; i++) {
    // Lv、HP上限、基礎攻撃力、基礎防御力だけ平均化し、それ以外はLowを選定する
    if (average_target_index_list.includes(i)) {
      // 1あたりの増加量を計算する
      let one_lv_add_value = Math.ceil((high_data_list[i] - low_data_list[i]) / low_high_lv_diff);

      // レベル差分に対応するデータ量を追加する
      average_character_data_list.push(low_data_list[i] + Math.ceil(one_lv_add_value * target_lv_diff));
    } else {
      average_character_data_list.push(low_data_list[i]);
    }
  }
  return average_character_data_list;
}

/**
 * 情報をステータス情報に加算する
 */
function _add_status_data(data_header, data_list, dh_start_index) {
  for (let dh = dh_start_index; dh < data_header.length; dh++) {
    // 増加するステータスキーを定義する
    let status_param_key = meta_data_dict["option"][data_header[dh]];

    // 文字列の場合は、0に置換する
    let add_data_value = 0;
    if (data_list[dh] !== "") {
      add_data_value = parseFloat(data_list[dh]);
    }

    // キャラ情報からパラメータを取得し、加算する
    if (status_param_key.indexOf("percent") !== -1) {
      calculation_data_dict["status"][status_param_key] += add_data_value / 100;
    } else {
      calculation_data_dict["status"][status_param_key] += add_data_value;
    }
  }
}

/**
 * ステータス計算結果を出力する
 */
function output_status(input_sheet, comparison_index) {
  // 初期変数
  let base_row = 8 + 33 * comparison_index;
  let base_column = 2;
  let cdd_s = calculation_data_dict["status"];

  // キャラ情報を出力する
  input_sheet.getRange(base_row, 4).setValue(calculation_data_dict["character"]["name"]);
  input_sheet.getRange(base_row + 1, 4).setValue(calculation_data_dict["weapon"]["name"]);
  input_sheet.getRange(base_row, 6).setValue(calculation_data_dict["character"]["lv"]);
  input_sheet.getRange(base_row + 1, 6).setValue(calculation_data_dict["weapon"]["lv"]);
  input_sheet.getRange(base_row, 7).setValue(calculation_data_dict["character"]["convex"]);
  input_sheet.getRange(base_row + 1, 7).setValue(calculation_data_dict["weapon"]["convex"]);

  // ステータス情報を出力する
  input_sheet.getRange(base_row, base_column).setValue(Math.round(cdd_s["base_hp_upper_limit"] * (1 + cdd_s["hp_percent"]) + cdd_s["hp_fixed_value"]));
  input_sheet
    .getRange(base_row + 1, base_column)
    .setValue(Math.round(cdd_s["base_offensive_power"] * (1 + cdd_s["offensive_power_percent"]) + cdd_s["offensive_power_fixed_value"]));
  input_sheet.getRange(base_row + 2, base_column).setValue(Math.round(cdd_s["base_defense_power"] * (1 + cdd_s["defense_power_percent"]) + cdd_s["defense_power_fixed_value"]));
  input_sheet.getRange(base_row + 3, base_column).setValue(cdd_s["failiarity_with_elements"]);
  input_sheet.getRange(base_row + 4, base_column).setValue(cdd_s["critical_percent"]);
  input_sheet.getRange(base_row + 5, base_column).setValue(cdd_s["critical_damage_percent"]);
  input_sheet.getRange(base_row + 6, base_column).setValue(cdd_s["element_charge_efficiency_percent"]);
  input_sheet.getRange(base_row + 7, base_column).setValue(cdd_s["cool_time_reduction"]);
  input_sheet.getRange(base_row + 8, base_column).setValue(cdd_s["shield_strengthening_percent"]);
  input_sheet.getRange(base_row + 9, base_column).setValue(cdd_s["flame_element_damage_percent"]);
  input_sheet.getRange(base_row + 10, base_column).setValue(cdd_s["water_element_damage_percent"]);
  input_sheet.getRange(base_row + 11, base_column).setValue(cdd_s["grass_element_damage_percent"]);
  input_sheet.getRange(base_row + 12, base_column).setValue(cdd_s["lightning_element_damage_percent"]);
  input_sheet.getRange(base_row + 13, base_column).setValue(cdd_s["wind_element_damage_percent"]);
  input_sheet.getRange(base_row + 14, base_column).setValue(cdd_s["ice_element_damage_percent"]);
  input_sheet.getRange(base_row + 15, base_column).setValue(cdd_s["rock_element_damage_percent"]);
  input_sheet.getRange(base_row + 16, base_column).setValue(cdd_s["physical_damage_percent"]);
  input_sheet.getRange(base_row + 17, base_column).setValue(cdd_s["normal_attack_damage_percent"]);
  input_sheet.getRange(base_row + 18, base_column).setValue(cdd_s["heavy_hit_damage_percent"]);
  input_sheet.getRange(base_row + 19, base_column).setValue(cdd_s["fall_attack_damage_percent"]);
  input_sheet.getRange(base_row + 20, base_column).setValue(cdd_s["elemental_skill_damage_percent"]);
  input_sheet.getRange(base_row + 21, base_column).setValue(cdd_s["elemental_explosion_damage_percent"]);
  input_sheet.getRange(base_row + 22, base_column).setValue(cdd_s["damage_buff_percent"]);
  input_sheet.getRange(base_row + 23, base_column).setValue(cdd_s["spread_damage_percent"]);
  input_sheet.getRange(base_row + 24, base_column).setValue(cdd_s["overload_damage_percent"]);
  input_sheet.getRange(base_row + 25, base_column).setValue(cdd_s["burning_damage_percent"]);
  input_sheet.getRange(base_row + 26, base_column).setValue(cdd_s["electric_shock_damage_percent"]);
  input_sheet.getRange(base_row + 27, base_column).setValue(cdd_s["superconducting_damage_percent"]);
  input_sheet.getRange(base_row + 28, base_column).setValue(cdd_s["evaporation_reaction_percent"]);
  input_sheet.getRange(base_row + 29, base_column).setValue(cdd_s["dissolution_reaction_percent"]);
}
