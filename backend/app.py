from flask import Flask, request, jsonify
from flask_cors import CORS
import random

app = Flask(__name__)
CORS(app)

def safe_eval(expression):
    try:
        return eval(expression)
    except:
        return None

# 複雑な式の辞書
complex_expressions = {
    'trigonometry': {
        1: ['三角関数式1', '三角関数式2', '三角関数式3'],
        2: ['式1', '式2', '式3'],
        3: ['式1', '式2', '式3'],
        4: ['式1', '式2', '式3'],
        5: ['式1', '式2', '式3'],
        6: ['式1', '式2', '式3'],
        7: ['式1', '式2', '式3'],
        8: ['式1', '式2', '式3'],
        9: ['式1', '式2', '式3'],
    },
    'calculus': {
        1: ['微積式1', '微積式2', '微積式3'],
        2: ['式1', '式2', '式3'],
        3: ['式1', '式2', '式3'],
        4: ['式1', '式2', '式3'],
        5: ['式1', '式2', '式3'],
        6: ['式1', '式2', '式3'],
        7: ['式1', '式2', '式3'],
        8: ['式1', '式2', '式3'],
        9: ['式1', '式2', '式3'],
    },
    # 他の数学分野を追加
}

def get_complex_expression(number, field):
    """指定された数字と分野に対応する複雑な式をランダムに返す"""
    expressions = complex_expressions[field].get(abs(number), [str(number)])
    return random.choice(expressions)

def complexify_operation(a, b, operation, field):
    """2つの1桁の数の演算を複雑化する"""
    expr_a = get_complex_expression(a, field)
    expr_b = get_complex_expression(b, field)
    return f"({expr_a}) {operation} ({expr_b})"

def process_expression(expression, field):
    """式を処理し、複雑化された形で返す"""
    # 加算と減算を扱う
    if '+' in expression or '-' in expression:
        if '+' in expression:
            parts = expression.split('+')
            operation = '+'
        else:
            parts = expression.split('-')
            operation = '-'
        
        if len(parts) == 2:
            a, b = map(str.strip, parts)
            if a.isdigit() and b.isdigit():
                a, b = int(a), int(b)
                if 1 <= abs(a) <= 9 and 1 <= abs(b) <= 9:
                    return complexify_operation(a, b, operation, field)
    
    # それ以外の場合は元の式をそのまま返す
    return expression

def complexify(expression, field=None):
    if field and field in complex_expressions:
        return process_expression(expression, field)
    else:
        # フィールドが指定されていない場合、ランダムに選択
        chosen_field = random.choice(list(complex_expressions.keys()))
        return process_expression(expression, chosen_field)

@app.route('/api/calculate', methods=['POST'])
def calculate():
    try:
        data = request.json
        if data is None:
            return jsonify({"error": "No JSON data received"}), 400
        
        expression = data.get('expression')
        field = data.get('field')
        if expression is None:
            return jsonify({"error": "No expression provided"}), 400
        
        result = safe_eval(expression)
        complex_expression = complexify(expression, field)
        
        return jsonify({
            "result": str(result) if result is not None else "Could not evaluate expression",
            "complex_expression": complex_expression
        })
    except Exception as e:
        app.logger.error(f"An error occurred: {str(e)}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)