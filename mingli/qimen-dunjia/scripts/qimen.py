"""奇门遁甲排盘引擎 — 输入时间，输出完整盘面JSON"""

import json
import os
import sxtwl
from pathlib import Path

DATA_DIR = Path(__file__).parent / "data"

TG = '甲乙丙丁戊己庚辛壬癸'
DZ = '子丑寅卯辰巳午未申酉戌亥'
JQ = ["冬至","小寒","大寒","立春","雨水","惊蛰","春分","清明","谷雨",
      "立夏","小满","芒种","夏至","小暑","大暑","立秋","处暑","白露",
      "秋分","寒露","霜降","立冬","小雪","大雪"]
CW = [1, 8, 3, 4, 9, 2, 7, 6]  # 顺时针物理宫序


def load_data(name):
    with open(DATA_DIR / f"{name}.json", encoding="utf-8") as f:
        return json.load(f)


# ==================== 四柱计算 ====================

def get_sizhu(year, month, day, hour):
    """用sxtwl计算四柱干支。hour为0-23整数。"""
    d = sxtwl.fromSolar(year, month, day)
    y = d.getYearGZ()
    m = d.getMonthGZ()
    dy = d.getDayGZ()
    h = d.getHourGZ(hour)
    return {
        "年柱": TG[y.tg] + DZ[y.dz],
        "月柱": TG[m.tg] + DZ[m.dz],
        "日柱": TG[dy.tg] + DZ[dy.dz],
        "时柱": TG[h.tg] + DZ[h.dz],
        "日干": TG[dy.tg],
        "日支": DZ[dy.dz],
        "时干": TG[h.tg],
        "时支": DZ[h.dz],
        "月支": DZ[m.dz],
    }


# ==================== 节气+定局 ====================

def find_jieqi(year, month, day, hour=0):
    """找到当前日期所在的节气。返回(节气名, 阴阳遁, 节气索引)。
    需要考虑交节精确时刻：同一天交节前后属不同节气。"""
    from datetime import datetime, date, timedelta

    input_dt = datetime(year, month, day, hour)

    # 向前找最近的节气
    for back in range(40):
        dt = date(year, month, day) - timedelta(days=back)
        d = sxtwl.fromSolar(dt.year, dt.month, dt.day)
        if d.hasJieQi():
            # 精确交节时刻（北京时间）
            jd = d.getJieQiJD()
            unix_days = jd - 2440587.5
            jq_utc = datetime(1970, 1, 1) + timedelta(seconds=unix_days * 86400)
            jq_beijing = jq_utc + timedelta(hours=8)

            # 输入时间在交节之前 → 此节气尚未生效，继续往前找
            if jq_beijing > input_dt:
                continue

            jq_idx = d.getJieQi()
            jq_name = JQ[jq_idx]

            # 阳遁: 冬至(0)→芒种(11), 阴遁: 夏至(12)→大雪(23)
            if jq_idx <= 11:
                dun = "阳遁"
            else:
                dun = "阴遁"

            return jq_name, dun, jq_idx

    return None, None, None


def find_yuan(sizhu):
    """拆补法确定上中下元。根据日干支找最近符头。"""
    futou_data = load_data("futou")
    dizhi_class = futou_data["地支分类"]

    day_gz = sizhu["日柱"]
    day_tg = TG.index(day_gz[0])
    day_dz = DZ.index(day_gz[1])

    # 日干支的甲子序号
    for n in range(60):
        if n % 10 == day_tg and n % 12 == day_dz:
            day_jiazi = n
            break

    # 往前找最近的甲(0)或己(5)日
    for back in range(10):
        idx = (day_jiazi - back) % 60
        if idx % 10 in [0, 5]:  # 甲或己
            futou_dz = DZ[idx % 12]
            yuan = dizhi_class[futou_dz]
            return yuan, TG[idx % 10] + futou_dz, back

    return None, None, None


def get_jushu(jq_name, yuan):
    """查节气局数表，返回局数。"""
    jq_data = load_data("jieqi_jushu")

    for dun_type in ["阳遁", "阴遁"]:
        if jq_name in jq_data[dun_type]:
            entry = jq_data[dun_type][jq_name]
            return entry[yuan]

    return None


# ==================== 地盘排布 ====================

def get_dipan(dun, jushu):
    """根据阴阳遁和局数，返回地盘排布 {宫号: 天干}。"""
    data = load_data("dipan_18ju")
    return data[dun][str(jushu)]


# ==================== 旬首+值符值使 ====================

def find_xun(sizhu):
    """根据时柱找旬首、六仪、甲子序号。"""
    kongwang_data = load_data("kongwang")
    hour_gz = sizhu["时柱"]
    h_tg = TG.index(hour_gz[0])
    h_dz = DZ.index(hour_gz[1])

    for n in range(60):
        if n % 10 == h_tg and n % 12 == h_dz:
            hour_jiazi = n
            break

    xun_start = (hour_jiazi // 10) * 10
    xun_names = {0:'甲子',10:'甲戌',20:'甲申',30:'甲午',40:'甲辰',50:'甲寅'}
    xun_name = xun_names[xun_start]
    xun_yi = kongwang_data["旬首六仪"][xun_name]
    kong = kongwang_data["旬空"][xun_name]

    return {
        "旬首": xun_name,
        "六仪": xun_yi,
        "空亡": kong["空亡"],
        "空亡落宫": kong["落宫"],
    }


def find_zhifu_zhishi(dipan, xun_info):
    """确定值符星和值使门。"""
    yuandan = load_data("yuandan")
    yi = xun_info["六仪"]

    # 旬首六仪在地盘哪个宫
    xun_gong = None
    for g, gan in dipan.items():
        if gan == yi:
            xun_gong = int(g)
            break

    if xun_gong is None and yi in ['癸']:
        # 癸可能在中五宫(寄坤二)
        if dipan.get("5") == yi:
            xun_gong = 2  # 寄坤二

    xing = yuandan["九宫"][str(xun_gong)]["九星"]
    men = yuandan["九宫"][str(xun_gong)]["八门"]

    return {
        "旬首落宫": xun_gong,
        "值符星": xing,
        "值使门": men if men else "死门",  # 中五宫无门寄坤二死门
    }


# ==================== 天盘九星 ====================

def rotate_tianpan(dipan, zhifu_info, sizhu):
    """排天盘九星+天干。"""
    yuandan = load_data("yuandan")
    xing_order = yuandan["排列顺序"]["九星"]

    # 值符星原宫
    zhifu_xing = zhifu_info["值符星"]
    orig_gong = yuandan["九星"][zhifu_xing]["原宫"]
    if orig_gong == 5:
        orig_gong = 2  # 天禽寄坤二

    # 时干在地盘哪个宫
    shi_gan = sizhu["时干"]
    shi_gong = None

    if shi_gan == '甲':
        # 甲遁在旬首六仪下
        shi_gong = zhifu_info["旬首落宫"]
    else:
        for g, gan in dipan.items():
            if gan == shi_gan:
                shi_gong = int(g)
                break
    if shi_gong == 5:
        shi_gong = 2  # 中五寄坤二，甲遁和普通时干统一处理

    # 偏移量
    orig_idx = CW.index(orig_gong)
    target_idx = CW.index(shi_gong)
    offset = (target_idx - orig_idx) % 8

    # 原始星的宫位
    orig_xing_gong = {}
    for xing in xing_order:
        og = yuandan["九星"][xing]["原宫"]
        if og == 5:
            og = 2  # 天禽寄坤二
        orig_xing_gong[xing] = og

    # 转动
    tianpan_xing = {}
    tianpan_gan = {}
    for xing, og in orig_xing_gong.items():
        oi = CW.index(og)
        ni = (oi + offset) % 8
        ng = CW[ni]
        tianpan_xing[ng] = xing
        tianpan_gan[ng] = dipan[str(og)]

    return tianpan_xing, tianpan_gan, shi_gong


# ==================== 人盘八门 ====================

def rotate_renpan(dipan, zhifu_info, sizhu, dun):
    """排人盘八门。"""
    yuandan = load_data("yuandan")
    men_order = yuandan["排列顺序"]["八门"]
    zhishi_men = zhifu_info["值使门"]
    xun_gong = zhifu_info["旬首落宫"]

    # 从旬首宫起甲，数天干到时干
    xun_name = None
    kongwang_data = load_data("kongwang")
    for name, yi in kongwang_data["旬首六仪"].items():
        if yi == zhifu_info.get("_六仪", ""):
            xun_name = name
            break

    # 时干在天干中的序号
    shi_tg_idx = TG.index(sizhu["时干"])
    # 旬首甲的天干序号
    xun_tg_idx = 0  # 甲=0，但如果旬首是甲X，则从甲开始

    # 阳遁顺数宫位: 1→2→3→4→(5寄2)→6→7→8→9
    yang_path = [1, 2, 3, 4, 6, 7, 8, 9, 9]  # 5寄2已处理
    # 阴遁逆数: 反向
    yin_path = [1, 9, 8, 7, 6, 4, 3, 2, 2]

    if dun == "阳遁":
        path = [1, 2, 3, 4, 6, 7, 8, 9]
    else:
        path = [9, 8, 7, 6, 4, 3, 2, 1]

    # 从旬首落宫开始，在path上找起点
    start_gong = xun_gong
    if start_gong == 5:
        start_gong = 2

    # 构建从start_gong开始的完整路径
    if dun == "阳遁":
        # 顺序: 从start_gong开始 1→2→3→4→(5→2)→6→7→8→9 循环
        full_path = []
        all_gongs = [1, 2, 3, 4, 6, 7, 8, 9]  # 跳过5
        start_idx = all_gongs.index(start_gong)
        for i in range(10):
            g = all_gongs[(start_idx + i) % 8]
            full_path.append(g)
        # 中五宫: 如果路径中应该经过5，实际走到2
    else:
        all_gongs = [9, 8, 7, 6, 4, 3, 2, 1]
        start_idx = all_gongs.index(start_gong)
        full_path = []
        for i in range(10):
            g = all_gongs[(start_idx + i) % 8]
            full_path.append(g)

    # 但中五宫需要特殊处理: 如果下一个宫号应该是5，跳到2
    # 用更简单的方式: 直接数
    # 从旬首起甲=0, 数到时干
    xun_start_jiazi = None
    for name, yi in kongwang_data["旬首六仪"].items():
        if yi == zhifu_info.get("_六仪_unused", ""):
            break

    # 简化: 直接算步数
    # 旬首是甲X, 时干是Y, 从甲数到Y需要几步?
    shi_tg = TG.index(sizhu["时干"])
    steps = shi_tg  # 甲=0, 乙=1, ..., 癸=9

    # 如果时干是甲(遁在六仪下), steps=0, 值使不动
    # 从旬首落宫走steps步
    if dun == "阳遁":
        ordered = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    else:
        ordered = [9, 8, 7, 6, 5, 4, 3, 2, 1]

    start_in_ordered = ordered.index(xun_gong)  # 中五宫在数步路径中仍占一步
    target_in_ordered = start_in_ordered + steps
    target_gong = ordered[target_in_ordered % 9]
    if target_gong == 5:
        target_gong = 2  # 中五寄坤二

    zhishi_gong = target_gong

    # 从值使门所在宫起，按固定顺序顺时针排其余门
    men_idx = men_order.index(zhishi_men)
    renpan = {}
    start_cw = CW.index(zhishi_gong)
    for i in range(8):
        men = men_order[(men_idx + i) % 8]
        gong = CW[(start_cw + i) % 8]
        renpan[gong] = men

    return renpan, zhishi_gong


# ==================== 神盘八神 ====================

def layout_shenpan(shi_gong, dun):
    """排神盘八神。"""
    yuandan = load_data("yuandan")
    shen_order = yuandan["排列顺序"]["八神"]

    shenpan = {}
    start_idx = CW.index(shi_gong)
    for i in range(8):
        shen = shen_order[i]
        if dun == "阳遁":
            gong = CW[(start_idx + i) % 8]
        else:
            gong = CW[(start_idx - i) % 8]
        shenpan[gong] = shen

    return shenpan


# ==================== 自动检测 ====================

def detect_all(dipan, tianpan_xing, tianpan_gan, renpan, shenpan, xun_info, sizhu, dun):
    """自动检测四害+格局+旺衰等。"""
    wuxing = load_data("wuxing")
    yuandan = load_data("yuandan")
    keying = load_data("shigan_keying_81")
    jixing_data = load_data("jixing")
    rumu_data = load_data("rumu")
    menpo_data = load_data("menpo")
    masing_data = load_data("masing")
    wubu_data = load_data("wubuyushi")
    dizhi_gong = load_data("dizhi_gong")

    result = {"宫": {}, "全局": {}}

    # 五不遇时
    wubu = False
    for item in wubu_data["五不遇时"]:
        if item["日干"] == sizhu["日干"] and item["时干"] == sizhu["时干"]:
            wubu = True
    result["全局"]["五不遇时"] = wubu

    # 马星
    ma_zhi = masing_data["时支查马"].get(sizhu["时支"])
    ma_gong = dizhi_gong["地支对宫"].get(ma_zhi) if ma_zhi else None
    result["全局"]["马星"] = {"地支": ma_zhi, "落宫": ma_gong}

    # 空亡
    result["全局"]["空亡"] = xun_info["空亡"]
    result["全局"]["空亡落宫"] = xun_info["空亡落宫"]

    # 内外盘
    if dun == "阳遁":
        nei = [1, 8, 3, 4]
        wai = [9, 2, 7, 6]
    else:
        nei = [9, 2, 7, 6]
        wai = [1, 8, 3, 4]
    result["全局"]["内盘"] = nei
    result["全局"]["外盘"] = wai

    # 伏吟/反吟检测
    # 对宫: CW中相距4位 → 1↔9, 8↔2, 3↔7, 4↔6
    duigong = {1:9, 9:1, 8:2, 2:8, 3:7, 7:3, 4:6, 6:4}

    # 星伏吟: 九星全部在原宫 (天盘干=地盘干)
    xing_fuyin = all(tianpan_gan.get(g) == dipan.get(str(g)) for g in CW)
    # 星反吟: 九星全部在对宫
    xing_fanyin = all(
        tianpan_gan.get(g) == dipan.get(str(duigong[g])) for g in CW
    )

    # 门伏吟: 八门全部在原宫
    men_orig = {int(k): v["八门"] for k, v in yuandan["九宫"].items() if v.get("八门")}
    men_fuyin = all(renpan.get(g) == men_orig.get(g) for g in CW if g in men_orig)
    # 门反吟: 八门全部在对宫
    men_fanyin = all(
        renpan.get(g) == men_orig.get(duigong[g]) for g in CW
        if g in men_orig and duigong[g] in men_orig
    )

    result["全局"]["星伏吟"] = xing_fuyin
    result["全局"]["星反吟"] = xing_fanyin
    result["全局"]["门伏吟"] = men_fuyin
    result["全局"]["门反吟"] = men_fanyin

    # 月令旺衰
    yue_zhi = sizhu["月支"]
    season = wuxing["月支对应季节"][yue_zhi]
    result["全局"]["月令"] = {"月支": yue_zhi, "季节": season}
    result["全局"]["旺衰"] = wuxing["旺相休囚死"][season]

    # 逐宫检查
    for g in CW:
        gong_info = {}
        gong_wx = yuandan["九宫"][str(g)]["五行"]

        # 十干克应
        tg = tianpan_gan.get(g, "")
        dg = dipan.get(str(g), "")
        combo_key = f"{tg}+{dg}"
        if combo_key in keying.get("组合", {}):
            gong_info["格局"] = keying["组合"][combo_key]
        else:
            gong_info["格局"] = {"格局": combo_key, "吉凶": "未知"}

        # 门迫检查
        men = renpan.get(g, "")
        if men and men in menpo_data["门迫"]:
            if g in menpo_data["门迫"][men]:
                gong_info["门迫"] = True
            else:
                gong_info["门迫"] = False
        else:
            gong_info["门迫"] = False

        # 宫制检查
        if men and men in menpo_data["宫制"]:
            gong_info["宫制"] = g in menpo_data["宫制"][men]
        else:
            gong_info["宫制"] = False

        # 击刑检查(地盘)
        di = dipan.get(str(g), "")
        if di in jixing_data["击刑"]:
            gong_info["击刑"] = jixing_data["击刑"][di]["击刑宫"] == g
        else:
            gong_info["击刑"] = False

        # 入墓检查
        if di in rumu_data["六仪入墓"]:
            gong_info["入墓"] = rumu_data["六仪入墓"][di]["落宫"] == g
        elif di in rumu_data["三奇入墓"]:
            gong_info["入墓"] = rumu_data["三奇入墓"][di]["落宫"] == g
        else:
            gong_info["入墓"] = False

        # 空亡检查
        kong_gongs = xun_info["空亡落宫"]
        gong_info["空亡"] = g in kong_gongs

        # 马星检查
        gong_info["马星"] = g == ma_gong

        # 旺衰
        wang_shuai = wuxing["旺相休囚死"][season]
        for status, wx in wang_shuai.items():
            if wx == gong_wx:
                gong_info["宫旺衰"] = status
                break

        result["宫"][g] = gong_info

    return result


# ==================== 主排盘函数 ====================

def paipan(year, month, day, hour):
    """完整排盘。返回盘面JSON。"""
    # Step 1: 四柱
    sizhu = get_sizhu(year, month, day, hour)

    # Step 2: 节气+阴阳遁
    jq_name, dun, jq_idx = find_jieqi(year, month, day, hour)

    # Step 3: 拆补法定局
    yuan, futou, back_days = find_yuan(sizhu)
    jushu = get_jushu(jq_name, yuan)

    # Step 4: 地盘
    dipan = get_dipan(dun, jushu)

    # Step 5: 旬首
    xun_info = find_xun(sizhu)

    # Step 6: 值符值使
    zhifu_info = find_zhifu_zhishi(dipan, xun_info)

    # Step 7: 天盘
    tianpan_xing, tianpan_gan, shi_gong = rotate_tianpan(dipan, zhifu_info, sizhu)

    # Step 8: 人盘
    renpan, zhishi_gong = rotate_renpan(dipan, zhifu_info, sizhu, dun)

    # Step 9: 神盘
    shenpan = layout_shenpan(shi_gong, dun)

    # Step 10: 自动检测
    detections = detect_all(dipan, tianpan_xing, tianpan_gan, renpan, shenpan, xun_info, sizhu, dun)

    # 组装结果
    yuandan = load_data("yuandan")
    gong_names = {int(k): v["名称"] for k, v in yuandan["九宫"].items()}

    result = {
        "输入": {"时间": f"{year}-{month:02d}-{day:02d} {hour:02d}:00", "北京时间": True},
        "四柱": sizhu,
        "定局": {
            "节气": jq_name, "阴阳遁": dun, "局数": jushu,
            "元": yuan, "符头": futou,
        },
        "旬首": xun_info,
        "值符值使": zhifu_info,
        "盘面": {},
        "检测": detections,
    }

    for g in CW:
        result["盘面"][g] = {
            "宫名": gong_names[g],
            "八神": shenpan.get(g, ""),
            "九星": tianpan_xing.get(g, ""),
            "天干": tianpan_gan.get(g, ""),
            "八门": renpan.get(g, ""),
            "地盘": dipan.get(str(g), ""),
        }

    return result


def print_pan(result):
    """格式化输出盘面。"""
    print(f"{'='*60}")
    print(f"奇门遁甲排盘 | {result['输入']['时间']}")
    print(f"{'='*60}")
    print(f"四柱: {result['四柱']['年柱']}年 {result['四柱']['月柱']}月 {result['四柱']['日柱']}日 {result['四柱']['时柱']}时")
    print(f"定局: {result['定局']['节气']} | {result['定局']['元']} | {result['定局']['阴阳遁']}{result['定局']['局数']}局")
    print(f"旬首: {result['旬首']['旬首']} | 六仪: {result['旬首']['六仪']}")
    print(f"值符: {result['值符值使']['值符星']} | 值使: {result['值符值使']['值使门']}")
    print(f"空亡: {result['旬首']['空亡']} | 马星: {result['检测']['全局']['马星']}")
    print(f"五不遇时: {'是 ⚠️' if result['检测']['全局']['五不遇时'] else '否'}")
    # 伏吟/反吟
    fy_flags = []
    if result['检测']['全局']['星伏吟']: fy_flags.append("星伏吟")
    if result['检测']['全局']['星反吟']: fy_flags.append("星反吟")
    if result['检测']['全局']['门伏吟']: fy_flags.append("门伏吟")
    if result['检测']['全局']['门反吟']: fy_flags.append("门反吟")
    if fy_flags:
        print(f"伏吟反吟: {' | '.join(fy_flags)} ⚠️")
    print()

    for g in [4, 9, 2, 3, 0, 7, 8, 1, 6]:
        if g == 0:
            print(f"  {'─'*50}")
            continue
        pan = result["盘面"][g]
        det = result["检测"]["宫"][g]
        flags = []
        if det.get("空亡"): flags.append("空")
        if det.get("马星"): flags.append("马")
        if det.get("门迫"): flags.append("迫")
        if det.get("击刑"): flags.append("刑")
        if det.get("入墓"): flags.append("墓")
        if det.get("宫制"): flags.append("制")
        flag_str = " [" + ",".join(flags) + "]" if flags else ""

        geju = det.get("格局", {})
        geju_name = geju.get("格局", "?") if isinstance(geju, dict) else "?"
        geju_jx = geju.get("吉凶", "") if isinstance(geju, dict) else ""

        print(f"  【{pan['宫名']}】{flag_str}")
        print(f"    {pan['八神']} | {pan['九星']} | {pan['八门']}")
        print(f"    天:{pan['天干']} 地:{pan['地盘']} → {geju_name}({geju_jx})")
        print()


# ==================== CLI ====================

if __name__ == "__main__":
    import sys
    if len(sys.argv) >= 5:
        y, m, d, h = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4])
    else:
        # 默认: 2026-03-28 13:00
        y, m, d, h = 2026, 3, 28, 13

    result = paipan(y, m, d, h)
    print_pan(result)

    # 也输出JSON
    json_path = Path(__file__).parent / "output.json"
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
    print(f"\nJSON已输出到: {json_path}")
