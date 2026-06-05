"""奇门遁甲排盘引擎自检 — 每步逻辑断言验证"""

import qimen
import sys
from datetime import datetime, timedelta

CW = [1, 8, 3, 4, 9, 2, 7, 6]
DUIGONG = {1:9, 9:1, 8:2, 2:8, 3:7, 7:3, 4:6, 6:4}
TG = '甲乙丙丁戊己庚辛壬癸'
WUXING_GAN = {'甲':'木','乙':'木','丙':'火','丁':'火','戊':'土','己':'土',
              '庚':'金','辛':'金','壬':'水','癸':'水'}
GONG_WX = {1:'水', 2:'土', 3:'木', 4:'木', 5:'土', 6:'金', 7:'金', 8:'土', 9:'火'}

yuandan = qimen.load_data("yuandan")
MEN_ORIG = {int(k): v["八门"] for k, v in yuandan["九宫"].items() if v.get("八门")}
XING_ORIG = {int(k): v["九星"] for k, v in yuandan["九宫"].items()}
XING_LIST = yuandan["排列顺序"]["九星"]  # 8颗星
MEN_LIST = yuandan["排列顺序"]["八门"]   # 8个门
SHEN_LIST = yuandan["排列顺序"]["八神"]  # 8个神

errors = []
warnings = []
total_checks = 0

def check(condition, step, msg):
    global total_checks
    total_checks += 1
    if not condition:
        errors.append(f"[{step}] {msg}")
        return False
    return True

def warn(condition, step, msg):
    if not condition:
        warnings.append(f"[{step}] {msg}")

def verify_one(year, month, day, hour):
    """对单个排盘结果做全面自检"""
    global errors, warnings, total_checks
    errors = []
    warnings = []
    total_checks = 0

    label = f"{year}-{month:02d}-{day:02d} {hour:02d}:00"

    try:
        r = qimen.paipan(year, month, day, hour)
    except Exception as e:
        errors.append(f"[引擎] 排盘崩溃: {e}")
        return False, errors, warnings, 0

    pan = r["盘面"]
    det = r["检测"]
    sz = r["四柱"]
    dj = r["定局"]
    zf = r["值符值使"]
    xs = r["旬首"]
    g = det["全局"]

    # === Step 1: 四柱基本检查 ===
    check(len(sz["年柱"]) == 2, "四柱", f"年柱长度异常: {sz['年柱']}")
    check(len(sz["月柱"]) == 2, "四柱", f"月柱长度异常: {sz['月柱']}")
    check(len(sz["日柱"]) == 2, "四柱", f"日柱长度异常: {sz['日柱']}")
    check(len(sz["时柱"]) == 2, "四柱", f"时柱长度异常: {sz['时柱']}")
    check(sz["日干"] in TG, "四柱", f"日干不合法: {sz['日干']}")
    check(sz["时干"] in TG, "四柱", f"时干不合法: {sz['时干']}")

    # === Step 2: 定局检查 ===
    check(dj["阴阳遁"] in ["阳遁", "阴遁"], "定局", f"阴阳遁异常: {dj['阴阳遁']}")
    check(1 <= dj["局数"] <= 9, "定局", f"局数越界: {dj['局数']}")
    check(dj["元"] in ["上元", "中元", "下元"], "定局", f"元异常: {dj['元']}")

    # === Step 3: 地盘检查 ===
    dipan_gans = set()
    for gg in CW:
        gan = pan[gg]["地盘"]
        check(gan in TG, "地盘", f"{gg}宫地盘干不合法: {gan}")
        dipan_gans.add(gan)
    # 地盘应有8个不同干（中五寄二，9干减1=8宫8干，但可能有重复因为中五宫）
    check(len(dipan_gans) == 8, "地盘", f"地盘干数量异常: {len(dipan_gans)} (应为8)")

    # 地盘排列: 8宫显示8干，都应属于三奇六仪（甲不上盘），缺1个在中五宫
    sanqi_liuyi = set("乙丙丁戊己庚辛壬癸")
    check(dipan_gans.issubset(sanqi_liuyi), "地盘", f"地盘干含非法值: {dipan_gans - sanqi_liuyi}")

    # === Step 4: 旬首+值符值使检查 ===
    check(xs["旬首"] in ['甲子','甲戌','甲申','甲午','甲辰','甲寅'],
          "旬首", f"旬首不合法: {xs['旬首']}")
    check(xs["六仪"] in "戊己庚辛壬癸", "旬首", f"六仪不合法: {xs['六仪']}")
    check(zf["值符星"] in XING_LIST or zf["值符星"] == "天禽",
          "值符值使", f"值符星不合法: {zf['值符星']}")
    check(zf["值使门"] in MEN_LIST, "值符值使", f"值使门不合法: {zf['值使门']}")
    check(1 <= zf["旬首落宫"] <= 9, "值符值使", f"旬首落宫越界: {zf['旬首落宫']}")

    # === Step 5: 天盘九星检查 ===
    tianpan_xings = set()
    for gg in CW:
        xing = pan[gg]["九星"]
        check(xing in XING_LIST, "天盘", f"{gg}宫九星不合法: {xing}")
        tianpan_xings.add(xing)
    check(len(tianpan_xings) == 8, "天盘", f"九星数量异常: {len(tianpan_xings)} (应为8)")

    # 天盘天干检查
    tianpan_gans = set()
    for gg in CW:
        gan = pan[gg]["天干"]
        check(gan in TG, "天盘", f"{gg}宫天干不合法: {gan}")
        tianpan_gans.add(gan)

    # === Step 6: 人盘八门检查 ===
    renpan_mens = set()
    for gg in CW:
        men = pan[gg]["八门"]
        check(men in MEN_LIST, "人盘", f"{gg}宫八门不合法: {men}")
        renpan_mens.add(men)
    check(len(renpan_mens) == 8, "人盘", f"八门数量异常: {len(renpan_mens)} (应为8，不重复)")

    # === Step 7: 神盘八神检查 ===
    shenpan_shens = set()
    for gg in CW:
        shen = pan[gg]["八神"]
        check(shen in SHEN_LIST, "神盘", f"{gg}宫八神不合法: {shen}")
        shenpan_shens.add(shen)
    check(len(shenpan_shens) == 8, "神盘", f"八神数量异常: {len(shenpan_shens)} (应为8)")

    # === Step 8: 逻辑一致性（深度验证） ===

    # 8a. 地盘与局数表一致：查dipan_18ju验证
    dipan_data = qimen.load_data("dipan_18ju")
    expected_dipan = dipan_data[dj["阴阳遁"]][str(dj["局数"])]
    for gg in CW:
        check(pan[gg]["地盘"] == expected_dipan.get(str(gg), ""),
              "地盘逻辑", f"{gg}宫地盘干与{dj['阴阳遁']}{dj['局数']}局表不一致: 实际{pan[gg]['地盘']} vs 表{expected_dipan.get(str(gg))}")

    # 8b. 旬首六仪应在旬首落宫地盘上
    xun_gong = zf["旬首落宫"]
    if xun_gong != 5:
        check(expected_dipan.get(str(xun_gong)) == xs["六仪"],
              "旬首逻辑", f"六仪{xs['六仪']}应在{xun_gong}宫地盘，实际地盘={expected_dipan.get(str(xun_gong))}")
    else:
        check(expected_dipan.get("5") == xs["六仪"],
              "旬首逻辑", f"六仪{xs['六仪']}应在5宫地盘，实际={expected_dipan.get('5')}")

    # 8c. 天盘等偏移一致性：所有星应偏移相同步数
    xing_offsets = []
    for gg in CW:
        xing = pan[gg]["九星"]
        orig = yuandan["九星"][xing]["原宫"]
        if orig == 5:
            orig = 2
        oi = CW.index(orig)
        ni = CW.index(gg)
        offset = (ni - oi) % 8
        xing_offsets.append(offset)
    check(len(set(xing_offsets)) == 1, "天盘逻辑", f"九星偏移不一致: {xing_offsets}")

    # 8d. 人盘等偏移一致性：所有门应偏移相同步数
    men_offsets = []
    for gg in CW:
        men = pan[gg]["八门"]
        if men in MEN_ORIG.values():
            orig_gong = [k for k, v in MEN_ORIG.items() if v == men][0]
            oi = CW.index(orig_gong)
            ni = CW.index(gg)
            offset = (ni - oi) % 8
            men_offsets.append(offset)
    check(len(set(men_offsets)) == 1, "人盘逻辑", f"八门偏移不一致: {men_offsets}")

    # 8e. 神盘排列连续性：八神按顺序（阳遁顺/阴遁逆）排列
    # 找值符位置，验证其余七神按序
    zhifu_gong = None
    for gg in CW:
        if pan[gg]["八神"] == "值符":
            zhifu_gong = gg
            break
    if zhifu_gong:
        start_idx = CW.index(zhifu_gong)
        for i in range(8):
            expected_shen = SHEN_LIST[i]
            if dj["阴阳遁"] == "阳遁":
                actual_gong = CW[(start_idx + i) % 8]
            else:
                actual_gong = CW[(start_idx - i) % 8]
            check(pan[actual_gong]["八神"] == expected_shen,
                  "神盘逻辑", f"八神顺序异常: {actual_gong}宫应为{expected_shen}, 实际{pan[actual_gong]['八神']}")

    # 8f. 值符星应在时干落宫（或甲遁在旬首落宫）
    shi_gan = sz["时干"]
    if shi_gan == "甲":
        expected_zhifu_gong = xun_gong if xun_gong != 5 else 2
    else:
        expected_zhifu_gong = None
        for gg_str, gan in expected_dipan.items():
            if gan == shi_gan:
                g_int = int(gg_str)
                expected_zhifu_gong = g_int if g_int != 5 else 2
                break
    if expected_zhifu_gong and zhifu_gong:
        check(zhifu_gong == expected_zhifu_gong,
              "值符逻辑", f"值符应在{expected_zhifu_gong}宫(时干{shi_gan}落宫), 实际在{zhifu_gong}宫")

    # 8g. 空亡地支与旬首匹配
    kongwang_data = qimen.load_data("kongwang")
    expected_kong = kongwang_data["旬空"][xs["旬首"]]["空亡"]
    check(xs["空亡"] == expected_kong,
          "空亡逻辑", f"空亡与旬首不匹配: 旬首{xs['旬首']}应空{expected_kong}, 实际{xs['空亡']}")

    # 8h. 内外盘与阴阳遁一致
    if dj["阴阳遁"] == "阳遁":
        check(g["内盘"] == [1, 8, 3, 4], "内外盘逻辑", f"阳遁内盘应为[1,8,3,4], 实际{g['内盘']}")
    else:
        check(g["内盘"] == [9, 2, 7, 6], "内外盘逻辑", f"阴遁内盘应为[9,2,7,6], 实际{g['内盘']}")

    # 8i. 五不遇时验证：独立计算日干克时干
    wubu_data = qimen.load_data("wubuyushi")
    real_wubu = any(item["日干"] == sz["日干"] and item["时干"] == sz["时干"]
                    for item in wubu_data["五不遇时"])
    check(g["五不遇时"] == real_wubu, "五不遇时逻辑", "五不遇时检测与独立计算不一致")

    # 8j. 月令旺衰与季节一致
    wuxing_data = qimen.load_data("wuxing")
    expected_season = wuxing_data["月支对应季节"][sz["月支"]]
    check(g["月令"]["季节"] == expected_season,
          "月令逻辑", f"月支{sz['月支']}应对应{expected_season}, 实际{g['月令']['季节']}")

    # === Step 9: 伏吟/反吟一致性 ===
    real_xing_fy = all(pan[p]["天干"] == pan[p]["地盘"] for p in CW)
    real_xing_fan = all(pan[p]["天干"] == pan[DUIGONG[p]]["地盘"] for p in CW)
    real_men_fy = all(pan[p]["八门"] == MEN_ORIG.get(p, "") for p in CW if p in MEN_ORIG)
    real_men_fan = all(
        pan[p]["八门"] == MEN_ORIG.get(DUIGONG[p], "")
        for p in CW if p in MEN_ORIG and DUIGONG[p] in MEN_ORIG
    )
    check(g["星伏吟"] == real_xing_fy, "伏吟反吟", "星伏吟检测不一致")
    check(g["星反吟"] == real_xing_fan, "伏吟反吟", "星反吟检测不一致")
    check(g["门伏吟"] == real_men_fy, "伏吟反吟", "门伏吟检测不一致")
    check(g["门反吟"] == real_men_fan, "伏吟反吟", "门反吟检测不一致")

    # === Step 9: 检测项完整性 ===
    for gg in CW:
        d = det["宫"][gg]
        check("格局" in d, "检测", f"{gg}宫缺少格局检测")
        check("门迫" in d, "检测", f"{gg}宫缺少门迫检测")
        check("击刑" in d, "检测", f"{gg}宫缺少击刑检测")
        check("入墓" in d, "检测", f"{gg}宫缺少入墓检测")
        check("空亡" in d, "检测", f"{gg}宫缺少空亡检测")
        check("马星" in d, "检测", f"{gg}宫缺少马星检测")

    check("五不遇时" in g, "检测", "缺少五不遇时全局检测")
    check("星伏吟" in g, "检测", "缺少星伏吟全局检测")
    check("门反吟" in g, "检测", "缺少门反吟全局检测")
    check("旺衰" in g, "检测", "缺少旺衰全局检测")

    # === Step 10: 断卦SOP数据完整性 ===
    # 确保用于断卦的关键字段都存在
    check("日干" in sz, "SOP数据", "四柱缺少日干")
    check("时干" in sz, "SOP数据", "四柱缺少时干")
    check("月支" in sz, "SOP数据", "四柱缺少月支")
    check("内盘" in g, "SOP数据", "缺少内外盘判断")
    check("外盘" in g, "SOP数据", "缺少内外盘判断")

    return len(errors) == 0, errors, warnings, total_checks


def run_batch(n=100):
    """批量随机测试"""
    import random
    passed = 0
    failed = 0
    total_c = 0
    all_errors = []

    for _ in range(n):
        y = random.randint(2000, 2030)
        m = random.randint(1, 12)
        d = random.randint(1, 28)
        h = random.choice(range(0, 24))
        ok, errs, warns, checks = verify_one(y, m, d, h)
        total_c += checks
        if ok:
            passed += 1
        else:
            failed += 1
            for e in errs:
                all_errors.append(f"{y}-{m:02d}-{d:02d} {h:02d}:00 {e}")

    print(f"批量自检: {n} 盘, {total_c} 项检查")
    print(f"通过: {passed} | 失败: {failed}")
    if all_errors:
        print(f"\n失败详情 (前20):")
        for e in all_errors[:20]:
            print(f"  {e}")
    else:
        print("✅ 全部通过")
    return failed == 0


if __name__ == "__main__":
    if len(sys.argv) >= 5:
        y, m, d, h = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4])
        ok, errs, warns, checks = verify_one(y, m, d, h)
        print(f"单盘自检: {y}-{m:02d}-{d:02d} {h:02d}:00 | {checks} 项检查")
        if ok:
            print("✅ 全部通过")
        else:
            print(f"❌ {len(errs)} 项失败:")
            for e in errs:
                print(f"  {e}")
        if warns:
            print(f"⚠️ {len(warns)} 项警告:")
            for w in warns:
                print(f"  {w}")
    else:
        n = int(sys.argv[1]) if len(sys.argv) > 1 else 200
        run_batch(n)
