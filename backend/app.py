from flask import Flask, request, jsonify
from flask_cors import CORS
import random
import math

app = Flask(__name__)
CORS(app)

def safe_eval(expression):
    try:
        return eval(expression)
    except:
        return None

def trigonometric(expression):
    return f"{expression} = sin²θ + cos²θ, where θ = arccos({expression}/2) (三角関数の基本恒等式)"

def calculus(expression):
    return f"{expression} = ∫_{0}^x f(t)dt, where f(x) = d/dx({expression}) (微積分の基本定理)"

def linear_algebra(expression):
    value = safe_eval(expression)
    size = max(2, int(value)) if value is not None else 'n'
    return f"{expression} = tr(A), where A is a {size}x{size} identity matrix (単位行列のトレース)"

def complex_analysis(expression):
    value = safe_eval(expression)
    n = value - 1 if value is not None else 'n'
    return f"{expression} = 1/(2πi) ∮_C z^n dz, where n = {n} (コーシーの積分公式)"

def number_theory(expression):
    return f"{expression} = φ(n) + 1, where n is the smallest integer such that φ(n) = {expression} - 1 (オイラーのφ関数)"

def differential_equations(expression):
    return f"{expression} = y(x), where y'' + {expression}y = 0 (2階線形微分方程式)"

def probability(expression):
    value = safe_eval(expression)
    prob = min(max(value / 10, 0.01), 0.99) if value is not None else 'p'
    return f"{expression} = P(X ≤ x), where X ~ N(0, 1) and x is such that P(X ≤ x) = {prob:.2f} (標準正規分布)"

def statistics(expression):
    value = safe_eval(expression)
    confidence_level = min(max(value * 100, 1), 99) if value is not None else 95
    return f"{expression} = x̄ ± z * (s / √n), where z corresponds to a {confidence_level:.1f}% confidence level (信頼区間)"

def topology(expression):
    return f"{expression} = diam(X), where X is a compact metric space with diameter {expression} (コンパクト距離空間の直径)"

def abstract_algebra(expression):
    value = safe_eval(expression)
    order = 2 * value if value is not None else '2n'
    return f"{expression} = |G/H|, where G is a group of order {order} and H is a normal subgroup of index 2 (商群の位数)"

def numerical_analysis(expression):
    return f"{expression} ≈ x, where x is the {expression}-th iteration of Newton's method for f(x) = x² - {expression} (ニュートン法)"

def combinatorics(expression):
    return f"{expression} = C(n, k), where n is the smallest integer such that C(n, n/2) > {expression} (二項係数)"

field_functions = {
    'trigonometry': trigonometric,
    'calculus': calculus,
    'linear_algebra': linear_algebra,
    'complex_analysis': complex_analysis,
    'number_theory': number_theory,
    'differential_equations': differential_equations,
    'probability': probability,
    'statistics': statistics,
    'topology': topology,
    'abstract_algebra': abstract_algebra,
    'numerical_analysis': numerical_analysis,
    'combinatorics': combinatorics
}

def complexify(expression, field=None):
    if field and field in field_functions:
        return field_functions[field](expression)
    else:
        chosen_field = random.choice(list(field_functions.values()))
        return chosen_field(expression)

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