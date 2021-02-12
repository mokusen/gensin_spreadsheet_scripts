// 初期値
let calculation_data_dict = {
  character: {
    name: "",
    lv: 0,
    convex: 0
  },
  weapon: {
    name: "",
    lv: 0,
    convex: 0
  },
  relic: {
    name_count_dict: {}
  },
  status: {
    base_hp_upper_limit: 0,
    base_offensive_power: 0,
    base_defense_power: 0,
    hp_fixed_value: 0,
    hp_percent: 0,
    offensive_power_fixed_value: 0,
    offensive_power_percent: 0,
    defense_power_fixed_value: 0,
    defense_power_percent: 0,
    failiarity_with_elements: 0,
    critical_percent: 0.05,
    critical_damage_percent: 0.5,
    element_charge_efficiency_percent: 1.0,
    cool_time_reduction: 0,
    shield_strengthening_percent: 0,
    flame_element_damage_percent: 0,
    water_element_damage_percent: 0,
    grass_element_damage_percent: 0,
    lightning_element_damage_percent: 0,
    wind_element_damage_percent: 0,
    ice_element_damage_percent: 0,
    rock_element_damage_percent: 0,
    physical_damage_percent: 0,
    normal_attack_damage_percent: 0,
    heavy_hit_damage_percent: 0,
    fall_attack_damage_percent: 0,
    elemental_skill_damage_percent: 0,
    elemental_explosion_damage_percent: 0,
    damage_buff_percent: 0,
    spread_damage_percent: 0,
    overload_damage_percent: 0,
    burning_damage_percent: 0,
    electric_shock_damage_percent: 0,
    superconducting_damage_percent: 0,
    evaporation_reaction_percent: 0,
    dissolution_reaction_percent: 0
  }
};

// メタ情報
let meta_data_dict = {
  option: {},
  relic: {}
}
