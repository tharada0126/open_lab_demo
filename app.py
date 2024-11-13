# app.py
from flask import Flask, render_template, request, jsonify
from genetic_algorithm_hamburger import Problem, genetic_algorithm 

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/calculate_sum', methods=['POST'])
def calculate_sum():
    data = request.json
    sliders = data.get('sliders', [])

    problem = Problem(sliders, 500)
    best_ind, best_price, best_value, selected_items = genetic_algorithm(100, problem, 500, 0.8, 0.1)
    print(f"Best Price: {best_price}, Best Value: {best_value}")
    print("Selected Items")
    for item in selected_items:
        print(item)
    selectedItems = [(v["category"], v["name"]) for v in selected_items]
    
    # 各カテゴリの最大アイテム名と合計値を返す
    result = {
        'price': best_price,
        'value': best_value,
        'selectedItems': selectedItems
    }
    
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)
    #app.run(debug=True, host="0.0.0.0")#サーバー動作時
