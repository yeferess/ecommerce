// static/js/search.js

document.addEventListener("DOMContentLoaded", () => {
  const alerta = document.getElementById("alerta");
  const cerrar = document.getElementById("cerrar");

  if (alerta && cerrar) {
    cerrar.addEventListener("click", () => {
      alerta.classList.add("opacity-0");
      setTimeout(() => alerta.remove(), 500);
    });
  }

  const searchInput = document.getElementById('searchInput');
  const searchDropdown = document.getElementById('searchDropdown');
  const searchForm = document.getElementById('searchForm');
  let searchTimeout;

  if (!searchInput || !searchDropdown || !searchForm) return; // seguridad

  searchInput.addEventListener('input', function() {
    const query = this.value.trim();
    clearTimeout(searchTimeout);

    if (query.length < 2) {
      searchDropdown.innerHTML = '';
      searchDropdown.classList.add('hidden');
      return;
    }

    searchTimeout = setTimeout(() => {
      fetch(`/products/search-ajax/?q=${encodeURIComponent(query)}`)
        .then(response => response.json())
        .then(data => displayDropdown(data.products, query))
        .catch(error => console.error('Error:', error));
    }, 300);
  });

  function displayDropdown(products, query) {
    if (products.length === 0) {
      searchDropdown.innerHTML = '<div class="p-4 text-gray-500">No products found</div>';
      searchDropdown.classList.remove('hidden');
      return;
    }

    let html = '';
    products.forEach(product => {
      html += `
        <div class="flex items-center gap-3 p-3 hover:bg-gray-50 cursor-pointer border-b border-gray-100"
             onclick="goToSearchResults('${query}')">
          ${product.image
            ? `<img src="${product.image}" alt="${product.name}" class="w-12 h-12 object-cover rounded">`
            : '<div class="w-12 h-12 bg-gray-200 rounded"></div>'}
          <div class="flex-1">
            <p class="font-semibold text-gray-800">${product.name}</p>
            <p class="text-sm text-gray-500 truncate">${product.description}</p>
            <p class="text-blue-600 font-bold mt-1">${product.price}</p>
          </div>
        </div>`;
    });

    html += `
      <div class="p-3 text-center bg-gray-50 border-t-2 border-gray-200 font-semibold text-blue-600 cursor-pointer hover:bg-gray-100"
           onclick="goToSearchResults('${query}')">
        View all ${products.length}+ results →
      </div>
    `;

    searchDropdown.innerHTML = html;
    searchDropdown.classList.remove('hidden');
  }

  function goToSearchResults(query) {
    window.location.href = `/search/?q=${encodeURIComponent(query)}`;
  }

  document.addEventListener('click', function(e) {
    if (!e.target.closest('#searchForm') && !e.target.closest('#searchDropdown')) {
      searchDropdown.classList.add('hidden');
    }
  });

  searchForm.addEventListener('submit', function() {
    searchDropdown.classList.add('hidden');
  });
});
