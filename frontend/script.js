document.addEventListener('DOMContentLoaded', () => {
    const API_BASE_URL = 'http://localhost:8000';

    // --- Static Ticker List ---
    // Instead of an API call, we define a list of popular tickers directly.
    const staticTickers = [
        { symbol: 'AAPL', name: 'Apple Inc.' },
        { symbol: 'MSFT', name: 'Microsoft Corporation' },
        { symbol: 'GOOGL', name: 'Alphabet Inc. (Google)' },
        { symbol: 'AMZN', name: 'Amazon.com, Inc.' },
        { symbol: 'NVDA', name: 'NVIDIA Corporation' },
        { symbol: 'TSLA', name: 'Tesla, Inc.' },
        { symbol: 'META', name: 'Meta Platforms, Inc.' },
        { symbol: 'JPM', name: 'JPMorgan Chase & Co.' },
        { symbol: 'V', name: 'Visa Inc.' },
        { symbol: 'JNJ', name: 'Johnson & Johnson' },
        { symbol: 'WMT', name: 'Walmart Inc.' },
        { symbol: 'PG', name: 'Procter & Gamble Company' },
        { symbol: 'DIS', name: 'The Walt Disney Company' }
    ];

    // --- Updated Function to Populate Ticker Dropdown ---
    const tickerSelect = document.getElementById('ticker-select');
    
    function populateTickerDropdown() {
        tickerSelect.innerHTML = '<option value="">-- Select a Ticker --</option>';
        
        staticTickers.forEach(ticker => {
            const option = document.createElement('option');
            option.value = ticker.symbol;
            option.textContent = `${ticker.symbol} - ${ticker.name}`;
            tickerSelect.appendChild(option);
        });
    }

    // Call the function when the page loads
    populateTickerDropdown();


    // --- Tab Switching (No Changes Needed) ---
    const tabNav = document.querySelector('.tab-nav');
    const switchTab = (tabName) => {
        document.querySelectorAll('.tab-link').forEach(tab => {
            tab.classList.toggle('active', tab.dataset.tab === tabName);
        });
        document.querySelectorAll('.tab-content').forEach(content => {
            content.classList.toggle('active', content.id === tabName);
        });
    };
    tabNav.addEventListener('click', (e) => {
        if (e.target.classList.contains('tab-link')) {
            switchTab(e.target.dataset.tab);
        }
    });

    // --- Helper function for loading states (No Changes Needed) ---
    const toggleLoader = (btn, isLoading) => {
        const btnText = btn.querySelector('.btn-text');
        const loader = btn.querySelector('.loader');
        if (isLoading) {
            btnText.classList.add('hidden');
            loader.classList.remove('hidden');
            btn.disabled = true;
        } else {
            btnText.classList.remove('hidden');
            loader.classList.add('hidden');
            btn.disabled = false;
        }
    };

    // --- Analyzer Logic (No Changes Needed) ---
    const analyzeBtn = document.getElementById('analyze-btn');
    const newsInput = document.getElementById('news-input');
    const runAnalysis = async (text) => {
        if (!text) return;
        toggleLoader(analyzeBtn, true);
        const resultsPlaceholder = document.getElementById('results-placeholder');
        const resultsOutput = document.getElementById('results-output');
        resultsPlaceholder.classList.add('hidden');
        resultsOutput.classList.add('hidden');
        try {
            const response = await fetch(`${API_BASE_URL}/analyze`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ text: text }),
            });
            if (!response.ok) throw new Error((await response.json()).detail);
            const data = await response.json();
            document.getElementById('summary-output').textContent = data.summary;
            const sentimentEl = document.getElementById('sentiment-output');
            sentimentEl.textContent = `${data.sentiment.label.toUpperCase()} (Score: ${data.sentiment.score.toFixed(2)})`;
            sentimentEl.className = data.sentiment.label.toLowerCase();
            resultsOutput.classList.remove('hidden');
        } catch (error) {
            resultsPlaceholder.classList.remove('hidden');
            resultsPlaceholder.textContent = `Error: ${error.message}`;
        } finally {
            toggleLoader(analyzeBtn, false);
        }
    };
    analyzeBtn.addEventListener('click', () => runAnalysis(newsInput.value.trim()));

    // --- News Fetcher Logic (No Changes Needed) ---
    const fetchBtn = document.getElementById('fetch-btn');
    const newsContainer = document.getElementById('news-container');
    
    fetchBtn.addEventListener('click', async () => {
        const ticker = tickerSelect.value;
        if (!ticker) {
            alert('Please select a ticker from the dropdown.');
            return;
        }
        
        toggleLoader(fetchBtn, true);
        newsContainer.innerHTML = '';

        try {
            const response = await fetch(`${API_BASE_URL}/fetch-news/${ticker}`);
            if (!response.ok) throw new Error((await response.json()).detail);
            const newsData = await response.json();

            if (newsData.length === 0) {
                newsContainer.innerHTML = '<p class="placeholder-text">No news found for this ticker.</p>';
            } else {
                newsData.forEach(article => {
                    if (!article.summary) return;
                    const date = new Date(article.publishedDate.replace("T", " ")).toLocaleString('en-US', { dateStyle: 'medium', timeStyle: 'short' });
                    const newsCard = document.createElement('div');
                    newsCard.className = 'news-card';
                    const summaryData = article.summary.replace(/'/g, "&apos;").replace(/"/g, "&quot;");
                    newsCard.innerHTML = `
                        <h4>${article.title}</h4>
                        <div class="metadata"><strong>${article.site}</strong> | ${date}</div>
                        <p class="summary">${article.summary}</p>
                        <div class="news-card-actions">
                            <a href="${article.url}" target="_blank" rel="noopener noreferrer">Read More &rarr;</a>
                            <button class="analyze-news-btn" data-summary='${summaryData}'>Analyze</button>
                        </div>
                    `;
                    newsContainer.appendChild(newsCard);
                });
            }
        } catch (error) {
            newsContainer.innerHTML = `<p class="placeholder-text" style="color: var(--danger-color);">Error: ${error.message}</p>`;
        } finally {
            toggleLoader(fetchBtn, false);
        }
    });

    // --- Event Delegation (No Changes Needed) ---
    newsContainer.addEventListener('click', (e) => {
        if (e.target.classList.contains('analyze-news-btn')) {
            const summaryText = e.target.dataset.summary;
            newsInput.value = summaryText;
            switchTab('analyzer');
            window.scrollTo({ top: 0, behavior: 'smooth' });
        }
    });
});