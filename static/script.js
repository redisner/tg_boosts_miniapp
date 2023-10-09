let tg = window.Telegram.WebApp;

function setThemeClass() {
    document.documentElement.className = tg.colorScheme;
}

tg.onEvent('themeChanged', setThemeClass);
setThemeClass();

tg.expand();

// Function to render the promo section
function renderPromoSection() {
    fetch('/get_ranking')
        .then(
            function (response) {
                if (response.ok) {
                    return response.text();
                } else {
                    throw new Error('Ошибка при запросе к серверу');
                }
            }
        )
        .then(function (data) {
            // Обработка успешного ответа от сервера
            var container = document.getElementById('ranked-list');

            // Clear any existing content
            container.innerHTML = '';

            var jsonData = JSON.parse(data);

            jsonData.forEach(function (item) {
                // Create promo item div
                var promoItem = document.createElement('div');
                promoItem.classList.add('ranked-item');

                promoItem.innerHTML = `
            <div class="rank-and-image">
                <span class="rank-number">1</span>
                <img src="${item.pic}" alt="${item.username}">
            </div>
            <div class="rank-and-channel-info">
                <span class="channel-name">${item.username}</span>
                <span class="boost-info">${item.level} LVL | ${item.boosts} Boosts</span>
            </div>
            <button class="gift-boost-btn"><atarget="_blank">GIFT BOOST</a></button>
        `

                console.log(promoItem);

                // Append the promo item to the container
                container.appendChild(promoItem);
            });
        })
}

// Call the function
renderPromoSection();
