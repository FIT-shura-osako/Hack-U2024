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
    value = safe_eval(expression)
    if value is None:
        return f"{expression} = sin²θ + cos²θ, θ = arccos({expression}/2)"
    theta = math.acos(value/2)
    return f"{expression} = sin²({theta:.4f}) + cos²({theta:.4f})"

def calculus(expression):
    value = safe_eval(expression)
    if value is None:
        return f"{expression} = ∫₀ˣ f(t)dt, f(x) = d/dx({expression})"
    def f(x):
        return value
    integral = value  # 簡単のため、積分を値そのものとします
    return f"{expression} = ∫₀^{value:.4f} {value:.4f}dt = {integral:.4f}"

def linear_algebra(expression):
    value = safe_eval(expression)
    if value is None:
        return f"{expression} = tr(A), A: n×n単位行列"
    size = max(2, int(value))
    return f"{expression} = tr(A), A: {size}×{size}単位行列"

def complex_analysis(expression):
    value = safe_eval(expression)
    if value is None:
        return f"{expression} = |∑ᵢ₌₀^∞ z^i|, |z| < 1"
    return f"{expression} = |∑ᵢ₌₀^∞ ({value:.4f})^i|, |{value:.4f}| < 1"

def number_theory(expression):
    value = safe_eval(expression)
    if value is None:
        return f"{expression} = φ(n), n: φ(n) = {expression}"
    return f"{expression} = φ({value+1})"

def differential_equations(expression):
    value = safe_eval(expression)
    if value is None:
        return f"{expression} = y(x), y'' + {expression}y = 0"
    return f"{expression} = y(x), y'' + {value:.4f}y = 0"

def probability(expression):
    value = safe_eval(expression)
    if value is None:
        return f"{expression} = P(X ≤ x), X ~ N(0, 1)"
    prob = min(max(value / 10, 0.01), 0.99)
    return f"{expression} = P(X ≤ {prob:.4f}), X ~ N(0, 1)"

def statistics(expression):
    value = safe_eval(expression)
    if value is None:
        return f"{expression} = x̄ ± z(s/√n), 95%信頼区間"
    confidence_level = min(max(value * 100, 1), 99)
    return f"{expression} = x̄ ± {value:.4f}(s/√n), {confidence_level:.1f}%信頼区間"

def topology(expression):
    value = safe_eval(expression)
    if value is None:
        return f"{expression} = χ(X), X: χ(X) = {expression}"
    return f"{expression} = χ(X), X: χ(X) = {value:.0f}"

def abstract_algebra(expression):
    value = safe_eval(expression)
    if value is None:
        return f"{expression} = |G/H|, |G| = 2{expression}, |H| = 2"
    order = 2 * value
    return f"{expression} = |G/H|, |G| = {order:.0f}, |H| = 2"

def numerical_analysis(expression):
    value = safe_eval(expression)
    if value is None:
        return f"{expression} ≈ x, x: {expression}次ニュートン法"
    return f"{expression} ≈ x, x: {value:.0f}次ニュートン法"

def combinatorics(expression):
    value = safe_eval(expression)
    if value is None:
        return f"{expression} = C(n, k), n: C(n, n/2) > {expression}"
    n = math.ceil(math.sqrt(2 * value))  # 近似値
    return f"{expression} = C({n}, {n//2})"

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