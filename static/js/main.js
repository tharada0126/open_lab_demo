// 各食材情報に値段を追加
const categories = {
    "肉類": [
        { name: "ベーコン", image: "hamburger_goods_bacon.png", price: 130 },
        { name: "チキン", image: "hamburger_goods_chicken.png", price: 180 },
        { name: "ハンバーグ", image: "hamburger_goods_hamburg.png", price: 200 },
        { name: "フィッシュ", image: "hamburger_goods_fish.png", price: 150 }
    ],
    "ソース類": [
        { name: "てりやきソース", image: "hamburger_goods_teriyaki.png", price: 50 },
        { name: "マヨネーズソース", image: "hamburger_goods_source_goods_mayo.png", price: 40 },
        { name: "マスタードソース", image: "hamburger_goods_source_goods_mustard.png", price: 45 },
        { name: "オーロラソース", image: "hamburger_goods_source_goods_aurore.png", price: 55 },
        { name: "ブラウンソース", image: "hamburger_goods_source_goods_brown.png", price: 60 },
        { name: "ケチャップソース", image: "hamburger_goods_source_goods_ketchup.png", price: 30 },
        { name: "タルタルソース", image: "hamburger_goods_sauce_tartar.png", price: 70 },
        { name: "なし", image: "no_image_logo.png", price: 0 }
    ],
    "その他トッピング": [
        { name: "目玉焼き", image: "hamburger_goods_medamayaki.png", price: 120 },
        { name: "ピクルス", image: "hamburger_goods_pickles.png", price: 75 },
        { name: "トマト", image: "hamburger_goods_tomato.png", price: 80 },
        { name: "レタス", image: "hamburger_goods_lettuce.png", price: 60 },
        { name: "玉ねぎ", image: "hamburger_goods_onion.png", price: 65 },
        { name: "アボカド", image: "hamburger_goods_avocado.png", price: 140 },
        { name: "キャベツ", image: "hamburger_goods_cabbage.png", price: 55 },
        { name: "チーズ", image: "hamburger_goods_cheese.png", price: 130 }
    ]
};

let budget = 500;

// 予算を表示する
document.getElementById('budget').textContent = budget;

// 予算セレクトボックスの変更イベント
document.getElementById('budgetSelect').addEventListener('change', (event) => {
    budget = Number(event.target.value);
    document.getElementById('budget').textContent = budget;
});

// スライダーアイテムを生成する関数
function sliderItem({ name, image, price }) {
    return `
        <div class="grid-item">
            <label>${name} - ${price}円</label>
            <img src="${baseImagePath}${image}" alt="${name}"/>
            <input type="range" class="slider" min="-100" max="100" step="1" value="50" name="${name.toLowerCase()}">
            <span id="${name.toLowerCase()}_value">50</span>
        </div>
    `;
}

// カテゴリセクションを生成する関数
function createCategorySection(category, items) {
    return `
        <div class="category-section">
            <div class="category-title">${category}</div>
            <div class="grid-container">
                ${items.map(sliderItem).join('')}
            </div>
        </div>
    `;
}

// HTML構築
const ingredientsDiv = document.getElementById('ingredients');
ingredientsDiv.innerHTML = Object.entries(categories)
    .map(([category, items]) => createCategorySection(category, items))
    .join('');

// 各スライダーの値をリアルタイムで更新
document.querySelectorAll('.slider').forEach(slider => {
    const valueDisplay = document.getElementById(`${slider.name}_value`);
    slider.addEventListener('input', () => {
        valueDisplay.textContent = slider.value;
    });
});

// 実行ボタン
document.getElementById('calculateButton').addEventListener('click', () => {
    const sliderData = Array.from(document.querySelectorAll('.category-section')).flatMap(categorySection => {
        const category = categorySection.querySelector('.category-title').textContent;
        return Array.from(categorySection.querySelectorAll('.slider')).map(slider => ({
            category: category,
            name: slider.name,
            value: Number(slider.value),
            price: categories[category].find(item => item.name === slider.name).price
        }));
    });

    fetch('/calculate_sum', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ sliders: sliderData, budget: budget })
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById('resultHeader').textContent = '選択された食材は以下のとおりです。';
        document.getElementById('sumPrice').textContent = `合計金額: ${data.price}円`;
        document.getElementById('sumValue').textContent = `合計満足度: ${data.value}`;

        const resultContainer = document.getElementById('selectedItems');
        resultContainer.innerHTML = '';

        for (let i = 0; i < data.selectedItems.length; i++){
            const [category, itemName] = data.selectedItems[i];
            const item = categories[category].find(item => item.name === itemName);
            const imagePath = `${baseImagePath}${item.image}`;

            const itemElement = document.createElement('div');
            itemElement.classList.add('selected-item');
            itemElement.innerHTML = `
                <p>${category} - ${item.name} (${item.price}円)</p>
                <img src="${imagePath}" alt="${item.name}" width="100" height="100">
            `;
            resultContainer.appendChild(itemElement);
        }
    })
    .catch(error => console.error('Error:', error));
});
