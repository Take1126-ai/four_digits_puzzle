import sys
import itertools
from collections import defaultdict

def calculate_possibilities(digits_str):
    """
    4つの数字から四則演算と括弧を用いて作成可能な整数と計算式のマッピングを計算する。

    Args:
        digits_str (str): 4桁の数字文字列。

    Returns:
        defaultdict: 結果の整数をキー、その整数を生成した式のリストを値とする辞書。
    """
    digits = [int(d) for d in digits_str]
    operators = ['+', '-', '*', '/']
    results = defaultdict(list)

    # 1. 数字の順列を生成
    for p_digits in set(itertools.permutations(digits)):
        a, b, c, d = p_digits

        # 2. 演算子の組み合わせを生成
        for p_ops in itertools.product(operators, repeat=3):
            op1, op2, op3 = p_ops

            # 3. 括弧のパターンを適用
            expressions = [
                f"(({a} {op1} {b}) {op2} {c}) {op3} {d}",
                f"({a} {op1} ({b} {op2} {c})) {op3} {d}",
                f"{a} {op1} (({b} {op2} {c}) {op3} {d})",
                f"{a} {op1} ({b} {op2} ({c} {op3} {d}))",
                f"({a} {op1} {b}) {op2} ({c} {op3} {d})"
            ]

            for expr in expressions:
                try:
                    # 4. 数式の評価
                    res = eval(expr)
                    # 評価結果が整数であり、かつ新しい式である場合のみ追加
                    if res == int(res) and expr not in results[int(res)]:
                        results[int(res)].append(expr)
                except ZeroDivisionError:
                    # ゼロ除算はスキップ
                    continue
    return results

def main():
    """
    コマンドライン引数を処理し、計算結果を表示するメイン関数。
    """
    # 入力検証
    if len(sys.argv) != 2:
        print(f"使い方: python3 {sys.argv[0]} <4桁の数字>", file=sys.stderr)
        sys.exit(1)

    digits_str = sys.argv[1]
    if len(digits_str) != 4 or not digits_str.isdigit():
        print("エラー: 引数には4桁の数字を指定してください。", file=sys.stderr)
        sys.exit(1)

    # コアロジックの実行
    results = calculate_possibilities(digits_str)

    if not results:
        print("計算可能な整数は見つかりませんでした。")
        return

    # 出力
    # 1. 結果リスト
    sorted_keys = sorted(results.keys())
    print(f"計算可能な数値 (全 {len(sorted_keys)} 個):")
    print(sorted_keys)

    # 2. 計算式リスト
    print("\n" + "="*20)
    print("計算式:")
    print("="*20)
    for key in sorted_keys:
        for expr in results[key]:
            cleaned_expr = expr.replace(" ", "")
            print(f"{key} = {cleaned_expr}")

if __name__ == "__main__":
    main()
