const fs = require("fs");
const path = require("path");
const os = require("os");

// Shared data directory
const dataDir = path.join(os.homedir(), ".market-widget");
if (!fs.existsSync(dataDir)) {
  fs.mkdirSync(dataDir, { recursive: true });
}

// File paths
const dataFile = path.join(dataDir, "widget_data.json");
const selectedStockFile = path.join(dataDir, "selected_stock.json");
const stocksFile = path.join(__dirname, "stocks.json");

// DOM elements
const selectorScreen = document.getElementById("selector-screen");
const dashboardScreen = document.getElementById("dashboard-screen");
const stockDropdown = document.getElementById("stock-dropdown");
const startBtn = document.getElementById("start-btn");
const settingsIcon = document.getElementById("settings");
const closeBtn = document.getElementById("close-btn");

// State
let stocks = [];
let selectedStock = null;

// Load stocks into dropdown
function loadStocks() {
  if (fs.existsSync(stocksFile)) {
    stocks = JSON.parse(fs.readFileSync(stocksFile));
    stockDropdown.innerHTML = "";
    stocks.forEach((stock, index) => {
      const option = document.createElement("option");
      option.value = index;
      option.textContent = stock.name;
      stockDropdown.appendChild(option);
    });
    // Default to INFOSYS (index 2)
    stockDropdown.selectedIndex = 2;
  }
}

// Load saved selection
function loadSavedSelection() {
  if (fs.existsSync(selectedStockFile)) {
    try {
      const data = JSON.parse(fs.readFileSync(selectedStockFile));
      if (data.name && data.symbol) {
        selectedStock = data;
        return true;
      }
    } catch (e) {
      console.error("Error loading saved selection:", e);
    }
  }
  return false;
}

// Save selection
function saveSelection(name, symbol) {
  const data = { name, symbol };
  fs.writeFileSync(selectedStockFile, JSON.stringify(data));
  selectedStock = data;

  // Write loading state to widget_data.json
  const loadingData = {
    stock: name,
    price: null,
    message: null,
    time: null,
    loading: true
  };
  fs.writeFileSync(dataFile, JSON.stringify(loadingData));
}

// Show selector screen
function showSelector() {
  selectorScreen.style.display = "flex";
  dashboardScreen.style.display = "none";
}

// Show dashboard screen
function showDashboard() {
  selectorScreen.style.display = "none";
  dashboardScreen.style.display = "flex";
  updateWidget();
}

// Update widget data
function updateWidget() {
  if (!dashboardScreen.style.display || dashboardScreen.style.display === "none") {
    return;
  }

  if (fs.existsSync(dataFile)) {
    try {
      const data = JSON.parse(fs.readFileSync(dataFile));
      const isLoading = data.loading || data.price === null;
      const stockMismatch = selectedStock && data.stock !== selectedStock.name;

      if (isLoading || stockMismatch) {
        // Show loading state
        document.getElementById("stock").innerText = selectedStock ? selectedStock.name : "—";
        document.getElementById("price").innerText = "₹ ...";
        document.getElementById("msg").innerText = "fetching data...";
        document.getElementById("time").innerText = "";
      } else {
        // Show actual data
        document.getElementById("stock").innerText = data.stock;
        document.getElementById("price").innerText = "₹ " + data.price;
        document.getElementById("msg").innerText = data.message || "—";
        document.getElementById("time").innerText = data.time ? "updated " + data.time : "";
      }
    } catch (e) {
      console.error("Error reading widget data:", e);
    }
  } else {
    // No data file yet - show loading
    document.getElementById("stock").innerText = selectedStock ? selectedStock.name : "—";
    document.getElementById("price").innerText = "₹ ...";
    document.getElementById("msg").innerText = "fetching data...";
    document.getElementById("time").innerText = "";
  }
}

// Event handlers
startBtn.addEventListener("click", () => {
  const index = stockDropdown.selectedIndex;
  if (index >= 0 && stocks[index]) {
    const stock = stocks[index];
    saveSelection(stock.name, stock.symbol);
    showDashboard();
  }
});

settingsIcon.addEventListener("click", () => {
  showSelector();
});

closeBtn.addEventListener("click", () => {
  window.close();
});

// Initialize
loadStocks();

if (loadSavedSelection()) {
  showDashboard();
} else {
  showSelector();
}

// Poll for updates
setInterval(updateWidget, 3000);
