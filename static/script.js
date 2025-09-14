console.log('Script loaded successfully'); // برای دیباگ

let activeFilters = {
    page: 1,
    per_page: 10, // نمایش ۱۰ آگهی در هر بار
    country: null,
    city: null,
    rent_type: null,
    Area: null,
    min_price: null,
    max_price: null,
    ISO_4217: null,
    min_rooms: null,
    max_rooms: null,
    rental_duration: null,
    roommate_gender: null,
    pets_allowed: null,
    smoking_allowed: null
};

function displayActiveFilters() {
    const activeFiltersDiv = document.getElementById('active-filters');
    if (!activeFiltersDiv) return;

    activeFiltersDiv.innerHTML = '';
    for (const [key, value] of Object.entries(activeFilters)) {
        if (value && key !== 'page' && key !== 'per_page') {
            const filterTag = document.createElement('span');
            filterTag.className = 'filter-tag';
            const filterName = key.replace('_', ' ').replace(/\b\w/g, c => c.toUpperCase());
            filterTag.innerHTML = `${filterName}: ${value} <span class="remove-filter" onclick="removeFilter('${key}')">×</span>`;
            activeFiltersDiv.appendChild(filterTag);
        }
    }
}

function removeFilter(filterKey) {
    activeFilters[filterKey] = null;
    activeFilters.page = 1;
    if (filterKey === 'country') {
        activeFilters.city = null;
        updateCities('filter-form');
        updateCities('post-ad-form');
    }
    displayActiveFilters();
    fetchAds();
}

function updateFilters() {
    const filterForm = document.getElementById('filter-form');
    if (!filterForm) return;

    activeFilters.country = filterForm.querySelector('select[name="country"]').value || null;
    activeFilters.city = filterForm.querySelector('select[name="city"]').value || null;
    activeFilters.rent_type = filterForm.querySelector('select[name="rent_type"]').value || null;
    activeFilters.Area = filterForm.querySelector('input[name="Area"]').value || null;
    activeFilters.min_price = filterForm.querySelector('input[name="min_price"]').value || null;
    activeFilters.max_price = filterForm.querySelector('input[name="max_price"]').value || null;
    activeFilters.ISO_4217 = filterForm.querySelector('input[name="ISO_4217"]').value || null;
    activeFilters.min_rooms = filterForm.querySelector('input[name="min_rooms"]').value || null;
    activeFilters.max_rooms = filterForm.querySelector('input[name="max_rooms"]').value || null;
    activeFilters.rental_duration = filterForm.querySelector('select[name="rental_duration"]').value || null;
    activeFilters.roommate_gender = filterForm.querySelector('select[name="roommate_gender"]').value || null;
    activeFilters.pets_allowed = filterForm.querySelector('select[name="pets_allowed"]').value || null;
    activeFilters.smoking_allowed = filterForm.querySelector('select[name="smoking_allowed"]').value || null;
    activeFilters.page = 1;

    displayActiveFilters();
    fetchAds();
}

function updateCities(formId) {
    const form = document.getElementById(formId);
    if (!form) return;

    const country = form.querySelector('select[name="country"]').value;
    const citySelect = form.querySelector('select[name="city"]');
    citySelect.innerHTML = '<option value="">Select City</option>';

    if (country) {
        fetch(`/api/get_cities?country=${encodeURIComponent(country)}`)
            .then(r => r.json())
            .then(cities => {
                cities.forEach(city => {
                    const option = document.createElement('option');
                    option.value = city;
                    option.textContent = city;
                    citySelect.appendChild(option);
                });
            })
            .catch(error => console.error('Error fetching cities:', error));
    }
}

function fetchAds(page = 1, append = false) {
    activeFilters.page = page;
    const params = new URLSearchParams();
    for (const [key, value] of Object.entries(activeFilters)) {
        if (value) params.append(key, value);
    }

    fetch(`/api/get_ads?${params.toString()}`)
        .then(r => r.json())
        .then(data => {
            const adsContainer = document.getElementById('ads-container');
            if (!adsContainer) return;

            if (!append) adsContainer.innerHTML = '';

            if (data.ads.length === 0 && !append) {
                adsContainer.innerHTML = '<p>No ads found.</p>';
            } else {
                data.ads.forEach(ad => {
                    const adElement = document.createElement('div');
                    adElement.className = 'ad';

                    let adContent = '';

                    if (ad.Image_URL) {
                        adContent += `<img class="ad-thumbnail" src="${ad.Image_URL}" alt="Thumbnail">`;
                    }
                    adContent += `<h3>${ad.Title || 'No Title'}</h3>`;

                    // Items in a two-column grid
                    adContent += '<div class="ad-row-grid">';
                    if (ad.country) adContent += `<p><strong>🌍 Country:</strong> ${ad.country}</p>`;
                    if (ad.city) adContent += `<p><strong>🏙 City:</strong> ${ad.city}</p>`;
                    adContent += '</div>';

                    adContent += '<div class="ad-row-grid">';
                    if (ad.price) adContent += `<p><strong>💰 Price:</strong> ${ad.price} ${ad.ISO_4217 || ''}</p>`;
                    if (ad.rooms_number) adContent += `<p><strong>🛏 Rooms:</strong> ${ad.rooms_number}</p>`;
                    adContent += '</div>';

                    adContent += '<div class="ad-row-grid">';
                    if (ad.rental_duration) adContent += `<p><strong>🕒 Rental Duration:</strong> ${ad.rental_duration}</p>`;
                    if (ad.rent_type) adContent += `<p><strong>📌 Rent Type:</strong> ${ad.rent_type}</p>`;
                    adContent += '</div>';

                    // Other items in a single row
                    if (ad.Area) adContent += `<p><strong>📏 Area:</strong> ${ad.Area}</p>`;
                    if (ad.available_date) adContent += `<p><strong>📅 Available Date:</strong> ${ad.available_date}</p>`;
                    if (ad.property_type) adContent += `<p><strong>🏠 Property Type:</strong> ${ad.property_type}</p>`;
                    if (ad.house_rules) adContent += `<p><strong>📜 House Rules:</strong> ${ad.house_rules}</p>`;
                    if (ad.contact_information) adContent += `<p><strong>☎ Contact:</strong> ${ad.contact_information}</p>`;
                    if (ad.roommate_gender) adContent += `<p><strong>🚻 Roommate Gender:</strong> ${ad.roommate_gender}</p>`;
                    if (ad.house_furniture) adContent += `<p><strong>🛋 Furniture:</strong> ${ad.house_furniture}</p>`;
                    if (ad.pets_allowed) adContent += `<p><strong>🐶 Pets Allowed:</strong> ${ad.pets_allowed}</p>`;
                    if (ad.smoking_allowed) adContent += `<p><strong>🚬 Smoking Allowed:</strong> ${ad.smoking_allowed}</p>`;
                    if (ad.website_reference) adContent += `<p><strong>🌐 Website:</strong> <a href="${ad.website_reference}" target="_blank">${ad.website_reference}</a></p>`;
                    if (ad.message) adContent += `<p><strong>📩 Message:</strong> ${ad.message}</p>`;
                    if (ad.username || ad.created_post) {
                        adContent += `<p><strong>👤 Posted by:</strong> ${ad.username || ''} 
                        ${ad.created_post ? ' on ' + new Date(ad.created_post).toLocaleString() : ''}</p>`;
                    }

                    adElement.innerHTML = adContent;
                    adsContainer.appendChild(adElement);
                });
            }
            document.getElementById('total-ads').textContent = data.total || 0;
        })
        .catch(error => {
            console.error('Error fetching ads:', error);
            document.getElementById('ads-container').innerHTML = '<p>Error loading ads. Please try again later.</p>';
        });
}

function postAd() {
    const form = document.getElementById('post-ad-form');
    if (!form) return;

    const formData = new FormData(form);
    const adData = {
        user_id: window.Telegram.WebApp.initDataUnsafe.user?.id || null,
        username: window.Telegram.WebApp.initDataUnsafe.user?.username || 'Anonymous',
        message: formData.get('message') || null,
        country: formData.get('country') || null,
        city: formData.get('city') || null,
        Area: formData.get('Area') || null,
        rent_type: formData.get('rent_type') || null,
        price: formData.get('price') ? parseFloat(formData.get('price')) : null,
        ISO_4217: formData.get('ISO_4217') || null,
        available_date: formData.get('available_date') || null,
        rooms_number: formData.get('rooms_number') ? parseInt(formData.get('rooms_number')) : null,
        property_type: formData.get('property_type') || null,
        house_rules: formData.get('house_rules') || null,
        contact_information: formData.get('contact_information') || null,
        rental_duration: formData.get('rental_duration') || null,
        roommate_gender: formData.get('roommate_gender') || null,
        house_furniture: formData.get('house_furniture') || null,
        pets_allowed: formData.get('pets_allowed') || null,
        smoking_allowed: formData.get('smoking_allowed') || null,
        Image_URL: formData.get('Image_URL') || null,
        Title: formData.get('Title') || null,
        website_reference: formData.get('website_reference') || null
    };

    fetch('/api/post_ad', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(adData)
    })
        .then(r => r.json())
        .then(data => {
            if (data.success) {
                document.getElementById('post-ad-dialog').close();
                fetchAds();
            } else {
                alert('Error posting ad: ' + data.error);
            }
        })
        .catch(error => {
            console.error('Error posting ad:', error);
            alert('Error posting ad. Please try again.');
        });
}

function applyFilters() {
    updateFilters();
    document.getElementById('filter-dialog').close();
}

// ✅ Infinite Scroll
window.addEventListener('scroll', () => {
    if (window.innerHeight + window.scrollY >= document.body.offsetHeight - 200) {
        activeFilters.page++;
        fetchAds(activeFilters.page, true);
    }
});

document.addEventListener('DOMContentLoaded', () => {
    console.log('DOM loaded, initializing...');
    if (window.Telegram.WebApp.initDataUnsafe.user) {
        const user = window.Telegram.WebApp.initDataUnsafe.user;
        const localPlaceholder = '/static/profile.png';
        const userPhotoUrl = user.photo_url;
        
        let profileImageUrl;
        
        if (userPhotoUrl) {
            profileImageUrl = userPhotoUrl;
        } else {
            profileImageUrl = localPlaceholder; // از عکس پیش‌فرض محلی استفاده کن
        }

        document.getElementById('user-id').textContent = user.id || 'N/A';
        document.getElementById('first-name').textContent = user.first_name || 'N/A';
        document.getElementById('last-name').textContent = user.last_name || 'N/A';
        document.getElementById('username').textContent = user.username || 'N/A';
        document.getElementById('language-code').textContent = user.language_code || 'N/A';
        document.getElementById('is-premium').textContent = user.is_premium ? 'Yes' : 'No';
        document.getElementById('profile-photo-url').textContent = userPhotoUrl || 'N/A';
        document.getElementById('header-profile-photo').src = profileImageUrl;
        document.getElementById('profile-photo-large').src = profileImageUrl;
    }
    fetchAds();
});