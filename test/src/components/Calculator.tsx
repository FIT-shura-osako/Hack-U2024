import React, { useState } from 'react';
import '../styles/Calculator.css';

const Calculator: React.FC = () => {
  const [input, setInput] = useState('');
  const [result, setResult] = useState('');
  const [complexExpression, setComplexExpression] = useState('');
  const [error, setError] = useState('');
  const [field, setField] = useState('');

  const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    setError('');
    setResult('');
    setComplexExpression('');

    try {
      const response = await fetch('http://localhost:5000/api/calculate', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ expression: input, field }),
      });

      if (!response.ok) {
        const errorText = await response.text();
        throw new Error(`HTTP error! status: ${response.status}, body: ${errorText}`);
      }

      const data = await response.json();
      if (data.error) {
        setError(data.error);
      } else {
        setResult(data.result);
        setComplexExpression(data.complex_expression);
      }
    } catch (error) {
      console.error('Calculation error:', error);
      setError(`計算中にエラーが発生しました: ${error instanceof Error ? error.message : String(error)}`);
    }
  };

  return (
    <div className="calculator">
      <h1>複雑計算機</h1>
      <form onSubmit={handleSubmit}>
        <input
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="式を入力 (例: 1+1)"
        />
        <select value={field} onChange={(e) => setField(e.target.value)}>
          <option value="">ランダム</option>
          <option value="trigonometry">三角関数</option>
          <option value="calculus">微積分</option>
          <option value="linear_algebra">線形代数</option>
          <option value="complex_analysis">複素解析</option>
          <option value="number_theory">数論</option>
          <option value="differential_equations">微分方程式</option>
          <option value="probability">確率論</option>
          <option value="statistics">統計学</option>
          <option value="topology">トポロジー</option>
          <option value="abstract_algebra">抽象代数</option>
          <option value="numerical_analysis">数値解析</option>
          <option value="combinatorics">組合せ論</option>
        </select>
        <button type="submit">計算</button>
      </form>
      {error && <div className="error">{error}</div>}
      {complexExpression && (
        <div className="complex-expression">
          複雑化した式: {complexExpression}
        </div>
      )}
      {result && <div className="result">結果: {result}</div>}
    </div>
  );
};

export default Calculator;

//掛け算割り算どうしよう
//ランダム選択時の各学問分野の結合を行う