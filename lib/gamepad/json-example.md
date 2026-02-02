 下面是一个字段齐全的 action_mapping_profile.json 示例（包含 version / navigation_priority / repeat / button_bindings / axis_bindings）：

  - button_bindings / axis_bindings 的 key 是 GamepadButton/GamepadAxis 的枚举整数（用字符串写）
  - value 为 actionId 字符串；设为 "" 表示显式解绑（覆盖默认 preset）
  - threshold 取值范围 0.0 ~ 1.0
  - repeat 仅对“方向动作”（DPad/LeftStick 方向映射）生效

  {
    "version": "1.0",
    "navigation_priority": "dpad_over_left_stick",
    "repeat": {
      "enabled": true,
      "delay_ms": 350,
      "interval_ms": 80
    },
    "button_bindings": {
      "13": "nav.up",
      "14": "nav.down",
      "15": "nav.left",
      "16": "nav.right",

      "0": "nav.accept",
      "1": "nav.back",
      "9": "nav.menu",
      "4": "nav.tab.prev",
      "5": "nav.tab.next",

      "2": "ui.secondary",
      "3": "ui.search",

      "12": ""
    },
    "axis_bindings": {
      "0": { "negative": "nav.left",  "positive": "nav.right", "threshold": 0.25 },
      "1": { "negative": "nav.up",    "positive": "nav.down",  "threshold": 0.25 },

      "2": { "negative": "ui.left",   "positive": "ui.right",  "threshold": 0.35 },
      "3": { "negative": "ui.up",     "positive": "ui.down",   "threshold": 0.35 },

      "4": { "positive": "ui.trigger.left",  "threshold": 0.05 },
      "5": { "positive": "ui.trigger.right", "threshold": 0.05 }
    }
  }

  常用枚举值（便于填 key）：

  - GamepadButton：0=A 1=B 2=X 3=Y 4=L1 5=R1 6=L2 7=R2 8=Select 9=Start 10=L3 11=R3 12=Guide 13=DPAD_UP 14=DPAD_DOWN 15=DPAD_LEFT 16=DPAD_RIGHT
  - GamepadAxis：0=LEFT_X 1=LEFT_Y 2=RIGHT_X 3=RIGHT_Y 4=TRIGGER_LEFT 5=TRIGGER_RIGHT

  ────
