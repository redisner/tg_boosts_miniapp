// let tg = window.Telegram.WebApp;
//
// function setThemeClass() {
//     document.documentElement.className = tg.colorScheme;
// }
//
// tg.onEvent('themeChanged', setThemeClass);
// setThemeClass();
//
// tg.expand();


function loadPageItems() {
    const rankedList = document.getElementById("ranked-list");
    const circle = document.querySelector(".circle");
    const page = document.getElementById("current-page").innerHTML;

    let sorted_by;

    if (circle.style.left === "65%") {
        sorted_by = 'level'
    } else {
        sorted_by = 'boosts_count'
    }

    let search_query = document.getElementById("search-bar").value;

    if (typeof search_query === 'undefined') {
        search_query = '';
    }

    fetch('/get_ranking' + '?page=' + page + '&sorted_by=' + sorted_by + '&search=' + search_query)
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
            const itemsToDisplay = JSON.parse(data);

            console.log(itemsToDisplay);

            // Clear existing items
            rankedList.innerHTML = '';

            // Append new items
            itemsToDisplay.forEach(item => {
                rankedList.innerHTML += `
                <div class="ranked-item">
                    <div class="rank-and-image">
                        <span class="rank-number">${item.place}</span>
                        <img src="data:image/png;base64, ${item.picture}" alt="${item.username}">
                    </div>
                    <div class="rank-and-channel-info">
                        <span class="channel-name">${item.name}</span>
                        <span class="boost-info">${item.level} LVL | ${item.boosts} Boosts</span>
                    </div>
                    <a href="https://t.me/${item.username}?boost" target="_blank"><button class="gift-boost-btn">GIFT BOOST</button></a>
                </div>
            `;
            });
        });
}

document.getElementById("search-bar").addEventListener("keyup", function(event) {
        if (event.key === "Enter") {
            loadPageItems()
        }
    });

document.querySelector(".toggle-container").addEventListener("click", function () {
    const toggleContainer = document.querySelector(".toggle-container");
    const circle = document.querySelector(".circle");

    if (circle.style.left === "65%") {
        circle.style.left = "1%";
        toggleContainer.classList.remove("active");
    } else {
        circle.style.left = "65%";
        toggleContainer.classList.add("active");
    }

    loadPageItems();
});

document.addEventListener('DOMContentLoaded', function () {
    var images = document.getElementsByTagName('img');
    for (var i = 0; i < images.length; i++) {
        images[i].addEventListener('dragstart', function (e) {
            e.preventDefault();
        });
    }
});

document.addEventListener('DOMContentLoaded', function () {
    // Pagination variables
    // const itemsPerPage = 10;
    // const totalPages = Math.ceil(rankedItems.length / itemsPerPage);
    const totalPages = 10;
    let currentPage = 1;

    // DOM Elements
    const prevPageButton = document.getElementById("prev-page");
    const nextPageButton = document.getElementById("next-page");
    const currentPageSpan = document.getElementById("current-page");
    const totalPagesSpan = document.getElementById("total-pages");

    // Initialize
    totalPagesSpan.textContent = totalPages;
    loadPageItems();

    // Previous Page Button Click Event
    prevPageButton.addEventListener("click", function () {
        if (currentPage > 1) {
            currentPage--;
            updatePageInfo();
            loadPageItems();
        }
    });

    // Next Page Button Click Event
    nextPageButton.addEventListener("click", function () {
        if (currentPage < totalPages) {
            currentPage++;
            updatePageInfo();
            loadPageItems();
        }
    });

    // Update Page Info
    function updatePageInfo() {
        currentPageSpan.textContent = currentPage;
        prevPageButton.disabled = (currentPage === 1);
        nextPageButton.disabled = (currentPage === totalPages);
    }
})